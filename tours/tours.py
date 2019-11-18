import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class UsersService:
    name = "tours"

    redis = Redis('development')

    @rpc
    def create(self, tour):
        
        """
        
        {
            "owner_id":"32d12asg132gegadg3br",
            "dog_id":"123aswueciueaebfhjebda",
            "walker_id":"asde2827382u8e9c8e8ce",
            "day":"Quarta",
            "time":"2019-11-17T08:12:38.803-03:00",
            "latitude":"41.40338, 2.17403",
            "longitude":"80.40238, 1.97003"
        }
        
        Salvo:

        tour:1f5ew18ae1c6e8ve81e8e81be = {         
            "owner_id":"32d12asg132gegadg3br",
            "dog_id":"123aswueciueaebfhjebda",
            "walker_id":"asde2827382u8e9c8e8ce",
            "day":"Quarta",
            "time":"2019-11-17T08:12:38.803-03:00",
            "latitude":"41.40338, 2.17403",
            "longitude":"80.40238, 1.97003",
            "status": "aguardando confirmação"
        }

        """

        tour_id = uuid.uuid4().hex
        key = "tour:" + tour_id

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

        self.redis.hmset(key, tour)

        return {
            "tour": tour,
            "status": 200
        }
    
    @rpc
    def get_by_user_and_status(self, user_id, tour_status):
        
        response = {
            "tours": {},
            "status": 418
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
            response['status'] = 200

        return response