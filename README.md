# Title: 🛰️ Automated Spatial QA for Urban GIS Layers using Python & PostGIS

# Project Summary: 
A Python-based QA engine to detect geometry errors in OSM urban datasets using PostGIS. Outputs include CSV reports and GIS-ready spatial files. Inspired by enterprise QA workflows and built to demonstrate spatial data automation skills.

## Project Phases:

**Phase 1:** Project setup, virtual environment, database setup  
**Phase 2:** Download OSM data, clip to Pune, import into PostGIS using `osm2pgsql`  
**Phase 3:** Run spatial QA checks (invalid geometry, overlaps, duplicates, slivers)  
**Phase 4:** Generate CSV and GeoPackage output  

---
## 🚀 Features
- Run 100% in Python + PostGIS
- Validate spatial data stored in PostGIS
- Detect invalid geometries, overlaps, topology errors, duplicates
- Auto-fix common geometry errors
- Generate error logs and summary QA reports

---
## 📁 Project Structure
```
automated_spatial_qa/
├── .gitignore                     # Files/folders to exclude from version control
├── requirements.txt              # Conda or pip dependencies
│
├── data/                          # Input spatial data (e.g., .osm.pbf files)
│   └── pune.osm.pbf
│
├── notebook/                      # Jupyter notebooks
│   └── run_all_qa.ipynb           # Final automation notebook (with markdown + code)
│
├── outputs/                       # QA output files
│   ├── qa_summary.csv             # CSV report of all spatial QA issues
│   └── spatial_qa_errors.gpkg     # GeoPackage of invalid/duplicate geometries
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

## ⚙️ Setup

```bash
pip install -r requirements.txt

conda create -n urbanqa_env python=3.11
conda activate urbanqa_env
conda install psycopg2 pandas geopandas sqlalchemy jupyter -c conda-forge

jupyter notebook

```
---
# Outputs

| Output Type              | Description                  |
| ------------------------ | ---------------------------- |
| `qa_summary.csv`         | Tabular log of all issues    |
| `spatial_qa_errors.gpkg` | Can be opened in QGIS/ArcGIS |
| `.ipynb` notebook        | Full code for entire spatial QA pipeline in one go |

