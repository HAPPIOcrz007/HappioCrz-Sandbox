# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 10:28:26 2026

@author: noaha
"""
import pandas as pd

def read_asc_file(filepath):
    """Read .asc file and return numeric data section as DataFrame."""
    with open(filepath, "r") as f:
        lines = f.readlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("#DATA"):
            start = i + 1
            break
    if start is None:
        raise ValueError(f"No #DATA section found in {filepath}")
    df = pd.read_csv(filepath, sep="\t", header=None, skiprows=start)
    df = df.dropna().reset_index(drop=True)
    return df

def process_files(file1, file2, file3, output_file):
    # Read three files
    df1 = read_asc_file(file1)
    df2 = read_asc_file(file2)
    df3 = read_asc_file(file3)

    # Build combined DataFrame
    combined = pd.DataFrame()
    combined["Wavelength"] = df1[0] / 1000   # microns
    combined["Col1"] = df1[1] / 100
    combined["Col2"] = df2[1] / 100
    combined["Col3"] = df3[1] / 100

    # Sort by wavelength
    combined = combined.sort_values(by="Wavelength").reset_index(drop=True)

    # Metadata header
    header = """{ Units Wavelength Units } SI Microns
{ Thickness } 6
{ Conductivity } 1
{ IR Transmittance } TIR=0
{ Emissivity front back } Emis= 0.837 0.613
{ }
{ Ef_Source: Text File }
{ Eb_Source: Text File }
{ IGDB_Checksum: 0 }
{ Product Name: 63486_Solar Series Neutral 34_6mm_AM }
{ Manufacturer: AIS }
{ NFRC ID: 63486 }
{ Type: Coated }
{ Material: N/A }
{ Coating Name: 63486_Solar Series Neutral 34_6mm_AM }
{ Coated Side: Back }
{ Substrate Filename: 63485_New_AIS_ClearFloatglass_10012023_6mm_BM.txt }
{ Appearance: NEUTRAL }
{ Acceptance: # }
{ Uses:  }
{ Availability:   }
{ Structure:  }"""

    # Save output
    with open(output_file, "w") as f:
        f.write(header + "\n")
        combined.to_csv(f, sep="\t", index=False, header=False)

    print(f"Processed file saved to {output_file}")

# Example usage:
process_files("tr_file1.asc", "rg_file2.asc", "rf_file3.asc", "output.txt")