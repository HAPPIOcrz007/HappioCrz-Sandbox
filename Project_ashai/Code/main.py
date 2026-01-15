import json
import os

import pandas as pd
import streamlit as sl

# # # # # # # # # # # # # # # # # # #
LASTFORM_NAME = "formLast.json"
BASE_DIRECTORY = "home"
OUT_DIRECTORY = "downloads"
CHECKED_FILE_NAME = "checkbox.json"
FILES_MOVED = 3

# # # # # # # # # # # # # # # # # # #


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


def build_header(form_data):
    """Build strict header block using form values."""
    return f"""{{ Units Wavelength Units }} SI Microns
{{ Thickness }} {form_data["Thickness"]}
{{ Conductivity }} {form_data["Conductivity"]}
{{ IR Transmittance }} TIR={form_data["IR_Transmittance"]}
{{ Emissivity front back }} Emis= {form_data["Emissivity_front"]} {form_data["Emissivity_back"]}
{{ }}
{{ Ef_Source: {form_data["Ef_Source"]} }}
{{ Eb_Source: {form_data["Eb_Source"]} }}
{{ IGDB_Checksum: {form_data["IGDB_Checksum"]} }}
{{ Product Name: {form_data["Full_Product_Name"]} }}
{{ Manufacturer: {form_data["Manufacturer"]} }}
{{ NFRC ID: {form_data["NFRC_id"]} }}
{{ Type: {form_data["Type"]} }}
{{ Material: {form_data["Material"]} }}
{{ Coating Name: {form_data["Coating_Name"]} }}
{{ Coated Side: {form_data["Coated_Side"]} }}
{{ Substrate Filename: {form_data["Substrate_filename"]} }}
{{ Appearance: {form_data["Appearance"]} }}
{{ Acceptance: {form_data["Acceptance"]} }}
{{ Uses: {form_data["Uses"]} }}
{{ Availability: {form_data["Availability"]} }}
{{ Structure:  }}"""


def processing_script(input_dir: str, output_dir: str):
    """Process files listed in checkbox.json and save output in output_dir."""
    # Load form metadata
    with open(LASTFORM_NAME, "r") as f:
        form_data = json.load(f)

    # Load selected files
    with open(CHECKED_FILE_NAME, "r") as f:
        checked_files = json.load(f)

    if len(checked_files) != 3:
        raise ValueError("Exactly 3 files must be selected in checkbox.json")

    # Read ASC files
    paths = [os.path.join(input_dir, f) for f in checked_files]
    df1, df2, df3 = [read_asc_file(p) for p in paths]

    # Build numeric table
    combined = pd.DataFrame()
    combined["Wavelength"] = df1[0] / 1000  # convert nm → microns
    combined["Col1"] = df1[1] / 100
    combined["Col2"] = df2[1] / 100
    combined["Col3"] = df3[1] / 100  # Sort and filter: keep only rows >= 0.32 microns

    combined = combined.sort_values(by="Wavelength").reset_index(drop=True)
    combined = combined[combined["Wavelength"] >= 0.32]

    # Format columns separately
    combined["Wavelength"] = combined["Wavelength"].astype(float).round(3).astype(str)
    combined["Col1"] = combined["Col1"].astype(float).round(8).astype(str)
    combined["Col2"] = combined["Col2"].astype(float).round(8).astype(str)
    combined["Col3"] = combined["Col3"].astype(float).round(8).astype(str)

    # Build header
    header = build_header(form_data)

    # Output filename based on Full_Product_Name
    output_file = os.path.join(output_dir, form_data["Full_Product_Name"])

    # Write output file
    with open(output_file, "w") as f:
        f.write(header + "\n")
        combined.to_csv(f, sep="\t", index=False, header=False)

    print(f"✅ Output saved to {output_file}")


# # # # # # # # # # # # # # # # # # #

# load existing JSON
try:
    with open(LASTFORM_NAME, "r") as lastForm:
        data = json.load(lastForm)
except (json.JSONDecodeError, FileNotFoundError):
    data = None  # file is empty, invalid, or missing

# Step 2: If empty, fill with base data
if data is None:
    print(f"{LASTFORM_NAME} is empty \n filling base data")
    lastForm_data = {
        "Wavelength": "",
        "Thickness": 0,
        "Conductivity": 0.000,
        "IR_Transmittance": 0.000,
        "Emissivity_front": 0.000,
        "Emissivity_back": 0.000,
        "Ef_Source": "Text Files",
        "Eb_Source": "Text Files",
        "IGDB_Checksum": 0.000,
        "Product_Name": "name",
        "Full_Product_Name": "",
        "Additional_Details": "aditional info",
        "Manufacturer": "AIS",
        "NFRC_id": 1000,
        "Type": "type",
        "Material": "N/A",
        "Coating Name": "",
        "Coated_Side": "side",
        "Substrate_filename": "file.txt",
        "Appearance": "appearence",
        "Acceptance": " ",
        "Uses": " ",
        "Availability": " ",
        "Directory": BASE_DIRECTORY,
        "Out_Directory": OUT_DIRECTORY,
    }

    lastForm_data["Full_Product_Name"] = (
        f"{int(lastForm_data['NFRC_id'])}_{lastForm_data['Product_Name']}_"
        f"{lastForm_data['Thickness']}mm_{lastForm_data['Additional_Details']}.txt"
    )
    lastForm_data["Coating_Name"] = (
        f"{int(lastForm_data['NFRC_id']) + 1}_{lastForm_data['Product_Name']}_"
        f"{lastForm_data['Thickness']}mm_{lastForm_data['Additional_Details']}.txt"
    )

    with open(LASTFORM_NAME, "w") as lastForm:
        json.dump(lastForm_data, lastForm, indent=4)

    print("default data added successfully")

# # # # # # # # # # # # # # # # # # #
with open(LASTFORM_NAME, "r") as lastForm:
    data = json.load(lastForm)

sl.set_page_config(page_title="File Compilation", layout="wide")
sl.title("📁 File Compiler 📁")
sl.header("Primary Data")

one, two = sl.columns(2)
with one:
    sl.text_input("Name", key="product", value=data.get("Product_Name", ""))
with two:
    sl.text_input(
        "Additional Details", key="details", value=data.get("Additional_Details", "")
    )
sl.number_input("Thickness", key="thickness", value=data.get("Thickness", 0))
sl.number_input(
    "Emmissivity Back",
    key="emissivity",
    min_value=0.000,
    value=data.get("Emissivity_back", 0.000),
)
sl.text_input("Appearence", key="appearence", value=data.get("Appearance", ""))
nfrcID = int(data.get("NFRC_id", 1)) + 1
sl.markdown("---")
sl.number_input(
    "NFRC id",
    key="nfrc_id",
    min_value=0,
    step=1,
    value=nfrcID,
)
nfrcID = sl.session_state["nfrc_id"]
full_Product_Name = f"{nfrcID}_{sl.session_state['product']}_{sl.session_state['thickness']}mm_{sl.session_state['details']}"
sl.text_input(
    "Substrate Filename", key="filename", value=data.get("Substrate_filename", "")
)
sl.text_input(
    "Product Name",
    key="f_p_name",
    value=f"{full_Product_Name}",
)
sl.markdown("---")
# # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # #
# Getting Files from the Directory

sl.text_input("Enter a Valid Directory", key="dir", value=data.get("Directory"))


directory = sl.session_state["dir"]

if not (directory):
    pass
elif not (os.path.isdir(directory)):
    sl.error(f"Please enter a valid directory. {directory} does not exist!")
    # directory = os.getcwd()
else:
    files = [
        file
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file))
    ]

    with sl.expander("Files"):
        selected = []

        col_a, col_b = sl.columns(2)

        with col_a:
            sl.text_input(
                "Enter File Name to search for in file seperated by commas",
                key="name_search",
            )
        with col_b:
            sl.text_input(
                "Enter tags to search for in file seperated by commas", key="search"
            )

        search = sl.session_state["search"].strip()
        name_search = sl.session_state["name_search"].strip()

        search_patterns = [p.strip() for p in search.split(",") if p.strip()]
        name_patterns = [n.strip() for n in name_search.split(",") if n.strip()]

        try:
            with open(CHECKED_FILE_NAME, "r") as f:
                checked_files = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            checked_files = []  # Show already checked files with numbering

        for file in files:
            show_file = False

            if file in checked_files:
                show_file = True

            if show_file:
                if sl.checkbox(file, key=f"{file}_checked", value=True):
                    print(f"{file} is already checked")
                else:
                    checked_files.remove(file)
                    print(f"{file} is removed from checked")
                    with open(CHECKED_FILE_NAME, "w") as f:
                        json.dump(checked_files, f, indent=4)
        for file in files:
            show_file = False

            if not search_patterns and not name_patterns:
                show_file = True

            for pattern in search_patterns:
                if (
                    pattern + "." in file
                    or pattern + "_" in file
                    or "_" + pattern in file
                    or "." + pattern in file
                ):
                    show_file = True
                    break

            for name in name_patterns:
                if name in file:
                    show_file = True
                    break

            if file in checked_files:
                show_file = False

            if show_file:
                if sl.checkbox(file, key=f"{file}_filter"):
                    checked_files.append(file)
                    print(f"{file} is checked")
                    with open(CHECKED_FILE_NAME, "w") as f:
                        json.dump(checked_files, f, indent=4)

try:
    with open(CHECKED_FILE_NAME, "r") as f:
        checked_files = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    checked_files = []

sl.write("Files Selected:", checked_files)

sl.text_input("Enter a Valid Directory", key="out_dir", value=data.get("Out_Directory"))

output_directory = sl.session_state["out_dir"]
sl.markdown("---")

sl.header("Secondary Data")
with sl.expander("Show Details"):
    one, two, three = sl.columns(3)

    with one:
        sl.text_input(
            "Wavelength Unit", key="wavelength", value=data.get("Wavelength", "")
        )
        sl.number_input(
            "Conductivity", key="conductivity", value=data.get("Conductivity", 0.000)
        )
        sl.text_input(
            "Enter IR Transmittance",
            key="tir",
            value=data.get("IR_Transmittance", 0.000),
        )
        sl.number_input(
            "Emissivity front",
            key="emissivity_front",
            value=data.get("Emissivity_front", 0.000),
        )
        sl.text_input("Ef_Source", key="efs", value=data.get("Ef_Source", "Text File"))

    with two:
        sl.text_input("Eb_Source", key="ebs", value=data.get("Eb_Source", "Text File"))
        sl.text_input(
            "Manufacturer", key="manufacturer", value=data.get("Manufacturer", "AIS")
        )
        sl.text_input("Type", key="type", value=data.get("Type", "Coated"))
        sl.text_input("Material", key="material", value=data.get("Material", "N/A"))
        sl.text_input("Coating name", key="coating_name", value=f"{full_Product_Name}")
        sl.text_input(
            "Coated Side", key="coated_side", value=data.get("Coated_Side", "")
        )

    with three:
        sl.text_input("Acceptance", key="acceptance", value=data.get("Acceptance", "#"))
        sl.text_input("Uses", key="uses", value=data.get("Uses", "N/A"))
        sl.text_input(
            "Availibility", key="availibility", value=data.get("Availability", "N/A")
        )
        sl.number_input(
            "IGDB_Checksum", key="igbd", value=data.get("IGDB_Checksum", 0.0)
        )
        sl.text_input("Appearence", key="appear", value=data.get("Appearance", "#"))

################################
if sl.button("💾 Save Data"):
    final_form = {
        "Wavelength": sl.session_state["wavelength"],
        "Thickness": sl.session_state["thickness"],
        "Conductivity": sl.session_state["conductivity"],
        "IR_Transmittance": sl.session_state["tir"],
        "Emissivity_front": sl.session_state["emissivity_front"],
        "Emissivity_back": sl.session_state["emissivity"],
        "Ef_Source": sl.session_state["efs"],
        "Eb_Source": sl.session_state["ebs"],
        "IGDB_Checksum": sl.session_state["igbd"],
        "Product_Name": sl.session_state["product"],
        "Full_Product_Name": (f"{full_Product_Name}.txt"),
        "Additional_Details": sl.session_state["details"],
        "Manufacturer": sl.session_state["manufacturer"],
        "NFRC_id": sl.session_state["nfrc_id"],
        "Type": sl.session_state["type"],
        "Material": sl.session_state["material"],
        "Coating_Name": sl.session_state["coating_name"],
        "Coated_Side": sl.session_state["coated_side"],
        "Substrate_filename": sl.session_state["filename"],
        "Appearance": sl.session_state["appear"],
        "Acceptance": sl.session_state["acceptance"],
        "Uses": sl.session_state["uses"],
        "Availability": sl.session_state["availibility"],
        "Directory": sl.session_state["dir"],
        "Out_Directory": sl.session_state["out_dir"],
    }

    # Build formatted product name
    final_form["Full_Product_Name"] = f"{full_Product_Name}.txt"

    # Save back to JSON
    with open(LASTFORM_NAME, "w") as f:
        json.dump(final_form, f, indent=4)

    sl.success("✅ Data saved successfully!")
    processing_script(sl.session_state["dir"], sl.session_state["out_dir"])
