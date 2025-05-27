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
    Create a `.env` file in the project directory and paste your personal Windy API tokens:
    ```properties
    WINDY_API_TOKEN_MAP=<your_map_token>
    WINDY_API_TOKEN_POINT=<your_point_token>
    WINDY_API_TOKEN_WEBCAMS=<your_webcams_token>
    ```
    Replace `<your_map_token>`, `<your_point_token>`, and `<your_webcams_token>` with your actual API tokens.

3.  **Run the setup script:**
    Open PowerShell, navigate to the project directory, and run:
    ```powershell
    .\restart_env.ps1
    ```
    This script will:
    *   Create a Python virtual environment in a `.venv` folder (if it doesn't exist).
    *   Activate the virtual environment.
    *   Install required Python packages from `requirements.txt` (Flask, Waitress).
    *   Start the web server using Waitress, making the site available at `http://localhost:8080`.

4.  **Access the site:**
    Open your web browser and go to `http://localhost:8080`.

5.  **To stop the server:**
    Press `CTRL+C` in the PowerShell window where `restart_env.ps1` is running.

## Files

*   `app.py`: The main Flask application that fetches weather data and serves routes.
*   `config.py`: Handles loading environment variables and API tokens.
*   `index.html`: The main HTML page that embeds the Windy.com map.
*   `serve_protected.py`: The Flask application that serves `index.html`.
*   `requirements.txt`: Lists the Python dependencies (Flask, Waitress).
*   `restart_env.ps1`: PowerShell script to automate setup and server launch.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.

## API Key

The Windy.com map embed in `index.html` uses an API key. If you have your own key, you can replace the existing one in the `iframe`'s `src` attribute in `index.html`.

## Legacy Files (Not actively used by the current setup)

*   `windy_map.html`
*   `generate_cert.py`
*   `localhost.crt`
*   `localhost.key`
*   `gunicorn_config.py`
*   `windy_point_forecast.py`

These files were part of previous development iterations and are not required for the current simple embedded map functionality. They can be removed or kept for reference.
