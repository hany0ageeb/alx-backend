#!/usr/bin/env python3
"""
Create a class LIFOCache that inherits from
BaseCaching and is a caching system:
- You must use self.cache_data
- You can overload def __init__(self):
def put(self, key, item):
    Must assign to the dictionary self.cache_data
    the item value for the key key
    If key or item is None, this method should not do anything.
    If the number of items in self.cache_data is higher
    that BaseCaching.MAX_ITEMS:
    you must discard the last item put in cache (LIFO algorithm)
    you must print DISCARD: with the key discarded
    and following by a new line
def get(self, key):
    Must return the value in self.cache_data linked to key
    If key is None or if the key doesn’t exist
    in self.cache_data, return None.
"""
from base_caching import BaseCaching
from collections import deque


class LIFOCache(BaseCaching):
    """LIFOCache
    """

    def __init__(self):
        """__init__
        """
        super().__init__()
        self._stack = deque(maxlen=BaseCaching.MAX_ITEMS)

    def get(self, key):
        """get
        return the value in self.cache_data linked to key
        """
        if key is None:
            return None
        return self.cache_data.get(key, None)

    def put(self, key, item):
        """put
        Must assign to the dictionary self.cache_data
        the item value for the key key
        """
        if key is None and item is None:
            return
        self.cache_data[key] = item
        if key in self._stack:
            self._stack.remove(key)
            self._stack.append(key)
        else:
            if len(self._stack) >= BaseCaching.MAX_ITEMS:
                discarded_key = self._stack.pop()
                print('DISCARD: {}'.format(discarded_key))
                del self.cache_data[discarded_key]
            self._stack.append(key)
