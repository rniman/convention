"""Build the wiki, or run a live local preview with --serve."""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true", help="Run a live preview")
    args = parser.parse_args()
    command = [sys.executable, "-m", "mkdocs"]
    if args.serve:
        command += ["serve", "--dev-addr", "127.0.0.1:8000"]
    else:
        command += ["build", "--strict"]
    return subprocess.call(command, cwd=Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    sys.exit(main())
