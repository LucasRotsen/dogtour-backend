import uuid

from nameko.rpc import RpcProxy, rpc
from nameko_redis import Redis


class DogsService:
    name = "dogs"

    users_rpc = RpcProxy('users')

    redis = Redis('development')

    @rpc
    def get(self, dog_id):
        dog = self.redis.hgetall(dog_id)

        return dog
    
    @rpc
    def create(self, dog_data):

        key = 'dog:' + dog_data['name']
        dog_id = uuid.uuid4().hex

        dog = {
            key: dog_id
        }

        user_email = self.redis.get(dog_data['user_id'])

        self.redis.hmset(user_email, dog)

        self.redis.hmset(dog_id, {
            "name": dog_data['name'],
            "sex": dog_data['sex'],
            "size": dog_data['size'],
            "temper": dog_data['temper']
        })

        response = {
            "dog_id": dog_id,
            "name": dog_data['name'],
            "status": 200
        }

        return response

    @rpc
    def get_user_dogs(self, user_id):
        
        response = {
            "dogs": {},
            "status": 418
        }

        user = self.users_rpc.get(user_id)
        
        dogs = {}
        keys = user.keys()

        for key in keys:
            if key.startswith('dog:'):
                dogs[user[key]] = self.get(user[key])
        
        if dogs:
            response['dogs'] = dogs
            response['status'] = 200

        return response


