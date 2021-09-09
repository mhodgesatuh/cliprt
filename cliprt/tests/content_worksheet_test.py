#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_identifier import ClientIdentifier
from cliprt.classes.client_identity_resolver import ClientIdentityResolver
from cliprt.classes.data_element_fragments_assembler import DataElementFragmentsAssembler as FragAssembler
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry
from cliprt.classes.client_identifier_registry import ClientIdentifierRegistry
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.content_worksheet import ContentWorksheet

class ContentWorksheetTest:

    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    dest_ws_registry = DestinationWorksheetsRegistry()
    ded_processor = DataElementDictionaryProcessor(
        client_info.wb, 
        client_info.ded_ws, 
        dest_ws_registry
    )
    client_id_registry = ClientIdentifierRegistry(dest_ws_registry)

    # Hydrate the DED before testing the ContentWorksheet methods.
    ded_processor.hydrate_ded()

    content_ws_name = client_info.wb.sheetnames[2]
    content_ws = ContentWorksheet(
        ded_processor.wb, 
        content_ws_name,
        ded_processor, 
        client_id_registry, 
        dest_ws_registry
    )

    def build_etl_map_test(self):
        """
        """
        # First populate the DED

        # Then process the client content worksheet.
        self.content_ws.build_etl_map()
        assert len(self.content_ws.frag_assembler_list) == 1
        assert len(self.content_ws.identifier_col_names) == 4
        assert len(self.content_ws.dest_ws_registry.dest_ws_by_ind_list) == 2
        assert len(self.content_ws.dest_ws_registry.dest_ws_list) == 2
        assert len(self.content_ws.dest_ws_registry.dest_ws_names) == 2

    def util_str_normalize_test(self):
        """
        """       
        assert self.content_ws.util_str_normalize('ABC_efg') == 'abc efg'
