# Movie Search
Project made with React for the frontend and Python/Flask for the backend

## Installation

npm and python are needed to run this project

Install the necessary modules for the backend (full instructions [here](https://flask.palletsprojects.com/en/2.2.x/installation/))
Make sure that your version of pip is recent, I had troubles installing pandas until I upgraded pip
```bash
cd backend
# Create an environment if needed, and activate it
python3 -m venv venv
. venv/bin/activate
# Install the libraries
pip install Flask
pip install pandas
pip install pytest
```

Install the necessary modules for the frontend
```bash
cd frontend
npm install
```

## Tests

You can run the unit tests using:
```bash
# In /backend
pytest
```

## Usage

Now you can start the webapp
First, start the backend
```bash
cd backend
flask --app lib/app run
```

When the backend is running, you can start the frontend
```bash
cd frontend
npm start
```

Now you can go to localhost:3000 and see the app working

## Note

The app is definitely not optimized, I focused on making the app work and tried to not lose time on optimization. If I had more time, I would make it faster and more complete.
I also know that I didn't take the time to add unit tests. I'll do if I get more time alloted.