Deadlock Prevention & Recovery Toolkit

Overview

The Deadlock Prevention & Recovery Toolkit is a web-based application that helps analyze system states, detect deadlocks, and determine safe execution sequences using the Banker's Algorithm and Resource Allocation Graph. This project is built using Flask for the backend and HTML, Tailwind CSS, and JavaScript for the frontend.

Features

🛠 Deadlock Detection: Identifies cycles in the resource allocation graph.

✅ Safe State Analysis: Determines if the system is in a safe state.

🔢 Banker's Algorithm Implementation: Computes the safe execution sequence.

🎨 Modern UI: Designed with Tailwind CSS and animated elements.

Technologies Used

Backend: Flask (Python), NetworkX (for graph-based deadlock detection), NumPy.

Frontend: HTML, Tailwind CSS, JavaScript.

Communication: Fetch API (for backend interaction).

Setup Instructions

1. Clone the Repository

git clone https://github.com/yourusername/os-project.git
cd os-project

2. Create & Activate Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Run the Flask Server

python app.py

The server will start at http://127.0.0.1:5000/.

5. Open the Frontend

Open index.html in a browser or run a local web server:

python -m http.server 8000  # Then visit http://127.0.0.1:8000/

API Endpoints

/simulate (POST)

Request Body (JSON):

{
  "processes": ["P0", "P1", "P2"],
  "resources": ["A", "B", "C"],
  "allocation": [[0, 1, 0], [2, 0, 0], [3, 0, 2]],
  "max_demand": [[7, 5, 3], [3, 2, 2], [9, 0, 2]],
  "available": [3, 3, 2]
}

Response:

{
  "safe_state": true,
  "safe_sequence": ["P1", "P3", "P0"],
  "deadlock_detected": false,
  "deadlock_cycle": []
}

Contributing

Fork the repository

Create a new branch: git checkout -b feature-branch

Commit your changes: git commit -m "Add new feature"

Push and create a PR

