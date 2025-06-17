# SMS Capstone Project

This project is a web application built with a React frontend, a Python (FastAPI) backend, and a PostgreSQL database.

## Technology Stack

* **Backend:** FastAPI (Python)
* **Frontend:** React (JavaScript)
* **Database:** PostgreSQL
* **Containerization:** Docker

---

## Prerequisites

Before you begin, make sure you have the following installed on your system:

* **Git:** To clone the repository.
* **Python 3.8+:** For the backend.
* **Node.js and npm // React:** For the frontend.
* **Docker Desktop:** To run the PostgreSQL database. Make sure it is running before you start.
* **A Code Editor:** I recommend [Visual Studio Code](https://code.visualstudio.com/).

---

## Environment Setup

Follow these steps in order to get your development environment up and running.

### 1. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone <your-repository-ssh-or-https-url>
cd sms-capstone
```

### 2. Start the Database with Docker

Our project uses Docker to ensure everyone has the same database setup without needing to install PostgreSQL locally.

* Make sure Docker Desktop is open and running on your machine.
* In the root directory of the project (`sms-capstone`), run the following command:

```bash
docker-compose up -d
```

This will start the PostgreSQL database server in the background. The `-d` flag stands for "detached mode".

### 3. Set Up the Backend (FastAPI)

Next, let's get the Python backend server running.

1.  **Create and Activate Virtual Environment:**
    * We will use the `venv` folder in the project root. To activate it, run the correct command for your operating system from the **project's root directory**.

    ```bash
    # For Windows Users (in Git Bash)
    source venv/Scripts/activate

    # For macOS / Linux Users
    source venv/bin/activate
    ```

    *You should now see `(venv)` at the beginning of your terminal prompt.*

2.  **Install Python Dependencies:**
    * Navigate to the backend folder and install the required packages from the `requirements.txt` file.

    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Run the Backend Server:**
    * While still in the `backend` directory, start the FastAPI server.

    ```bash
    uvicorn main:app --reload
    ```

4.  **Verify Backend is Running:**
    * Open your web browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs). You should see the interactive FastAPI documentation page.

### 4. Set Up the Frontend (React)

Finally, let's get the React frontend running. **Open a new, separate terminal window for this part.**

1.  **Navigate to the Frontend Directory:**
    * In your **new terminal**, navigate into the `frontend` folder from the project root.

    ```bash
    cd frontend
    ```

2.  **Install Node.js Dependencies:**
    * Install all the required packages defined in `package.json`.

    ```bash
    npm install
    ```

3.  **Run the Frontend Development Server:**
    * Start the React application.

    ```bash
    npm start
    ```

4.  **Verify Frontend is Running:**
    * Your web browser should automatically open a new tab to [http://localhost:3000](http://localhost:3000). You should see the React application.

---

## Done

I would also suggest to use DBeaver when working in the database for clarity but up to you. 

You now have the full development environment running:

* **PostgreSQL Database** on port `5432`
* **FastAPI Backend** on [http://localhost:8000](http://localhost:8000)
* **React Frontend** on [http://localhost:3000](http://localhost:3000)
