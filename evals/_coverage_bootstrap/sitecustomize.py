"""Bootstrap coverage dans chaque subprocess Python.

Python auto-execute `sitecustomize.py` a l'import de `site` si un fichier de ce
nom est trouvable dans sys.path. On l'utilise pour initialiser coverage.py dans
tous les subprocess Python spawnes par les tests, pour tracer les scripts du
bundle appeles par evals/_helpers/*.

Active uniquement si COVERAGE_PROCESS_START est defini (pointe vers .coveragerc).
Sans cette env var, ce fichier est un no-op.
"""

import os

if os.environ.get("COVERAGE_PROCESS_START"):
    try:
        import coverage
        coverage.process_startup()
    except ImportError:
        pass
