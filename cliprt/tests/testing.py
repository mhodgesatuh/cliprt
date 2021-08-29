"""
import inspect
import os.path
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

print(os.path.dirname(__file__))
print(os.path.abspath(os.path.dirname(__file__)))
print(sys.path)
from classes.data_element_dictionary import DataElementDictionary

ded = DataElementDictionary('aa')
print(ded.__class__)


# Fatal error
raise Exception('Error: Worksheet already exists: {}, function {}, line {}.'.format(
    __name__, 
    inspect.getouterframes(inspect.currentframe()[1].function),
    inspect.currentframe().f_lineno)) 
"""


