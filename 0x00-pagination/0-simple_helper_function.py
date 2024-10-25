#!/usr/bin/env python3
"""
Write a function named index_range
that takes two integer arguments page and page_size.
The function should return a tuple of size two containing a start index
and an end index
orresponding to the range of indexes to return in a list for those particular
pagination parameters.
Page numbers are 1-indexed, i.e. the first page is page 1.
"""
from typing import Tuple


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
