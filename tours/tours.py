import uuid
import time
import asyncio

from nameko.rpc import rpc
from nameko_redis import Redis


class ToursService:
    name = "tours"

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
                
                tours[tour_key.split(':')[1]] = tour
        
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
                tours[tour_key.split(':')[1]] = tour
        
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
                tours[tour_key.split(':')[1]] = tour
        
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
            'status': 2 #ongoing tour
        }

        self.redis.hmset(tour_key, data)

        return {
            'status': 200
        }
    
    @rpc
    def request(self, data):

        tour_id = self.create(data)
         
        response = {}
        timeout = time.time() + 60*2

        while not response and time.time() < timeout:
            response = self.match_walker(tour_id['tour_id'])
            asyncio.sleep(2)
        
        return {
            'tour': response,
            'status': 200 if response else 418
        }
    
    @rpc
    def match_walker(self, tour_id):

        tour = self.redis.hgetall('tour:' + tour_id)

        return tour if ('walker_id' in tour) else {}



