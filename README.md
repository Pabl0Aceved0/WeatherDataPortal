# WeatherData Portal

A simple web application to display a Windy.com map embed.

## Setup and Run

This project uses Python and Flask, served by Waitress.

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd WeatherData # Or your repository folder name
    ```

2.  **Run the setup script:**
    Open PowerShell, navigate to the project directory, and run:
    ```powershell
    .\restart_env.ps1
    ```
    This script will:
    *   Create a Python virtual environment in a `.venv` folder (if it doesn't exist).
    *   Activate the virtual environment.
    *   Install required Python packages from `requirements.txt` (Flask, Waitress).
    *   Start the web server using Waitress, making the site available at `http://localhost:8080`.

3.  **Access the site:**
    Open your web browser and go to `http://localhost:8080`.

4.  **To stop the server:**
    Press `CTRL+C` in the PowerShell window where `restart_env.ps1` is running.

## Files

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
