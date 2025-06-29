
<details open id="solar-axions">
<summary><span style="font-size:2em;font-weight:bold;color:#228B22;">Solar Axions</span></summary>


An accurate fit of solar axion fluxes at Earth obtained after integrating over the AGSS09 solar model [<a href="https://iopscience.iop.org/article/10.1088/0004-637X/705/2/L123">Serenelli et al. 2009</a>, <a href="https://link.springer.com/article/10.1007/s10509-009-0174-8">Serenelli 2010</a>] is given by:

$$
\frac{d\Phi_a}{dE_a}= C_0 \left(\frac{g_{ax}}{g_{\mathrm{ref}}}\right)^2 \left(\frac{E}{E_0}\right)^\beta e^{-(1+\beta)\frac{E}{E_0}},
$$

where the axion parameters are shown in the following Table:


  <table>
    <thead>
      <tr>
        <th></th>
        <th>$$g_{\text{ref}}$$</th>
        <th>$$ C_0\, (\text{keV}^{-1}~\text{s}^{-1}~\text{cm}^{-2})$$</th>
        <th>$$ E_0\, (\text{keV})$$</th>
        <th>$$ \beta $$</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Primakoff, $$x = \gamma $$</td>
        <td>$$ 10^{-12}~\text{GeV}^{-1} $$</td>
        <td>$$ (2.19 \pm 0.08)\,10^8 $$</td>
        <td>$$ 4.17 \pm 0.02 $$</td>
        <td>$$ 2.531 \pm 0.008 $$</td>
      </tr>
      <tr>
        <td>Bremsstrahlung, $$ x = e $$</td>
        <td>$$ 10^{-12} $$</td>
        <td>$$ (3.847 \pm 0.007)\,10^{11} $$</td>
        <td>$$ 1.63 \pm 0.01 $$</td>
        <td>$$ 0.8063 \pm 0.0003 $$</td>
      </tr>
      <tr>
        <td>Compton, $$ x = e $$</td>
        <td>$$ 10^{-12} $$</td>
        <td>$$ (8.8 \pm 0.1) \, 10^{11} $$</td>
        <td>$$ 5.10 \pm 0.03 $$</td>
        <td>$$ 2.979 \pm 0.001 $$</td>
      </tr>
    </tbody>
  </table>



<p style="font-style: italic; font-size: 0.9em; margin-top: 0.5em;">
    <strong>Table:</strong> Summary of the fitting parameters to reproduce the axion emission from the Sun via Primakoff (coupling to photons \(g_{a\gamma}\)), Bremsstrahlung, and Compton (coupling to electrons \(g_{ae}\)), see [<a href="https://iopscience.iop.org/article/10.1088/1475-7516/2024/11/009">Hoof et al.</a>, <a href="https://iopscience.iop.org/article/10.1088/1475-7516/2021/09/006">Wu and Xu</a>] and the <a href="https://github.com/pcarenza95/SolarAxionCode">GitHub code</a>. The uncertainty on the fitting parameters includes the most recent solar models [<a href="https://www.aanda.org/articles/aa/full_html/2022/05/aa42971-21/aa42971-21.html">Magg et al. 2022</a>].
  </p>


<h3>
    <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/blob/main/notebooks/SolarAxions.ipynb" target="_blank" rel="noopener noreferrer">
      View Notebook (.ipynb)
    </a>
  </h3>

<hr>



<details  id="sol-prim">
<summary><span style="font-size:1.5em;color:#228B22;">Primakoff</span></summary>

<img align="right" width="500" src="plots/plots_png/Primakoff_SolarAxion_flux_plot.png">


<h3>&nbsp;</h3>
\(g_{a\gamma}=10^{-12}\,\text{GeV}^{-1}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Primakoff_SolarAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Primakoff_SolarAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3>
<h3>&nbsp;</h3>
<h3>&nbsp;</h3>


</details>
<hr>


<details  id="sol-brem">
<summary><span style="font-size:1.5em;color:#228B22;">Bremsstrahlung</span></summary>


<img align="right" width="500" src="plots/plots_png/Bremsstrahlung_SolarAxion_flux_plot.png"> 

<h3>&nbsp;</h3>

\(g_{ae}=10^{-12}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Bremsstrahlung_SolarAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Bremsstrahlung_SolarAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>


<h3>&nbsp;</h3>
<h3>&nbsp;</h3>
<h3>&nbsp;</h3>


</details>
<hr>


<details  id="sol-com">
<summary><span style="font-size:1.5em;color:#228B22;">Compton</span></summary>

<img align="right" width="500" src="plots/plots_png/Compton_SolarAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{ae}=10^{-12}\)



<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Compton_SolarAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Compton_SolarAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>


<h3>&nbsp;</h3>
<h3>&nbsp;</h3>
<h3>&nbsp;</h3>


</details>
<hr>

</details>
<div class="green-line"></div>