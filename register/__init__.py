import logging
import pymongo
import random
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    std_client = pymongo.MongoClient("mongodb+srv://Dbroot:dbroot@cluster0.xhnv9.azure.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE")
    student_db = std_client["studify"]
    std_col = student_db["students"]

    #username and password from request parameters
    username = req.params.get('username')
    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')

    password = req.params.get('password')
    if not password:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            password = req_body.get('password')

    full_query = {'username':username,'password':password}
    std_details=std_col.find(full_query)
    results1 = list(std_details) 
 
    name_query={'username':username}
    std_name=std_col.find(name_query)
    results2 = list(std_name) 

    if len(results1)==0 and len(results2)==0 and username and password:
        user_id=random.randint(0000000,9999999)
        #ensure all user ids are unique
        while len(list(std_col.find({'user_id':user_id})))!=0:
            user_id=random.randint(1000000,9999999)
        new_user={'user_id':user_id}
        new_user.update(full_query)
        std_col.insert_one(new_user)
        return func.HttpResponse(f"Welcome to Studify {username}",status_code=200)

    elif len(results2)!=0:
        return func.HttpResponse("An account with the provided username had already been created",status_code=200)
    else:
        return func.HttpResponse(
             "Incorrect query parameter given",
             status_code=400
        )