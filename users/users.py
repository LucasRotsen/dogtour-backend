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
    def register_availability(self, user_data):

        user = self.get(user_data['user_id'])

        day_availability_id = uuid.uuid4().hex

        if not user_data['day'] in user:

            self.redis.hmset(day_availability_id, {
                1 : user_data['time']
            })

            day_availability = {
                user_data['day']: day_availability_id
            }

            self.redis.hmset(user['email'], day_availability)
        
        else:

            availability = self.redis.hgetall(user[user_data['day']])
            key = max(list(map(int, availability.keys()))) + 1

            data = {
                key : user_data['time']
            }

            self.redis.hmset(user[user_data['day']], data)

        return {
            "status": 200
        }
    
    @rpc
    def get_availability(self, user_id):
        
        WEEKDAYS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        availability = {}

        user = self.get(user_id)
        keys = user.keys()

        for key in keys:
            if key in WEEKDAYS:
                day_availability = self.redis.hgetall(user[key])
                availability[key] = day_availability

        return {
            "availability": availability,
            "status": 200 if availability else 418
        }