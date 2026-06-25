---
layout: archive
title: "UNR Device"
permalink: /unr-device/
excerpt: "Business allocation & person management/analysis Tool"
collection: portfolio
#author_profile: true
---
A UNR is an unfilled requirement or position on a project.
UNR Device was made with the aim of helping leadership find all possible roles any given person could fill for a project. 
Currently reports all personnel in a given department but could be theoretically updated to return specific people.

# Usage
* place clarity csv in the same directory as _look.py_
* change the `dept_employees` variable on _src/look.py:73_ to the name of the department you want to run this tool for
* run `./look.py` on the command line

## Technical Explanation
This program requires a csv file from Clarity as input and leverages MITREs proprietary `mii` python module.
It outputs an excel workbook for each person in a department with UNRs they can work. 
The tool assumes you can work on things that are 1 step above your "level".
Each workbook has 3 tabs: 
- Jobs your level that do not require an active clearance
- Jobs your level that do
- Jobs that have been posted without a level or security requirement

Taking the form of a python command line tool, the structure of the source code will be made up of a `main()` function that is called to be executed on the last step of the program.
```python
#!/usr/bin/env python

from mii import ActivePeople as ap
import pandas as pd
import os
import xlsxwriter
```

After the python shebang and imports, we define a that will be used along an axis (or column) on the dataframe. 
```python
def integerizer(step):
    if isinstance(step, str):
        step = int(step[0])
    return step

```

Now we define `main()` by first importing clarity's list of UNRS and then sanitizing the input by renaming, reording, and dropping some projects/columns. 
```python
def main():
    df = pd.read_csv("<csv from clarity>", header=1)
    
    # clean/reorganize file
    df = df[df["Type"] != 'Idea'] 
    df.drop('team_____internalid', axis=1, inplace=True)
    df.rename(columns={'oldName': 'newName'...}, inplace=True) 
    # reorder columns to have date first
    df = df[["Last Updated Date", "MITRE Number", "Last Updated By", "Project Leader", "Project Name"...]]
    # sort df by date descending (most recent first)
    df.sort_values(by=["Last Updated Date"], inplace=True, ascending=False)
```

Now we have to pull the list of employees using the proprietary python module, and align/translate a value to connect this data set with Claritys:
```python
    dept_employees = ap.get_department_employees("P531")
    # align the other dataset's "step" value to allow for numerical comparison
    for employee in dept_employees:
        match employee.job_level:
            case "Associate":
                employee.job_level = 1
            case "Intermediate":
                employee.job_level = 2
            case "Senior":
                employee.job_level = 3
            case "Lead":
                employee.job_level = 4
            case "Principal":
                employee.job_level = 5
            case "Senior Principal":
                employee.job_level = 6
            case "Distinguished":
                employee.job_level = 7
            case _:
                continue
```

We only need to define this dataframe once since it is not different per-employee:
```python
    no_step_or_clearance = df[(df["clearance"].isna()) & (df["step"].isna())]
```

lastly we need to loop through every employee in a department and, for each one:
* get their level
* create two dataframes with UNRs they can fill
* create an excel workbook with tabs of each dataframe  
* Adjust the width of the column so the workbook can be read
```python
    for employee in dept_employees:
        emp_step = employee.job_level
        base_emp_df = df[df["step"] <= emp_step + 1]
        emp_no_clearance_df = base_emp_df[base_emp_df["clearance"].isna()]
        emp_clearance_df = base_emp_df[base_emp_df["clearance"].notna()]

        with pd.ExcelWriter(f"files/bulk_out/{employee.first_name}-{employee.last_name}-unrs.xlsx", engine="xlsxwriter") as writer:
            emp_no_clearance_df.to_excel(writer, sheet_name='No Clearance', index=False)
            emp_clearance_df.to_excel(writer, sheet_name='Clearance', index=False)
            no_step_or_clearance.to_excel(writer, sheet_name='No Step or Clearance', index=False)
            # column widths courtesy of xlsxwriter.autofit()
            for sheet in writer.sheets:
                worksheet = writer.sheets[sheet]
                worksheet.autofit()
```

This tool found use in the hands of a few group leaders and department managers that wanted a total set of opportunities for the person they were working with.
