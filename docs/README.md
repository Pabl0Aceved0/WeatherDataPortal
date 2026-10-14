# WeatherData Portal

A simple web application to display weather data and Windy.com map embeds.

## Setup and Run

This project uses Python and Flask, served by Waitress.

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd WeatherData # Or your repository folder name
    ```

2.  **Configure API Tokens:**
    Copy `.env.example` to `.env` (it is git-ignored; never commit it) and add your personal Windy API tokens:
    ```properties
    WINDY_API_TOKEN_MAP=<your_map_token>
    WINDY_API_TOKEN_POINT=<your_point_token>
    WINDY_API_TOKEN_WEBCAMS=<your_webcams_token>
    ```
    Replace `<your_map_token>`, `<your_point_token>`, and `<your_webcams_token>` with your actual API tokens.

3.  **Run the setup script:**
    Open PowerShell, navigate to the project directory, and run:
    ```powershell
    .\scripts\restart_env.ps1
    ```
    This script will:
    *   Create a Python virtual environment in a `.venv` folder (if it doesn't exist).
    *   Activate the virtual environment.
    *   Install the Python packages from `requirements.txt`.
    *   Start the web server using Waitress, making the site available at `http://localhost:8080`.

4.  **Access the site:**
    Open your web browser and go to `http://localhost:8080`.

5.  **To stop the server:**
    Press `CTRL+C` in the PowerShell window where `scripts\restart_env.ps1` is running.

## Files

*   `src/app.py`: The main Flask application that fetches weather data and serves routes.
*   `src/config.py`: Single place where environment variables and API tokens are loaded (values are never logged).
*   `src/serve_protected.py`: Minimal Flask app that serves `static/index.html`.
*   `run.py`: Local entry point (`python run.py`, or `--prod` for Waitress).
*   `static/`: HTML pages, PWA manifest and service worker.
*   `requirements.txt`: Python dependencies (`tests/requirements.txt` adds pytest).
*   `.env.example`: Template for the local `.env` file.
*   `scripts/restart_env.ps1`: PowerShell script to automate setup and server launch.
*   `tests/`: Pytest suite (run `pytest`).

## API Key

The Windy.com map embed in `index.html` uses an API key. If you have your own key, you can replace the existing one in the `iframe`'s `src` attribute in `index.html`.

## Legacy Files (Not actively used by the current setup)

*   `static/windy_map.html`
*   `scripts/generate_cert.py`
*   `scripts/windy_embed_snippet.py`
