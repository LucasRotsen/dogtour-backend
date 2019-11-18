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
    
    @http('DELETE', '/api/user/<string:user_id>/delete')
    def delete_user(self, request, user_id):
        response = self.users_rpc.delete(user_id)

        return Response(
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
    
    @http('POST', '/api/user/rate')
    def rate_user(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.users_rpc.rate(data)
        
        return Response(
            json.dumps({'rating': response['rating']}),
            status=response['status'],
            mimetype='text/plain'
        )
    
    @http('POST', '/api/user/availability')
    def register_user_availability(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.users_rpc.register_availability(data)
        
        return Response(
            status=response['status'],
            mimetype='text/plain'
        )
    
    @http('GET', '/api/user/<string:user_id>/availability')
    def get_user_availability(self, request, user_id):
        response = self.users_rpc.get_availability(user_id)
        
        return Response(
            json.dumps({'availability': response['availability']}),
            status=response['status'],
            mimetype='text/plain'
        )
    
    @http('POST', '/api/tour/schedule')
    def schedule_a_tour(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.tours_rpc.create(data)
        
        return Response(
            json.dumps({'tour': response['tour']}),
            status=response['status'],
            mimetype='text/plain'
        )
    
    @http('GET', '/api/user/<string:user_id>/tours/<string:tour_status>')
    def get_user_tours_by_status(self, request, user_id, tour_status):
        response = self.tours_rpc.get_by_user_and_status(user_id, tour_status)
        
        return Response(
            json.dumps({'tours': response['tours']}),
            status=response['status'],
            mimetype='text/plain'
        )
    
    