#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
            CLIPRT, sounds like liberty.  Pronounced clipperty.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
import unittest
from cliprt.classes.data_element import DataElement

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.data_element = DataElement('The widget')

    def tearDown(self):
        self.data_element.dispose()

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()