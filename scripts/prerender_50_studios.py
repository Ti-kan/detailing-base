#!/usr/bin/env python3
import subprocess, sys

if __name__ == "__main__":
    res = subprocess.run([sys.executable, "/Users/takanov/detailing-base/scripts/build_landing.py"])
    sys.exit(res.returncode)
