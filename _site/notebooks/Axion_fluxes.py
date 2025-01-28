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


# Solar Axion fluxes

processSolAx = {'Primakoff': {'C0': 2.19e8, 'ga_ref': 1e-12, 'E0': 4.17, 'beta': 2.531}, 
            'Bremsstrahlung': {'C0': 3.847e11, 'ga_ref': 1e-12, 'E0': 1.63, 'beta': 0.8063},
            'Compton': {'C0': 8.8e11, 'ga_ref': 1e-12, 'E0': 5.1, 'beta': 2.979}
            }


# Define the axion flux function

def SolAx_flux(Ea: float, ga: float, process_i: str) -> float:
    """
    Return the solar axion flux for the process_i.

    Returns
    -------
    flux : function
        The axion flux function.
    """
    C0, ga_ref, E0, beta = processSolAx[process_i]['C0'], processSolAx[process_i]['ga_ref'], processSolAx[process_i]['E0'], processSolAx[process_i]['beta']

    return C0 * (ga / ga_ref)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0)

def plot_SolarAxion_flux(proc: str, Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, (Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = SolAx_flux(E_values, 1e-12, proc)*1.e-6
    # Customize the range of the plot
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, np.max(flux1)*1.1)  # Custom y-axis limits   
    # Plot the axion flux
    plt.plot(E_values, flux1, color='black')
    # Add labels and legend
    plt.xlabel(r'$E_a ({\rm keV})$', fontsize=30)
    plt.ylabel(r'$\frac{d\Phi_{a}}{d E_a}(\times10^{6}\,{\rm keV}^{-1}{\rm s}^{-1}{\rm cm}^{-2})$', fontsize=30)
    plt.grid(True) 
    # Save the plot as PDF
    plt.savefig(plotfolder + proc + '_SolarAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/' + proc + '_SolarAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass


# Main sequence axion fluxes

def processMainSeq(proc: str, Mstar: float):
    C0Prim = np.where(Mstar < 10, -0.140+0.053*Mstar**(-0.347)*np.exp(Mstar**0.379), -0.014+0.011*Mstar**(1.081))
    betaBrem = np.where(Mstar < 10,0.57+0.18*np.exp(-Mstar**1.09),0.48+0.05*Mstar**0.19)
    process = {'Primakoff': {'C0':C0Prim*1e40, 'ga_ref': 1e-12, 'E0': 3.7+1.13*Mstar**0.355, 'beta': 1.223+3.63*np.exp(-Mstar**0.29)}, 
               'Bremsstrahlung': {'C0': (55.21+1.62e4*Mstar**(-0.65))*1e40, 'ga_ref': 1e-12, 'E0': 0.06+1.8*Mstar**0.23, 'beta': betaBrem},
               'Compton': {'C0': (0.14+1.01*Mstar**1.49)*1e40, 'ga_ref': 1e-12, 'E0': 0.0225+6.014*Mstar**0.225, 'beta': 2.99-0.56*np.exp(-Mstar**0.09)}
            }
    return process[proc]



# Define the axion flux function

def MSax_flux(Ea: float, ga: float, process_i: str, Mstar: float) -> float:
    """
    Return the solar axion flux for the process_i.

    Returns
    -------
    flux : function
        The axion flux function.
    """

    C0, ga_ref, E0, beta = processMainSeq(process_i, Mstar)['C0'], processMainSeq(process_i, Mstar)['ga_ref'], processMainSeq(process_i, Mstar)['E0'], processMainSeq(process_i, Mstar)['beta']

    return C0 * (ga / ga_ref)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0)

def plot_MainSequenceAxion_flux(proc: str, Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, (Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = MSax_flux(E_values, 1e-12, proc, 5)
    flux2 = MSax_flux(E_values, 1e-12, proc, 20)
    # Customize the range of the plot
    maxflux = max(np.max(flux1),np.max(flux2))
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black')
    fl2 = plt.plot(E_values, flux2*10**(-int(np.log10(maxflux))), color='blue')
    # Add labels and legend
    plt.xlabel(r'$E_a ({\rm keV})$', fontsize=30)
    plt.ylabel(r'$\frac{d\Phi_{a}}{d E_a}(\times10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm keV}^{-1}{\rm s}^{-1}{\rm cm}^{-2})$', fontsize=30)
    plt.grid(True) 
    h = [fl1[0], fl2[0]]
    # r'$e^-$ at rest']
    l = [r'$M = 5 M_\odot$', r'$M = 20 M_\odot$']
    leg = plt.legend(h, l, loc='upper right', fontsize=20, facecolor='white', framealpha=1)
    # Save the plot as PDF
    plt.savefig(plotfolder + proc + '_MSAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/' + proc + '_MSAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass