#!/usr/bin/env python3
"""
Create a class BasicCache that inherits from
BaseCaching and is a caching system:
    - You must use self.cache_data -
    dictionary from the parent class BaseCaching
    - This caching system doesn’t have limit
    - def put(self, key, item):
        - Must assign to the dictionary
        self.cache_data the item value for the key key.
        - If key or item is None,
        this method should not do anything.
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """BasicCache
    inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """
        Args:
            No Arguments
        """
        super().__init__()

    def put(self, key, item):
        """put
        assign to the dictionary
        self.cache_data the item value for the key key
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """get
        return the value in self.cache_data linked to key
        """
        if key is None:
            return None
        return self.cache_data.get(key, None)
