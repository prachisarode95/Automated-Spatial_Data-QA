import psycopg2
from datetime import datetime

# === DB CONFIG ===
DB_PARAMS = {
    "host": "localhost",
    "dbname": "urban_qa",
    "user": "postgres",
    "password": "",  # Replace with actual password
}

# === QA CHECK QUERIES ===
qa_queries = {
    "Invalid Geometry": """
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'polygons',
          area_id,
          'Invalid Geometry',
          ST_IsValidReason(geom),
          geom
        FROM polygons
        WHERE NOT ST_IsValid(geom);
    """,
    
    "Overlaps": """
        WITH building_polygons AS (
          SELECT * FROM polygons WHERE tags ? 'building'
        )
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'polygons',
          a.area_id,
          'Overlap',
          'Overlaps with another polygon',
          a.geom
        FROM building_polygons a
        JOIN building_polygons b
        ON ST_Overlaps(a.geom, b.geom) AND a.area_id < b.area_id;
    """,
    
    "Duplicate Geometry": """
        WITH building_polygons AS (
          SELECT * FROM polygons WHERE tags ? 'building'
        )
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'polygons',
          a.area_id,
          'Duplicate Geometry',
          'Same geometry as another feature',
          a.geom
        FROM building_polygons a
        JOIN building_polygons b
        ON ST_Intersects(a.geom, b.geom)
           AND ST_Equals(a.geom, b.geom)
           AND a.area_id < b.area_id;
    """,
    
    "Sliver Polygon": """
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'polygons',
          area_id,
          'Sliver Polygon',
          'Area below minimum threshold',
          geom
        FROM polygons
        WHERE ST_Area(ST_Transform(geom, 4326)::geography) < 5;
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
                f"""SELECT COUNT(*) FROM pune_qa_log WHERE issue_type = %s;""",
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
