import numpy as np
import requests
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import quad
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LogNorm
import matplotlib as mpl

plotfolder = '../plots/'

# Enable LaTeX rendering
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "axes.labelsize": 25,   # Custom label size
    "xtick.labelsize": 25,  # Custom x-axis tick label size
    "ytick.labelsize": 25,  # Custom y-axis tick label size
    "legend.fontsize": 20,  # Custom legend font size
})


process = {'Primakoff': {'C0': 2.19e8, 'ga_ref': 1e-12, 'E0': 4.17, 'beta': 2.531}, 
            'Bremsstrahlung': {'C0': 3.847e11, 'ga_ref': 1e-12, 'E0': 1.63, 'beta': 0.8063},
            'Compton': {'C0': 8.8e11, 'ga_ref': 1e-12, 'E0': 5.1, 'beta': 2.979}
            }


# Define the axion flux function

def axion_flux(Ea: float, ga: float, process_i: str) -> float:
    """
    Return the axion flux function for the process_i.

    Returns
    -------
    flux : function
        The axion flux function.
    """
    C0, ga_ref, E0, beta = process[process_i]['C0'], process[process_i]['ga_ref'], process[process_i]['E0'], process[process_i]['beta']

    return C0 * (ga / ga_ref)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0)

def plot_axion_flux(proc: str, Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, (Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = axion_flux(E_values, 1e-12, proc)*1.e-6
    # Plot the axion flux
    plt.plot(E_values, flux1, color='black')
    # Add labels and legend
    plt.xlabel(r'$\omega({\rm keV})$', fontsize=30)
    plt.ylabel(r'$\frac{d\Phi_{a}}{d\omega}(\times10^{6}\,{\rm keV}^{-1}{\rm s}^{-1}{\rm cm}^{-2})$', fontsize=30)
    plt.grid(True) 
    # Save the plot as PDF
    plt.savefig(plotfolder + proc + '_axion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/' + proc + '_axion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass