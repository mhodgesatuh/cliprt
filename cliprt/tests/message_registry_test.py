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
    @staticmethod
    def init_test():
        """
        Unit test
        """
        message_registry = MessageRegistry()
        assert len(message_registry.message) > 1

    @staticmethod
    def msg_test():
        """
        Unit test
        """
        message_registry = MessageRegistry()
        assert message_registry.msg(1000)[0:8] == '(E1000) '
        assert message_registry.msg(5000)[0:8] == '(W5000) '
