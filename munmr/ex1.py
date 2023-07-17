import streamlit as st
import datamol as dm
from rdkit import Chem

from stmol import showmol
import py3Dmol

st.title("Molecular Data Analysis")
smiles = st.text_input("SMILES", "CCO")

mol = dm.to_mol(smiles, add_hs=True)

mol_svg = dm.to_image(mol)

st.image(mol_svg)

# Odd - since we have generated Hs above, we need to set add_hs=False here
confs = dm.conformers.generate(mol, add_hs=False) 

Nconfs = len(confs.GetConformers())

i_conf = st.slider("Conformer", 0, Nconfs-1, 0)

xyzview = py3Dmol.view(width=400,height=400)
xyzview.addModel(dm.to_molblock(confs, conf_id=i_conf, ), "mol")
xyzview.setStyle({'stick':{}})

showmol(xyzview)

st.write(dm.to_molblock(confs, conf_id=i_conf))