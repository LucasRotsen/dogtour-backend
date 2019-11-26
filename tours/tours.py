import uuid
import time

from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis


class ToursService:
    name = "tours"

    dogs_rpc = RpcProxy('dogs')
    users_rpc = RpcProxy('users')

    redis = Redis('development')

    @rpc
    def create(self, tour):

        tour_id = uuid.uuid4().hex
        key = "tour:" + tour_id

        if 'walker_id' in tour:

            tour = {
                "owner_id": tour['owner_id'],
                "dog_id": tour['dog_id'],
                "walker_id": tour['walker_id'],
                "day": tour['day'],
                "time": tour['time'],
                "latitude": tour['latitude'],
                "longitude": tour['longitude'],
                "status": 0
            }

        else:
            
            tour = {
                "owner_id": tour['owner_id'],
                "dog_id": tour['dog_id'],
                "latitude": tour['latitude'],
                "longitude": tour['longitude'],
                "status": 0
            }

        self.redis.hmset(key, tour)

        return {
            "tour_id": tour_id,
            "status": 200
        }
    
    @rpc
    def get_by_user_and_status(self, user_id, tour_status):
        
        response = {
            "tours": {},
            "status": 200
        }

        tours_keys = self.redis.keys('*tour:*')

        tours = {}

        for tour_key in tours_keys:
            tour = self.redis.hgetall(tour_key)

            if  (tour['status'] == tour_status and 
                (tour['owner_id'] == user_id or tour['walker_id'] == user_id)):
                
                tours[tour_key.split(':')[1]] = self.extract_tour_info(tour)
        
        if tours:
            response['tours'] = tours

        return response

    @rpc
    def get_by_user(self, user_id):
        
        response = {
            "tours": {},
            "status": 200
        }

        tours_keys = self.redis.keys('*tour:*')

        tours = {}

        for tour_key in tours_keys:
            tour = self.redis.hgetall(tour_key)

            if (tour['owner_id'] == user_id or tour['walker_id'] == user_id):
                tours[tour_key.split(':')[1]] = self.extract_tour_info(tour)
        
        if tours:
            response['tours'] = tours

        return response
    
    @rpc
    def get_requested(self):
        
        response = {
            "tours": {},
            "status": 200
        }

        tours_keys = self.redis.keys('*tour:*')

        tours = {}

        for tour_key in tours_keys:
            tour = self.redis.hgetall(tour_key)

            if not 'walker_id' in tour:
                tours[tour_key.split(':')[1]] = self.extract_tour_info(tour)
        
        if tours:
            response['tours'] = tours

        return response

    @rpc
    def update(self, tour_data):
        tour_key = 'tour:' + tour_data['tour_id']

        data = {
            'status': tour_data['status']
        }

        self.redis.hmset(tour_key, data)

        return {
            'status': 200
        }

    @rpc
    def confirm(self, tour_data):

        tour_key = 'tour:' + tour_data['tour_id']

        data = {
            'walker_id': tour_data['user_id'],
            'w_latitude': tour_data['latitude'],
            'w_longitude': tour_data['longitude'],
            'status': 2 #ongoing tour
        }

        self.redis.hmset(tour_key, data)

        return {
            'tour': self.extract_tour_info(self.redis.hgetall(tour_key)),
            'status': 200
        }
    
    @rpc
    def request(self, data):

        tour_id = self.create(data)
         
        response = {}
        timeout = time.time() + 60*3

        while not response and time.time() < timeout:
            response = self.match_walker(tour_id['tour_id'])
            time.sleep(1)

        if not response:
            self.redis.delete(tour_id['tour_id'])
        
        return {
            'tour': response,
            'status': 200 if response else 418
        }
    
    @rpc
    def match_walker(self, tour_id):

        tour = self.redis.hgetall('tour:' + tour_id)

        return self.extract_tour_info(tour) if ('walker_id' in tour) else {}

    def extract_tour_info(self, tour):

        return {
            'owner': self.users_rpc.get(tour['owner_id']),
            'dog': self.dogs_rpc.get(tour['dog_id']),
            'walker': self.users_rpc.get(tour['walker_id']) if ('walker_id' in tour) else "",
            'latitude': tour['latitude'],
            'longitude': tour['longitude'],
            'w_latitude': tour['w_latitude'] if ('w_latitude' in tour) else "",
            'w_longitude': tour['w_longitude'] if ('w_longitude' in tour) else "",
            'status': tour['status']    
        }




