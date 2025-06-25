import psycopg2
from datetime import datetime

DB_PARAMS = {
    "host": "localhost",
    "dbname": "urban_qa",
    "user": "postgres",
    "password": "perry95",  # Replace
}

point_qa_queries = {
    "Duplicate Point": """
        WITH point_data AS (
          SELECT * FROM osm2pgsql_point
        )
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_point',
          a.osm_id,
          'Duplicate Point',
          'Point has exact same location as another',
          a.geom
        FROM point_data a
        JOIN point_data b
        ON ST_Equals(a.geom, b.geom)
           AND a.osm_id < b.osm_id;
    """,

    "Invalid Geometry (Point)": """
        INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'osm2pgsql_point',
          osm_id,
          'Invalid Geometry (Point)',
          ST_IsValidReason(geom),
          geom
        FROM osm2pgsql_point
        WHERE NOT ST_IsValid(geom);
    """
}

def run_point_qa():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        print(f"\n📍 Point QA checks started at {datetime.now()}\n")

        for check_name, query in point_qa_queries.items():
            print(f"🔍 Running: {check_name}")
            cur.execute(query)
            conn.commit()

            cur.execute(
                f"""SELECT COUNT(*) FROM spatial_qa_log WHERE issue_type = %s;""",
                (check_name,)
            )
            count = cur.fetchone()[0]
            print(f"✅ Inserted rows for {check_name}: {count}\n")

        print(f"🏁 Point QA completed at {datetime.now()}\n")

    except Exception as e:
        print(f"❌ Error in Point QA: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_point_qa()
