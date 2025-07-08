---
layout: default
use_math: true
---

<style>
  html {
    scroll-behavior: smooth;
  }
</style>

<style>
.green-line {
  height: 2px;
  background-color: green;
  width: 100%;
  margin: 1em 0;
}
</style>


<style>
  .toc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2em;
    max-width: 900px;
    margin: auto;
  }

  .toc-grid li {
    margin-bottom: 0.5em;
  }

  .toc-grid li ul {
    margin-left: 1.2em;
    margin-top: 0.3em;
  }

  .toc-grid ul:first-child {
    border-right: 2px solid #228B22; /* green vertical line */
    padding-right: 1.5em;
  }
</style>


<summary><span style="font-size:2em;font-weight:bold;color:#228B22;">Table of contents</span></summary>
<div class="toc-grid">
  <ul>
    <li><a href="#solar-axions">Solar Axions</a>
      <ul>
        <li><a href="#sol-prim">Primakoff</a></li>
        <li><a href="#sol-brem">Bremsstrahlung</a></li>
        <li><a href="#sol-com">Compton</a></li>
      </ul>
    </li>
    <li><a href="#MS-axions">Main Sequence Axions</a>
      <ul>
        <li><a href="#ms-prim">Primakoff</a></li>
        <li><a href="#ms-brem">Bremsstrahlung</a></li>
        <li><a href="#ms-com">Compton</a></li>
      </ul>
    </li>
    <li><a href="#rg-axions">Red Giants Axions</a>
      <ul>
        <li><a href="#rg-brem">Electron-ion Bremsstrahlung</a></li>
      </ul>
    </li>
    <li><a href="#HB-axions">Horizontal Branch Axions</a>
      <ul>
        <li><a href="#hb-prim">Primakoff</a></li>
      </ul>
    </li>
  </ul>

  <ul>
    <!-- <li><a href="#ARG-axions">Asymptotic Red Giants Axions</a></li> -->
    <li><a href="#WD-axions">White Dwarfs Axions</a>
      <ul>
        <li><a href="#wd-brem">Electron-ion Bremsstrahlung</a></li>
      </ul>
    </li>
    <li><a href="#RSG-axions">Red Supergiants Axions</a>
      <ul>
        <li><a href="#rsg-prim">Primakoff</a></li>
        <li><a href="#rsg-brem">Bremsstrahlung</a></li>
        <li><a href="#rsg-com">Compton</a></li>
      </ul>
    </li>
    <li><a href="#CCSN-axions">Core-collapse SN Axions</a>
      <ul>
        <li><a href="#ccsn-brem">NN Bremsstrahlung</a></li>
        <li><a href="#ccsn-pi">Pion conversion</a></li>
      </ul>
    </li>
    <!-- <li><a href="#NS-axions">Neutron Star Axions</a></li>
    <li><a href="#BNSM-axions">Binary neutron star merger Axions</a></li> -->
  </ul>
</div>

{% include solar_axions.md %}
{% include MS_axions.md %}
{% include RG_axions.md %}
{% include HB_axions.md %}
<!-- {% include ARG_axions.md %} -->
{% include WD_axions.md %}
{% include RSG_axions.md %}
{% include CCSN_axions.md %}
<!-- {% include NS_axions.md %}
{% include BNSM_axions.md %} -->

This webpage hosts data files and python notebooks for axion astrophysical fluxes. 

Please, email me [giovanni.grilli@lngs.infn.it] for questions, comments or complaints.

{% raw %}
<script>
function openDetailsFromHash() {
  const hash = window.location.hash;
  if (hash) {
    const target = document.querySelector(hash);
    if (target) {
      // If target is itself a <details>, open it
      if (target.tagName.toLowerCase() === "details") {
        target.open = true;
      }
      // Also open all parent <details> elements
      let parent = target.parentElement;
      while (parent) {
        if (parent.tagName.toLowerCase() === "details") {
          parent.open = true;
        }
        parent = parent.parentElement;
      }
      target.scrollIntoView();
    }
  }
}

// Run on load
document.addEventListener("DOMContentLoaded", openDetailsFromHash);
// Run on clicking any link that changes the hash
window.addEventListener("hashchange", openDetailsFromHash);
</script>
{% endraw %}

