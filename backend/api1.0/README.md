# Project README

## Installation

1. Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-project.git
Navigate to the project directory:

bash
Copy code
cd your-project
Create a virtual environment (optional but recommended):

bash
Copy code
python3 -m venv venv
Activate the virtual environment:

bash
Copy code
source venv/bin/activate
Install project dependencies from requirements.txt:

bash
Copy code
pip install -r requirements.txt
Folder Structure
The project follows the following folder structure:

bash
Copy code
your-project/
│
├── app.py             # Main Flask application
│
├── routes/            # Route modules
│   ├── search.py      # Search endpoint implementation
│   ├── forecast.py    # Forecast endpoint implementation
│   ├── portfolio.py   # Portfolio endpoint implementation
│   └── persist.py     # Persist endpoint implementation
│
├── tests/             # Test cases
│   └── test_search.py # Example test case for the search endpoint
└── requirements.txt   # List of project dependencies

Running Tests
To run tests with the pytest command, you can set up an alias for pytest with the following command:

bash
Copy code
alias pytest='python3 -m pytest'
After setting up the alias, you can run tests as follows:

bash
Copy code
pytest --capture=no
The --capture=no option is used to prevent pytest from capturing and suppressing the standard output, allowing you to see any print statements or pretty-printed JSON responses during test execution.

That's it! You've successfully installed the project, understand its folder structure, and know how to run tests using pytest.


## Running with docker

Navigate to backend/api1.0/finapp

Go to .env and configure desired values.

docker build -t ww-backend .

docker run -p 5000:5000 ww-backend

API will run at http://localhost:5000/


