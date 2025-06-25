# Title: 🛰️ Automated Spatial QA for Urban GIS Layers using Python & PostGIS

# Project Summary: 
A Python-based QA engine to detect geometry errors in OSM urban datasets using PostGIS. Outputs include CSV reports and GIS-ready spatial files. Inspired by enterprise QA workflows and built to demonstrate spatial data automation skills.

## Project Phases:

**Phase 1:** Project setup, virtual environment, database setup  
**Phase 2:** Download OSM data, clip to Pune, import into PostGIS using `osm2pgsql`  
**Phase 3:** Run spatial QA checks (invalid geometry, overlaps, duplicates, slivers)  
**Phase 4:** Generate CSV and GeoPackage output reports  

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
urban-gis-spatial-qa/
├── notebooks/
│   └── run_all_qa.ipynb            # Final QA automation notebook
├── scripts/
│   ├── run_qa_checks.py            # Polygon QA
│   ├── run_qa_lines.py             # Line QA
│   ├── run_qa_points.py            # Point QA
│   └── run_all_qa.py               # Combined script (optional if notebook used)
├── outputs/
│   ├── qa_summary.csv              # Tabular report
│   └── spatial_qa_errors.gpkg      # Spatial output for GIS tools
├── data/
│   └── pune.osm.pbf # Source data (or link in README)
├── README.md                       # Full project documentation
└── requirements.txt                # Conda or pip dependencies

```

## ⚙️ Setup

```bash
pip install -r requirements.txt

conda create -n urbanqa_env python=3.10
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
| `.ipynb` notebook        | Full code + explanations     |

