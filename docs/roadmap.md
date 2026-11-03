# Roadmap

Each milestone adds one joint between layers. It is done only when its gate
checks pass against experiment (see [Principles](principles.md)).

## M0: H2, quantum to classical atoms (done)

- Layer 0: exact solution of the Schrödinger equation for H2 (full CI).
- Bridge: a Morse bond rule derived from the layer-0 curve.
- Layer 1: two classical atoms obeying Newton's law and the derived rule.
- Gates: bond length, vibration frequency, dissociation energy and the
  fundamental transition against NIST.

## M1: the first reaction, D + H2 → HD + H (done)

The simplest chemical reaction still involves only hydrogen. With 3 electrons,
layer 0 can stay exact. Deuterium is used because D + H2 has direct
high-temperature measurements, and one Born–Oppenheimer surface serves every
isotope.

- Layer 0: full-CI H3 near the barrier, plus points used only to measure loss.
- Bridge 1: a reactive LEPS rule built from the M0 bond rule, with one Sato
  parameter fixed by the layer-0 barrier.
- Layer 1: classical collisions that break and form bonds by themselves.
- Bridge 2: a rate constant from transition state theory with Wigner tunnelling.
- Gates: k(T) at 700–1900 K against shock-tube data, within a factor of 2.
  Result: within a factor of 1.21. See [M1](milestones/m1-dh2.md).

## M1b: rates by counting trajectories

- Fully three-dimensional, thermally sampled classical trajectories on the M1
  rule; the rate is counted, not assumed.
- Compare with M1's transition state theory and with experiment, to measure
  recrossing directly.
- Check the rule's saddle-point frequencies against layer 0.

## M2: small molecules, derived force fields

- Layer 0: coupled cluster / DFT for H2O, NH3, CH4, CO2 (full CI no longer feasible).
- Bridge: bond, angle and torsion rules derived from layer-0 Hessians and scans.
- Gates: vibrational spectra; then a water box (density, radial distribution) for the
  derived intermolecular rule.

## M3: open reactive chemistry

- An ML interatomic potential trained on layer-0 data, using an existing open-source
  library rather than a new one.
- Nanoreactor-style runs on a mix of H, C, N, O, with the reaction network
  extracted automatically from trajectories.
- Gates: reaction energies and barriers of known reactions.

## M4: rates to a kinetic layer

- Rate constants derived from M1 and M3 feed a concentration-level (kinetic) layer.
- Gates: measured rate constants and equilibrium constants.

## M5: self-assembly

- Coarse-grained beads derived from atomistic runs (force matching or iterative
  Boltzmann inversion).
- Amphiphiles forming micelles and membranes by themselves.
- Gates: experimental critical micelle concentration or bilayer thickness.

## M6: a joint into a cell model

- Take an open whole-cell model, such as the JCVI-syn3A minimal-cell models.
- Replace a subset of its experimentally measured parameters with groundup-derived ones.
- Measure how far the cell-level prediction moves. This is the first time a
  derived rule would reach biology.

Milestones beyond M1b are a direction, not a promise. Their order will change as
we learn where the joints break.
