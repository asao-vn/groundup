# Principles

groundup exists to test one idea: **a higher layer of nature can run on rules
derived from the layer below, with nothing typed in by hand.** These rules keep
the project honest about whether that idea works.

## 1. Only layer 0 is written by hand

Layer 0 is established physics (the Schrödinger equation for electrons and
nuclei), solved by established solvers (PySCF). It is the only place where
physics enters. Nothing at layer 0 is fitted to experiment.

## 2. Every rule above layer 0 is derived

A bond potential, a force field, a reaction rate, a coarse-grained bead: each
must be produced by code from the output of the layer below. A derived rule is
never a number copied from a paper or a table.

## 3. Every derived rule carries provenance

Each rule records where it came from: the source layer, the method, the inputs,
and the procedure (`groundup.provenance.Provenance`). Results are written as
JSON so any number can be traced back to the layer-0 calculation that produced it.

## 4. Every joint records what it loses

Deriving a simpler rule always throws information away. The residual of the
rule against its source data is part of the provenance. Known limitations are
recorded as `info` checks next to the passing ones. Hiding a loss is worse than
failing a check.

## 5. Validate against experiment, never against yourself

Every milestone ends with `gate` checks that compare predictions with measured
values from a cited source. Agreement with another simulation does not count as
validation; it only counts as a consistency check between layers.

## 6. Integrate, don't reinvent

Quantum chemistry, molecular dynamics and machine-learned potentials already
have excellent open-source tools. groundup's own value is the joints between
layers, the provenance, and the validation. Use existing solvers wherever they fit.

## 7. Honest scope

Simulating a living cell atom by atom is out of reach for any computer that
exists. groundup does not claim otherwise. The goal is to push the point where
rules stop being derived and start being typed in, one joint at a time.
