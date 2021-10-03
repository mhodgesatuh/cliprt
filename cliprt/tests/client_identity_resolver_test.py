#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_identity_resolver import ClientIdentityResolver
from cliprt.classes.client_registry import ClientRegistry
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.identifier import Identifier
from cliprt.classes.identifier_registry import IdentifierRegistry

class ClientIdentityResolverTest:
    """
    Client Identity Resolver test harness.    
    """
    # Dependencies
    identifier_registry = IdentifierRegistry()
    client_registry = ClientRegistry(identifier_registry)
    id_resolver = ClientIdentityResolver(client_registry, identifier_registry)

    # Test data
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    client_info.ded_processor.hydrate_ded()

    def init_test(self):
        """
        Unit test
        """
        assert self.client_id_resolver.matched_identifier_types == []
        assert self.client_id_resolver.identifier_matched == []
        assert self.client_id_resolver.identifier_unmatched == []

    def assess_identifier_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor.ded

        bad_phone_id = Identifier('home phone', '(999) 888-0000', test_ded)
        retval = self.id_resolver.assess_identifier(bad_phone_id)
        assert not retval

        bad_phone_id = Identifier('home phone', '(999) 888-9999', test_ded)
        retval = self.id_resolver.assess_identifier(bad_phone_id)
        assert not retval

        bad_phone_id = Identifier('home phone', '12345', test_ded)
        retval = self.id_resolver.assess_identifier(bad_phone_id)
        assert not retval

        bad_email_id = Identifier('email', 'noemail', test_ded)
        retval = self.id_resolver.assess_identifier(bad_email_id)
        assert not retval

        bad_email_id = Identifier('email', 'botched@com', test_ded)
        retval = self.id_resolver.assess_identifier(bad_email_id)
        assert not retval

        good_phone_id = Identifier('home phone', '(999) 888-0001', test_ded)
        retval = self.id_resolver.assess_identifier(good_phone_id)
        assert retval

        good_email_id = Identifier('email', 'albe@gmail.not', test_ded)
        retval = self.id_resolver.assess_identifier(good_email_id)
        assert retval
        
    def match_existing_identity_test(self):
        """
        Unit test
        """
        