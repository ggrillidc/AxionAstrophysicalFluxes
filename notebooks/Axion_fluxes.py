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
    E_values = np.linspace(Eamin, Eamax, int((Eamax-Eamin)*20))  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = SolAx_flux(E_values, 1e-12, proc)*1.e-6
    # Customize the range of the plot
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, np.max(flux1)*1.1)  # Custom y-axis limits   
    # Plot the axion flux
    plt.plot(E_values, flux1, color='black')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm keV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d\Phi_{a}}{d E_a}\,[10^{6}\,{\rm keV}^{-1}{\rm s}^{-1}{\rm cm}^{-2}]$', fontsize=30)
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
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = MSax_flux(E_values, 1e-12, proc, 5)
    flux2 = MSax_flux(E_values, 1e-12, proc, 20)
    # Customize the range of the plot
    maxflux = max(np.max(flux1),np.max(flux2))
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black', ls='-')
    fl2 = plt.plot(E_values, flux2*10**(-int(np.log10(maxflux))), color='black', ls='--')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm keV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d\Phi_{a}}{d E_a}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm keV}^{-1}{\rm s}^{-1}{\rm cm}^{-2}]$', fontsize=30)
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



def RGax_flux(Ea: float, gae: float) -> float:

    C0 = 3.92
    E0 = 19.63
    beta = 1.25

    return 1e39 * C0* (gae / 1e-13)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0) 


def plot_RedGiantAxion_flux(Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = RGax_flux(E_values, 1e-13)
    # Customize the range of the plot
    maxflux = np.max(flux1)
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm keV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d N_{a}}{d E_a\,d t}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm keV}^{-1}{\rm s}^{-1}]$', fontsize=30)
    plt.grid(True) 
    # Save the plot as PDF
    plt.savefig(plotfolder + 'RGAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/RGAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass

def HBax_flux(Ea: float, gagamma: float) -> float:

    C0 = 94.76
    E0 = 36.59
    beta = 2.74

    return 1e36 * C0 * (gagamma / 1e-12)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0) 


def plot_HorizontalBranchAxion_flux(Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = HBax_flux(E_values, 1e-12)
    # Customize the range of the plot
    maxflux = np.max(flux1)
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm keV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d N_{a}}{d E_a\,d t}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm keV}^{-1}{\rm s}^{-1}]$', fontsize=30)
    plt.grid(True) 
    # Save the plot as PDF
    plt.savefig(plotfolder + 'HBAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/HBAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass




def WDax_flux(Ea: float, gae: float) -> float:
    """
    Return the solar axion flux for the process_i.

    Returns
    -------
    flux : function
        The axion flux function.
    """

    C0 = 1.25
    E0 = 9.38
    beta = 1.23

    return 1e16 * C0 * (gae / 1e-13)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0)

def plot_WhiteDwarfAxion_flux(Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = WDax_flux(E_values, 1e-13)
    # Customize the range of the plot
    maxflux = np.max(flux1)
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm keV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d N_{a}}{d E_a\,d t}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm keV}^{-1}{\rm s}^{-1}]$', fontsize=30)
    plt.grid(True) 
    # Save the plot as PDF
    plt.savefig(plotfolder + 'WDAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/WDAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass




def get_NNbremsstrahlungSNaxion_parameters(t):
    """
    Returns (E0_NN [MeV], beta_NN, A_NN [MeV^-1 s^-1]) 
    for a given t_pb [s].
    """
    data = {
        1: (70.19, 1.44, 4.56e54),
        2: (70.39, 1.42, 4.31e54),
        3: (56.91, 1.36, 2.41e54),
        4: (58.36, 1.31, 1.10e54),
        5: (47.41, 1.24, 3.95e53),
        6: (35.02, 1.17, 1.04e53),
        7: (23.98, 1.12, 2.20e52),
        8: (16.10, 1.10, 4.01e51),
    }
    
    if t not in data:
        raise ValueError(f"Unsupported t = {t}. Available t values are {list(data.keys())}")
    
    return data[t]



def NNbremsstrahlungSNax_flux(Ea: float, g_ap: float, t_pb: int) -> float:
    """
    Return the axion flux for the NN bremsstrahlung process in a supernova.
    
    Parameters
    ----------
    Ea : float
        Axion energy in MeV.
    t_pb : int
        Time post-bounce in seconds (1 to 8).
    
    Returns
    -------
    float
        The axion flux in MeV^-1 s^-1.
    """
    
    E0_NN, beta_NN, A_NN = get_NNbremsstrahlungSNaxion_parameters(t_pb)
    
    return A_NN * (g_ap / 5e-10)**2 * (Ea / E0_NN)**beta_NN * np.exp(- (beta_NN + 1) * (Ea / E0_NN))

def plot_NNbremsstrahlungSNAxion_flux(Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = NNbremsstrahlungSNax_flux(E_values, 5e-10, 1)
    flux2 = NNbremsstrahlungSNax_flux(E_values, 5e-10, 3)
    flux3 = NNbremsstrahlungSNax_flux(E_values, 5e-10, 5)
    # Customize the range of the plot
    maxflux = max(np.max(flux1),np.max(flux2),np.max(flux3))
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black', ls='-')
    fl2 = plt.plot(E_values, flux2*10**(-int(np.log10(maxflux))), color='black', ls='--')
    fl3 = plt.plot(E_values, flux3*10**(-int(np.log10(maxflux))), color='black', ls='-.')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm MeV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d N_{a}}{d E_a\,d t}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm MeV}^{-1}{\rm s}^{-1}]$', fontsize=30)
    plt.grid(True) 
    h = [fl1[0], fl2[0], fl3[0]]
    # r'$e^-$ at rest']
    l = [r'$t_\mathrm{pb}=1$ s', r'$t_\mathrm{pb}=3$ s', r'$t_\mathrm{pb}=5$ s']
    leg = plt.legend(h, l, loc='upper right', fontsize=20, facecolor='white', framealpha=1)
    # Save the plot as PDF
    plt.savefig(plotfolder + 'Bremsstrahlung_SNAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/Bremsstrahlung_SNAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass



def get_piNSNaxion_parameters(t):
    """
    Returns (E0_piN [MeV], beta_piN, A_piN [MeV^-1 s^-1], omega_c [MeV])
    for a given t_pb [s].
    """
    data = {
        1: (126.43, 1.20, 2.77e54, 103.27),
        2: (94.47,  1.03, 1.24e54, 98.87),
        3: (56.14,  0.54, 9.78e52, 107.00),
        4: (37.20,  0.65, 2.20e52, 107.06),
        5: (25.02,  0.47, 3.63e51, 108.59),
        6: (15.62,  0.40, 2.53e50, 108.04),
        7: (9.18,   0.37, 3.10e48, 108.33),
        8: (5.64,   0.37, 6.64e45, 108.37),
    }
    
    if t not in data:
        raise ValueError(f"Unsupported t = {t}. Available t values are {list(data.keys())}")
    
    return data[t]

def PionConversionSNAxion_flux(E_a, g_ap, tpb=1):
    """
    Computes (d^2N_a) / (dE_a dt) for piN.
    """
    E0_piN, beta_piN, A_piN, omega_c = get_piNSNaxion_parameters(tpb)  # Using t_pb = 1 as default
    delta_E = E_a - omega_c
    # if delta_E < 0:
    #     return 0.0
    delta_E=np.where(delta_E < 0, 0, delta_E)  # Ensure delta_E is non-negative
    
    factor_g = (g_ap / 5e-10)**2
    factor_power = (delta_E / E0_piN)**beta_piN
    factor_exp = np.exp(- (beta_piN + 1) * delta_E / E0_piN)
    
    return A_piN * factor_g * factor_power * factor_exp



def plot_pionConversionSNAxion_flux(Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = PionConversionSNAxion_flux(E_values, 5e-10, 1)
    flux2 = PionConversionSNAxion_flux(E_values, 5e-10, 3)
    flux3 = PionConversionSNAxion_flux(E_values, 5e-10, 5)
    # Customize the range of the plot
    maxflux = max(np.max(flux1),np.max(flux2),np.max(flux3))
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black', ls='-')
    fl2 = plt.plot(E_values, flux2*10**(-int(np.log10(maxflux))), color='black', ls='--')
    fl3 = plt.plot(E_values, flux3*10**(-int(np.log10(maxflux))), color='black', ls='-.')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm MeV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d N_{a}}{d E_a\,d t}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm MeV}^{-1}{\rm s}^{-1}]$', fontsize=30)
    plt.grid(True) 
    h = [fl1[0], fl2[0], fl3[0]]
    # r'$e^-$ at rest']
    l = [r'$t_\mathrm{pb}=1$ s', r'$t_\mathrm{pb}=3$ s', r'$t_\mathrm{pb}=5$ s']
    leg = plt.legend(h, l, loc='upper right', fontsize=20, facecolor='white', framealpha=1)
    # Save the plot as PDF
    plt.savefig(plotfolder + 'PionConversion_SNAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/PionConversion_SNAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass



def get_RedSupergiants_parameters(model: int, process: str) -> tuple:
    """
    Returns (C, E, beta) for the given model number and process name.

    Args:
        model (int): Model number from 1 to 8.
        process (str): One of 'Primakoff', 'Bremsstrahlung', or 'Compton'.

    Returns:
        tuple: (C, E, beta) values.
    """
    data = {
        1: {
            'Primakoff':      (3.36, 74.7, 2.10),
            'Bremsstrahlung': (2.18e-2, 36.1, 0.732),
            'Compton':        (5.24, 115, 3.12)
        },
        2: {
            'Primakoff':      (9.70, 173, 2.01),
            'Bremsstrahlung': (0.530, 95.3, 0.857),
            'Compton':        (116, 267, 3.18)
        },
        3: {
            'Primakoff':      (13.1, 208, 2.02),
            'Bremsstrahlung': (1.06, 118, 0.901),
            'Compton':        (211, 315, 3.18)
        },
        4: {
            'Primakoff':      (26.9, 339, 1.97),
            'Bremsstrahlung': (8.53, 226, 1.08),
            'Compton':        (991, 489, 3.23)
        },
        5: {
            'Primakoff':      (23.3, 367, 1.85),
            'Bremsstrahlung': (11.3, 255, 1.10),
            'Compton':        (991, 525, 3.15)
        },
        6: {
            'Primakoff':      (31.5, 495, 1.77),
            'Bremsstrahlung': (23.1, 333, 1.09),
            'Compton':        (1430, 680, 2.90)
        },
        7: {
            'Primakoff':      (94.5, 858, 1.89),
            'Bremsstrahlung': (73.5, 593, 1.11),
            'Compton':        (8430, 1090, 3.09)
        },
        8: {
            'Primakoff':      (92.8, 1000, 1.79),
            'Bremsstrahlung': (86.0, 685, 1.07),
            'Compton':        (8030, 1260, 2.85)
        }
    }

    process = process.capitalize()
    if model not in data:
        raise ValueError(f"Model {model} not found. Available models: {list(data.keys())}")
    if process not in data[model]:
        raise ValueError(f"Process '{process}' not found. Choose from 'Primakoff', 'Bremsstrahlung', or 'Compton'.")

    return data[model][process]


def RedSupergiantsAxion_flux(E: float, gref:float, model: int, process: str):
    """
    Computes the differential emission rate dṄa/dE for a single process
    (Primakoff, Bremsstrahlung, or Compton) for the given model, energy E (in keV),
    and reference coupling (gagamma/(1e-11 GeV^{-1})) or (gae/1e-13).

    Args:
        model (int): Model number (1 to 8).
        process (str): Process name ('Primakoff', 'Bremsstrahlung', or 'Compton').
        E (float): Energy in keV.
        g_13 (float): Dimensionless coupling for Bremsstrahlung and Compton (scaled to 10^-13).
        g_11 (float): Dimensionless coupling for Primakoff (scaled to 10^-11).

    Returns:
        float: The differential emission rate in (keV s)^-1.
    """
    
    # Extract parameters
    C, E0, beta = get_RedSupergiants_parameters(model, process)

    coupling = gref
    
    # Compute the rate
    rate = 1e42 * C * coupling**2 * (E / E0)**beta * np.exp(-(beta + 1) * E / E0)

    return rate



def plot_RedSupergiantsAxion_flux(proc: str, Eamin: float, Eamax: float):
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = RedSupergiantsAxion_flux(E_values, 1, 1, proc)
    flux2 = RedSupergiantsAxion_flux(E_values, 1, 2, proc)
    flux3 = RedSupergiantsAxion_flux(E_values, 1, 3, proc)
    flux4 = RedSupergiantsAxion_flux(E_values, 1, 4, proc)
    flux5 = RedSupergiantsAxion_flux(E_values, 1, 5, proc)
    flux6 = RedSupergiantsAxion_flux(E_values, 1, 6, proc)
    flux7 = RedSupergiantsAxion_flux(E_values, 1, 7, proc)
    flux8 = RedSupergiantsAxion_flux(E_values, 1, 8, proc)
    # Customize the range of the plot
    maxflux = max(np.max(flux1),np.max(flux2),np.max(flux3),np.max(flux4),np.max(flux5),np.max(flux6),np.max(flux7),np.max(flux8))
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black', ls='-')
    fl2 = plt.plot(E_values, flux2*10**(-int(np.log10(maxflux))), color='black', ls='--')
    fl3 = plt.plot(E_values, flux3*10**(-int(np.log10(maxflux))), color='black', ls='-.')
    fl4 = plt.plot(E_values, flux4*10**(-int(np.log10(maxflux))), color='black', ls=':')
    fl5 = plt.plot(E_values, flux5*10**(-int(np.log10(maxflux))), color='red', ls='-')
    fl6 = plt.plot(E_values, flux6*10**(-int(np.log10(maxflux))), color='red', ls='--')
    fl7 = plt.plot(E_values, flux7*10**(-int(np.log10(maxflux))), color='red', ls='-.')
    fl8 = plt.plot(E_values, flux8*10**(-int(np.log10(maxflux))), color='red', ls=':')

    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm keV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d\Phi_{a}}{d E_a}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm keV}^{-1}{\rm s}^{-1}{\rm cm}^{-2}]$', fontsize=30)
    plt.grid(True) 
    h = [fl1[0], fl2[0], fl3[0], fl4[0], fl5[0], fl6[0], fl7[0], fl8[0]]
    # r'$e^-$ at rest']
    l = [r'He burning', r'start C burning', r'C burning', r'start Ne burning', r'start O burning', r'O burning', r'start Si burning', r'Si burning']
    leg = plt.legend(h, l, loc='upper right', fontsize=20, facecolor='white', framealpha=1)
    # Save the plot as PDF
    plt.savefig(plotfolder + proc + '_RSGAxion_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/' + proc + '_RSGAxion_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass


