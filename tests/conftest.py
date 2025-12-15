import os
import sys

# Ensure the project root (where `src/` lives) is on sys.path so that
# `import src.*` works regardless of how pytest is invoked.
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
