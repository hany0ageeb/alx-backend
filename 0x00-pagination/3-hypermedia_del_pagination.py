#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """
        Args:
        Returns:
        """
        indexed_dataset = self.indexed_dataset()
        first_index = min(indexed_dataset.keys())
        last_index = max(indexed_dataset.keys())
        assert index >= first_index and index <= last_index
        data = []
        result = {
            'index': index,
            'data': data,
            'page_size': None,
            'next_index': None,
        }
        while page_size > 0 and index <= last_index:
            if index in indexed_dataset:
                data.append(indexed_dataset[index])
                page_size -= 1
                if result['index'] is None:
                    result['index'] = index
            index += 1
        result['page_size'] = len(data)
        result['next_index'] = index if index < last_index else None
        return result
