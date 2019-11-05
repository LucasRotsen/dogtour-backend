import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class UsersService:
    name = "users"

    redis = Redis('development')

    @rpc
    def login(self, user_id):
        user = self.redis.hgetall(user_id)
        return user

    @rpc
    def get(self, user_id):
        user = self.redis.hgetall(user_id)
        return user

    @rpc
    def create(self, user):
        user_id = uuid.uuid4().hex
        self.redis.hmset(user_id, {
            "name": user['name'],
            "email": user['email'],
            "password": user['password'],
            "role": user['role']
        })
        return user_id