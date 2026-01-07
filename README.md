# TSV Form Generator

This project generates a PDF membership form for the TSV Berlin-Wedding 1862 e.V. sports club. It uses Python and ReportLab to create a high-quality, printable, and fillable PDF document.

## Features

*   **PDF Generation**: Creates a standardized membership form `tsv.pdf`.
*   **Custom Typography**: Uses OpenSans fonts for consistent branding.
*   **SVG Support**: Embeds the club logo from an SVG source.
*   **Dynamic Layout**: Uses ReportLab's Platypus engine for flowable layout of text, tables, and form fields.

## Prerequisites

*   Python 3.13 or higher
*   `uv` (recommended for dependency management) or `pip`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd tsv-form
    ```

2.  **Install dependencies:**
    Using `uv`:
    ```bash
    uv sync
    ```
    
    Using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a `requirements.txt` from `pyproject.toml` if not using `uv`)*

## Usage

To generate the PDF form:

```bash
uv run main.py
```

This will create a `tsv.pdf` file in the current directory.

## Project Structure

*   `main.py`: Entry point for the application.
*   `fonts/`: Directory containing OpenSans font files.
*   `media/`: Directory containing the logo.
*   `pyproject.toml`: Project configuration and dependencies.

## Development

This project uses `uv` for package management.

*   **Add a dependency:** `uv add <package>`
*   **Run script:** `uv run main.py`
