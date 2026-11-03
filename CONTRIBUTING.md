# Contributing

Thanks for helping. groundup is small and early, so the rules are short.

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest            # fast tests (seconds)
.venv/bin/pytest -m slow    # end-to-end milestones (minutes, real quantum chemistry)
.venv/bin/ruff check src tests
```

## What a change must include

Read [docs/principles.md](docs/principles.md) first. In practice:

1. **A new rule above layer 0 must be derived by code**, with a `Provenance`
   that records its source, inputs, procedure and residuals.
2. **A new milestone needs gate checks against experiment**, each with a cited
   source in `groundup/reference.py` (a URL or a paper).
3. **Known limitations are recorded**, as `info` checks or in the provenance.
4. **Tests**: a fast unit test for each new function, and a `@pytest.mark.slow`
   end-to-end test for each milestone.
5. **Run the milestones locally before pushing** (`.venv/bin/pytest -m slow`)
   and say in the PR that they passed. CI runs only the fast tests and the docs
   build on every push. The milestones take many minutes of real quantum
   chemistry, so CI runs them only when started by hand (Actions → ci → Run
   workflow).

## Documentation and citations

The pages in `docs/` are the source of the project website (MkDocs).

- Every fact taken from someone else's work must be cited, even background
  material. Add the source to `docs/references.md` with an anchor, a DOI or URL,
  and a "Used for" line, then link to it from the page.
- Check DOIs against [Crossref](https://api.crossref.org) before adding them.
- If you only read a source through news coverage or a summary, mark it
  *secondary*.
- Mark groundup's own estimates as such, with their assumptions.
- Build the site locally before opening a PR:

```bash
.venv/bin/pip install -e '.[docs]'
.venv/bin/mkdocs build --strict    # or: mkdocs serve
```

## Units

Inside the code everything is in Hartree atomic units. Convert only in reports
and when comparing with experiment, using `groundup/units.py`.

## Discussions

Open an issue before starting a new milestone or layer. The roadmap order is
open to debate, and the joints are where the interesting arguments are.
