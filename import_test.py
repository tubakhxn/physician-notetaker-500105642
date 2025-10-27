import traceback
import sys

try:
    import nlp_pipeline as np
    print("IMPORTED OK")
    names = [n for n in dir(np) if not n.startswith("__")]
    print(names)
except Exception:
    traceback.print_exc()
    sys.exit(1)
