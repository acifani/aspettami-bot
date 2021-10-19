from typing import List, Union
import redis

from aspettami.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

favs = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True
)


def get_fav(user: int) -> List[int]:
    user_id = str(user)
    if favs.exists(user_id):
        return favs.lrange(user_id, 0, -1)
    else:
        return list()


def is_fav(user: int, stop_code: Union[int, str]):
    return stop_code in get_fav(user)


def add_fav(user: int, stop: int):
    user_id = str(user)
    favs.lpush(user_id, stop)


def del_fav(user: int, stop: int):
    user_id = str(user)

    favs.lrem(user_id, 0, stop)

    # auto clean up
    if favs.llen(user_id) == 0:
        favs.delete(user_id)
