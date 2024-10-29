#!/usr/bin/env python3
"""
Create a class LRUCache that
inherits from BaseCaching and is a caching system:
- You must use self.cache_data - dictionary
from the parent class BaseCaching
- You can overload def __init__(self):
but don’t forget to call the parent init: super().__init__()
def get(self, key):
    Must return the value in self.cache_data linked to key.
    If key is None or if the key doesn’t
    exist in self.cache_data, return None.
def put(self, key, item):
    Must assign to the dictionary
    self.cache_data the item value for the key key.
    If key or item is None, this method should not do anything.
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache
    """
    def __init__(self):
        """__init__
        """
        super().__init__()

    def put(self, key, item):
        """
        assign to the dictionary
        self.cache_data the item value for the key key.
        """
        if key is None or item is None:
            return
        pass
        

    def get(self, key):
        """
        return the value in self.cache_data linked to key
        """
        if key is None:
            return None
        pass