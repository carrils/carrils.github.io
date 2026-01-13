---
layout: archive
title: "Machine-Readable File (MRF) Comparison Tool"
permalink: /mrf-comparison-tool/
excerpt: "A command-line tool that compares the contents of MRFs and produces an Excel workbook for increased ease of interpretation"
collection: portfolio
#author_profile: true
---
MRF Comparison Tool was made for performing informal desk audits of the MRFs that insurers and hospitals were required to make publicly available from the two rules CMS made. I was asked to look into whether the prices in the files for charge items and services matched between the insurers and hospitals files. 

This work supported CMS in their price transparency initivaitves for both [health insurers](https://www.cms.gov/priorities/key-initiatives/healthplan-price-transparency) and [hospitals](https://www.cms.gov/priorities/key-initiatives/hospital-price-transparency).

# Usage

```zsh
  ./mrf-comparison.py
```
Running the tool from the command line compares the two MRFS and produces an Excel workbook and finds matching charge items between them. This allows us to compare the reported price in one file versus the other.


# Technical Explanation
Taking the usual form of a python script it starts with a python shebang and importing dependencies, followed by a main function that will be called as the last step in the script.

We will stay in `main()` until the script calls the main function last: 
```python
#!/usr/local/bin/python3

import csv
import openpyxl
import json
from datetime import datetime
import numpy as np
import pandas as pd

def main():
```

Next we use pandas to create DataFrames of both MRFs from insurers and hospitals:
```python
    # Hospital MRF dataframe
    hpt_df = pd.read_excel(
    "https://healthcare.ascension.org/-/media/project/ascension/healthcare/price-transparency-files/in/350869066_ascension-st-vincent-hospital_standardcharges.xlsx",
    'Standard Charges', header=1, usecols='B, C, D, E, F, G, H, I, J, AF,AG, AH, AI, BR')

    # Insurer MRF dataframe
    tic_df = pd.read_json(
        "https://mysmarthealth.org/-/media/Files/SmartHealth/Documents/Transparency-in-coverage/2022-06-24_ABS_AscensionSmartHealth_in-network-rates.json?la=en&hash=71F0E7907ADFED24203A25BCB20FD8EF380CF477",
        orient='columns')
```

After initializing a variable to help us collect the hospital-specific charge items, we begin to iterate through the insurer MRF file, creating a frame for each `in_network` object we encounter:
```python
    asc_items = []

    for row in tic_df.itertuples():
        # create frame for in_network object
        df = pd.DataFrame.from_dict(row.in_network)
```
These objects represent the in-network rates files outlined in the rule.
A 'rate' here means the price of a charge item under this plan.

For every in-network rate we encounter we want to iterate through its negotiated rates with providers and gather:
- the negotiated price
- the providers' tax identification numbers

```python
        for rate in df.itertuples():
            negotiated_rate_details_object = rate.negotiated_rates
            # The negotiated price
            negotiated_prices_object = pd.DataFrame.from_dict(negotiated_rate_details_object['negotiated_prices'])
            
            providers = pd.DataFrame.from_dict(negotiated_rate_details_object['provider_groups'])
            # The providers' tax identification numbers
            tin = pd.DataFrame.from_records(providers['tin'])
```

This next part uses the Tax Identification Number (hardcoded) for the hospital we pulled the MRF of in the first step.
This can be changed to the TIN of whichever hospital you pulled the MRF of. You do not need to change anything for the insurer file, you need only supply it.

We look through the TINs of the providers to find the TIN of the hospital we are interested in.
If found, we create an item for the charge item and append it to the list variable:
```python
            # the hardcoded hospital tin
            if tin.value.loc[0] == '350869066' and tin.type.loc[0] == 'ein':
                # create item
                asc_item_name = df.name.loc[0]
                asc_item_billing_code = df.billing_code.loc[0]
                asc_item_code_type = df.billing_code_type.loc[0]
                asc_item_negotiated_price = negotiated_prices_object.negotiated_rate.loc[0]
                # append item
                asc_items.append([asc_item_billing_code, asc_item_code_type, asc_item_name, asc_item_negotiated_price])
```

Now that we have the hospitals in-network charge items from the insurer MRF in `asc_items`, we create a new dataframe with those items and begin to process the hospital MRF.
```python
    tic_comparison_df = pd.DataFrame.from_records(data=asc_items, columns=['Code', 'Code_Type', 'Description', '"TiC-Parsed" Negotiated Price'])
    # only include columns from the hospital file we are interested in
    hpt_comparison_df = hpt_df[
        ["Code", "Code_Type", "Description", "Commercial_Other_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_3499",
         "Commercial_Other_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_2364", "Commercial_Other_SMARTHEALTH_SMARTHEALTH_3499",
         "Commercial_Other_SMARTHEALTH_SMARTHEALTH_2364",
         "Blue_Cross_Blue_Shield_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_3943"]]
```

Now we merge the two frames on the billing code for the charge item to bridge the two data sets.
This is where the charge items from both data sets are connected. 
We need to select the columns on the resulting merge dataframe that we need, and then rename them.
```python
    result_merge = hpt_comparison_df.merge(tic_comparison_df, how='inner', on='Code')
    # column select
    result_merge = result_merge[['Code', 'Code_Type_x', 'Code_Type_y', '"TiC-Parsed" Negotiated Price',
                     'Commercial_Other_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_3499',
                     'Commercial_Other_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_2364',
                     'Commercial_Other_SMARTHEALTH_SMARTHEALTH_3499',
                     'Commercial_Other_SMARTHEALTH_SMARTHEALTH_2364',
                     'Blue_Cross_Blue_Shield_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_3943', 'Description_x',
                     'Description_y']]
    rename_dict = {'Code': 'Code', 'Code_Type_x': 'Code_Type_HPT', 'Code_Type_y': 'Code_Type_TiC',
                   '"TiC-Parsed" Negotiated Price': 'TiC-Parsed Negotiated Price',
                   'Commercial_Other_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_3499': 'SMARTHEALTH_PPO_HDHP_ASCEN_3499',
                   'Commercial_Other_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_2364': 'SMARTHEALTH_PPO_HDHP_ASCEN_2364',
                   'Commercial_Other_SMARTHEALTH_SMARTHEALTH_3499': 'SMARTHEALTH_SMARTHEALTH_3499',
                   'Commercial_Other_SMARTHEALTH_SMARTHEALTH_2364': 'SMARTHEALTH_SMARTHEALTH_2364',
                   'Blue_Cross_Blue_Shield_SMARTHPPOA_SMARTHEALTH_PPO_HDHP_ASCEN_3943': 'BCBS - SMARTHEALTH_PPO_HDHP_ASCEN_3943',
                   'Description_x': 'HPT Description',
                   'Description_y': 'TiC Description'}
    # column rename
    result_merge = result_merge.rename(rename_dict, axis="columns")
```

Lastly we need to export the merged information to an Excel workbook. We are including the base insurer and hospital frames as well:
```python
    with pd.ExcelWriter("HPT_Billing_Information.xlsx") as writer:
        hpt_df.to_excel(writer, sheet_name='HPT Billing Code Items', na_rep='N/A', float_format='%.2f')
        tic_df.to_excel(writer, 'TiC Billing Code Items', na_rep='N/A')
        result_merge.to_excel(writer, 'inner join on Code value', na_rep='N/A', float_format='%.2f')
        
```

That concludes `main()`. Now all that's left to do is to call it.

```python
if __name__ == '__main__':
    main()
```

