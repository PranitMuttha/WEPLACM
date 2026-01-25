# Python Worker

## 1. Create a virtual environment
With [virtualenv](https://virtualenv.pypa.io/en/latest/):
```
virtualenv venv && source venv/bin/activate
python -m pip install -r requirements.txt
```

or with [uv](https://github.com/astral-sh/uv):
```
uv venv
uv pip install -r requirements.txt
```

## 2. Run the scripts
Example for a client: just starts the demo process
```
python client.py
# OR uv:
uv run client.py
```

Start the worker for the demo process. When a process instance reaches the *Calculation of mood* task (**MoodCalculator** job type), the worker executes the defined function.
```
python worker.py 
# OR uv:
uv run worker.py
```

