# 🛰️ Automated Spatial QA of Urban GIS Datasets

This project performs automated quality assurance (QA) checks on urban GIS layers (e.g., buildings, roads, parcels) using **Python + PostGIS**. It detects geometry/topology issues, logs errors, and applies auto-fixes when applicable.

---
## 🚀 Features
- Validate spatial data stored in PostGIS
- Detect invalid geometries, overlaps, topology errors, duplicates
- Auto-fix common geometry errors
- Generate error logs and summary QA reports

---
## 📁 Project Structure
```
automated_spatial_qa/
├── data/ # Sample GIS data
├── sql/ # QA SQL checks
├── scripts/ # Python scripts to run QA/fixes
├── utils/ # Helpers (DB connection, logging)
├── logs/ # QA logs
├── reports/ # Summary reports
```

## ⚙️ Setup

```bash
pip install -r requirements.txt
```
---
