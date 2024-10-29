#!/usr/bin/env python3
"""
Create a class MRUCache that inherits from BaseCaching and is a caching system:
- You must use self.cache_data - dictionary from the parent class BaseCaching
- You can overload def __init__(self): but don’t forget
to call the parent init: super().__init__()
def put(self, key, item):
 Must assign to the dictionary self.cache_data the item value for the key key.
 If key or item is None, this method should not do anything.
 If the number of items in self.cache_data is higher that BaseCaching.MAX_ITEMS
 def get(self, key):
 Must return the value in self.cache_data linked to key.
 If key is None or if the key doesn’t exist in self.cache_data, return None
"""
from base_caching import BaseCaching
from collections import deque


class MRUCache(BaseCaching):
    """MRUCache
    """

    def __init__(self):
        """__init__
        """
        super().__init__()
        self._access = deque(maxlen=BaseCaching.MAX_ITEMS)

    def put(self, key, item):
        """put
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self._access.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discarded_key = self._access.pop()
            print('DISCARD: {}'.format(discarded_key))
            del self.cache_data[discarded_key]
        self.cache_data[key] = item
        self._access.append(key)

    def get(self, key):
        """get
        """
        if key is None or key not in self.cache_data:
            return None
        self._access.remove(key)
        self._access.append(key)
        return self.cache_data[key]
