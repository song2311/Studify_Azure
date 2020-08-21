import logging
import pymongo
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    std_client = pymongo.MongoClient("mongodb+srv://Dbroot:dbroot@cluster0.xhnv9.azure.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE")
    student_db = std_client["studify"]
    class_col = student_db["classes"]

    #username and password from request parameters
    username = req.params.get('username')
    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
        
    #get classes for student
    class_query = {'username':username}
    class_details=class_col.find(class_query)
    results = list(class_details) 

    if len(results)!=0:
        return func.HttpResponse(f"Classes for user {username} fetched successfully.\n{results}",status_code=200)
    else:
        return func.HttpResponse(
             f"Please provide proper details so class for user can be fetched",
             status_code=400
        )
