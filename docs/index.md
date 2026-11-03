# groundup

**Simulate nature layer by layer, where every layer above the bottom runs only
on rules derived from the layer below.**

groundup is an open-source research project by [ASAO](https://asao.vn).
[Tiếng Việt](vi/index.md)

Physics, chemistry and biology are usually simulated with separate models, and
each higher level's rules are typed in from experiments. groundup writes the
physics once at the bottom and *derives* each higher layer's rules by code. Every
derived rule records where it came from and what it lost, and every layer is
checked against experiment.

## Where to start

- [Vision](vision.md): what has been done, and the gap groundup works on
- [Concepts](concepts.md): layers, emergence, and why a cell cannot be simulated atom by atom
- [M0: H2 from the ground up](milestones/m0-h2.md): the first joint, with results
- [M1: D + H2 → HD + H](milestones/m1-dh2.md): the first reaction, bonds breaking and forming by themselves
- [Principles](principles.md): the rules that keep the project honest
- [Roadmap](roadmap.md): next is M1b, counting reactive trajectories in 3D
- [References](references.md): every source these pages draw on

## Status

| Milestone | Joint | Status |
|---|---|---|
| [M0](milestones/m0-h2.md) | exact quantum H2 → derived bond rule → classical atoms | passed, within ~1% of NIST |
| [M1](milestones/m1-dh2.md) | exact H3 → reactive rule → collisions → rate constant | passed, k(T) within a factor of 1.21 of experiment |
| M1b | the same rule → 3D thermal trajectories → counted rate constant | next |
