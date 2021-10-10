#!/usr/bin/env python
"""
Project:  CLIPRT - Client Information Parsing and Reporting Tool.
Version:  0.1.0
@author:    mhodges
Copyright 2020 Michael Hodges
"""
from dateutil.parser import *
from datetime import *
import operator

def save_identifier(identity, identifier_matching, de_name, de_value, identifier_types):
    """
    Search for the identifier value to see if we have a potential identity match.
    Add the identifier to the identifier-matching list.
    """
    if de_value == None:
        # If there's no value there's nothing to do.
        return

    if de_value in identity['value']:
        identifier_matching['matched'][de_name] = {'value': de_value}
        # Track the number of unique types found since it takes a minimal number
        # to indicate an identity match.

        ## TODO: need to ensure that remapped identifiers don't get accounted as distinct
        ##       identifier types.
        
        if not de_name in identifier_types:
            identifier_types.append(de_name)
    else:
        # Save the identifier value since it doesn't match any existing saved identifier.
        identity['value'][de_value] = {'de_name': de_name, 'idno_set': set()}
        identifier_matching['unmatched'][de_name] = {'value': de_value}

def format_date(date_value):
    date_obj = parse(date_value)
    return date_obj.strftime("%m/%d/%Y")

def format_name(data_value):
    name_pieces = data_value.split(",")
    # If there are no pieces there's nothing to do.
    if len(name_pieces) <= 1:
        return data_value
    # Convert format 'last, first' to 'first last'.
    ret_value = ''
    # Start with the 2nd piece.
    i = 1
    # No problem if there are extra commas.
    while i < len(name_pieces):
        ret_value+=name_pieces[i]
        i+=1
    # Last name goes last.
    ret_value+=' '+name_pieces[0]
    return ret_value

def format_phone(data_value, area_code = '808', country_code = '1'):
    # Digits only.
    pho_no = ''.join(i for i in data_value if i.isdigit())
    # Output mask: 1-999-123-4567
    pho_mask = '{}-{}-{}-{}'
    # Format known phone number data lengths.
    if len(pho_no) == 7:
        return pho_mask.format(country_code, area_code, pho_no[0:3], pho_no[3:7])
    elif len(pho_no) == 10:
        return pho_mask.format(country_code, pho_no[0:3], pho_no[3:6], pho_no[6:10])
    elif len(pho_no) == 11:
        return pho_mask.format(pho_no[0:1], pho_no[1:4], pho_no[4:7], pho_no[7:11])
    else:
        return data_value

def id_number_matcher(idno_sets):
    """
    Apply set theory to the sets containing identity data matches in order to determine
    which existing identity is likely the best match.
    """

    # Create a list of all identity numbers.
    first_idno_set = list(idno_sets)[0]
    idno_list = first_idno_set.union(*idno_sets)

    # Count the occurences of each identity number across all sets of identity numbers.
    idno_match_cnt = {}
    for idno in idno_list:

        # Initialize the count for each identity number.
        idno_match_cnt[idno] = 0

        # Render it as a set in order to compare to the identity number sets.
        idno_match_set = {idno}

        # Count number of sets in which the identity number is found.
        for idno_set in idno_sets:
            if idno_match_set.issubset(idno_set):
                idno_match_cnt[idno]+=1

    # Sort such that the identity number with the most matches is listed first.
    sorted_idno_by_cnt = sorted(idno_match_cnt.items(), key=operator.itemgetter(1), reverse=True)

    # The best match identity number is in the first key of the first tuple.
    return sorted_idno_by_cnt[0][0]

def init_list(cnt):
    """
    Initialize a list to a prespecifiled length.
    """
    ims_list = []
    i = 0
    while i < cnt:
        ims_list.append(None)
        i+=1
    return ims_list

def init_ws(wb, ws_name):
    if ws_name in wb.sheetnames:
        # Clear the worksheet if it exists
        ws = wb[ws_name]
        ws.delete_rows(ws.min_row, amount=ws.max_row - ws.min_row + 1)
    else:
        # Create the worksheet if needed
        ws = wb.create_sheet(title=ws_name)
    return ws

def list_to_str(a_list, delim=' '):
    str_value = ''
    for an_item in a_list:
        if an_item == None:
            continue
        str_value += delim + an_item
    return str_value[1:len(str_value)]

def lowercase(str_value):
    return None if str_value == None else str_value.lower()

# Convert a comma-delimited string to a list.  
def make_list(str_value):
    return None if str_value == None else str_value.replace(' ','').split(',')

# Convert numbers and text to lowercase strings; strip leading and trailing spaces.
def make_searchable(str_value):
    if type(str_value) != str:
        return str(str_value)
    elif str_value == None:
        return None
    else:
        return " ".join(str_value.split()).lower()

def update_dest_cell(ws, row_idx, col_idx, cell_data, data_format = None):
    """
    Determine if the destination cell already has a value in it add the new value to the
    using a comma delimitor.
    """
    
    if cell_data == None:
        # If there's no new data there's nothing to do.
        return

    # Format the new cell data if a data format has been provided.
    if data_format == 'date':
        formatted_data = format_date(cell_data)
    elif data_format == 'name':
        formatted_data = format_name(cell_data)
    elif data_format == 'phone':
        formatted_data = format_phone(cell_data)
    else:
        formatted_data = str(cell_data)

    cell_value = ws.cell(row_idx, col_idx).value

    if cell_value == None:
        # Simply write the new cell data to an empty destination cell.
        ws.cell(row_idx, col_idx, value=formatted_data)
        return

    # todo: idea: utilize duplicate information to update an id match confidence indicator
    if formatted_data in cell_value:
        # Don't save the same data twice.
        return
        
    ws.cell(row_idx, col_idx, value='{}, {}'.format(cell_value, formatted_data))