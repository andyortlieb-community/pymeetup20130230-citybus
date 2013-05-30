import json

from db import Model

###
###     Our REST API
###

# Just a base class, not terribly useful.
class REST:
    def render(self):
        return json.dumps({"Success":None}),204

class Success(REST):

    def __init__(self, data=None):
        if data: self.data = data

    def render(self):
        output = {"Success":True}
        if hasattr(self, 'data') and self.data:

            # Is it a single model?
            if isinstance(self.data, Model):
                output['Data'] =  self.data.toDict()
    
            # Does our data have a toDict() for us?
            if hasattr(self.data,'toDict'):
                output['Data'] = self.data.toDict()

            elif isinstance(self.data, list):
                output['Data'] = [ model.toDict() for model in self.data ] 

            else:
                output['Data'] = None

        return json.dumps(output),200

class NotFound(REST):
    def __init__(self,msg="The item was not found"):
        self.msg = msg

    def render(self):
        return json.dumps({
            'Success': False,
            'Msg':self.msg
        }),404