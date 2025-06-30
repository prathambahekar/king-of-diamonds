import sys
import os

# Ensure the backend directory is a package and in the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import app

if __name__ == "__main__":
    app.run(debug=True) 