"""
run.py — One-command setup and launch script.

Usage:
    python run.py

This will:
  1. Install required packages (if missing)
  2. Train ML models (if not already trained)
  3. Run database migrations
  4. Start the Django development server
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def step(msg):
    print(f"\n{'='*60}\n  {msg}\n{'='*60}")


def run(cmd, check=True):
    """Run a shell command and stream output."""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0


def check_python():
    if sys.version_info < (3, 10):
        print(f"⚠  Python {sys.version_info.major}.{sys.version_info.minor} detected.")
        print("   This project requires Python 3.10 or newer.")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} OK")


def install_deps():
    step("Installing dependencies")
    try:
        import django  # noqa
        import sklearn  # noqa
        import pandas  # noqa
        print("✓ All dependencies already installed")
    except ImportError:
        run(f'"{sys.executable}" -m pip install -r requirements.txt')


def train_models():
    step("Training ML models")
    saved = BASE_DIR / 'dashboard' / 'ml' / 'saved_models'
    if (saved / 'ctr_model.pkl').exists() and (saved / 'cvr_model.pkl').exists():
        print("✓ Models already trained — skipping. Delete .pkl files to retrain.")
        return
    run(f'"{sys.executable}" dashboard/ml/train_model.py')


def setup_db():
    step("Setting up database")
    run(f'"{sys.executable}" manage.py makemigrations dashboard', check=False)
    run(f'"{sys.executable}" manage.py migrate')


def start_server():
    step("Starting Django server at http://127.0.0.1:8000")
    print("Press CTRL+C to stop.\n")
    run(f'"{sys.executable}" manage.py runserver')


if __name__ == '__main__':
    os.chdir(BASE_DIR)
    print("\n  Social Media Ad Performance Prediction System")
    print("  ============================================\n")
    check_python()
    install_deps()
    train_models()
    setup_db()
    start_server()
