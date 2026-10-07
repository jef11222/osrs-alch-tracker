import os
import sys

# Ensure current directory is on python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from gui import OSRSAlchDashboard

def main():
    app = OSRSAlchDashboard()
    app.mainloop()

if __name__ == "__main__":
    main()
