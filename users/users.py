import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class UsersService:
    name = "users"

    redis = Redis('development')

    @rpc
    def login(self, user_data):
        auth_info = self.redis.hgetall(user_data['email'])
        
        response = {
            "user_id": None, 
            "status": 418
        }

        if auth_info and (user_data['password'] == auth_info['password']):
            response['user_id'] = auth_info['user_id']
            response['status'] = 200
    
        return response

    @rpc
    def get(self, user_id):
        user_email = self.redis.get(user_id)
        user = self.redis.hgetall(user_email)

        return user
    
    @rpc
    def create(self, user):

        response = {
            "user_id": None,
            "status": 418
        }

        user_exists = self.redis.hgetall(user['email'])
        
        if not user_exists:
            
            user_id = uuid.uuid4().hex

            self.redis.set(user_id, user['email'])

            self.redis.hmset(user['email'], {
                "user_id": user_id,
                "email": user['email'],
                "password": user['password'],
                "name": user['name'],
                "role": user['role']
            })

            response['user_id'] = user_id
            response['status'] = 200

        return response
    
    @rpc
    def delete(self, user_id):
        user = self.get(user_id)

        response = {
            "status": 418
        }

        if user:
            self.redis.delete(user_id)
            self.redis.delete(user['email'])
            
            response['status'] = 200

        return response
  
    @rpc
    def get_by_role(self, role):

        response = {
            "users": {},
            "status": 418
        }

        users_keys = self.redis.keys('*@*')
        users = {}

        for user_key in users_keys:
            user = self.redis.hgetall(user_key)

            if user['role'] == role:
                users[user['user_id']] = user
        
        if users:
            response['users'] = users
            response['status'] = 200

        return response
    
    @rpc
    def rate(self, user_data):

        user = self.get(user_data['user_id'])
        rating = int(user_data['rating'])

        if 'rating' in user:
            rating = (rating + int(user['rating'])) // 2

        user_rating = {
            "rating": rating
        }

        self.redis.hmset(user['email'], user_rating)

        return {
            "rating": rating,
            "status": 200  
        }
    
    @rpc
    def get_availability(self, user_id):
        
        user = self.get(user_id)

        response = {
            'availability': {},
            'status': 418
        }
        
        if 'availability' in user:
            user_availability = self.redis.hgetall(user['availability'])
            response['availability'] = user_availability
            response['status'] = 200

        return response

    @rpc
    def register_availability(self, user_data):

        user = self.get(user_data['user_id'])

        if 'availability' in user:
            self.redis.delete(user['availability'])

        availability_list = user_data['availability']
        
        user_availability_id = uuid.uuid4().hex
        user_availability = {
            "availability" : user_availability_id
        }
        self.redis.hmset(user['email'], user_availability)

        for i in range(0, len(availability_list)):

            day_time = availability_list[i]['day'] + '|' + availability_list[i]['time']

            data = {
                'day:' + str(i) : day_time
            }

            self.redis.hmset(user_availability_id, data)

        return {
            "status": 200
        }
    
    @rpc
    def flush_all(self, request):

        qtty_keys = 0
        keys = self.redis.keys('*')

        for key in keys:
            qtty_keys += self.redis.delete(key)

        return {
            'qtty': qtty_keys,
            'status': 200 if keys else 418
        }
        
    
