# Concepts

## Layers

Ordinary matter is built in layers. Each layer uses the one below as its
alphabet:

| Layer | Building blocks | Number of possibilities |
|---|---|---|
| Fundamental particles | up quark, down quark, electron (plus the forces between them) | 3 kinds of matter particle |
| Nuclei and atoms | protons and neutrons (made of quarks), electrons | 118 known elements |
| Molecules | atoms | an estimated ~10⁶⁰ drug-like molecules alone ([Bohacek et al. 1996](references.md#bohacek1996)) |
| Proteins | 20 amino acids in a chain | 20¹⁰⁰ ≈ 10¹³⁰ sequences for a chain of length 100 |
| Genomes | 4 bases (A, C, G, T) | the human genome is ~3.06 billion bases long ([Nurk et al. 2022](references.md#nurk2022)) |

The number of possible structures grows exponentially at every step. For
comparison, the observable universe is usually estimated to hold about 10⁸⁰
atoms, far fewer than the number of possible proteins of length 100.

## Structure matters more than ingredients

The same atoms arranged differently give different matter. Diamond and graphite
are both pure carbon. Ethanol and dimethyl ether have the same formula, C₂H₆O,
but one is a drinkable liquid and the other a gas. A simulation that only
counted ingredients would miss everything that makes them different.

## Emergence: "more is different"

Anderson argued that each level of organisation has properties and laws of its
own, which are consistent with the level below but not obvious from it
([Anderson 1972](references.md#anderson1972)). A single water molecule is not
wet. A single atom is not alive. Wetness and life appear only in large
assemblies, and each layer is best described by rules that fit that layer.

This is why groundup derives a *new* rule at each joint instead of carrying the
full lower-level description upward: the higher layer needs a simpler rule that
keeps what matters at its own scale.

## Why not simulate a cell atom by atom?

Two walls stand in the way.

**1. Exact quantum mechanics grows exponentially.** Representing the exact
quantum state of many interacting particles takes resources that grow
exponentially with their number, so exact simulation on classical computers
stops at very small systems ([Feynman 1982](references.md#feynman1982);
[Helgaker et al. 2000](references.md#helgaker2000)). That is why M0 can solve
H2 exactly, while larger molecules will need approximate methods.

**2. Time scales.** Atoms vibrate on femtosecond time scales, so molecular
dynamics steps are about a femtosecond long
([Frenkel & Smit 2023](references.md#frenkel2023)). A rough estimate for the
smallest known free-living cell:

- JCVI-syn3A is about 6 × 10⁹ atoms ([Stevens et al. 2023](references.md#stevens2023)).
- One second of its life at 1 fs per step is 10¹⁵ steps, so about 6 × 10²⁴ atom-steps.
- *Assume* a machine that sustains 10¹² atom-steps per second, which is generous
  for classical force fields today.
- One simulated second then takes about 6 × 10¹² s, roughly 200,000 years.
  The whole ~105-minute cell cycle ([Thornburg et al. 2026](references.md#thornburg2026))
  would take over a billion years.

This estimate is groundup's own. It uses classical force fields, which cannot
break or form chemical bonds; reactive or quantum-accurate dynamics cost
several orders of magnitude more.

## The accuracy, size and time triangle

Every simulation today chooses two of three:

- **Accurate physics + small size + short time:** the nanoreactor
  ([Wang et al. 2014](references.md#wang2014)). Real chemistry emerges, for nanoseconds.
- **Large size + long time + simplified rules:** whole-cell kinetic models
  ([Thornburg et al. 2026](references.md#thornburg2026)) or artificial life
  ([Agüera y Arcas et al. 2024](references.md#aguera2024)). Life-like
  behaviour, but the rules are given rather than derived.

groundup does not try to break the triangle. It tries to connect its corners:
each joint carries a rule from an accurate, small layer to a larger, simpler one,
so that fewer rules have to be typed in by hand.
