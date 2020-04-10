# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.apirest.controllers.api import ApiRestBaseController

class ClassAppAPI(ApiRestBaseController):
    ApiRestBaseController._allowedModels.update({
        'class':'classapp'
    })

    ### CREATE 
    @http.route('/api/class/', 
        auth='public', type="json", methods=['POST'])
    def postResponse(self, **kw):
        params = http.request.params
        modelToAccess = "class"

        model = "{}.{}".format(self._allowedModels[modelToAccess],modelToAccess)
        modelObj = http.request.env[model]
        
        if 'token' in params.keys():
            secret = ApiRestBaseController.getSecret()
            token = str(params['token'])
            try:
                decoded = jwt.decode(token, secret, algorithms=['HS256'])
                params['author_id'] = decoded['id']
            
                del params['token']
                create = modelObj.create(params)
                parsedResult = create.parseOne()
                del params['author_id']
                
                return parsedResult
            except:
                return {'Error': "Invalid token"}
        else:
            return {'Error': 'No token'}