**CLIPRT - Client Information Parsing and Reporting Tool**
Pronunciation: "cliprt" sounds a bit like "liberty" (clipperty)

# Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [CLIPRT Command Line](#cliprt-command-line)
- [Definitions and Abbreviations](#definitions-and-abbreviations)
- [Overview](#overview)
- [Preparation Work](#preparation-work)
- [Worksheets](#worksheets)
  * [Main Worksheets](#main-worksheets)
  * [Supplemental Worksheet(s)](#supplemental-worksheet-s-)
- [The Data Element Dictionary (DED)](#the-data-element-dictionary--ded-)
  * [Required DED Column Headings](#required-ded-column-headings)
    + [Content Data Element Types](#content-data-element-types)
  * [Example DED](#example-ded)
- [Development Notes](#development-notes)
  * [Future considerations](#future-considerations)
  * [Version 1.0.0 - future](#version-100---future)
  * [Version 0.3.0 - currently under development](#version-030---currently-under-development)
  * [Version 0.2.0 - object oriented version](#version-020---object-oriented-version)
  * [Version 0.1.0 - prototype](#version-010---prototype)
- [References](#references)
# Overview
For a small business that uses multiple social media and 3rd-party applications to collect customer data,
prove a tool for defining how to merge the data to create reports, unique (deduplicated) customer lists,
etc to be used for marketing, communications and other purposes. Use a single Excel-compatible workbook
with multipe spreadsheets to collect the customer data into one place, define the reporting requirements,
and to generate the requested reports.
# Requirements
- python 3
- A single workbook with multiple worksheets, such that there is:
  - A single worksheet that provides the data element dictionary. _This can now be generated by CLIPRT._
  - Multiple content worksheets that contain the client information to be merged and used for reporting.
# Installation
Download this project to your computer.

**Notes on setting up on MacOS**

Set up an anaconda3 Python development environment:
- Edit the .zshrc with the following (change PATH as needed):

        # Force everything to use Python3 until Python2 is finally eliminated
        alias python=python3
        alias pip=pip3
        export PATH=/Users/username/opt/anaconda3/bin:$PATH
- Make sure you have the latest versions of setuptools and wheel installed:

        python -m pip install --user --upgrade setuptools wheel

 - Now run this command from the same directory where setup.py is located:

        python setup.py sdist bdist_wheel
Install the following CLIPRT dependencies:

    $ pip install openpyxl
    $ pip install python-dateutil
# CLIPRT Command Line
    $ python cliprt_cli.py

You can find a sample workbook in /resources
# Definitions and Abbreviations
- Client
  - Client informtion is collected from multiple sources, such as social media accounts and cloud services.
  - Each source provides a client worksheet that can be combined into a single workbook for analysis and reporting.
- DE (Data Element)
  - Data elements are listed in the data element dictionary.
  - Data elements are derived from the column headings of each the client content worksheets.
- DED (Data Element Dictionary)
  - All of the data elements are stored in the DED.
  - The DED is a worksheet, one row per data element.
  - The DED is used to define for each data element the client reporting requirements.
  - The DED's initial population can be performed automatically, or hand-built from scratch.
- Identifier
  - Client data includes data elements that can be used to identify a person.
  - Examples include name, phone number, email address.
  - By default client data across multiple sources can be matched if 3 or more identifiers match.
- Identity
  - Each client has a unique identity based on a set of identifiers.
  - Identity matching is the process of determining if a single client's information is available across multiple sources/worksheets.
  - At least 3 identifiers must be designted in the DED for identity matching to be utilized.
- Workbook
  - All of the related worksheets will be collected in a single Excel-compatible workbook.
- WS (Worksheet)
  - For CLIPRT reporting, multiple worksheets are required and include the following:
    - DED - CLIPRT can create this for you.  It will be the first worksheet in the workbook.
    - Two or more client worksheets, one per source.
    - One or more report worksheets, as specificed in the DED by you.  CLIPRT will create these.
# Overview
The DED worksheet, content worksheets, and the generated report worksheets will all be in a single Excel workbook.

This report utility will read the DED worksheet, use the instructions provided therein to process the content (source) worksheets, and produce one or more report (destination) worksheets as required.

Each row of each content worksheet represents information for a single client.  This utility will attempt to recognize when different rows from different content worksheets represent the same client, in which case it will merge the client content into a single row on each of the report worksheets.  Likewise, it can also detect when two different rows from the same content worksheet represent the same client.

Note that report worksheets are also referred to as **destination** worksheets.
# Preparation Work
The usefulness of your reports depends entirely on how well you perform this preparation work:

1. Create the DED worksheet **"DED"** at the front of the workbook.
1. Read through the content worksheets to create a unique list of column headings in the **"Content DE Name"** column of the the DED worksheet. CLIPRT can generate the DED automatically.
1. Identify which data elements are identifiers in the **"Dest DE Format"** column of the DED worksheet.
1. Select at least 3 data elements and set the **"Content DE Type"** column to "identifier".
1. Define one or more report destinations in the **"Dest WS"** column of the DED worksheet.

Note: the report destination worksheets will be created at the end of the workbook.
# Worksheets
All of the following worksheets must exist in a single workbook.
## Main Worksheets
The primary worksheets come in 3 main flavors:
- DED
  - The data element dictionary (DED) worksheet used for defining the reporting instructions.
  - CLIPRT can create this worksheet for you to get you started.
  - Update the worksheet to define your reporting requirements.
  - This worksheet is always first and always named "DED".
- Client content (source)
  - The data content worksheets are extracted from various sources to be used for providing the client data.
- Report Output (destination)
  - The report worksheets, are based on the provided client content.

And there are additional, supplemental worksheets.
## Supplemental Worksheet(s)
1. Identity Near Match Report - List identities that share one or more identifiers.
# The Data Element Dictionary (DED)
## Required DED Column Headings
- **"Content DE Name"** - Data element name
  - The cell value is the name of the data element.
  - It is **required** and it is single valued.
  - Example data
    - "First Name"
- **"Content DE Type"** - Data element type
  - The cell value designates the data element type.
  - It is **optional** and it is single valued.
  - Valid types
    - "identifier"
    - "fragment=n" where 'n' is an positive integer
  - Example data
    - "fragment=1"
- **"Dest WS"** - Destination Worksheet indicator
  - The cell value designates ouput to one more more destination reports.
  - It is **required if** "Dest DE Name" is not designated.
  - It is multi valued. Comma-separate multiple designations.
  - Example data for two report destinations
    - "social,newsletter"
- **"Dest DE Name"** - Destination data element name.
  - The cell value can be used to redirect a data element to a different data element in the report.
  - Is is **required if** "Dest WS" is not designated.
  - It is single valued.
  - Example data
    - "phone" to collect cell phone and home phone information in a single column on the report.
- **"Dest DE Format"** - Destination Data Element Format
  - The cell value can indicate a standard formatting schema for the data element on the destination worksheet.
  - It is multi valued.  Comma-separate multiple indicators.
  - Valid data element formats
    1. **"date"** format
       - Data to be formatted as close to "mm/dd/yyyy" as possible.
    1. **"name"** format
       - Data to be formatted as close to "first middle last" as possible.
    1. **"phone"** format
       - Data to be formatted as close to "n-nnn-nnn-nnnn" as possible.
### Content Data Element Types
The **"identifier"** designation indicates the data elements that will be used for identity matching. Since a single person will likely show up on multiple content worksheets, it is important to select the data that will be used to perform identity matching. Be sure to select at least three data elements.

The **"fragment=n"** designation is used for combining two source data elments into a single destination data element. Typically, it is used to map separate first and last name data elements to a single destination "name" data element.
- "fragment=1" is typically used to designate the first name fragment.
- "fragment=2" is typically used to designate last name fragment.
- Note: a "Dest DE Name" is required to define where the fragments will be mapped.
## Example DED
Worksheet columns A-E:
|Content DE Name|Content DE Type|Dest WS|Dest DE Name|Dest DE Format|
|-|-|-|-|-|
|id|identifier|newsletter| | |
|client|identifier|newsletter| |name|
|first name|fragment=1| |client| |
|last name|fragment=2| |client| |
|birthday|identifier| | | |
|home phone| | |phone| |
|cell phone| | |phone| |
|phone|identifier|newsletter| |phone|
|wk email| |newsletter| | |
|email|identifier|newsletter| |email|
# Development Notes
Most recent listed first.
## Future considerations
- GUI tools for running CLIPRT
- GUI tools for configuring the DED
- RESTful API for offering CLIPRT as a service
## Version 1.0.0 - future
- publish
## Version 0.3.0 - currently under development
- logging feature
- separate content_de_type from dest_de_format so that it is no longer overloaded
## Version 0.2.0 - object oriented version
- a command line interface for CLIPRT
- classes
- automated DED creation
- robust DED input validation
- robust unit testing and maximise code coverage
## Version 0.1.0 - prototype
- strictly procedural coding
- dynamic workbook destinations
- multiple destinations per data element
- format logic for: date, name, phone data
- advanced format logic for: identifiers, fragments
- destination logic for merging multiple source columns to a single destination column
- logic for processing identifiers and detecting identity matches and merging client data
# References
Since this is my first python program, the following are a subset of the links that helped me to get started.
- https://foss.heptapod.net/openpyxl/openpyxl/-/tree/branch/3.0/openpyx
- https://www.w3schools.com/python/python_dictionaries.asp
- https://docs.python.org/3/reference/index.html
- https://www.w3schools.com/python/ref_string_format.asp
- https://www.python-course.eu/python3_properties.php
- https://devblogs.microsoft.com/python/category/visual-studio-code/
- https://www.geeksforgeeks.org/counters-in-python-set-1/
- https://docs.python.org/3/library/functions.html#sorted
- https://docs.python.org/3/howto/sorting.html#sortinghowto
- https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-itemgetter/
- https://stackabuse.com/converting-strings-to-datetime-in-python/
- https://docs.python.org/3/tutorial/modules.html#packages
