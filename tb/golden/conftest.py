# tb/golden/conftest.py
# Makes `import params` / `import primitives` work from tb/golden/tests/
# without turning tb/golden into a package (params.py, primitives.py stay
# plain modules, as required by mlkem-guard's check_params.py, which reads
# tb/golden/params.py directly).
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
