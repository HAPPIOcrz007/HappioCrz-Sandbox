import json
import os

import streamlit as sl  # if you plan to use Streamlit later

LASTFORM_NAME = "formLast.json"
BASE_DIRECTORY = "home"

# Step 1: Try to load existing JSON
try:
    with open(LASTFORM_NAME, "r") as lastForm:
        data = json.load(lastForm)
except (json.JSONDecodeError, FileNotFoundError):
    data = None  # file is empty, invalid, or missing

# Step 2: If empty, fill with base data
if data is None:
    print(f"{LASTFORM_NAME} is empty \n filling base data")
    lastForm_data = {
        "Wavelength": "SI Microns",
        "Thickness": 0,
        "Conductivity": 0.000,
        "IR_Transmittance": 0.000,
        "Emissivity_front": 0.000,
        "Emissivity_back": 0.000,
        "Ef_Source": "Text File",
        "Eb_Source": "Text File",
        "IGDB_Checksum": 0.000,
        "Raw_Product_Name": "Name",  # keep raw name separately
        "Additional_Details": "AM",
        "NFRC_id": "1000",
        "Manufacturer": "AIS",
        "Type": "Coated",
        "Material": "N/A",
        "Coated_Side": "Back",
        "Substrate_filename": "file.txt",
        "Appearance": "NEUTRAL",
        "Acceptance": "#",
        "Uses": "N/A",
        "Availability": "N/A",
        "Directory": BASE_DIRECTORY,
    }

    # Build formatted product name
    lastForm_data["Product_Name"] = (
        f"{lastForm_data['NFRC_id']}_{lastForm_data['Raw_Product_Name']}_"
        f"{lastForm_data['Thickness']}mm_{lastForm_data['Additional_Details']}.txt"
    )
    lastForm_data["Coating_Name"] = lastForm_data["Product_Name"]

    # Step 3: Save JSON
    with open(LASTFORM_NAME, "w") as lastForm:
        json.dump(lastForm_data, lastForm, indent=4)

    print("default data added successfully")
# data default filling done
# now form


with open(LASTFORM_NAME, "r") as lastForm:
    data = json.load(lastForm)

sl.set_page_config(page_title="File Compilation", layout="wide")
sl.title("📁 File Compiler 📁")
sl.header("Primary Data")

one, two = sl.columns(2)
with one:
    sl.text_input("Product Name", key="product", value=data.get("Product_Name", ""))
with two:
    sl.text_input(
        "Additional Details", key="details", value=data.get("Additional_Details", "")
    )

sl.number_input("Thickness", key="thickness", value=data.get("Thickness", 0))
sl.number_input(
    "Emissivity Back",
    key="emissivity",
    min_value=0.000,
    value=data.get("Emissivity_back", 0.000),
)
sl.text_input("Appearance", key="appearance", value=data.get("Appearance", ""))

sl.markdown("---")
sl.number_input(
    "NFRC id", key="nfrc_id", min_value=0, step=1, value=int(data.get("NFRC_id", 0))
)
sl.text_input(
    "Substrate Filename", key="filename", value=data.get("Substrate_filename", "")
)
sl.text_input(
    "Product Name (Raw)",
    key="p_name",
    value=f"{sl.session_state.nfrc_id}_{sl.session_state.product}_{sl.session_state.thickness}mm_{sl.session_state.details}",
)
sl.markdown("---")

sl.text_input(
    "Enter a Valid Directory", key="dir", value=data.get("Directory", BASE_DIRECTORY)
)

if sl.button("💾 Save Data"):
    data["Product_Name"] = sl.session_state.product
    data["Additional_Details"] = sl.session_state.details
    data["Thickness"] = sl.session_state.thickness
    data["Emissivity_back"] = sl.session_state.emissivity
    data["Appearance"] = sl.session_state.appearance
    data["NFRC_id"] = sl.session_state.nfrc_id
    data["Substrate_filename"] = sl.session_state.filename
    data["Raw_Product_Name"] = sl.session_state.p_name
    data["Directory"] = sl.session_state.dir

    with open(LASTFORM_NAME, "w") as f:
        json.dump(data, f, indent=4)
    sl.success("✅ Data saved successfully!")
