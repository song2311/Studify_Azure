import logging
import azure.functions as func
import pymongo
std_client = pymongo.MongoClient("mongodb+srv://Dbroot:dbroot@cluster0.xhnv9.azure.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE")
student_db = std_client["studify"]
class_col = student_db["classes"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    class_id = req.params.get('class_id')
    if not class_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            class_id = req_body.get('class_id')

    if class_id:
        class_id=int(class_id)
        if len(list(class_col.find({'class_id':class_id})))==0:
            return(f"Class ID {class_id} is not a valid class ID")
        delete_query={'class_id':class_id}
        class_col.delete_one(delete_query)
        return func.HttpResponse(f"Class ID {class_id} is deleted from the database!",status_code=200)
    else:
        return func.HttpResponse(
             "Please pass a class_id on the query string or in the request body",
             status_code=400
        )
