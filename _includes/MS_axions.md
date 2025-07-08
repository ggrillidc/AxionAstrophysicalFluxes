
<details open id="MS-axions">
<summary><span style="font-size:2em;font-weight:bold;color:#228B22;">Main Sequence stars axions</span></summary>

<p>
  The quasi-thermal Main Sequence stars axion spectrum at the source can be parametrized by 
</p>

<p>
$$
\frac{d\Phi_a}{dE_a}= C_0 \left(\frac{g_{ax}}{g_{\mathrm{ref}}}\right)^2 
\left(\frac{E}{E_0}\right)^\beta e^{-(1+\beta)\frac{E}{E_0}}
$$
</p>

<p>
where the axion parameters are now a function of the stellar mass and are given in the following table:
</p>

<table>
  <thead>
    <tr>
      <th></th>
      <th>$$g_{a x}$$</th>
      <th>$$C_{0} (10^{40}\,\text{keV}^{-1}\,\text{s}^{-1}\,\text{cm}^{-2})$$</th>
      <th>$$E_{0} (\text{keV})$$</th>
      <th>$$\beta$$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Primakoff $$x=\gamma$$</td>
      <td>$$10^{-12}\,\text{GeV}^{-1}$$</td>
      <td>$$\begin{cases} 
        -0.140+0.053\,M^{-0.347}e^{M^{0.379}} & \text{for } M<10 \\
        -0.014+0.011\,M^{1.081} & \text{for } M\geq 10
      \end{cases}$$ </td>
      <td>$$3.70+1.13\,M^{0.355}$$</td>
      <td>$$1.23+3.63\,e^{-M^{0.29}}$$</td>
    </tr>
    <tr>
      <td>Bremsstrahlung $$x=e$$</td>
      <td>$$10^{-12}$$</td>
      <td>$$55.21+1.62\times10^{4}M^{-0.65}$$</td>
      <td>$$0.06+1.80\,M^{0.23}$$</td>
      <td>$$\begin{cases}
        0.57 + 0.18 e^{-M^{1.09}} & \text{for } M\le 10  \\
        0.48+0.05 \,M^{0.19} & \text{for } M\geq 10 
      \end{cases}$$</td>
    </tr>
    <tr>
      <td>Compton $$x=e$$</td>
      <td>$$10^{-12}$$</td>
      <td>$$0.14+1.01\,M^{1.49}$$</td>
      <td>$$0.025+6.014\,M^{0.225}$$</td>
      <td>$$2.99-0.56\,e^{-M^{0.09}}$$</td>
    </tr>
  </tbody>
</table>

<p style="font-style: italic; font-size: 0.9em; margin-top: 0.5em;">
  <strong>Table:</strong> Summary of the fitting parameters to be used in the equation above, where \(M\) is in units of solar masses \({\rm M}_{\odot}\). These fits are valid in the range 
  \(1-100~{\rm M}_{\odot}\) and can be obtained with this 
  <a href="https://github.com/pcarenza95/MainSequence-Axion" target="_blank" rel="noopener noreferrer">GitHub code</a>.
</p>

<h3>
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/blob/main/notebooks/MainSequenceAxions.ipynb" target="_blank" rel="noopener noreferrer">
    View Notebook (.ipynb)
  </a>
</h3>

<hr>

<details  id="ms-prim">
<summary><span style="font-size:1.5em;color:#228B22;">Primakoff</span></summary>

<img align="right" width="500" src="plots/plots_png/Primakoff_MSAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{a\gamma}=10^{-12}\,\text{GeV}^{-1}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Primakoff_MSAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Primakoff_MSAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>

</details>
<hr>

<details  id="ms-brem">
<summary><span style="font-size:1.5em;color:#228B22;">Bremsstrahlung</span></summary>

<img align="right" width="500" src="plots/plots_png/Bremsstrahlung_MSAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{ae}=10^{-12}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Bremsstrahlung_MSAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Bremsstrahlung_MSAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>

</details>
<hr>

<details   id="ms-com">
<summary><span style="font-size:1.5em;color:#228B22;">Compton</span></summary>

<img align="right" width="500" src="plots/plots_png/Compton_MSAxion_flux_plot.png">

<h3>&nbsp;</h3>
\(g_{ae}=10^{-12}\)

<p>
  Plot (
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/Compton_MSAxion_flux_plot.pdf" target="_blank" rel="noopener noreferrer">pdf</a>,
  <a href="https://github.com/ggrillidc/AxionAstrophysicalFluxes/raw/main/plots/plots_png/Compton_MSAxion_flux_plot.png" target="_blank" rel="noopener noreferrer">png</a>
  )
</p>

<h3>&nbsp;</h3><h3>&nbsp;</h3><h3>&nbsp;</h3>

</details>
<hr>

</details>
<div class="green-line"></div>
