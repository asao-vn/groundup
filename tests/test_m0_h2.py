"""End-to-end milestone M0. Runs real quantum chemistry: ``pytest -m slow``."""

import pytest

pytest.importorskip("pyscf")

from groundup.pipelines.m0_h2 import run


@pytest.mark.slow
def test_m0_h2_passes_all_gates(tmp_path):
    result = run(out_path=tmp_path / "m0.json", log=lambda _msg: None)
    failed = [c["name"] for c in result["checks"] if c["kind"] == "gate" and not c["passed"]]
    assert not failed, f"gates failed: {failed}"
    assert (tmp_path / "m0.json").exists()
    assert result["derived_rule"]["provenance"]["source_method"] == "FCI/cc-pvtz"
