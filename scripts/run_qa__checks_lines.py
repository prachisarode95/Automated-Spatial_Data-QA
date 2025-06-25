import psycopg2
from datetime import datetime

DB_PARAMS = {
    "host": "localhost",
    "dbname": "urban_qa",
    "user": "postgres",
    "password": "perry95",  # Replace
}

line_qa_queries = {
    "Invalid Geometry (Line)": """
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_line',
          osm_id,
          'Invalid Geometry (Line)',
          ST_IsValidReason(geom),
          geom
        FROM osm2pgsql_line
        WHERE NOT ST_IsValid(geom);
    """,
    
    "Zero-Length Line": """
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_line',
          osm_id,
          'Zero-Length Line',
          'Line length below threshold (1m)',
          geom
        FROM osm2pgsql_line
        WHERE ST_Length(geom::geography) < 1;
    """,
    
    "Duplicate Line": """
        WITH line_data AS (
          SELECT * FROM osm2pgsql_line
        )
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_line',
          a.osm_id,
          'Duplicate Line',
          'Same geometry as another line',
          a.geom
        FROM line_data a
        JOIN line_data b
        ON ST_Intersects(a.geom, b.geom)
           AND ST_Equals(a.geom, b.geom)
           AND a.osm_id < b.osm_id;
    """
}

def run_line_qa():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        print(f"\n🚦 Line QA checks started at {datetime.now()}\n")

        for check_name, query in line_qa_queries.items():
            print(f"🔍 Running: {check_name}")
            cur.execute(query)
            conn.commit()

            cur.execute(
                f"""SELECT COUNT(*) FROM spatial_qa_log WHERE issue_type = %s;""",
                (check_name,)
            )
            count = cur.fetchone()[0]
            print(f"✅ Inserted rows for {check_name}: {count}\n")

        print(f"🎯 Line QA completed at {datetime.now()}\n")

    except Exception as e:
        print(f"❌ Error in Line QA: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_line_qa()
