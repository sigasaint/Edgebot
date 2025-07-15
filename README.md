# EdgeBot MK-II Flask Web App

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask app:
   ```bash
   python run.py
   ```

3. Open your browser and go to [http://localhost:5000](http://localhost:5000)

## Project Structure

- `app/` — Flask app code
  - `templates/` — HTML templates
  - `static/` — Static files (images, CSS, etc.)
  - `routes.py` — All backend routes
  - `__init__.py` — App factory
- `run.py` — App entry point
- `requirements.txt` — Python dependencies

## Notes
- All static assets (images, firmware, zips) are served from the `static/` folder.
- All HTML pages use Bootstrap 5 for a modern, responsive look.
- Dark mode is available on all pages. 