import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response

class GatewayService:
    name = 'gateway'

    users_rpc = RpcProxy('users')
    dogs_rpc = RpcProxy('dogs')
    tours_rpc = RpcProxy('tours')

    @http('POST', '/api/login')
    def login(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.users_rpc.login(data)

        return Response(
            json.dumps({'user_id': response['user_id']}),
            status=response['status'],
            mimetype='text/plain'
        )

    @http('GET', '/api/user/<string:user_id>')
    def get_user(self, request, user_id):
        user = self.users_rpc.get(user_id)

        return json.dumps({'user': user})

    @http('POST', '/api/user')
    def post_user(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.users_rpc.create(data)

        return Response(
            json.dumps({'user_id': response['user_id']}),
            status=response['status'],
            mimetype='text/plain'
        )

    @http('GET', '/api/dog/<string:dog_id>')
    def get_dog(self, request, dog_id):
        dog = self.dogs_rpc.get(dog_id)
        
        return json.dumps({'dog': dog})

    @http('POST', '/api/dog')
    def post_dog(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.dogs_rpc.create(data)

        return Response(
            json.dumps({
                'dog_id': response['dog_id'],
                'name': response['name']
            }),
            status=response['status'],
            mimetype='text/plain'
        )
    
    @http('GET', '/api/user/<string:user_id>/dogs')
    def get_user_dogs(self, request, user_id):
        response = self.dogs_rpc.get_user_dogs(user_id)
        
        return Response(
            json.dumps({'dogs': response['dogs']}),
            status=response['status'],
            mimetype='text/plain'
        )

    @http('GET', '/api/users/<string:role>')
    def get_users_by_role(self, request, role):
        response = self.users_rpc.get_by_role(role)
        
        return Response(
            json.dumps({'users': response['users']}),
            status=response['status'],
            mimetype='text/plain'
        )