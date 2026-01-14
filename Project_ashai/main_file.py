import streamlit as sl
import os
from re import search
    
sl.set_page_config(page_title="File Compilation", layout="wide")
sl.title("📁 File Compiler 📁")

sl.header("Primary Data")
one, two = sl.columns(2)
with one:    
    sl.text_input("Product Name",key="product")
with two:
    sl.text_input("Additional Details",key="details")
sl.number_input("Thickness",key="thickness")
sl.number_input("Emmissivity Back",key="emissivity",min_value=0.000)
sl.text_input("Appearence",key="appearence")

sl.markdown("---")
sl.number_input("NFRC id",key='nfrc_id',min_value=0,step=1)
sl.text_input("Substrate Filename",key="filename")
sl.text_input("Product Name",key="p_name")
sl.markdown("---")

# Getting Files from the Directory

# Validating Directory
sl.text_input("Enter a Valid Directory",key="dir")

#default


directory = sl.session_state["dir"]

if not(directory):
    pass
elif not(os.path.isdir(directory)):
    sl.error(f"Please enter a valid directory. {directory} does not exist!")
    #directory = os.getcwd()
else:
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    with sl.expander("Files"):
    
        selected = []
        
        col_a,col_b = sl.columns(2)
        
        with col_a:
            sl.text_input("Enter File Name to search for in file seperated by commas",key="name_search")
        with col_b:
            sl.text_input("Enter tags to search for in file seperated by commas",key="search")
        
        for file in files:
            for pattern in sl.session_state["search"].split(","):
                if (pattern + "." in file) or (pattern + "_" in file):
                    if sl.checkbox(file,key=file):
                        selected.append(file)
                    break                
            if sl.session_state["name_search"]:  
                for name in sl.session_state["name_search"].split(","):
                    if name in file:
                        if sl.checkbox(file,key=file):
                            if file not in selected : selected.append(file)
                        break   

    sl.write("Files Selected:",selected)
sl.markdown("---")
sl.header("Secondary Data")
with sl.expander("Show Details"):
    one, two, three = sl.columns(3)
    with one:
        sl.text_input("Wavelength Unit",key="wavelength")
        sl.number_input("Conductivity",key="conductivity")
        sl.text_input("Enter IR Transmittance",key="TIR")
        sl.number_input("Emissivity front",key="emissivity_front")
        sl.text_input("Ef_Source",key="efs")
        
    
    with two:
        sl.text_input("Eb_Source",key="ebs")
        sl.text_input("Manufacturer",key="manufacturer")
        sl.text_input("Type",key="type")
        sl.text_input("Material",key="material")
        sl.text_input("Coated Side",key="coated_side")
        
    with three:
        sl.text_input("Acceptance",key="acceptance")
        sl.text_input("Uses",key="uses")
        sl.text_input("Availibility",key="availibility")
        sl.text_input("Structure",key="struct")
        sl.write("")
        


