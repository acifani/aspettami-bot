from typing import List, Union

import pickledb

favs = pickledb.load("./favs.db", True)


def get_fav(user: int) -> List[int]:
    user_id = str(user)
    if favs.exists(user_id):
        return favs.lgetall(user_id)
    else:
        return list()


def is_fav(user: int, stop_code: Union[int, str]):
    return stop_code in get_fav(user)


def add_fav(user: int, stop: int):
    user_id = str(user)
    if not favs.exists(user_id):
        favs.lcreate(user_id)
    favs.ladd(user_id, stop)


def del_fav(user: int, stop: int):
    user_id = str(user)

    if not is_fav(user, stop):
        return

    favs.lremvalue(user_id, stop)
    # workaround for pickledb bug
    favs.dump()

    # auto clean up
    if favs.llen(user_id) == 0:
        favs.lremlist(user_id)
