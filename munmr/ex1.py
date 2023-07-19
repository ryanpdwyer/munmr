import streamlit as st
from rdkit import Chem
from openbabel import pybel

from stmol import showmol
import py3Dmol

##############################################
### Smiles input and display 
###############################################

st.title("Molecular Data Analysis")
smiles = st.text_input("SMILES", "CCO")

mol = dm.to_mol(smiles, add_hs=True)

mol_svg = dm.to_image(mol)

st.image(mol_svg)

# st.markdown(mol_svg.data, unsafe_allow_html=True)

st.code(mol_svg, language="html")

# Odd - since we have generated Hs above, we need to set add_hs=False here
confs = dm.conformers.generate(mol, add_hs=False) 

Nconfs = len(confs.GetConformers())

i_conf = st.slider("Conformer", 0, Nconfs-1, 0)

xyzview = py3Dmol.view(width=400,height=400)
xyzview.addModel(dm.to_molblock(confs, conf_id=i_conf), "mol")
xyzview.setStyle({'stick':{}})
xyzview.addLabel('1', {'position': {'x': 0, 'y': 0, 'z': 0}})

showmol(xyzview)

conformer_xyz = Chem.rdmolfiles.MolToXYZBlock(confs, confId=i_conf)

st.markdown("### Conformer XYZ")
st.code(conformer_xyz)

conformer_xyz_just_coordinates = "\n".join(conformer_xyz.split("\n")[2:])

title=st.text_input("Title", smiles)

gaussian_input = f"""\
%NProcShared=4
%CHK=output.chk
#N B3LYP/6-31G(d) Opt

{title}

0 1
{conformer_xyz_just_coordinates}
"""
# st.code(gaussian_input)

##############################################
### Conformer data analysis input and display 
###############################################


with open("gaussian.gjf", "w") as f:
    f.write(gaussian_input)

mymol = pybel.readstring("xyz", conformer_xyz)

route = """%NProcShared=4
%CHK=output.chk
#N b3lyp/6-31g(d) opt"""

nmr_calculation = """"""

gaussian_pybel = mymol.write("gjf", opt={'k': route}).replace("\n\n ", f"\n\n {title}")

with open("gaussian_pybel.gjf", "w") as f:
    f.write(gaussian_pybel)

