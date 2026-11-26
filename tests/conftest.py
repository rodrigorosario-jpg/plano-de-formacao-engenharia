import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))


@pytest.fixture
def disc_min():
    base = {"semestre_inicio": 0, "semestre_fim": 0, "status": "nao_iniciada", "horas_previstas": 10}
    return {
        "XA1": {**base, "codigo": "XA1", "prerequisitos": []},
        "XA2": {**base, "codigo": "XA2", "prerequisitos": ["XA1"]},
    }
