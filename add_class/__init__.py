import logging
import pymongo
import random
import azure.functions as func

#this function gets the query parameters and places them into a dictionary so processing can made easier, will throw an
# AttributeError if important query parameters are missing
def class_dictionary(req):
    class_query_dict={}

    username = req.params.get('username')
    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            username = req_body.get('username')
    class_query_dict['username'] = username

    class_name = req.params.get('class_name')
    if not class_name:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            class_name = req_body.get('class_name')
    class_query_dict['class_name'] = class_name
    
    zoom_meeting_id = req.params.get('zoom_meeting_id')
    if not zoom_meeting_id:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            zoom_meeting_id = req_body.get('zoom_meeting_id')
    class_query_dict['zoom_meeting_id'] = zoom_meeting_id
    
    zoom_meeting_password = req.params.get('zoom_meeting_password')
    if not zoom_meeting_password:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            zoom_meeting_password = req_body.get('zoom_meeting_password')
    class_query_dict['zoom_meeting_password'] = zoom_meeting_password
    
    meeting_type = req.params.get('meeting_type')
    if not meeting_type:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            meeting_type = req_body.get('meeting_type')
    class_query_dict['meeting_type'] = meeting_type

    teacher_email = req.params.get('teacher_email')
    if not teacher_email:
        try:
            req_body = req.get_json()
        #optional teacher email
        except ValueError:
            pass
        else:
            teacher_email = req_body.get('teacher_email')
    class_query_dict['teacher_email'] = teacher_email

    date = req.params.get('date')
    if not date:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            date = req_body.get('date')
    class_query_dict['date'] = date
    
    time_from = req.params.get('time_from')
    if not time_from:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            time_from = req_body.get('time_from')
    class_query_dict['time_from'] = time_from

    time_to = req.params.get('time_to')
    if not time_from:
        try:
            req_body = req.get_json()
        except ValueError:
            raise AttributeError
        else:
            time_from = req_body.get('time_to')
    class_query_dict['time_to'] = time_to
    
    return class_query_dict

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    std_client = pymongo.MongoClient("mongodb+srv://Dbroot:dbroot@cluster0.xhnv9.azure.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE")
    student_db = std_client["studify"]
    std_col = student_db["students"]

    try:
        class_query_dict=class_dictionary(req)
    except AttributeError:
        return func.HttpResponse("Incomplete details given in the query string, new class cannot be added",status_code=400)

    name_query={'username':class_query_dict.get('username')}
    std_name=std_col.find(name_query)
    std_lst=list(std_name)

    if len(std_lst)==1:
        class_col= student_db["classes"]
        #query to check whether the class is already added for students 
        class_name_query={'username':class_query_dict.get('username'),'class_name': class_query_dict.get('class_name'),
        'meeting_type':class_query_dict.get('meeting_type')}
        classses=class_col.find(class_name_query)
        class_lst=list(classses)
        #if class already added don't add new class for that user
        if len(class_lst)!=0:
            return func.HttpResponse(f"{class_query_dict.get('class_name')} {class_query_dict.get('meeting_type')} is already added for user {class_query_dict.get('username')}")

        class_id=random.randint(1000000,9999999)
        #ensure all class ids are unique
        while len(list(class_col.find({'class_id':class_id})))!=0:
            class_id=random.randint(1000000,9999999)
        class_dict={'class_id':class_id}
        class_dict.update(class_query_dict)
        class_col.insert_one(class_dict)
        return func.HttpResponse(f"Successfully added new class {class_dict.get('class_name')} {class_dict.get('meeting_type')} for user {class_dict.get('username')}",status_code=200)
    else:
        return func.HttpResponse(f"user {class_query_dict.get('username')} is not a registered user",status_code=400)
