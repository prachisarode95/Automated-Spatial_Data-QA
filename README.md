# Spatial Data Quality Automation Pipeline  
> Automated Spatial QA for Urban Spatial Layers using Python & PostGIS
---

## 1. Problem Statement

1. Urban geospatial datasets (e.g., OpenStreetMap, municipal GIS layers) often contain topology and geometry inconsistencies such as invalid geometries, overlaps, duplicates, and sliver polygons. These errors directly impact downstream applications like routing, urban planning, and spatial analytics.
2. Manual QA processes are time-consuming, error-prone, and non-scalable for large datasets.
3. This project builds an automated spatial data validation pipeline to systematically detect and report geometry and topology issues using Python and PostGIS.

---

## 2. Why It Matters: According to the Industry Use-Cases

Accurate geospatial data is critical across multiple industries:

- **Logistics & Mobility**: Incorrect geometries affect routing engines and delivery optimization
- **Urban Planning**: Overlapping or invalid parcels lead to incorrect zoning decisions
- **Autonomous Systems**: High-quality spatial data is essential for navigation models
- **GIS Data Providers**: Ensuring data integrity before publishing datasets

---

## 3. System Architecture
            ┌──────────────────────────┐
            │   OSM Raw Data (.pbf)    │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │   Data Ingestion Layer   │
            │     (osm2pgsql)          │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │   PostGIS Database       │
            │ (Spatial Data Storage)   │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │   QA Engine (Python)     │
            │  - Geometry Checks       │
            │  - Topology Checks       │
            │  - Duplicate Detection   │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │   Output Layer           │
            │ CSV Reports + GeoPackage │
            └──────────────────────────┘

            
---

## 4. Tech Stack

- **Programming**: Python (3.10+)
- **Database**: PostgreSQL + PostGIS
- **Spatial Libraries**: GeoPandas, Shapely
- **Database Access**: Psycopg2, SQLAlchemy
- **Data Source**: OpenStreetMap (PBF format)
- **Visualization & Execution**: Jupyter Notebook
- **ETL Tooling**: osm2pgsql

---

## 5. How It Works (Workflow)

### Step 1: Data Ingestion
- Download OpenStreetMap `.pbf` data
- Clip dataset to Pune region
- Import into PostGIS using `osm2pgsql`

### Step 2: Data Storage
- Store spatial layers (points, lines, polygons) in PostGIS
- Ensure indexing for spatial queries

### Step 3: QA Validation Engine
Run automated QA checks using SQL + Python:

- **Geometry Validation** → `ST_IsValid()`
- **Overlap Detection** → `ST_Overlaps()`
- **Duplicate Detection** → `ST_Equals()`, `ST_Intersects()`
- **Sliver Detection** → `ST_Area() < threshold`
- **Zero-Length Lines** → `ST_Length() = 0`

### Step 4: Output Generation
- Export detected errors to:
  - CSV (tabular logs)
  - GeoPackage (spatial visualization)
- Enable direct inspection in QGIS/ArcGIS

---

## Output Visualization of Errors
![Visualizing Spatial QA Errors](https://github.com/user-attachments/assets/eca582f6-4627-46e5-9bb3-5e0dbd7e6282)

> Shows detected geometry errors visualized in QGIS.

---

## Key Takeaways

- Demonstrates **spatial data pipeline design**
- Combines **database + automation + geospatial analytics**
- Represents a transition from **manual GIS workflows → scalable engineering systems**
