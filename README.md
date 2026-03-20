# Techmanthan- — Smart City Prototype

This repository contains a Smart City resource-allocation prototype (Udaipur) and supporting scripts. The main interactive component is a Streamlit dashboard located in `smart-city-allocation/` which predicts traffic congestion and waste overflow and displays emergency metrics and a city map.

This README explains how to set up and run the project on macOS, Linux, or Windows.

## Repository layout (relevant files)

- `smart-city-allocation/`
  - `app.py` — Streamlit dashboard (main entry point)
  - `create_data.py` — synthetic data generator (produces CSVs in `data/`)
  - `preprocess.py` — data preprocessing
  - `train_traffic.py`, `train_waste.py` — training scripts to create model `.pkl` files
  - `generate_map.py` — generates `map.html` used by the dashboard
  - `data/` — CSV files used by the app (traffic, waste, emergency)
  - `traffic_model.pkl`, `waste_model.pkl` — trained models used by the app
  - `map.html` — embedded map shown in the Streamlit UI
- `scripts/` — helper shell/PowerShell scripts
- `docs/`, `adapters/`, and other repo-level docs

## Prerequisites

- Python 3.8–3.12 installed (3.12 is known to work in this workspace).
- Recommended: git, a terminal (zsh on macOS), and a browser.

Optional for macOS: Xcode command line tools (for Watchdog and better file-watching performance with Streamlit):

```bash
xcode-select --install
```

## Recommended setup (macOS / Linux / WSL)

1. Open a terminal and change to the repository root:

```bash
cd "/Users/jayeshvyas/Desktop/Neev Paliwal/techmanthan-"
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Upgrade pip and install required Python packages:

```bash
python -m pip install --upgrade pip
python -m pip install pandas numpy scikit-learn joblib streamlit folium
# Optional (recommended for faster file-watching in Streamlit):
python -m pip install watchdog
```

Note: There is no `requirements.txt` in this repo snapshot. If you need a pinned environment, create a `requirements.txt` and pin versions.

## Generate data, models, and map (if missing)

If the `data/` CSVs or the `.pkl` model files are missing or you want to regenerate them, run the pipeline in this order from inside `smart-city-allocation/`:

```bash
cd smart-city-allocation
python create_data.py    # generates CSVs under data/
python preprocess.py    # optional preprocessing
python train_traffic.py # creates traffic_model.pkl
python train_waste.py   # creates waste_model.pkl
python generate_map.py  # builds map.html
```

Each script uses relative paths inside `smart-city-allocation/`, so run them from that folder to avoid path issues.

## Run the Streamlit dashboard

Always start Streamlit with the same Python interpreter that has your packages installed. The safest option is:

```bash
# from inside smart-city-allocation/ (recommended):
cd smart-city-allocation
python -m streamlit run app.py
```

Or, if `streamlit` is installed into the active venv and `which streamlit` points at the venv binary, you may run:

```bash
streamlit run app.py
```

Open the Local URL shown by Streamlit (usually http://localhost:8501).

## Troubleshooting

- ModuleNotFoundError for `joblib` or other packages: ensure your venv is active and install missing packages into that venv. Example:

```bash
source .venv/bin/activate
python -m pip install joblib
python -m streamlit run app.py
```

- Streamlit runs with the wrong Python (e.g., Conda base): run it with `python -m streamlit run app.py` after activating the correct venv, or deactivate Conda (`conda deactivate`) and then activate the venv.

- `map.html` missing: run `python generate_map.py` to create it.

- `.pkl` pickle load errors: these can occur if the scikit-learn version used to create the pickles differs from your installed version. Fixes:
  - Re-train models locally with `train_traffic.py` / `train_waste.py`.
  - Or install the scikit-learn version originally used (if known).

- Port already in use: start Streamlit on a different port:

```bash
python -m streamlit run app.py --server.port 8502
```

## Quick checks

Confirm imports work in your active environment:

```bash
python -c "import joblib, sklearn, pandas; print('ok', joblib.__version__, sklearn.__version__, pandas.__version__)"
```

Confirm `streamlit` binary location points to your venv (when activated):

```bash
which python
which streamlit
```

## Suggested next steps (optional)

- Add a `requirements.txt` with pinned versions for reproducibility.
- Add a small script `run_local.sh` that validates files and launches the app.
- Add unit tests for the data generation scripts.

If you'd like, I can add a `requirements.txt` and a small `run_local.sh` helper and run the pipeline once to validate everything — tell me which you'd prefer.

---

If you need platform-specific automation (Dockerfile, GitHub Actions CI, or a Windows-specific setup script), tell me which environment you want and I will add it.
