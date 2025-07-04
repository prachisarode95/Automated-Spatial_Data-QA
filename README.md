# Title: Automated Spatial QA for Urban GIS Layers using Python & PostGIS

## Project Summary: 
A Python-based QA engine to detect geometry errors in OSM urban datasets using PostGIS. Outputs include CSV reports and GIS-ready spatial files. Inspired by enterprise QA workflows and built to demonstrate spatial data automation skills.

## Project Phases:

**Phase 1:** Project setup, virtual environment, database setup  
**Phase 2:** Download OSM data, clip to Pune, import into PostGIS using `osm2pgsql`  
**Phase 3:** Run spatial QA checks (invalid geometry, overlaps, duplicates, slivers)  
**Phase 4:** Generate CSV and GeoPackage output  

---
## Features
- Run 100% in Python + PostGIS
- Validate spatial data stored in PostGIS
- Detect invalid geometries, overlaps, topology errors, duplicates
- Auto-fix common geometry errors
- Generate error logs and summary QA reports

---
## Sample QA Logic Implemented

| Check             | Function                          |
| ----------------- | --------------------------------- |
| Invalid Geometry  | `ST_IsValid()`                    |
| Overlaps          | `ST_Overlaps()`                   |
| Duplicates        | `ST_Equals()` + `ST_Intersects()` |
| Slivers           | `ST_Area() < threshold`           |
| Zero-Length Lines | `ST_Length()`                     |
| Point Duplicates  | `ST_Equals()` between points      |

---

## Project Structure
```
automated_spatial_qa/
├── .gitignore                     # Files/folders to exclude from version control
├── requirements.txt              # Conda or pip dependencies
│
├── data/                          # Input spatial data (e.g., .osm.pbf files)
│   └── pune.osm.pbf
    └── generic.lua
│
├── notebook/                      # Jupyter notebooks
│   └── run_all_qa.ipynb           # Final automation notebook (with markdown + code)
│
├── outputs/                       # QA output files
│   ├── pune_qa_errors.csv             # CSV report of all spatial QA issues
│   └── pune_qa_errors.gpkg     # GeoPackage of invalid/duplicate geometries
│
├── scripts/                       # Python scripts for modular QA
│   ├── run_all_qa.py              # Master script for full automation
│   ├── run_qa_checks_polygons.py  # Polygon QA (invalid, overlap, sliver, duplicate)
│   ├── run_qa_checks_lines.py     # Line QA (invalid, zero-length, duplicate)
│   └── run_qa_checks_points.py    # Point QA (invalid, duplicate location)
│
├── sql/                           # Optional: future SQL-only QA scripts (raw)
│   └── (optional custom .sql files)

```
## Technologies Used
- Python (3.10)

- PostgreSQL + PostGIS (v14+)

- Geopandas, Pandas, Psycopg2, SQLAlchemy

- OpenStreetMap PBF data

- Jupyter Notebook for interactive runs

---

## How to Run This Project

### Clone the Repository
```bash
git clone https://github.com/prachisarode95/Automated-Spatial_Data-QA.git
cd Automated-Spatial_Data-QA
```
### Set Up Conda Environment
```bash
conda create -n urbanqa_env python=3.11
conda activate urbanqa_env
conda install psycopg2 pandas geopandas sqlalchemy jupyter -c conda-forge
```
### Start the Notebook
```
jupyter notebook

```
Note: Open notebook/run_all_qa.ipynb and run all cells. Alternatively, run scripts/run_all_qa.py from the terminal.

---

# Outputs

| Output Type              | Description                  |
| ------------------------ | ---------------------------- |
| `pune_qa_errors.csv`         | Tabular log of all issues    |
| `pune_qa_errors.gpkg` | Can be opened in QGIS/ArcGIS |
| `.ipynb` notebook        | Full code for entire spatial QA pipeline in one go |

---
# Outputs Visualization
![Visualizing Spatial QA Errors](https://github.com/user-attachments/assets/eca582f6-4627-46e5-9bb3-5e0dbd7e6282)

---
