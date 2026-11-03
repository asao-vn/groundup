# Vision: the missing middle

## The question

Can a higher layer of nature run on rules that were *derived* from the layer
below, instead of rules typed in from experiment?

In principle, yes. In 1929 Dirac wrote that "the underlying physical laws
necessary for the mathematical theory of a large part of physics and the whole
of chemistry are thus completely known, and the difficulty is only that the
exact application of these laws leads to equations much too complicated to be
soluble" ([Dirac 1929](references.md#dirac1929)). Chemistry is electrons and
nuclei obeying quantum mechanics, and no extra "life force" has ever been needed
to explain biology. So the rules at the bottom should be enough.

In practice, nobody has carried a simulation from those rules all the way to a
living cell. groundup is an attempt to push that chain forward one link at a time.

## What has been done

| Work | Year | What it achieved | Do higher rules emerge from lower ones? |
|---|---|---|---|
| Wöhler synthesises urea ([Wöhler 1828](references.md#wohler1828)) | 1828 | A biological molecule made from inorganic chemicals | In the lab |
| Miller–Urey experiment ([Miller 1953](references.md#miller1953)) | 1953 | Amino acids formed from simple gases and electric sparks | In the lab |
| Light hadron masses from QCD ([Dürr et al. 2008](references.md#durr2008)) | 2008 | Proton mass computed from quarks and gluons | Yes, particles to nucleons |
| Synthetic genome ([Gibson et al. 2010](references.md#gibson2010)); minimal genome ([Hutchison et al. 2016](references.md#hutchison2016)) | 2010, 2016 | A cell run by a chemically synthesised genome; a 473-gene minimal cell | No: an existing cell's machinery was reused |
| Ab initio nanoreactor ([Wang et al. 2014](references.md#wang2014)) | 2014 | Quantum dynamics alone found reaction routes to glycine, with no preset reaction steps | **Yes, physics to chemistry**, but thousands of atoms for nanoseconds |
| ML potentials for prebiotic chemistry ([Saitta group](references.md#saitta2026)) | 2025–26 | Near-quantum accuracy for prebiotic reaction pathways, microsecond reactive sampling | Yes, a few reactions at a time |
| Martini model of a whole minimal cell ([Stevens et al. 2023](references.md#stevens2023)) | 2023 | JCVI-syn3A built as 561 million coarse-grained beads (~6 billion atoms) | Model built; no completed full-cell run found |
| Whole cell cycle in 4D ([Thornburg et al. 2026](references.md#thornburg2026)) | 2026 | A minimal cell grows, replicates DNA and divides; the ~105-minute cycle runs in about six days of GPU time | **No**: reaction rates come from experiment |
| Emergent self-replicators ([Agüera y Arcas et al. 2024](references.md#aguera2024)) | 2024 | Self-replicating programs arise from random ones with no fitness goal | Yes, but the "physics" is machine code, not chemistry |
| AI virtual cells ([Arc Institute, CZI](references.md#virtualcell2025)) | 2025 | Models trained on hundreds of millions of real cells predict responses to perturbations | No: learned from data, not from physical law |

## The gap

The field is advancing from two ends that have not met:

- **From the bottom:** the nanoreactor uses real physical law and chemistry
  emerges, but only for tiny systems over nanoseconds.
- **From the top:** the 2026 whole-cell model has a living cell over its whole
  life, but its biochemical rules are measured in the lab and typed in.

The missing middle is a single chain where higher-level rules are produced
automatically from lower-level ones, with a record of what each step loses.

## What groundup does about it

groundup does not try to simulate a cell atom by atom; see
[Concepts](concepts.md) for why that is out of reach. Instead it builds the
**joints**:

1. Solve a layer with established physics.
2. Derive the next layer's rules from it by code, with provenance.
3. Run the next layer on those rules only.
4. Check both against experiment, and record what was lost.

The first joint (quantum to classical atoms, for H2) is
[milestone M0](milestones/m0-h2.md). The [roadmap](roadmap.md) works upward
from there, towards the point where a derived rule can replace a measured one
inside a real cell model.
