import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response

class GatewayService:
    name = 'gateway'

    users_rpc = RpcProxy('users')
    dogs_rpc = RpcProxy('dogs')
    tours_rpc = RpcProxy('tours')

    @http('POST', '/login')
    def login(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.users_rpc.login(data)

        return Response(
            json.dumps({'user_id': response['user_id']}),
            status=response['status'],
            mimetype='application/json'
        )

    @http('GET', '/user/<string:user_id>')
    def get_user(self, request, user_id):
        user = self.users_rpc.get(user_id)

        return json.dumps({'user': user})

    @http('POST', '/user')
    def post_user(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.users_rpc.create(data)

        return Response(
            json.dumps({'user_id': response['user_id']}),
            status=response['status'],
            mimetype='application/json'
        )

    @http('GET', '/dog/<string:dog_id>')
    def get_dog(self, request, dog_id):
        dog = self.dogs_rpc.get(dog_id)
        
        return json.dumps({'dog': dog})

    @http('POST', '/dog')
    def post_dog(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.dogs_rpc.create(data)

        return Response(
            json.dumps({
                'dog_id': response['dog_id'],
                'name': response['name']
            }),
            status=response['status'],
            mimetype='application/json'
        )