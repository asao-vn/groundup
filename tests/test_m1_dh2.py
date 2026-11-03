"""End-to-end milestone M1. Runs real quantum chemistry: ``pytest -m slow``."""

import pytest

pytest.importorskip("pyscf")

from groundup.pipelines.m1_dh2 import run


@pytest.mark.slow
def test_m1_dh2_passes_all_gates(tmp_path):
    result = run(out_path=tmp_path / "m1.json", log=lambda _msg: None)
    failed = [c["name"] for c in result["checks"] if c["kind"] == "gate" and not c["passed"]]
    assert not failed, f"gates failed: {failed}"
    assert result["layer1"]["threshold_ev"] is not None
    assert result["reactive_rule"]["provenance"]["source_method"] == "FCI/cc-pvtz"
