# Automated Spatial QA Pipeline for Urban GIS Layers
import psycopg2
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd
import subprocess
import os

# === CONFIGURATION ===
DB_PARAMS = {
    "host": "localhost",
    "dbname": "urban_qa",
    "user": "postgres",
    "password": ""  # Replace with your secure password
}

POSTGIS_URL = f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}/{DB_PARAMS['dbname']}"

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === STEP 1: Run QA Scripts for All Geometry Types ===
def run_qa_scripts():
    print("\n Starting Pune QA checks at", datetime.now())

    try:
        #subprocess.call(["python", "scripts/run_qa_checks_lines.py"])
        #subprocess.call(["python", "scripts/run_qa_checks_points.py"])
        subprocess.call(["python", "scripts/run_qa_checks_polygons.py"])
    except Exception as e:
        print(f" Error running QA scripts: {e}")
        return

    print(" All QA scripts executed.\n")

# === STEP 2: Generate CSV Summary ===
def export_csv_summary():
    print(" Generating CSV summary...")
    try:
        query = """
            SELECT table_name, feature_id, issue_type, issue_description, checked_at
            FROM pune_qa_log
            ORDER BY checked_at DESC;
        """
        engine = create_engine(POSTGIS_URL)
        df = pd.read_sql_query(query, con=engine)
        csv_path = os.path.join(OUTPUT_DIR, "pune_qa_errors.csv")
        df.to_csv(csv_path, index=False)
        print(f" Summary saved at: {csv_path}")
    except Exception as e:
        print(f" Error exporting CSV: {e}")

# === STEP 3: Export Pune QA Errors to GeoPackage ===
def export_geopackage_errors():
    print(" Exporting Pune QA errors as GeoPackage...")
    try:
        engine = create_engine(POSTGIS_URL)
        gdf = gpd.read_postgis(
            "SELECT * FROM pune_qa_log WHERE geometry IS NOT NULL;",
            con=engine,
            geom_col='geometry'
        )
        gpkg_path = os.path.join(OUTPUT_DIR, "pune_qa_errors.gpkg")
        gdf.to_file(gpkg_path, driver="GPKG")
        print(f" GeoPackage saved at: {gpkg_path}")
    except Exception as e:
        print(f" Error exporting GeoPackage: {e}")

# === RUN THE PIPELINE ===
if __name__ == "__main__":
    run_qa_scripts()
    export_csv_summary()
    export_geopackage_errors()
    print(f"\n Full QA pipeline completed successfully at {datetime.now()}\n")
