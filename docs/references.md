# References

Every fact in these docs that comes from someone else's work is cited here.
DOIs were checked against Crossref when this page was written (2026-11-04).
Entries marked *secondary* were read through news coverage or a project page,
not the original paper.

## Foundations of the idea

<a id="dirac1929"></a>
**Dirac 1929.** P. A. M. Dirac, "Quantum mechanics of many-electron systems",
*Proc. R. Soc. Lond. A* 123, 714–733 (1929).
[doi:10.1098/rspa.1929.0094](https://doi.org/10.1098/rspa.1929.0094).
Used for: the laws behind all of chemistry are known; the obstacle is solving them.

<a id="anderson1972"></a>
**Anderson 1972.** P. W. Anderson, "More is different", *Science* 177, 393–396 (1972).
[doi:10.1126/science.177.4047.393](https://doi.org/10.1126/science.177.4047.393).
Used for: each level of organisation has properties and laws of its own.

<a id="feynman1982"></a>
**Feynman 1982.** R. P. Feynman, "Simulating physics with computers",
*Int. J. Theor. Phys.* 21, 467–488 (1982).
[doi:10.1007/BF02650179](https://doi.org/10.1007/BF02650179).
Used for: exact simulation of quantum systems on classical computers grows
exponentially with system size.

## Physics and methods used in M0

<a id="born1927"></a>
**Born & Oppenheimer 1927.** M. Born, R. Oppenheimer, "Zur Quantentheorie der Molekeln",
*Ann. Phys.* 389, 457–484 (1927).
[doi:10.1002/andp.19273892002](https://doi.org/10.1002/andp.19273892002).
Used for: separating electron motion from nuclear motion, which defines a
potential energy curve.

<a id="szabo1996"></a>
**Szabo & Ostlund 1996.** A. Szabo, N. S. Ostlund, *Modern Quantum Chemistry:
Introduction to Advanced Electronic Structure Theory*, Dover (1996).
Used for: Hartree-Fock and full configuration interaction (exact within a basis set).

<a id="helgaker2000"></a>
**Helgaker, Jørgensen & Olsen 2000.** T. Helgaker, P. Jørgensen, J. Olsen,
*Molecular Electronic-Structure Theory*, Wiley (2000).
Used for: full CI, basis sets, and the cost of exact electronic-structure methods.

<a id="dunning1989"></a>
**Dunning 1989.** T. H. Dunning Jr., "Gaussian basis sets for use in correlated
molecular calculations. I. The atoms boron through neon and hydrogen",
*J. Chem. Phys.* 90, 1007–1023 (1989).
[doi:10.1063/1.456153](https://doi.org/10.1063/1.456153).
Used for: the cc-pVTZ basis set.

<a id="sun2018"></a>
**Sun et al. 2018.** Q. Sun et al., "PySCF: the Python-based simulations of
chemistry framework", *WIREs Comput. Mol. Sci.* 8, e1340 (2018).
[doi:10.1002/wcms.1340](https://doi.org/10.1002/wcms.1340).

<a id="sun2020"></a>
**Sun et al. 2020.** Q. Sun et al., "Recent developments in the PySCF program package",
*J. Chem. Phys.* 153, 024109 (2020).
[doi:10.1063/5.0006074](https://doi.org/10.1063/5.0006074).
Used for: the layer-0 solver (PySCF 2.14 in M0).

<a id="morse1929"></a>
**Morse 1929.** P. M. Morse, "Diatomic molecules according to the wave mechanics.
II. Vibrational levels", *Phys. Rev.* 34, 57–64 (1929).
[doi:10.1103/PhysRev.34.57](https://doi.org/10.1103/PhysRev.34.57).
Used for: the Morse potential and its closed-form vibrational levels.

<a id="swope1982"></a>
**Swope et al. 1982.** W. C. Swope, H. C. Andersen, P. H. Berens, K. R. Wilson,
"A computer simulation method for the calculation of equilibrium constants for
the formation of physical clusters of molecules: application to small water clusters",
*J. Chem. Phys.* 76, 637–649 (1982).
[doi:10.1063/1.442716](https://doi.org/10.1063/1.442716).
Used for: the velocity Verlet integrator in layer 1.

<a id="frenkel2023"></a>
**Frenkel & Smit 2023.** D. Frenkel, B. Smit, *Understanding Molecular Simulation:
From Algorithms to Applications*, 3rd ed., Academic Press (2023).
Used for: molecular dynamics practice, including femtosecond time steps.

## Experimental data

<a id="nist-h2"></a>
**NIST / Huber & Herzberg.** NIST Chemistry WebBook, "Constants of diatomic
molecules", H2 ground state X ¹Σg⁺, compiled by K. P. Huber and G. Herzberg
(from *Molecular Spectra and Molecular Structure IV. Constants of Diatomic
Molecules*, Van Nostrand Reinhold, 1979).
[webbook.nist.gov](https://webbook.nist.gov/cgi/cbook.cgi?ID=C1333740&Mask=1000),
read 2026-11-04.
Used for: r_e = 0.74144 Å, ω_e = 4401.213 cm⁻¹, ω_e x_e = 121.336 cm⁻¹,
D_0 = 36118.3 cm⁻¹. The fundamental 4158.541 cm⁻¹ is computed by groundup from
the tabulated constants as ω_e − 2ω_e x_e.

## Building blocks and scale

<a id="durr2008"></a>
**Dürr et al. 2008.** S. Dürr et al., "Ab initio determination of light hadron masses",
*Science* 322, 1224–1227 (2008).
[doi:10.1126/science.1163233](https://doi.org/10.1126/science.1163233).
Used for: the proton mass computed from quarks and gluons.

<a id="bohacek1996"></a>
**Bohacek, McMartin & Guida 1996.** R. S. Bohacek, C. McMartin, W. C. Guida,
"The art and practice of structure-based drug design: a molecular modeling perspective",
*Med. Res. Rev.* 16, 3–50 (1996).
[doi:10.1002/(SICI)1098-1128(199601)16:1<3::AID-MED1>3.0.CO;2-6](https://doi.org/10.1002/(SICI)1098-1128(199601)16:1%3C3::AID-MED1%3E3.0.CO;2-6).
Used for: the often-quoted estimate of ~10⁶⁰ possible drug-like molecules.

<a id="nurk2022"></a>
**Nurk et al. 2022.** S. Nurk et al., "The complete sequence of a human genome",
*Science* 376, 44–53 (2022).
[doi:10.1126/science.abj6987](https://doi.org/10.1126/science.abj6987).
Used for: the human genome length (~3.06 billion base pairs).

## From chemistry towards life

<a id="wohler1828"></a>
**Wöhler 1828.** F. Wöhler, "Ueber künstliche Bildung des Harnstoffs",
*Ann. Phys.* 88, 253–256 (1828).
[doi:10.1002/andp.18280880206](https://doi.org/10.1002/andp.18280880206).
Used for: the first synthesis of a biological molecule from inorganic starting materials.

<a id="miller1953"></a>
**Miller 1953.** S. L. Miller, "A production of amino acids under possible
primitive Earth conditions", *Science* 117, 528–529 (1953).
[doi:10.1126/science.117.3046.528](https://doi.org/10.1126/science.117.3046.528).

<a id="gibson2010"></a>
**Gibson et al. 2010.** D. G. Gibson et al., "Creation of a bacterial cell
controlled by a chemically synthesized genome", *Science* 329, 52–56 (2010).
[doi:10.1126/science.1190719](https://doi.org/10.1126/science.1190719).

<a id="hutchison2016"></a>
**Hutchison et al. 2016.** C. A. Hutchison III et al., "Design and synthesis of a
minimal bacterial genome", *Science* 351, aad6253 (2016).
[doi:10.1126/science.aad6253](https://doi.org/10.1126/science.aad6253).
Used for: JCVI-syn3.0, 473 genes.

## Simulation: the state of the art

<a id="wang2014"></a>
**Wang et al. 2014.** L.-P. Wang, A. Titov, R. McGibbon, F. Liu, V. S. Pande,
T. J. Martínez, "Discovering chemistry with an ab initio nanoreactor",
*Nature Chemistry* 6, 1044–1048 (2014).
[doi:10.1038/nchem.2099](https://doi.org/10.1038/nchem.2099)
([open access](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239668)).
Used for: reactions, including routes to glycine, emerging from first-principles
dynamics without preset reaction coordinates.

<a id="saitta2026"></a>
**Saitta group, Sorbonne Université / ENS.** Machine-learned interatomic potentials
for prebiotic reaction pathways (glycine; a step towards adenine), reported in
*ACS Earth and Space Chemistry* (2026), HAL record
[hal-05498507](https://hal.sorbonne-universite.fr/CPCV/hal-05498507v1); group summary at
[cpcv.chimie.ens.fr](https://cpcv.chimie.ens.fr/topics/machine-learning-for-chemical-reactivity).
*Secondary*: full title and author list not verified (the HAL page blocked automated access).

<a id="stevens2023"></a>
**Stevens et al. 2023.** J. A. Stevens et al., "Molecular dynamics simulation of
an entire cell", *Front. Chem.* 11, 1106495 (2023).
[doi:10.3389/fchem.2023.1106495](https://doi.org/10.3389/fchem.2023.1106495).
Used for: a Martini model of JCVI-syn3A, 561 million coarse-grained beads,
about 6 billion atoms. A perspective describing model construction, not a finished run.

<a id="thornburg2026"></a>
**Thornburg et al. 2026.** Z. R. Thornburg et al., "Bringing the genetically
minimal cell to life on a computer in 4D", *Cell* (2026).
[doi:10.1016/j.cell.2026.02.009](https://doi.org/10.1016/j.cell.2026.02.009).
*Secondary*: details (105-minute cycle simulated in about six days on GPUs,
cycle time within about two minutes of experiment, rates taken from experiment)
are from [JCVI](https://www.jcvi.org/publications/bringing-genetically-minimal-cell-life-computer-4d),
[Illinois QCB](https://qcb.illinois.edu/qcb-team-simulates-a-living-cell-that-grows-and-divides/) and
[astrobiology.com](https://astrobiology.com/2026/03/11/simulating-a-living-cell-first-simulation-of-an-entire-cell-cycle/).

<a id="aguera2024"></a>
**Agüera y Arcas et al. 2024.** B. Agüera y Arcas et al., "Computational life:
how well-formed, self-replicating programs emerge from simple interaction",
arXiv:2406.19108 (2024). [arxiv.org/abs/2406.19108](https://arxiv.org/abs/2406.19108).

<a id="virtualcell2025"></a>
**AI virtual cells, 2025.** Arc Institute's *State* model
([BiopharmaTrend](https://www.biopharmatrend.com/news/arc-institute-releases-its-first-virtual-cell-model-trained-on-270-million-cells-1302/))
and the Chan Zuckerberg Initiative's virtual cell programme
([Freethink](https://www.freethink.com/artificial-intelligence/virtual-cells)).
*Secondary*: news coverage only.
