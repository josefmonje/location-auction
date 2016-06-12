from django.template import Library
from itertools import cycle
import math

register = Library()

@register.filter
def exact_columns(items, number_of_columns):
    """Divides a list in an exact number of columns.
    The number of columns is guaranteed.
    
    Examples:
    
        8x3:
        [[1, 2, 3], [4, 5, 6], [7, 8]]
        
        2x3:
        [[1], [2], []]
    """
    try:
        number_of_columns = int(number_of_columns)
        items = list(items)
    except (ValueError, TypeError):
        return [items]
    
    number_of_columns=int(math.ceil(len(items)/float(number_of_columns)))

    columns = [[] for x in range(number_of_columns)]
    actual_column = cycle(range(number_of_columns))
    for item in items:
        columns[actual_column.next()].append(item)
    
    return columns
