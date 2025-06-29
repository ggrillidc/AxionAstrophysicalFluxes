
<details open id="CCSN-axions"> 
<summary><span style="font-size:2em;font-weight:bold;color:#228B22;">Core-collapse Supernovae axions</span></summary>

<p>
  Axion emission from the inner regions of the SN core is expected to be strongly enhanced by the extreme temperature and density conditions,
  reaching values as high as 
  \(T\sim 40\,\text{MeV}\) 
  and 
  \(\rho\sim 3\times 10^{14}\,\text{g}\,\text{cm}^{-3}\).
</p>

<p>
  The following spectrum adopts the 1D spherically symmetric GARCHING group's SN model SFHo-s18.8 provided in the 
  <a href="https://wwwmpa.mpa-garching.mpg.de/ccsnarchive//" target="_blank" rel="noopener noreferrer">Garching core-collapse SN research archive</a> 
  and based on the neutrino-hydrodynamics code PROMETHEUS-VERTEX 
  [<a href="https://www.aanda.org/articles/aa/abs/2002/46/aa2451/aa2451.html" target="_blank" rel="noopener noreferrer">Rampp and Janka</a>].
</p>

<p>
  The most efficient axion production channels from the SN core are related to their couplings to nuclear matter. 
  The production in the nuclear medium is due to NN bremsstrahlung
  \(N+N\to N+N+a\)
  and the 
  \(\pi N\)
  Compton-like process 
  \(\pi + N \to a + N\).
</p>

<p>
  The bremsstrahlung axion spectrum can be described by the fitting formula 
  [<a href="https://iopscience.iop.org/article/10.1088/1475-7516/2024/11/009" target="_blank" rel="noopener noreferrer">Lella et al.</a>]
</p>

<p>
$$
\left(\frac{d^2N_{a}}{dE_a\,dt}\right)_{NN}
= A_{NN}\,\left(\frac{g_{ap}}{5\times 10^{-10}}\right)^2\,
\left(\frac{E_a}{E_{NN}^0}\right)^{\beta_{NN}} 
\exp\!\left[-(\beta_{NN}+1)\,\frac{E_a}{E^0_{NN}}\right],
$$
</p>

<p>
with fitting parameters referring to axion emission at different instants after the core-bounce 
\(t_{\rm pb}\) 
provided in the Table below.
</p>

<table>
<thead>
<tr>
  <th>$$t_{\mathrm{pb}}\,[\mathrm{s}]$$</th>
  <th>$$E^0_{NN}\,[\mathrm{MeV}]$$</th>
  <th>$$\beta_{NN}$$</th>
  <th>$$A_{NN}\,[\mathrm{MeV}^{-1}\,\mathrm{s}^{-1}]$$</th>
</tr>
</thead>
<tbody>
<tr><td>1</td><td>$$70.19$$</td><td>$$1.44$$</td><td>$$4.56 \times 10^{54}$$</td></tr>
<tr><td>2</td><td>$$70.39$$</td><td>$$1.42$$</td><td>$$4.31 \times 10^{54}$$</td></tr>
<tr><td>3</td><td>$$56.91$$</td><td>$$1.36$$</td><td>$$2.41 \times 10^{54}$$</td></tr>
<tr><td>4</td><td>$$58.36$$</td><td>$$1.31$$</td><td>$$1.10 \times 10^{54}$$</td></tr>
<tr><td>5</td><td>$$47.41$$</td><td>$$1.24$$</td><td>$$3.95 \times 10^{53}$$</td></tr>
<tr><td>6</td><td>$$35.02$$</td><td>$$1.17$$</td><td>$$1.04 \times 10^{53}$$</td></tr>
<tr><td>7</td><td>$$23.98$$</td><td>$$1.12$$</td><td>$$2.20 \times 10^{52}$$</td></tr>
<tr><td>8</td><td>$$16.10$$</td><td>$$1.10$$</td><td>$$4.01 \times 10^{51}$$</td></tr>
</tbody>
</table>

<p style="font-style: italic; font-size: 0.9em; margin-top: 0.5em;">
<strong>Table:</strong> Summary of the fitting parameters for the NN bremsstrahlung case.
</p>

<p>
  The pion conversion emission rate is estimated as 
  [<a href="https://iopscience.iop.org/article/10.1088/1475-7516/2024/11/009" target="_blank" rel="noopener noreferrer">Lella et al.</a>]
</p>

<p>
$$
\left(\frac{d^2N_{a}}{dE_a\,dt}\right)_{\pi N}
= A_{\pi N}\,\left(\frac{g_{ap}}{5\times 10^{-10}}\right)^2\,
\left(\frac{E_a-\omega_c}{E^0_{\pi N}}\right)^{\beta_{\pi N}} 
\exp\!\left[-(\beta_{\pi N}+1)\,\frac{E_a-\omega_c}{E^0_{\pi N}}\right]
\Theta(E_a-\omega_c),
$$
</p>

<p>
where 
\(\Theta(E)\) 
is the Heaviside theta function. 
Fitting parameters for different times after the SN core bounce are:
</p>

<table>
<thead>
<tr>
  <th>$$t_{\mathrm{pb}}\,[\mathrm{s}]$$</th>
  <th>$$E^{0}_{\pi N}\,[\mathrm{MeV}]$$</th>
  <th>$$\beta_{\pi N}$$</th>
  <th>$$A_{\pi N}\,[\mathrm{MeV}^{-1}\,\mathrm{s}^{-1}]$$</th>
  <th>$$\omega_c\,[\mathrm{MeV}]$$</th>
</tr>
</thead>
<tbody>
<tr><td>1</td><td>$$126.43$$</td><td>$$1.20$$</td><td>$$2.77 \times 10^{54}$$</td><td>$$103.27$$</td></tr>
<tr><td>2</td><td>$$94.47$$</td><td>$$1.03$$</td><td>$$1.24 \times 10^{54}$$</td><td>$$98.87$$</td></tr>
<tr><td>3</td><td>$$56.14$$</td><td>$$0.54$$</td><td>$$9.78 \times 10^{52}$$</td><td>$$107.00$$</td></tr>
<tr><td>4</td><td>$$37.20$$</td><td>$$0.65$$</td><td>$$2.20 \times 10^{52}$$</td><td>$$107.06$$</td></tr>
<tr><td>5</td><td>$$25.02$$</td><td>$$0.47$$</td><td>$$3.63 \times 10^{51}$$</td><td>$$108.59$$</td></tr>
<tr><td>6</td><td>$$15.62$$</td><td>$$0.40$$</td><td>$$2.53 \times 10^{50}$$</td><td>$$108.04$$</td></tr>
<tr><td>7</td><td>$$9.18$$</td><td>$$0.37$$</td><td>$$3.10 \times 10^{48}$$</td><td>$$108.33$$</td></tr>
<tr><td>8</td><td>$$5.64$$</td><td>$$0.37$$</td><td>$$6.64 \times 10^{45}$$</td><td>$$108.37$$</td></tr>
</tbody>
</table>

<p style="font-style: italic; font-size: 0.9em; margin-top: 0.5em;">
<strong>Table:</strong> Summary of the fitting parameters for the pion conversion case.
</p>

<h3>
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/blob/main/notebooks/CoreCollapseSNAxions.ipynb" target="_blank" rel="noopener noreferrer">
    View Notebook (.ipynb)
  </a>
</h3>

<hr>

<details  id="ccsn-brem">
<summary><span style="font-size:1.5em;color:#228B22;">NN Bremsstrahlung</span></summary>

<img align="right" width="500" src="plots/plots_png/Bremsstrahlung_SNAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{ap}=5\times10^{-10}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Bremsstrahlung_SNAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Bremsstrahlung_SNAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>

</details>
<hr>

<details  id="ccsn-pi">
<summary><span style="font-size:1.5em;color:#228B22;">Pion conversion</span></summary>

<img align="right" width="500" src="plots/plots_png/PionConversion_SNAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{ap}=5\times10^{-10}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/PionConversion_SNAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/PionConversion_SNAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>

</details>
<hr>

</details>
<div class="green-line"></div>