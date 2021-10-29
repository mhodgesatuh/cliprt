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
    err_str = 'Error: Python version 3 is required. Found version {}.'
    raise Exception(err_str.format(sys.version_info[0]))

WELCOME_MSG =\
    'Welcome to CLIPRT, the Client Information Parsing and Reporting Tool.'
EXIT_MSG = 'Ended cliprt as requested.'

def request_create_client_reports(wb):
    """
    Create the client report worksheets.
    """
    prompt_a =\
        'Run the client report without providing any progress reporting?'
    prompt_b = 'Disable progress reporting?'
    verbosity = user_requests(prompt_a, prompt_b)
    print('\nCLIPR has started working on your client worksheets...'\
        'this may take some time.')
    print('  ...creating report worksheet(s)...')
    wb.create_client_reports(verbosity)
    sys.exit(0)

def request_create_ded(wb):
    """
    Prompt to see if the DED worksheet should be generated.
    """
    prompt_a =\
        'The DED worksheet has not been created. Create the DED worksheet?'
    prompt_b = 'Create the worksheet?'
    if user_requests(prompt_a, prompt_b):
        print('  ...creating DED worksheet, pkease wait...')
        wb.create_ded_worksheet()
        msg =\
            'The DED worksheet has been created. '\
            'Open the workbook and configure the DED '\
            'for your reporting requirements.'
        print(msg)
        sys.exit(0)

def request_print_ded(wb):
    """
    Print the DED for review?
    """
    prompt_a = 'Skip the client reporting? Only print the DED configuration?'
    prompt_b = 'Print the DED configuration?'
    if user_requests(prompt_a, prompt_b):
        wb.print_ded_report()
    return True

def request_workbook():
    """
    Prompt for the client data workbook.
    """
    prompt_hint = '(Help/Quit) <Quit>: '
    print('\nEnter the path and name of an Excel-compatible client workbook.')
    inputting = True
    while inputting:
        workbook_file = input(prompt_hint) or 'q'
        if workbook_file[0].lower() in ['q']:
            # Exit if the user has lost interest.
            print(EXIT_MSG)
            sys.exit(0)
        if workbook_file[0].lower() in ['h']:
            # Provide the User Guide if requested.
            CliprtUserGuide()
            continue
        if os.path.exists(workbook_file):
            # If work book ws provided successfully, we can continue
            # with processing the workbook.
            print('  ...opening workbook...', end='')
            wb = ClientInformationWorkbook(workbook_file)
            print('opened!')
            # Ready to move on and process the workbook.
            inputting = False
        else:
            err_str =\
                '\nWarning: workbook file not found. '\
                'Check the file path, your spelling and try again.'
            print(err_str)
            print('Path and name?')
    # Return the workbook for further processing.
    return wb

def user_requests(prompt_a, prompt_b):
    """
    Generic user request handler.
    """
    print(f'\n{prompt_a}')
    inputting = True
    prompt_hint = '(Yes/No/Help/Quit) <No>: '
    while inputting:
        user_input = input(prompt_hint).lower() or 'n'
        if user_input[0] in ['n']:
            return False
        if user_input[0] in ['y']:
            return True
        if user_input[0] in ['h']:
            CliprtUserGuide()
            continue
        if user_input[0] in ['q', 'e']:
            print(EXIT_MSG)
            sys.exit(0)
        print('Your intention is not clear. Please answer "Yes" or "No".')
        print(f'{prompt_b} {prompt_hint}')

# ------------------------------------------------
# This is the CLIPRT command line interface (CLI).
# ------------------------------------------------
print(WELCOME_MSG)

# Prompt for the workbook.
client_info_wb = request_workbook()

input_loop = True
while input_loop:

    # Process the workbook.
    if not client_info_wb.has_a_ded_ws():
        # Create a new DED and exit so that the use can configure it
        # for the client reporting.
        request_create_ded(client_info_wb)

    # Create the client reports.
    client_info_wb.ded_processor.hydrate_ded()
    client_info_wb.ded_processor.hydration_validation()
    if client_info_wb.ded_is_verified:
        request_print_ded(client_info_wb)
    request_create_client_reports(client_info_wb)

print(EXIT_MSG)
