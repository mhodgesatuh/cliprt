#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_identity_resolver import ClientIdentityResolver
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.identifier import Identifier

class ClientIdentityResolverTest:
    """
    Client Identity Resolver test harness.    
    """
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    client_info.ded_processor.hydrate_ded()

    def _reset__registries(self):
        """
        Reset the client registry and the identifier registry after a
        unit test.
        """
        if len(self.client_info.client_reg.client_id_list) > 0:
            self.client_info.client_reg.client_id_list = {}
            self.client_info.client_reg.next_client_idno = 1000

        if len(self.client_info.identifier_reg.identifier_list) > 0:
            self.client_info.identifier_reg.identifier_list = {}

    def init_test(self):
        """
        Unit test
        """
        id_resolver = ClientIdentityResolver(
            self.client_info.client_reg, 
            self.client_info.identifier_reg
        )
        assert id_resolver.matched_identifier_types == []
        assert id_resolver.identifier_matched == []
        assert id_resolver.identifier_unmatched == []

    def create_identity_test(self):
        """
        Unit test
        """
        id_resolver = ClientIdentityResolver(
            self.client_info.client_reg, 
            self.client_info.identifier_reg
        )
        client_identity = id_resolver.create_identity()
        assert client_identity.client_idno == 1000
        assert client_identity.dest_ws == {'ims': 2, 'fb': 2}
        assert 1000 in self.client_info.client_reg.client_id_list
        assert self.client_info.client_reg.next_client_idno == 1001
        self._reset__registries()

    def match_existing_identity_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor.ded
        id_resolver = ClientIdentityResolver(
            self.client_info.client_reg, 
            self.client_info.identifier_reg
        )

        # Create a set of identifiers to be matched.
        identifiers = [
            ['id', '99912345'],
            ['phone', '(999) 888-0001'],
            ['home phone', '(999) 888-0001'],
            ['email', 'albe@gmail.not'],
        ]
        for id_data in identifiers:
            identifier = Identifier(id_data[0], id_data[1], test_ded)
            assert id_resolver.save_identifier(identifier)

        # Match these against the identifiers set up above.
        matching_identifiers = [
            ['client id', '99912345'],
            ['mobile phone', '999-888-0001'],
            ['email', 'albe@gmail.not'],
        ]
        for id_data in matching_identifiers:
            identifier = Identifier(id_data[0], id_data[1], test_ded)
            assert id_resolver.save_identifier(identifier)

        # Good identifiers are stored in the identifier registry.
        assert len(self.client_info.identifier_reg.identifier_list) == 3
        assert len(id_resolver.identifier_matched) == 3
        assert id_resolver.matched_identifier_types == ['phone', 'client id', 'email']

        self._reset__registries()

    def resolve_client_identity_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor.ded

        id_resolver = ClientIdentityResolver(
            self.client_info.client_reg, 
            self.client_info.identifier_reg
        )
        assert id_resolver.resolve_client_identity(3) == None

        """
        Test identity-matching logic.
        """
        identifiers_lists = [
            [
                ['id', '99912345'],
                ['phone', '(999) 888-0001'],
                ['home phone', '(999) 888-8708'],
                ['email', 'albe@gmail.not'],
            ],
            [
                ['client id', '99912345'],
                ['mobile phone', '999-888-0001'],
                ['email', 'albeebee@gmail.not'],
            ],
            [
                ['client id', '99912345'],
                ['mobile phone', '999-888-0001'],
                ['email', 'albe@gmail.not'],
            ],
        ]
        for identifiers in identifiers_lists:
            id_resolver = ClientIdentityResolver(
                self.client_info.client_reg, 
                self.client_info.identifier_reg
            )
            for id_data in identifiers:
                identifier = Identifier(id_data[0], id_data[1], test_ded)
                id_resolver.save_identifier(identifier)
            id_resolver.resolve_client_identity(3)

        assert 1000 in self.client_info.client_reg.client_id_list
        assert 1001 in self.client_info.client_reg.client_id_list
        assert self.client_info.client_reg.next_client_idno == 1002
        assert self.client_info.identifier_reg.identifier_list['client id::99912345'].client_ids == {1000, 1001}
        self._reset__registries()

    def save_identifier_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor.ded
        id_resolver = ClientIdentityResolver(
            self.client_info.client_reg, 
            self.client_info.identifier_reg
        )

        # Test bad identifiers.
        bad_identifiers = [
            ['home phone', '(999) 888-0000'],
            ['home phone', '(999) 888-9999'],
            ['home phone', '12345'],
            ['email', 'noemail'],
            ['email', 'botched@com'],
        ]
        for id_data in bad_identifiers:
            bad_identifier = Identifier(id_data[0], id_data[1], test_ded)
            assert not id_resolver.save_identifier(bad_identifier)

        # Test good identifiers.
        good_identifiers = [
            ['home phone', '(999) 888-0001'],
            ['email', 'albe@gmail.not'],
        ]
        for id_data in good_identifiers:
            identifier = Identifier(id_data[0], id_data[1], test_ded)
            assert id_resolver.save_identifier(identifier)

        # Good identifiers are stored in the identifier registry.
        assert len(self.client_info.identifier_reg.identifier_list) == 2

        # Test for a threshold number of identifiers by adding the third
        # identifier.
        identifiers = [
            ['client id', '123456789'],
        ]
        for id_data in identifiers:
            identifier = Identifier(id_data[0], id_data[1], test_ded)
            assert id_resolver.save_identifier(identifier)
        assert len(self.client_info.identifier_reg.identifier_list) == 3
        assert len(id_resolver.identifier_matched) == 0
        assert len(id_resolver.identifier_unmatched) == 3
        self._reset__registries()