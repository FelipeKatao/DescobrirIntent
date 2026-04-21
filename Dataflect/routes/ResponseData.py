import json

from flask  import Blueprint
from controller.MensagesController import MensagesController

Responses = Blueprint('Responses', __name__)
msg_controller = MensagesController()

@Responses.route('/sendmensage/API/<text>', methods=['GET'])
def Send(text):
    Response =  json.loads( msg_controller.a(text))
    if Response.get("Error") != None:
          return {"Response": Response["Error"]}
    if Response.get("Rule") != None:
          return {"Response": f" One of the rules was triggered \n: {Response['Rule']}"}
    if str(Response["intent"]) == "UNKNOWN":
           return {"Response":"I couldn't understand what was sent, please check if there are no spelling, syntax, or context errors. And try again"}
    return {"Response": f"""
       The user asked {text}. \n
       And object of sentence is {str(Response["MajorKeywords"])} , with entities {str(Response["Entities"])}.
       With aditional sentiment {str(Response["Sentiment"])}
       and aditional intent {str(Response["intent"][0])}

    """}


