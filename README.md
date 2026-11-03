# groundup

**Simulate nature layer by layer, where every layer above the bottom runs only on
rules derived from the layer below.**

An open-source research project by [ASAO](https://asao.vn).

Physics, chemistry and biology are usually simulated with separate models, and
the rules of each higher level are typed in by hand from experiments. groundup
explores the opposite: write the physics once at the bottom, then *derive* each
higher layer's rules by code. Each derived rule records where it came from and
what it lost, and each layer is checked against experiment.

## Why

Today the field advances from two ends that have not met:

- **Bottom up:** the *ab initio nanoreactor*
  ([Wang et al., Nature Chemistry 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239668))
  started from quantum mechanics alone and found reaction pathways to glycine
  that nobody programmed. It covers thousands of atoms for nanoseconds.
- **Top down:** the first simulation of a whole cell cycle
  ([Thornburg et al., Cell 2026](https://www.jcvi.org/publications/bringing-genetically-minimal-cell-life-computer-4d))
  runs a living minimal cell. Its biochemical rates are measured in the lab and typed in.

The gap in between is a chain where higher rules come from lower ones
automatically. groundup builds that chain one joint at a time, starting from
the simplest molecule there is.

## Milestone M0: H2 from the ground up

```
layer 0   quantum     exact Schrödinger solution for H2 (full CI, PySCF)
   │                  → potential energy curve; no empirical input
bridge    derive      Morse bond rule extracted from that curve
   │                  → with provenance and residuals
layer 1   classical   two atoms obeying Newton's law + the derived rule
   │
validate              predictions vs NIST experimental data
```

```bash
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m groundup m0        # ~15 s on a laptop
```

Result (FCI/cc-pVTZ):

| | check | groundup | experiment (NIST) | error |
|---|---|---|---|---|
| PASS | bond length r_e | 0.7426 Å | 0.7414 Å | +0.16% |
| PASS | harmonic frequency ω_e | 4411.1 cm⁻¹ | 4401.2 cm⁻¹ | +0.22% |
| PASS | dissociation energy D_0 | 4.430 eV | 4.478 eV | −1.06% |
| PASS | fundamental G(1)−G(0) | 4154.4 cm⁻¹ | 4158.5 cm⁻¹ | −0.10% |
| PASS | layer-1 MD frequency = layer-0 ω_e | 4410.9 cm⁻¹ | 4411.1 cm⁻¹ | −0.00% |
| INFO | anharmonicity ω_e x_e | 128.3 cm⁻¹ | 121.3 cm⁻¹ | +5.8% |
| INFO | classical MD frequency vs fundamental | 4410.9 cm⁻¹ | 4158.5 cm⁻¹ | +6.1% |

The two `INFO` rows are losses we record on purpose. The Morse shape only
approximates the true curve, and classical atoms have no zero-point motion.
Every number is written to `results/m0_h2.json` with its full provenance.

## Layout

```
src/groundup/
  quantum.py      layer 0: exact quantum chemistry (PySCF)
  bridge.py       derive layer-1 rules from layer-0 data
  classical.py    layer 1: classical atoms (velocity Verlet)
  provenance.py   the record every derived rule carries
  validate.py     checks against experiment
  reference.py    experimental data, each value with its source
  pipelines/      one end-to-end chain per milestone
```

## Documentation

The `docs/` folder is the source of the project website. Every outside fact in
it is cited in [docs/references.md](docs/references.md).

- [Vision](docs/vision.md): what has been done, and the gap groundup works on
- [Concepts](docs/concepts.md): layers, emergence, and why a cell cannot be simulated atom by atom
- [M0 in detail](docs/milestones/m0-h2.md): method, results, losses, limitations
- [Principles](docs/principles.md): the rules that keep the project honest
- [Roadmap](docs/roadmap.md): next is M1, the first reaction (H + H2 → H2 + H)
- [Contributing](CONTRIBUTING.md)

Build the site locally:

```bash
.venv/bin/pip install -e '.[docs]'
.venv/bin/mkdocs serve
```

## Tóm tắt tiếng Việt

groundup là dự án nghiên cứu mã nguồn mở của ASAO. Bản đầy đủ:
[docs/vi/index.md](docs/vi/index.md).

groundup mô phỏng tự nhiên theo từng tầng. Chỉ tầng dưới cùng (cơ học lượng tử)
được viết tay. Luật của mọi tầng phía trên đều do máy **tự rút ra** từ tầng
dưới, kèm hồ sơ nguồn gốc và phần thông tin bị mất. Mỗi tầng được kiểm chứng với
số đo thực nghiệm. Bước đầu (M0): giải chính xác phân tử H₂, tự rút ra luật liên
kết, rồi cho hai nguyên tử chuyển động theo luật đó. Kết quả khớp số đo của NIST
trong khoảng 1%.

## License

[Apache-2.0](LICENSE)
