#!/usr/bin/env python3
"""
Copy index_range from the previous task and the following class into your code
Implement a method named get_page that takes two integer arguments
page with default value 1 and page_size with default value 10.
Implement a get_hyper method that takes the same arguments
(and defaults) as get_page
and returns a dictionary containing the following key-value pairs:
    - page_size: the length of the returned dataset page
    - page: the current page number
    - data: the dataset page (equivalent to return from previous task)
    - next_page: number of the next page, None if no next page
    - prev_page: number of the previous page, None if no previous page
    - total_pages: the total number of pages in the dataset as an integer
    Make sure to reuse get_page in your implementation.

"""
from typing import Tuple, List, Dict, Union
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Args:
        page(int): page number starting from 1
        page_size(int): page size
    Return
        a tuple of size two containing a start index
and an end index
orresponding to the range of indexes to return in a list for those particular
pagination parameters.
    """
    start_index: int = (page - 1) * page_size
    end_index: int = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Use assert to verify that both arguments are integers greater than 0.
        Use index_range to find the correct indexes to
        paginate the dataset correctly
        return the appropriate page of the dataset
        (i.e. the correct list of rows).
        If the input arguments are out of range for the dataset,
        an empty list should be returned.
        """
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0
        (start_index, end_index) = index_range(page, page_size)
        data_set_len = len(self.dataset())
        if start_index >= data_set_len or end_index >= data_set_len:
            return []
        return self.dataset()[start_index: end_index]

    def get_hyper(
            self,
            page: int = 1,
            page_size: int = 10) -> Dict[str, Union[int, None, List[List]]]:
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset())/page_size)
        """
        Args:
            page(int): page number > 0
            page_size(int): page size > 0
        Return:
            dict: a dictionary containing the following key-value pairs:
            - page_size: the length of the returned dataset page
            - page: the current page number
            - data: the dataset page (equivalent to return from previous task)
            - next_page: number of the next page, None if no next page
            - prev_page: number of the previous page, None if no previous page
            - total_pages(int): the total number of pages in the dataset
        """
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page':  page + 1 if page + 1 <= total_pages else None,
            'prev_page': page - 1 if page - 1 > 0 else None,
            'total_pages': total_pages
        }
