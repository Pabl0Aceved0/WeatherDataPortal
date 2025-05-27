import sys
import os
from waitress import serve

# Ensure src is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app

def main():
    if '--prod' in sys.argv:
        print('Starting with Waitress (production mode) on http://localhost:8080')
        serve(app, host='0.0.0.0', port=8080)
    else:
        print('Starting Flask development server on http://localhost:8080')
        app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
