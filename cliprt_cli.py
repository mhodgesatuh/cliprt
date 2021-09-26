#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
            CLIPRT, sounds like liberty.  Pronounced clipperty.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
import os
import sys

from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.cliprt_user_guide import CliprtUserGuide

if sys.version_info[0] < 3:
    raise Exception('Error: Python version 3 is required. Found version {}.'.format(sys.version_info[0]))

EXIT_MSG = 'Ended cliprt as requested.'

# Initializations
client_info_wb = None

"""
This is the CLIPRT command line interface (CLI).
"""

def user_requests(prompt_a, prompt_b):
    """
    Process the generic user prompting
    """
    print('\n{}'.format(prompt_a))
    inputting = True
    prompt_hint = '(Yes/No/Help/Quit) <No>: '
    while inputting:
        user_input = input(prompt_hint).lower() or 'n'
        if user_input in ['n', 'no']:
            return False
        if user_input in ['y', 'yes']:
            return True
        if user_input in ['h', 'help']:
            CliprtUserGuide()
            continue
        if user_input in ['q', 'quit', 'e', 'exit']:
            print(EXIT_MSG)
            sys.exit(0)
        print('Warning: your intention is not clear. Please answer "Yes" or "No".')
        print('{} {}'.format(prompt_b, prompt_hint))

print('\n\n*******    ******      *      *           *           *         *')
print('Welcome to CLIPRT, the Client Information Parsing and Reporting Tool.')
print('FYI, the client data element dictionary is referenced as the "DED" from hereon.')
print('***')
cliprting = True
prompt_hint = '(Help/Quit) <Quit>: '
while cliprting:
    """
    Prompt for the client data workbook.
    """
    print('\nEnter the path and name of an Excel-compatible client workbook.')
    inputting = True
    while inputting:
        workbook_file = input(prompt_hint) or 'q'
        if workbook_file.lower() in ['q', 'quit']:
            print(EXIT_MSG)
            sys.exit(0)
        if workbook_file.lower() in ['h', 'help']:
            CliprtUserGuide()
            continue
        if os.path.exists(workbook_file):
            print('  ...opening workbook...', end='')
            client_info_wb = ClientInformationWorkbook(workbook_file)
            print('opened!')
            inputting = False
        else:
            print('\nWarning: workbook file not found.  Check the file path, your spelling and try again.')
            print('Path and name?')
    """
    The workbook is available.
    """
    if not client_info_wb.has_a_ded_ws():
        """
        Prompt to see if the DED worksheet should be generated.
        """
        prompt_a = 'The DED worksheet has not been created.  Create the DED worksheet?'
        prompt_b = 'Create the worksheet?'
        if user_requests(prompt_a, prompt_b):
            print('  ...creating worksheet...')
            client_info_wb.create_ded_worksheet()
            print('The DED worksheet has been created.  Open the workbook and configure the DED for your reporting requirements.')
            continue
        else:
            inputting = False
    """
    The Data Element Dictionary is available.
    """
    # Verify the DED.  Exceptions will be thrown if any errors are encountered.
    client_info_wb.ded_is_verified()
    """
    The Data Element Dictionary is verified. 
    Ready to create the client report (destination) worksheets.
    """
    # Print the DED for review?
    prompt_a = 'Skip the client reporting?  Only print the DED reporting configuration?'
    prompt_b = 'Print the DED configuration?'
    if user_requests(prompt_a, prompt_b):  
        client_info_wb.print_ded_report()
        continue
    
    # Create the client report worksheets.
    prompt_a = 'Run the client report without providing any progress reporting?'
    prompt_b = 'Disable progress reporting?'
    disable = user_requests(prompt_a, prompt_b)
    print('\nCLIPR has started working on your client worksheets...this may take some time.')
    print('  ...creating report worksheet(s)...')
    client_info_wb.create_client_reports(disable)
    sys.exit(0)

print(EXIT_MSG)