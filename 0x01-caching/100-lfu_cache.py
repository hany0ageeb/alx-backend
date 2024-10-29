#!/usr/bin/env python3
"""
Create a class LFUCache that inherits from BaseCaching and is a caching system:
- You must use self.cache_data - dictionary from the parent class BaseCaching
- You can overload def __init__(self):
def put(self, key, item):
    Must assign to the dictionary self.cache_data
    the item value for the key key.
    If key or item is None, this method should not do anything.
    If the number of items in self.cache_data is
    higher that BaseCaching.MAX_ITEMS:
     -
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache
    """

    def __init__(self):
        super().__init__()
        self._frequency = {}

    def get(self, key):
        """get
        """
        if key is None or key not in self.cache_data:
            return None
        # Frequency
        self._frequency[key][0] += 1
        # Least recently used
        self._frequency[key][1] += 1
        return self.cache_data[key]

    def put(self, key, item):
        """put
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self._frequency[key][0] += 1
            self._frequency[key][1] += 1
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                kvps = sorted(self._frequency.items(), key=lambda x: x[1][0])
                least_freq = kvps[0][1][0]
                kvps = filter(lambda kvp: kvp[1][0] == least_freq, kvps)
                kvps = sorted(kvps, key=lambda kvp: kvp[1][1])
                discarded_key = kvps[0][0]
                print('DISCARD: {}'.format(discarded_key))
                del self.cache_data[discarded_key]
                del self._frequency[discarded_key]
            self.cache_data[key] = item
            self._frequency[key] = [1, 1]
