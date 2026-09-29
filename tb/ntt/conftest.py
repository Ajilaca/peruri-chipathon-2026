# tb/ntt/conftest.py
# Makes `import params` / `import primitives` (the golden model) available from cocotb test
# modules under tb/ntt/, the same way tb/golden/conftest.py does for tb/golden/tests/.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))
