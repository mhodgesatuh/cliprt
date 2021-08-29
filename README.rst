# Installation
You will need run shell commands for the following statements.
1. pip install openpyxl
1. pip install python-dateutil

# Getting Version 0.2.x of this utility to run
TBD

# Requirements
- A single workbook with multiple worksheets, such that there is:
  - A single worksheet that provides the data element dictionary.
  - Multiple content worksheets that contain the client information.
    to the defined destination worksheets.

# Context

The DED worksheet, content worksheets, and the generated report worksheets
will all be in a single workbook.

This report utility will read the DED worksheet, use the instructions 
provided therein to process the content worksheets, and produce one or
more report worksheets as required.

Each row of each content worksheet represents information for a single
client.  This utility will attempt to recognize when different rows from
different content worksheets represent the same client, in which case it
will merge the client content into a single row on each of the report
worksheets.  Likewise, it can also detect when two different rows from
the same content worksheet represent the same client.

Note that report worksheets are also referred to as destination worksheets.
Same thing.

# Preparation Work

The usefulness of your reports depends entirely on now well you perform this
this preparation work.

1. Create the DED worksheet **"Data Elements"** at the front of the workbook.
1. Read through the content worksheets to create a unique list of column
   headings in the **"Data Element"** column of the the DED worksheet.
1. Identify which data elements are identifiers in the **"Dest Format"**
   column of the DED worksheet.
1. Define one or more report destinations in the **"Dest WS"** column of
   the DED worksheet.

Note: the report destination worksheets will be created at the end of
the workbook.

# Worksheets 
## Main Worksheets
Worksheets come in 3 main flavors:
1. DED Input - The data element dictionary (DED) worksheet used for providing
   reporting instructions.
1. Content Input (source) - Data content worksheets extracted from various sources, to
   be used for providing the reporting data.
1. Report Output (destination) - Communication reports planning worksheets, based on data 
content transformations.

Understanding the main worksheets:
- The first two flavors provide input for reporting.  
- The last flavor is the output from running this app. 
  - In other words.  Your reports are created by adding new worksheets.

And there are additional, supplemental worksheets.

## Supplemental worksheet(s)
1. Identity Matching Log - Log all identity matching activities. (not yet implemented)

# The Data Element Dictionary (DED)
## The Required DED Column Headings
- **"Data Element"**
  - The cell value is the name of the data element.
  - It is single valued.
  - Example data
    - "First Namee"
- **"Dest WS"** - Destination Worksheet indicator 
  - The cell value is the indicator (see below) of which report worksheet(s) 
    the data content will be reported in.
  - It is multi valued.  Comma-separate multiple indicators.
  - Example data
    - "fb,ims,lm" for Facebook, Infinity Movement Studio, Linda Melodia
- **"Dest Element"** - Destination Element
  - The cell value can be used to redirect a data element to a different element,
    for example: map "cell pbone" content data to "phone" destination data.
  - It is single valued.
  - Example data
    - "phone"
- **"Dest Format"** - Destination Data Element Format 
  - The cell value can indicate a standard formatting schema for the data element
    on the destination worksheet.
  - It is multi valued.  Comma-separate multiple indicators. 
  - Valid data element formats
    1. **"date"**
       - Data to be formatted as close to "mm/dd/yyyy" as possible.
    1. **"name"**
       - Data to be formatted as close to "first middle last" as possible.
    1. **"phone"**
       - Data to be formatted as close to "n-nnn-nnn-nnnn" as possible.
    1. **"identifier"**
    1. **"fragment=n"** where n is an integer

### About the Destination Data Element Format Options

The first 3 are used to standardize the way the data will look on the destination
worksheet.  **_Only one may be used at a time._**

The **"identifier"** format is important for selecting the data that will be used for identity
matching.  Since a single person will likely show up on multiple content worksheets,
it is important to select the data that will be used to perform identity matching.
Be sure to select at least two data elements; three would be optimal.

The **"fragment"** format is used for combining two source columns into a single destination
column.  Typically it is used to map separate source first and last name columns to accept
single destination "name" column.
- "fragment=1" is typically used for the first name format.
- "fragment=2" is typically used for the last name format.

### Example Data Element Formats
Example First Name:
- "identifier,name,fragment=1"

Example Last Name:
- "identifier,name,fragment=2"

Example Phone:
- 'identifier,phone'

_Bad example, don't do this.  It makes no sense; it's either one or the other._
- "name,phone"

# Development Notes
## Version: 0.1.0 - prototype, first release, currently under development
- dynamic workbook destinations
- multiple destinations per data element
- format logic for: date, name, phone data
- advanced format logic for: identifiers, fragments
- destination logic for merging multiple source columns to a single destination column
- advance logic for detecting identifier matches and merging client data
## Version 0.2.0 - first object oriended version
- implement a report package that is proceduraly utilized by the main module.
- accept the workbook name as a command line parameter instead of hard coding it.
- If no DED is present generate one by reading the column heads from the content worksheets.
## Version 0.3.0 - future
- add a logging feature
## Version 1.0.0 - future
- Publish
## Version 2.0.0 - future
- Integrate with a WordPress plugin.


# References
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