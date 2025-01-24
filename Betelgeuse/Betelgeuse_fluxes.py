import numpy as np


models = {'HeBurning': {'tc': 155000, 'log10Lratio': 4.9, 'log10Teff/K': 3.572,
                        'CP': 1.36, 'E0P': 50, 'betaP': 1.95,
                        'CB': 1.3e-3, 'E0B': 35.26, 'betaB': 1.16,
                        'CC': 1.39, 'E0C': 77.86, 'betaC': 3.15},
          'beforeCBurning1': {'tc': 23000, 'log10Lratio': 5.06, 'log10Teff/K': 3.552,
                              'CP': 4.0, 'E0P': 80, 'betaP': 2.0,
                              'CB': 2.3e-3, 'E0B': 56.57, 'betaB': 1.16,
                              'CC': 8.55, 'E0C': 125.8, 'betaC': 3.12},
          'inCBurning7': {'tc': 480, 'log10Lratio': 5.16, 'log10Teff/K': 3.542,
                              'CP': 13.0, 'E0P': 180, 'betaP': 2.0,
                              'CB': 0.789, 'E0B': 134.54, 'betaB': 1.02,
                              'CC': 153.2, 'E0C': 279.9, 'betaC': 3.15}
          }


def dNadot_dE(E: float, gagamma: float, gae: float, model: str) -> float:
    g13 = gae * 1e13
    g11 = gagamma * 1e11 # GeV^{-1}
    CB = models[model]['CB']
    CC = models[model]['CC']
    CP = models[model]['CP']
    betaB = models[model]['betaB']
    betaC = models[model]['betaC']
    betaP = models[model]['betaP']
    E0B = models[model]['E0B']
    E0C = models[model]['E0C']
    E0P = models[model]['E0P']
    retB = 1e42 * CB * g13**2 * (E / E0B)**betaB * \
        np.exp(-(betaB+1) * E / E0B)
    retC = 1e42 * CC * g13**2 * (E / E0C)**betaC * \
        np.exp(-(betaC+1) * E / E0C)
    retP = 1e42 * CP * g11**2 * (E / E0P)**betaP * \
        np.exp(-(betaP+1) * E / E0P)
    ret = retB + retC + retP 
    return  [retB, retC, retP, ret]
