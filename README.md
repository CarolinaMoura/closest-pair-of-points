# Closest pair of points
## Running locally
### Create a virtual environment

    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt

### Run the code
    python3 interface.py

## The app
You may resize the window for bigger area.

The app runs the closest pair of points algorithm in $O(n \, log \, n)$. It highlights in grey every comparison it makes and highlights in green every comparison that updates the current minimum answer. You may check the console output for comparison with the quadratic case.
