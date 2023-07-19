import streamlit as st
import sys
import pandas as pd
import numpy as np
from rdkit import Chem
import subprocess
import pickle


@st.experimental_memo
def cascade(smiles, fname):
    return subprocess.run([sys.executable, "run_cascade.py", smiles, fname])

# Use streamlit to output the python environment / path
st.write(sys.executable)

smiles = st.text_input("SMILES", "CCO")

fname = f"output/{hash(smiles)}.pickle"

cascade(smiles, fname)

with open(fname, "rb") as f:
    out = pickle.load(f)

outC, outH = out["outC"], out["outH"]

st.write(outC[0])
st.write(outC[1])
st.write(len(outC[0]))