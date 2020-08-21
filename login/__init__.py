import logging
import pymongo
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

    name_query = {'username':username,'password':password}
    std_details=std_col.find(name_query)
    results = list(std_details) 

    if len(results)!=0 and username and password:
        return func.HttpResponse(f"Hello {username}!",status_code=200)

    elif len(results)==0 and username and password:
        return func.HttpResponse("Incorrect login details provided",status_code=200)
    else:
        return func.HttpResponse(
             "Please provide login details with username and password",
             status_code=400
        )
