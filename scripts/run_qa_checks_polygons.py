import psycopg2
from datetime import datetime

# === DB CONFIG ===
DB_PARAMS = {
    "host": "localhost",
    "dbname": "urban_qa",
    "user": "postgres",
    "password": "perry95",  # Replace with actual password
}

# === QA CHECK QUERIES ===
qa_queries = {
    "Invalid Geometry": """
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_polygon',
          osm_id,
          'Invalid Geometry',
          ST_IsValidReason(geom),
          geom
        FROM osm2pgsql_polygon
        WHERE NOT ST_IsValid(geom);
    """,
    
    "Overlaps": """
        WITH building_polygons AS (
          SELECT * FROM osm2pgsql_polygon WHERE tags ? 'building'
        )
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_polygon',
          a.osm_id,
          'Overlap',
          'Overlaps with another polygon',
          a.geom
        FROM building_polygons a
        JOIN building_polygons b
        ON ST_Overlaps(a.geom, b.geom) AND a.osm_id < b.osm_id;
    """,
    
    "Duplicate Geometry": """
        WITH building_polygons AS (
          SELECT * FROM osm2pgsql_polygon WHERE tags ? 'building'
        )
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_polygon',
          a.osm_id,
          'Duplicate Geometry',
          'Same geometry as another feature',
          a.geom
        FROM building_polygons a
        JOIN building_polygons b
        ON ST_Intersects(a.geom, b.geom)
           AND ST_Equals(a.geom, b.geom)
           AND a.osm_id < b.osm_id;
    """,
    
    "Sliver Polygon": """
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_polygon',
          osm_id,
          'Sliver Polygon',
          'Area below minimum threshold',
          geom
        FROM osm2pgsql_polygon
        WHERE ST_Area(geom::geography) < 5;
    """
}

# === MAIN EXECUTION ===
def run_qa_checks():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        print(f"\n QA checks started at {datetime.now()}\n")

        for check_name, query in qa_queries.items():
            print(f" Running: {check_name}")
            cur.execute(query)
            conn.commit()

            # Get inserted row count for this check
            cur.execute(
                f"""SELECT COUNT(*) FROM spatial_qa_log WHERE issue_type = %s;""",
                (check_name,)
            )
            count = cur.fetchone()[0]
            print(f" Inserted rows for {check_name}: {count}\n")

        print(f" All QA checks completed at {datetime.now()}\n")

    except Exception as e:
        print(f" Error during QA checks: {e}")
        conn.rollback()

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_qa_checks()
