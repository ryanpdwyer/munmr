import nfp
import sys
from keras import backend as K
import tensorflow as tf
import pandas as pd
import numpy as np
from rdkit import Chem
from nfp.preprocessing import MolAPreprocessor, GraphSequence
from keras.layers import Input
from keras.models import load_model
from nfp.layers import (Squeeze, EdgeNetwork,
                               ReduceBondToPro, ReduceBondToAtom, GatherAtomToBond, ReduceAtomToPro)
from nfp.models import GraphModel
from cascade.apply import predict_NMR_C, _modelpath_C, _modelpath_H, predict_NMR_H

NMR_model_C = load_model(_modelpath_C, custom_objects={'GraphModel': GraphModel,
                                            'ReduceAtomToPro': ReduceAtomToPro,
                                            'Squeeze': Squeeze,
                                            'GatherAtomToBond': GatherAtomToBond,
                                            'ReduceBondToAtom': ReduceBondToAtom}, compile=False)
NMR_model_H = load_model(_modelpath_H, custom_objects={'GraphModel': GraphModel,
                                            'ReduceAtomToPro': ReduceAtomToPro,
                                            'Squeeze': Squeeze,
                                            'GatherAtomToBond': GatherAtomToBond,
                                            'ReduceBondToAtom': ReduceBondToAtom}, compile=False)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        smiles = sys.argv[1]
        fname = sys.argv[2]

    outC = predict_NMR_C(smiles, NMR_model_C)
    outH = predict_NMR_H(smiles, NMR_model_H)

    # df_carbon_shifts = outC[1]
    # df_carbon_conformers = outC[2]

    # df_hydrogen_shifts = outH[1]
    # df_hydrogen_conformers = outH[2]

    # df_carbon_shifts.to_csv("carbon_shifts.csv")
    # df_carbon_conformers.to_csv("carbon_conformers.csv")
    # df_hydrogen_shifts.to_csv("hydrogen_shifts.csv")
    # df_hydrogen_conformers.to_csv("hydrogen_conformers.csv")
    # Save all conformers to an sdf file:
    import pickle
    with open(fname, "wb") as f:
        pickle.dump(dict(outC=outC, outH=outH), f)


