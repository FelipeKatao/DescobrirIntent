from flask  import Blueprint,request
from controller.MensagesController import MensagesController

Responses = Blueprint('Responses', __name__)
@Responses.route('/sendmensage/API/<text>', methods=['GET'])
def Send(text):
    return MensagesController().ReturnResponse(text)
