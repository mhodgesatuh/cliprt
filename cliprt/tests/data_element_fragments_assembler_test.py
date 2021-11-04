#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.data_element_fragments_assembler import DataElementFragmentsAssembler\
        as FragAssembler

class DataElementFragmentsAssemblerTest:
    """
    Data Element Fragments Assembler test harness.
    """
    @staticmethod
    def add_fragment_col_index_test():
        """
        Unit test
        """
        frag_assembler = FragAssembler('test de')
        frag_assembler.add_fragment_col_index('test dest de', 1)
        assert frag_assembler.fragments_col_indicies == {'test dest de': 1}

    @staticmethod
    def add_fragment_value_test():
        """
        Unit test
        """
        frag_assembler = FragAssembler('test de')
        frag_assembler.add_fragment_value(1, 'frag part 1')
        assert frag_assembler.fragments_values == {1: 'frag part 1'}

    @staticmethod
    def assembled_value_test():
        """
        Unit test
        """
        frag_assembler = FragAssembler('test de')
        frag_assembler.add_fragment_value(1, 'frag part 1')
        frag_assembler.add_fragment_value(2, 'and part 2')
        assert frag_assembler.assembled_value() == 'frag part 1 and part 2'

    @staticmethod
    def init_test():
        """
        Unit test
        """
        frag_assembler = FragAssembler('test de')
        assert frag_assembler.assembled_de_name == 'test de'
        assert frag_assembler.fragments_col_indicies == {}
        assert frag_assembler.fragments_values == {}

    @staticmethod
    def str_test():
        """
        Unit test
        """
        frag_assembler = FragAssembler('test de')
        frag_assembler.add_fragment_col_index('test dest de one', 1)
        frag_assembler.add_fragment_col_index('test dest de two', 2)
        retval = "'test de': {{'test dest de one': '1'}, {'test dest de two': '2'}}"
        assert frag_assembler.__str__() == retval
