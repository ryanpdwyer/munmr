import streamlit as st
import sys
import pandas as pd
import numpy as np
from rdkit import Chem
import subprocess
import pickle


@st.experimental_memo
def cascade(smiles):
    """Runs cascade using a separate python process, saving the results to a pickle file,
    then loading them back into the main process."""
    fname = f"output/{hash(smiles)}.pickle"

    return_code = subprocess.run([sys.executable, "run_cascade.py", smiles, fname])
    # pickle file saves a dictionary with keys outC and outH, 
    # the outputs from running the cascade Carbon and Hydrogen
    # prediction models
    with open(fname, "rb") as f:
        out = pickle.load(f)

    return out["outC"], out["outH"]



# Use streamlit to output the python environment / path
st.write(sys.executable)

smiles = st.text_input("SMILES", "CCO")

# Run cascade using a separate python process
outC, outH = cascade(smiles)

st.write(outC[0])
st.write(outC[1])
st.write(len(outC[0]))