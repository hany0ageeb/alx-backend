#!/usr/bin/env python3
"""
Create a class FIFOCache that inherits
from BaseCaching and is a caching system:
- ou must use self.cache_data - dictionary
from the parent class BaseCaching
- You can overload def __init__(self): but don’t forget
to call the parent init: super().__init__()
- def put(self, key, item):
    - Must assign to the dictionary self.cache_data
    the item value for the key key.
    - If key or item is None, this method should not do anything.
    - If the number of items in self.cache_data
    is higher that BaseCaching.MAX_ITEMS:
    - you must discard the first item put in cache (FIFO algorithm)
    - you must print DISCARD: with the key discarded
    and following by a new line
def get(self, key):
    Must return the value in self.cache_data linked to key.
    If key is None or if the key doesn’t exist
    in self.cache_data, return None.
"""
from base_caching import BaseCaching
from collections import deque


class FIFOCache(BaseCaching):
    """FIFOCache
    """

    def __init__(self):
        """__init__
        """
        super().__init__()
        self.__queue = deque(maxlen=BaseCaching.MAX_ITEMS)

    def put(self, key, item):
        """put
        assign to the dictionary
        self.cache_data the item value for the key key
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if key not in self.__queue:
            if len(self.__queue) >= BaseCaching.MAX_ITEMS:
                discarde_key = self.__queue.pop()
                print('DISCARD: {}'.format(discarde_key))
                del self.cache_data[discarde_key]
            self.__queue.appendleft(key)

    def get(self, key):
        """get
        return the value in self.cache_data linked to key
        """
        if key is None:
            return None
        return self.cache_data.get(key, None)
