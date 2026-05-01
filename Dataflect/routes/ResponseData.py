import json
from project import DataFlectApi
from flask  import Blueprint,request
from controller.MensagesController import MensagesController
from controller.ConfigController import ConfigController
Responses = Blueprint('Responses', __name__)
msg_controller = MensagesController()

@Responses.route('/sendmensage/API/<text>', methods=['GET'])
def Send(text):
    Response = json.loads(msg_controller.analyze(text))
    if Response.get("Error") != None:
          return {"Response": Response["Error"]}
    if Response.get("Rule") != None:
          return {"Response": f" One of the rules was triggered: <br/> {Response['Rule']}"}
    intent_raw = Response.get("intent")
    intent_name = intent_raw[0] if isinstance(intent_raw, (list, tuple)) else intent_raw
    if intent_name == "UNKNOWN":
           return {"Response":"I couldn't understand what was sent, please check if there are no spelling, syntax, or context errors. And try again"}
    ctx = Response.get("context", {})
    Config =  dict(ConfigController().GetAllConfigsYaml())
    ConfigsData = {"FormResponse":""}
    
    if Config.get("Form_format_rule") :
         Config_form = Config.get("Form_format_rule").replace("[","").replace("]","").replace("'","").split(",")
         print(Config_form[0])
         print(Response["action"])
         if Config_form[0] == Response["action"][0]:
              ConfigsData["FormResponse"] = "true"
              
    return {"Response": f"""
       The user asked {text}. <br/>
       And object of sentence is {str(Response["Entidade"])} , with entities {str(Response["Objeto"])}.<br/>
       With aditional sentiment {str(Response["Sentiment"])}.
       With  Itens {str(Response["Itens"])}
      and action {str(Response["action"])}      
      
       ""","Config":ConfigsData,"Field":str(Response["Itens"])}


@Responses.route('/secury/check', methods=['POST'])
def SecuryCheck():
    
    if DataFlectApi.get("Secuty_by_pass") == True:
      return {"Response": "1"}
    return {"Response": "0"}

@Responses.route('/forms/send', methods=['POST'])
def SendForms():
     Config =  dict(ConfigController().GetAllConfigsYaml())
     data = request.args.get('data')
     dados = request.get_json()
     for campo, valor in dados.items():
        print(f"{campo}: {valor}")
     if Config.get("Form_action_"+data):
          values =  ConfigController().CreateVectorToSTR(Config.get("Form_action_"+data))
          return {"Response": values}
     return {"Response": "1"}