#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.message_registry import MessageRegistry

class MessageRegistryTest():
    """
    Message registry test harness.
    """
    def init_test(self):
        """
        Unit test
        """
        message_registry = MessageRegistry()
        assert len(message_registry.message) > 1

    def msg_test(self):
        """
        Unit test
        """
        message_registry = MessageRegistry()
        assert len(message_registry.msg(1000)) > 1