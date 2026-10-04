"""Academic Harness foundation with the retained ARIS literature runtime."""

from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = REPOSITORY_ROOT / "vendor" / "aris"
sys.path.insert(0, str(VENDOR_ROOT))
