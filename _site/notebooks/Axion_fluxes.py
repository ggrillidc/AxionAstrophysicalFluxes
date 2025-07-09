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
    Compute the differential solar axion flux at Earth for a given energy, coupling, and production process.

    Args:
        Ea (float): Axion energy in keV.
        ga (float): Axion coupling constant (e.g. gaγγ or gae) in appropriate units.
        process_i (str): Key identifying the production process (e.g. 'Primakoff', 'Bremsstrahlung', 'Compton'), used to retrieve the fit parameters from `processSolAx`.

    Returns:
        float: Differential axion flux (in keV^-1 s^-1 cm^-2), according to the fitted model.
    """
    C0, ga_ref, E0, beta = processSolAx[process_i]['C0'], processSolAx[process_i]['ga_ref'], processSolAx[process_i]['E0'], processSolAx[process_i]['beta']

    return C0 * (ga / ga_ref)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0)

def plot_SolarAxion_flux(proc: str, Eamin: float, Eamax: float):
    """
    Plot the differential solar axion flux for a given production process over a specified energy range.

    Generates a plot of the solar axion flux (scaled by 1e-6) as a function of axion energy,
    saves it in both PDF and PNG formats, and displays it.

    Args:
        proc (str): The production process (e.g. 'Primakoff', 'Bremsstrahlung', 'Compton'),
            used to select fit parameters from `processSolAx`.
        Eamin (float): Minimum axion energy (keV) for the plot range.
        Eamax (float): Maximum axion energy (keV) for the plot range.

    Returns:
        None
    """

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
    """
    Compute the fit parameters for axion production processes in Main Sequence stars.

    Given the stellar mass, returns a dictionary of parameters (C0, ga_ref, E0, beta) 
    for the specified axion production process (Primakoff, Bremsstrahlung, or Compton).
    These parameters can be used to model the axion emission spectrum.

    Args:
        proc (str): The production process. Must be one of:
            'Primakoff', 'Bremsstrahlung', or 'Compton'.
        Mstar (float): Mass of the star in solar masses.

    Returns:
        dict: A dictionary with the following keys:
            - 'C0' (float): Normalization constant of the emission rate (keV^{-1} s^{-1}).
            - 'ga_ref' (float): Reference coupling used in scaling the flux.
            - 'E0' (float): Characteristic energy scale (keV).
            - 'beta' (float): Exponential shape parameter of the spectrum.

    Example:
        >>> params = processMainSeq('Primakoff', 5.0)
        >>> print(params['C0'], params['E0'])
    """

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
    Compute the differential axion flux from a Main Sequence star.

    Given an axion energy, coupling, production process, and stellar mass, 
    returns the differential axion flux (per unit energy and time) 
    at Earth from Main Sequence stars. 

    The flux follows the parameterized expression:
        dN_a / (dE_a dt) = C0 * (ga / ga_ref)^2 * (Ea / E0)^beta * exp[-(1+beta) * Ea / E0]

    Args:
        Ea (float): Axion energy in keV.
        ga (float): Axion coupling constant (e.g., g_{agamma} or g_{ae}).
        process_i (str): The production process. Should be one of:
            'Primakoff', 'Bremsstrahlung', or 'Compton'.
        Mstar (float): Stellar mass in solar masses.

    Returns:
        float: Differential axion flux at Earth in keV^{-1} s^{-1}.

    Example:
        >>> flux = MSax_flux(5.0, 1e-12, 'Primakoff', 3.0)
        >>> print(flux)
    """

    C0, ga_ref, E0, beta = processMainSeq(process_i, Mstar)['C0'], processMainSeq(process_i, Mstar)['ga_ref'], processMainSeq(process_i, Mstar)['E0'], processMainSeq(process_i, Mstar)['beta']

    return C0 * (ga / ga_ref)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0)

def plot_MainSequenceAxion_flux(proc: str, Eamin: float, Eamax: float):
    """
    Plot the axion flux spectrum for a main sequence star with given parameters.

    This function computes and plots the differential axion flux 
    (dΦ_a/dE_a) as a function of axion energy E_a, for two stellar masses 
    (5 and 20 solar masses). The plot is saved as both PDF and PNG files 
    in predefined folders.

    The flux is normalized and scaled according to the maximum flux value 
    for better visualization.

    Args:
        proc (str): Identifier for the stellar process or star type, 
            used to name the output files.
        Eamin (float): Minimum axion energy (keV) for the plot range.
        Eamax (float): Maximum axion energy (keV) for the plot range.

    Raises:
        ValueError: If Eamax is not greater than Eamin.
    
    Side Effects:
        Saves the generated plot as PDF and PNG files in `plotfolder` paths.
        Displays the plot using matplotlib.

    Notes:
        The function assumes the existence of a global variable `plotfolder`
        specifying the directory for saving plots, and a function `MSax_flux`
        that computes the axion flux.
    """
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
    """
    Calculate the axion flux from red giant stars as a function of energy and coupling.

    Computes the differential axion flux (dΦ_a/dE_a) for red giant stars using a
    parametric formula involving the axion energy and axion-electron coupling.

    Args:
        Ea (float): Axion energy in keV.
        gae (float): Axion-electron coupling constant.

    Returns:
        float: Differential axion flux [keV⁻¹ s⁻¹].

    Notes:
        The flux is calculated using the formula:
            flux = 1e39 * C0 * (gae / 1e-13)^2 * (Ea / E0)^beta * exp(-(1 + beta) * Ea / E0)
        with parameters:
            C0 = 3.92,
            E0 = 19.63 keV,
            beta = 1.25.
    """
    C0 = 3.92
    E0 = 19.63
    beta = 1.25

    return 1e39 * C0* (gae / 1e-13)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0) 


def plot_RedGiantAxion_flux(Eamin: float, Eamax: float):
    """
    Plot the axion flux spectrum for red giant stars over a specified energy range.

    This function computes the differential axion flux (dN_a / dE_a dt) as a function 
    of axion energy between `Eamin` and `Eamax` using a fixed axion-electron coupling, 
    and plots the normalized flux. The plot is saved in both PDF and PNG formats.

    Args:
        Eamin (float): Minimum axion energy (keV) for the plot range.
        Eamax (float): Maximum axion energy (keV) for the plot range.

    Side Effects:
        Saves the generated plot as 'RGAxion_flux_plot.pdf' and 'RGAxion_flux_plot.png' 
        in the directory specified by the global variable `plotfolder`.
        Displays the plot using matplotlib.

    Notes:
        Assumes a global variable `plotfolder` is defined to specify the output folder.
        The flux is computed with a fixed axion-electron coupling of 1e-13.
    """
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
    """
    Calculate the axion flux from horizontal branch stars as a function of energy and coupling.

    Computes the differential axion flux (dΦ_a/dE_a) for horizontal branch stars using a 
    parametric formula based on the axion energy and axion-photon coupling constant.

    Args:
        Ea (float): Axion energy in keV.
        gagamma (float): Axion-photon coupling constant.

    Returns:
        float: Differential axion flux [keV⁻¹ s⁻¹ cm⁻²].

    Notes:
        The flux is calculated using the formula:
            flux = 1e36 * C0 * (gagamma / 1e-12)^2 * (Ea / E0)^beta * exp(-(1 + beta) * Ea / E0)
        with parameters:
            C0 = 94.76,
            E0 = 36.59 keV,
            beta = 2.74.
    """

    C0 = 94.76
    E0 = 36.59
    beta = 2.74

    return 1e36 * C0 * (gagamma / 1e-12)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0) 


def plot_HorizontalBranchAxion_flux(Eamin: float, Eamax: float):
    """
    Plot the axion flux spectrum from horizontal branch stars over a specified energy range.

    This function computes the differential axion flux (dN_a / dE_a dt) as a function 
    of axion energy between `Eamin` and `Eamax`, using a fixed axion-photon coupling. 
    It then generates and saves a normalized plot of the flux.

    Args:
        Eamin (float): Minimum axion energy (keV) for the plot range.
        Eamax (float): Maximum axion energy (keV) for the plot range.

    Side Effects:
        Saves the generated plot as 'HBAxion_flux_plot.pdf' and 
        'HBAxion_flux_plot.png' in directories specified by the global variable `plotfolder`.
        Displays the plot using matplotlib.

    Notes:
        - Assumes a global variable `plotfolder` exists to specify output directories.
        - Uses a fixed axion-photon coupling of 1e-12 for the flux computation.
        - The flux is normalized by its order of magnitude to improve visualization.
    """
    
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
    Calculate the axion flux from white dwarf stars as a function of energy and coupling.

    Computes the differential axion flux (dΦ_a/dE_a) for white dwarf stars using a 
    parametric formula involving the axion energy and axion-electron coupling constant.

    Args:
        Ea (float): Axion energy in keV.
        gae (float): Axion-electron coupling constant.

    Returns:
        float: Differential axion flux [keV⁻¹ s⁻¹ cm⁻²].

    Notes:
        The flux is calculated using the formula:
            flux = 1e16 * C0 * (gae / 1e-13)^2 * (Ea / E0)^beta * exp(-(1 + beta) * Ea / E0)
        with parameters:
            C0 = 1.25,
            E0 = 9.38 keV,
            beta = 1.23.
    """

    C0 = 1.25
    E0 = 9.38
    beta = 1.23

    return 1e16 * C0 * (gae / 1e-13)**2 * (Ea / E0)**beta * np.exp(-(1 + beta) * Ea / E0)

def plot_WhiteDwarfAxion_flux(Eamin: float, Eamax: float):
    """
    Plot the axion flux spectrum from white dwarf stars over a specified energy range.

    This function computes the differential axion flux (dN_a / dE_a dt) 
    as a function of axion energy between `Eamin` and `Eamax`, using 
    a fixed axion-electron coupling. It then generates a normalized 
    plot of the flux and saves it in both PDF and PNG formats.

    Args:
        Eamin (float): Minimum axion energy (keV) for the plot range.
        Eamax (float): Maximum axion energy (keV) for the plot range.

    Side Effects:
        - Saves the generated plot as 'WDAxion_flux_plot.pdf' and 
          'WDAxion_flux_plot.png' in directories specified by the global 
          variable `plotfolder`.
        - Displays the plot using matplotlib.

    Notes:
        - Assumes a global variable `plotfolder` exists that specifies 
          the output directories for plots.
        - Uses a fixed axion-electron coupling of 1e-13 for the flux calculation.
        - The flux is scaled by its order of magnitude to improve visualization.
    """
    
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
    Retrieve the parameters for the NN bremsstrahlung supernova axion flux model at a given time step.

    Given an integer `t` (representing a discrete time snapshot), this function returns 
    a tuple of parameters used to model the supernova axion flux due to nucleon-nucleon 
    bremsstrahlung. These parameters typically correspond to fits for (E0, beta, normalization).

    Args:
        t (int): Time index (1 to 8) corresponding to specific snapshots of the 
            supernova evolution.

    Returns:
        tuple: A tuple of the form (E0, beta, norm), where
            - E0 (float): Characteristic energy scale in MeV.
            - beta (float): Power-law index.
            - norm (float): Normalization factor.

    Raises:
        ValueError: If `t` is not an integer between 1 and 8.

    Notes:
        The returned parameters are precomputed and typically used in the formula:
            flux ∝ norm * (Ea / E0)^beta * exp(-(1 + beta) * Ea / E0)
        to describe the differential axion flux from a supernova at different stages.
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
    Compute the axion flux from nucleon-nucleon bremsstrahlung in a supernova.

    Calculates the differential axion flux (dΦ_a/dE_a) produced by NN bremsstrahlung 
    processes in a supernova at a given post-bounce time snapshot.

    Args:
        Ea (float): Axion energy in MeV.
        g_ap (float): Axion-proton coupling constant.
        t_pb (int): Post-bounce time index (1 to 8) specifying the supernova evolution stage.

    Returns:
        float: Differential axion flux [MeV⁻¹ s⁻¹ cm⁻²].

    Raises:
        ValueError: If `t_pb` is not a valid index (1 to 8), as enforced by 
        `get_NNbremsstrahlungSNaxion_parameters`.

    Notes:
        The flux is computed using:
            flux = A_NN * (g_ap / 5e-10)^2 * (Ea / E0_NN)^beta_NN * exp(- (1 + beta_NN) * (Ea / E0_NN))
        where the parameters (E0_NN, beta_NN, A_NN) are determined by the time index `t_pb`.
    """
    
    E0_NN, beta_NN, A_NN = get_NNbremsstrahlungSNaxion_parameters(t_pb)
    
    return A_NN * (g_ap / 5e-10)**2 * (Ea / E0_NN)**beta_NN * np.exp(- (beta_NN + 1) * (Ea / E0_NN))

def plot_NNbremsstrahlungSNAxion_flux(Eamin: float, Eamax: float):
    """
    Plot the supernova axion flux from NN bremsstrahlung over a specified energy range.

    This function computes the differential axion flux (dN_a / dE_a dt) from 
    nucleon-nucleon bremsstrahlung in a supernova for three different 
    post-bounce times (1 s, 3 s, 5 s). It then generates a normalized 
    plot and saves it as both PDF and PNG files.

    Args:
        Eamin (float): Minimum axion energy (MeV) for the plot range.
        Eamax (float): Maximum axion energy (MeV) for the plot range.

    Side Effects:
        - Saves the generated plot as 'Bremsstrahlung_SNAxion_flux_plot.pdf' and 
          'Bremsstrahlung_SNAxion_flux_plot.png' in directories specified by the 
          global variable `plotfolder`.
        - Displays the plot using matplotlib.

    Notes:
        - Assumes a global variable `plotfolder` exists to specify the output directories.
        - Uses a fixed axion-proton coupling of 5e-10 for the flux calculation.
        - Fluxes are computed at three different post-bounce times (1 s, 3 s, 5 s).
        - The fluxes are scaled by their order of magnitude to improve visualization.
    """
    
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
    Retrieve the parameters for the πN bremsstrahlung supernova axion flux model at a given time step.

    Given an integer `t` (representing a discrete post-bounce time snapshot), 
    this function returns a tuple of parameters used to model the axion flux 
    from πN (pion-nucleon) bremsstrahlung processes in a supernova.

    Args:
        t (int): Time index (1 to 8) corresponding to specific snapshots 
            of the supernova evolution.

    Returns:
        tuple: A tuple of the form (E0, beta, norm, omega_c), where
            - E0 (float): Characteristic energy scale in MeV.
            - beta (float): Power-law index.
            - norm (float): Normalization factor.
            - omega_c (float): Cutoff energy in MeV.

    Raises:
        ValueError: If `t` is not an integer between 1 and 8.

    Notes:
        The returned parameters are typically used in a formula like:
            flux ∝ norm * ( (Ea - omega_c) / E0 )^beta * exp(-(1 + beta) * (Ea - omega_c) / E0)
        to describe the differential axion flux from supernova πN bremsstrahlung 
        at different evolutionary stages.
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
    Compute the axion flux from pion-nucleon (πN) conversion in a supernova.

    Calculates the differential axion flux (dΦ_a/dE_a) produced by πN bremsstrahlung 
    processes in a supernova at a given post-bounce time snapshot. 
    The flux is suppressed for energies below the cutoff omega_c.

    Args:
        E_a (float or np.ndarray): Axion energy in MeV.
        g_ap (float): Axion-proton coupling constant.
        tpb (int, optional): Post-bounce time index (1 to 8) specifying the 
            supernova evolutionary stage. Defaults to 1.

    Returns:
        float or np.ndarray: Differential axion flux [MeV⁻¹ s⁻¹ cm⁻²] at energy `E_a`.

    Raises:
        ValueError: If `tpb` is not a valid index (1 to 8), as enforced by 
            `get_piNSNaxion_parameters`.

    Notes:
        The flux is computed using the formula:
            flux = A_piN * (g_ap / 5e-10)^2 * ((E_a - omega_c)/E0_piN)^beta_piN 
                   * exp(-(1 + beta_piN)*(E_a - omega_c)/E0_piN)
        where (E0_piN, beta_piN, A_piN, omega_c) are determined by `tpb`.

        Energies below the cutoff `omega_c` yield a suppressed (zeroed) contribution.
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
    """
    Plot the supernova axion flux from pion-nucleon (πN) conversion over a specified energy range.

    This function computes the differential axion flux (dN_a / dE_a dt) from 
    πN bremsstrahlung processes in a supernova for three different 
    post-bounce times (1 s, 3 s, 5 s). It then generates a normalized 
    plot of these fluxes and saves it in both PDF and PNG formats.

    Args:
        Eamin (float): Minimum axion energy (MeV) for the plot range.
        Eamax (float): Maximum axion energy (MeV) for the plot range.

    Side Effects:
        - Saves the generated plot as 'PionConversion_SNAxion_flux_plot.pdf' and 
          'PionConversion_SNAxion_flux_plot.png' in directories specified by 
          the global variable `plotfolder`.
        - Displays the plot using matplotlib.

    Notes:
        - Assumes a global variable `plotfolder` exists that specifies 
          the output directories for saving plots.
        - Uses a fixed axion-proton coupling of 5e-10 for all flux computations.
        - The flux is evaluated at three post-bounce times (1 s, 3 s, 5 s) to 
          illustrate the time evolution.
        - The flux curves are scaled by their order of magnitude to improve 
          visualization on the plot.
    """
    
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
    Retrieve the parameters for axion flux models from red supergiant stars.

    Given a stellar model index and a production process name, this function 
    returns a tuple of parameters used to compute the axion flux from 
    red supergiants. The parameters typically correspond to fits of 
    the form (normalization, E0, beta) for different processes.

    Args:
        model (int): Integer index from 1 to 8 specifying the red supergiant 
            stellar model (increasing mass and luminosity).
        process (str): Name of the axion production process. Must be one of:
            'Primakoff', 'Bremsstrahlung', or 'Compton' (case-insensitive).

    Returns:
        tuple: A tuple of the form (A, E0, beta), where
            - A (float): Normalization constant.
            - E0 (float): Characteristic energy scale in keV.
            - beta (float): Power-law index.

    Raises:
        ValueError: If `model` is not an integer from 1 to 8, or if 
            `process` is not one of the allowed strings.

    Notes:
        These parameters are typically used in spectral formulas such as:
            flux ∝ A * (Ea / E0)^beta * exp(- (1 + beta) * Ea / E0)
        to model the differential axion flux from different production 
        channels in red supergiants.
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
    Calculate the axion flux from red supergiant stars for a given model and process.

    Computes the differential axion flux (dΦ_a/dE) as a function of axion energy, 
    stellar model, and production process, scaled by the square of the axion coupling.

    Args:
        E (float): Axion energy in keV.
        gref (float): Reference axion coupling constant.
        model (int): Red supergiant stellar model index (1 to 8).
        process (str): Axion production process; one of 'Primakoff', 'Bremsstrahlung', or 'Compton'.

    Returns:
        float: Differential axion flux [keV⁻¹ s⁻¹ cm⁻²].

    Raises:
        ValueError: If `model` or `process` are invalid, as enforced by `get_RedSupergiants_parameters`.

    Notes:
        The flux is computed using the formula:
            flux = 1e42 * C * gref^2 * (E / E0)^beta * exp(-(beta + 1) * E / E0)
        where (C, E0, beta) are parameters from the selected stellar model and process.
    """
    
    # Extract parameters
    C, E0, beta = get_RedSupergiants_parameters(model, process)

    coupling = gref
    
    # Compute the rate
    rate = 1e42 * C * coupling**2 * (E / E0)**beta * np.exp(-(beta + 1) * E / E0)

    return rate



def plot_RedSupergiantsAxion_flux(proc: str, Eamin: float, Eamax: float):
    """
    Plot the axion flux spectra from red supergiant stars across multiple stellar models.

    This function computes the differential axion flux (dΦ_a/dE_a) for eight red supergiant 
    stellar models at a fixed axion coupling, for a given production process. 
    It then generates a normalized plot showing the flux evolution across different 
    stellar burning stages and saves the plot in both PDF and PNG formats.

    Args:
        proc (str): Axion production process to plot, e.g. 'Primakoff', 'Bremsstrahlung', or 'Compton'.
        Eamin (float): Minimum axion energy (keV) for the plot range.
        Eamax (float): Maximum axion energy (keV) for the plot range.

    Side Effects:
        - Saves the generated plot as '{proc}_RSGAxion_flux_plot.pdf' and 
          '{proc}_RSGAxion_flux_plot.png' inside directories specified by the 
          global variable `plotfolder`.
        - Displays the plot using matplotlib.

    Notes:
        - Assumes a global variable `plotfolder` exists for output file paths.
        - Uses a fixed axion coupling constant gref = 1 for all flux calculations.
        - The plot includes flux curves for stellar models representing different 
          burning stages, labeled in the legend.
        - Fluxes are scaled by their order of magnitude to enhance visualization.
    """
    
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


def get_NNbremsstrahlungBNSaxion_parameters(t):
    """
    Retrieve the parameters for the NN bremsstrahlung axion flux model from a BNS merger at a given time snapshot.

    Given an integer `t` (representing the time after merger in milliseconds), this function returns 
    a tuple of parameters used to model the axion flux due to nucleon-nucleon bremsstrahlung 
    from a binary neutron star (BNS) merger.

    Args:
        t (int): Time after merger in ms (must be one of 5, 10, 15, or 20).

    Returns:
        tuple: A tuple of the form (E0, beta, C), where
            - E0 (float): Characteristic energy scale in MeV.
            - beta (float): Power-law index.
            - C (float): Normalization factor in MeV^-1 s^-1.

    Raises:
        ValueError: If `t` is not one of the supported times.

    Notes:
        These parameters are precomputed fits for the differential axion flux formula:
            flux ∝ C * (Ea / E0)^beta * exp(-(1 + beta) * Ea / E0)
        derived from a BNS merger simulation (1.375-1.375 M_sun, DD2 EOS) 
        for ALP-proton coupling g_ap = 5 × 10^{-10}.
    """

    data = {
        5:  (34.27, 1.31, 3.80e53),
        10: (37.98, 1.36, 4.83e53),
        15: (37.84, 1.36, 4.40e53),
        20: (36.93, 1.35, 3.92e53),
    }

    if t not in data:
        raise ValueError(f"Unsupported t = {t}. Available t values are {list(data.keys())}")

    return data[t]



def NNbremsstrahlungBNSMax_flux(Ea: float, g_ap: float, t_pm: int) -> float:
    """
    Compute the axion flux from nucleon-nucleon bremsstrahlung in a binary neutron star merger event.

    Calculates the differential axion flux (dΦ_a/dE_a) produced by NN bremsstrahlung 
    processes in a neutron star merger event at a given time snapshot.

    Args:
        Ea (float): Axion energy in MeV.
        g_ap (float): Axion-proton coupling constant.
        t_pm (int): Post-merger time index (5,  10,  15 or 20) in ms.

    Returns:
        float: Differential axion flux [MeV⁻¹ s⁻¹ cm⁻²].

    Raises:
        ValueError: If `t_pm` is not a valid index (5,  10,  15 or 20), as enforced by 
        `get_NNbremsstrahlungBNSaxion_parameters`.

    Notes:
        The flux is computed using:
            flux = A_NN * (g_ap / 5e-10)^2 * (Ea / E0_NN)^beta_NN * exp(- (1 + beta_NN) * (Ea / E0_NN))
        where the parameters (E0_NN, beta_NN, A_NN) are determined by the time index `t_pb`.
    """
    
    E0, beta, C = get_NNbremsstrahlungBNSaxion_parameters(t_pm)
    
    return C * (g_ap / 5e-10)**2 * (Ea / E0)**beta * np.exp(- (beta + 1) * (Ea / E0))



def plot_NNbremsstrahlungBNSMax_flux(Eamin: float, Eamax: float):
    """
    Plot the supernova axion flux from NN bremsstrahlung over a specified energy range.

    This function computes the differential axion flux (dN_a / dE_a dt) from 
    nucleon-nucleon bremsstrahlung in a supernova for three different 
    post-bounce times (1 s, 3 s, 5 s). It then generates a normalized 
    plot and saves it as both PDF and PNG files.

    Args:
        Eamin (float): Minimum axion energy (MeV) for the plot range.
        Eamax (float): Maximum axion energy (MeV) for the plot range.

    Side Effects:
        - Saves the generated plot as 'NNBrehm_BNSM_flux_plot.pdf' and 
          'NNBrehm_BNSM_flux_plot.png' in directories specified by the 
          global variable `plotfolder`.
        - Displays the plot using matplotlib.

    Notes:
        - Assumes a global variable `plotfolder` exists to specify the output directories.
        - Uses a fixed axion-proton coupling of 5e-10 for the flux calculation.
        - Fluxes are computed at three different post-bounce times (1 s, 3 s, 5 s).
        - The fluxes are scaled by their order of magnitude to improve visualization.
    """
    
    plt.figure(figsize=(10, 6))
    # Energy range
    E_values = np.linspace(Eamin, Eamax, int(Eamax-Eamin)*20)  # Energy values from 0 to 10 keV
    # Compute axion flux
    flux1 = NNbremsstrahlungBNSMax_flux(E_values, 5e-10, 5)
    flux2 = NNbremsstrahlungBNSMax_flux(E_values, 5e-10, 10)
    flux3 = NNbremsstrahlungBNSMax_flux(E_values, 5e-10, 15)
    flux4 = NNbremsstrahlungBNSMax_flux(E_values, 5e-10, 20)
    # Customize the range of the plot
    maxflux = max(np.max(flux1),np.max(flux2),np.max(flux3),np.max(flux4))
    plt.xlim(Eamin, Eamax)  # Custom x-axis limits
    plt.ylim(0, maxflux*1.1*10**(-int(np.log10(maxflux))))  # Custom y-axis limits   
    # Plot the axion flux
    fl1 = plt.plot(E_values, flux1*10**(-int(np.log10(maxflux))), color='black', ls='-')
    fl2 = plt.plot(E_values, flux2*10**(-int(np.log10(maxflux))), color='black', ls='--')
    fl3 = plt.plot(E_values, flux3*10**(-int(np.log10(maxflux))), color='black', ls='-.')
    fl4 = plt.plot(E_values, flux4*10**(-int(np.log10(maxflux))), color='black', ls=':')
    # Add labels and legend
    plt.xlabel(r'$E_a\,[{\rm MeV}]$', fontsize=30)
    plt.ylabel(r'$\frac{d N_{a}}{d E_a\,d t}\,[10^{' + str(int(np.log10(maxflux))) + r'}\,{\rm MeV}^{-1}{\rm s}^{-1}]$', fontsize=30)
    plt.grid(True) 
    h = [fl1[0], fl2[0], fl3[0], fl4[0]]
    # r'$e^-$ at rest']
    l = [r'$t_\mathrm{pm}=5$ ms', r'$t_\mathrm{pm}=10$ ms', r'$t_\mathrm{pm}=15$ ms', r'$t_\mathrm{pm}=20$ ms']
    leg = plt.legend(h, l, loc='upper right', fontsize=20, facecolor='white', framealpha=1)
    # Save the plot as PDF
    plt.savefig(plotfolder + 'NNBrehm_BNSM_flux_plot.pdf', bbox_inches='tight')
    plt.savefig(plotfolder + 'plots_png/NNBrehm_BNSM_flux_plot.png', bbox_inches='tight')
    plt.show()
    pass

