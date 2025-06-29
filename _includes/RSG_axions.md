
<details open id="RSG-axions">
<summary><span style="font-size:2em;font-weight:bold;color:#228B22;">Red Supergiants axions</span></summary>

<p>
ALP production in massive stars at supergiant stages is dominated by their couplings to photons and electrons. 
The dominant ALP production process induced by the ALP-photon interaction is the Primakoff effect,
\(\gamma + Ze \rightarrow a + Ze\),
corresponding to the conversion of a thermal photon into an ALP in the electrostatic field of charged particles in the stellar plasma 
[<a href="https://doi.org/10.1016/0370-2693(94)01529-L" target="_blank">Carlson</a>].
</p>

<p>
On the other hand, axions interacting with electrons are mainly produced via Compton scattering,
\(\gamma + e \rightarrow e + a\) 
[<a href="https://wwwth.mpp.mpg.de/members/raffelt/mypapers/Stars.pdf" target="_blank">Raffelt</a>],
and the electron-ion Bremsstrahlung,
\(e + Ze \rightarrow e + Ze + a\) 
[<a href="https://journals.aps.org/prd/abstract/10.1103/PhysRevD.103.123024" target="_blank">Carenza and Lucente</a>].
</p>

<p>
The total amount of ALPs produced by the star is obtained by integrating the production rates over the entire volume of the star.
The Red-Giant Branch (RGB) ALP production spectrum integrated over the star volume can be fitted as
</p>

<p>
$$
\frac{d N_a}{dE dt}=\frac{10^{42}}{\mathrm{keV}\,\mathrm{s}}\biggl[{\mathcal C}_B\,g_{13}^2\,\left(\frac{E}{E_{0,B}}\right)^{\beta_B}\,e^{-(\beta_B+1)E/E_{0,B}}\\ 
+ {\mathcal C}_C\,g_{13}^2\,\left(\frac{E}{E_{0,C}}\right)^{\beta_C}\,e^{-(\beta_C+1)E/E_{0,C}} \\ 
+ {\mathcal C}_P\,g_{11}^2\,\left(\frac{E}{E_{0,P}}\right)^{\beta_P}\,e^{-(\beta_P+1)E/E_{0,P}}\biggr]\,,
$$
</p>

<p>
where 
\(g_{11} \equiv g_{a\gamma}/10^{-11}\,\mathrm{GeV}^{-1}\),
\(g_{13}\equiv g_{ae}/10^{-13}\),
\({\mathcal C}_{B/C/P}\) are normalization constants, 
\(E_{0,{B/C/P}}\) is the average energy 
and 
\(\beta_{B/C/P}\) is the spectral index for Bremsstrahlung, Compton and Primakoff processes, respectively. 
</p>

<table>
<thead>
<tr>
  <th rowspan="2">Model</th>
  <th rowspan="2">Phase</th>
  <th colspan="3">Primakoff</th>
  <th colspan="3">Bremsstrahlung</th>
  <th colspan="3">Compton</th>
</tr>
<tr>
  <th>$$\mathcal{C}_P$$</th>
  <th>$$E_{0,P}\,[\mathrm{keV}]$$ </th>
  <th>$$\beta_P$$</th>
  <th>$$\mathcal{C}_B$$</th>
  <th>$$E_{0,B}\,[\mathrm{keV}]$$</th>
  <th>$$\beta_B$$</th>
  <th>$$\mathcal{C}_C$$</th>
  <th>$$E_{0,C}\,[\mathrm{keV}]$$</th>
  <th>$$\beta_C$$</th>
</tr>
</thead>
<tbody>
<tr><td>1</td><td>He burning</td><td>$$3.36$$</td><td>$$74.7$$</td><td>$$2.10$$</td><td>$$2.18\cdot10^{-2}$$</td><td>$$36.1$$</td><td>$$0.732$$</td><td>$$5.24$$</td><td>$$115$$</td><td>$$3.12$$</td></tr>
<tr><td>2</td><td>start C burning</td><td>$$9.70$$</td><td>$$173$$</td><td>$$2.01$$</td><td>$$0.530$$</td><td>$$95.3$$</td><td>$$0.857$$</td><td>$$116$$</td><td>$$267$$</td><td>$$3.18$$</td></tr>
<tr><td>3</td><td>C burning</td><td>$$13.1$$</td><td>$$208$$</td><td>$$2.02$$</td><td>$$1.06$$</td><td>$$118$$</td><td>$$0.901$$</td><td>$$211$$</td><td>$$315$$</td><td>$$3.18$$</td></tr>
<tr><td>4</td><td>start Ne burning</td><td>$$26.9$$</td><td>$$339$$</td><td>$$1.97$$</td><td>$$8.53$$</td><td>$$226$$</td><td>$$1.08$$</td><td>$$991$$</td><td>$$489$$</td><td>$$3.23$$</td></tr>
<tr><td>5</td><td>start O burning</td><td>$$23.3$$</td><td>$$367$$</td><td>$$1.85$$</td><td>$$11.3$$</td><td>$$255$$</td><td>$$1.10$$</td><td>$$991$$</td><td>$$525$$</td><td>$$3.15$$</td></tr>
<tr><td>6</td><td>O burning</td><td>$$31.5$$</td><td>$$495$$</td><td>$$1.77$$</td><td>$$23.1$$</td><td>$$333$$</td><td>$$1.09$$</td><td>$$1430$$</td><td>$$680$$</td><td>$$2.90$$</td></tr>
<tr><td>7</td><td>start Si burning</td><td>$$94.5$$</td><td>$$858$$</td><td>$$1.89$$</td><td>$$73.5$$</td><td>$$593$$</td><td>$$1.11$$</td><td>$$8430$$</td><td>$$1090$$</td><td>$$3.09$$</td></tr>
<tr><td>8</td><td>Si burning</td><td>$$92.8$$</td><td>$$1000$$</td><td>$$1.79$$</td><td>$$86.0$$</td><td>$$685$$</td><td>$$1.07$$</td><td>$$8030$$</td><td>$$1260$$</td><td>$$2.85$$</td></tr>
</tbody>
</table>

<p style="font-style: italic; font-size: 0.9em; margin-top: 0.5em;">
<strong>Table:</strong> Summary of the fitting parameters to be used in the equation above.
</p>

<h3>
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/blob/main/notebooks/RedSuperGiantsAxions.ipynb" target="_blank" rel="noopener noreferrer">
    View Notebook (.ipynb)
  </a>
</h3>

<hr>

<details  id="rsg-prim">
<summary><span style="font-size:1.5em;color:#228B22;">Primakoff</span></summary>

<img align="right" width="500" src="plots/plots_png/Primakoff_RSGAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{a\gamma}=10^{-11}\,\text{GeV}^{-1}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Primakoff_RSGAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Primakoff_RSGAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>
</details>
<hr>

<details  id="rsg-brem">
<summary><span style="font-size:1.5em;color:#228B22;">Bremsstrahlung</span></summary>

<img align="right" width="500" src="plots/plots_png/Bremsstrahlung_RSGAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{ae}=10^{-13}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Bremsstrahlung_RSGAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Bremsstrahlung_RSGAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>
</details>
<hr>

<details  id="rsg-com">
<summary><span style="font-size:1.5em;color:#228B22;">Compton</span></summary>

<img align="right" width="500" src="plots/plots_png/Compton_RSGAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{ae}=10^{-13}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Compton_RSGAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Compton_RSGAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>
</details>
<hr>

</details>
<div class="green-line"></div>