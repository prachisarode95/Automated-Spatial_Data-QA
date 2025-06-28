import psycopg2
from datetime import datetime

DB_PARAMS = {
    "host": "localhost",
    "dbname": "urban_qa",
    "user": "postgres",
    "password": "",  # Replace with your password
}

line_qa_queries = {
    "Invalid Geometry (Line)": """
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'lines',
          way_id,
          'Invalid Geometry (Line)',
          ST_IsValidReason(geom),
          geom
        FROM lines
        WHERE NOT ST_IsValid(geom);
    """,
    
    "Zero-Length Line": """
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'lines',
          way_id,
          'Zero-Length Line',
          'Line length below threshold (1m)',
          geom
        FROM lines
        WHERE ST_Length(ST_Transform(geom, 4326)::geography) < 1;
    """,
    
    "Duplicate Line": """
        WITH line_data AS (
          SELECT * FROM lines
        )
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'lines',
          a.way_id,
          'Duplicate Line',
          'Same geometry as another line',
          a.geom
        FROM line_data a
        JOIN line_data b
        ON ST_Intersects(a.geom, b.geom)
           AND ST_Equals(a.geom, b.geom)
           AND a.way_id < b.way_id;
    """
}

def run_line_qa():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        print(f"\n Line QA checks started at {datetime.now()}\n")

        for check_name, query in line_qa_queries.items():
            print(f" Running: {check_name}")
            cur.execute(query)
            conn.commit()

            cur.execute(
                f"""SELECT COUNT(*) FROM pune_qa_log WHERE issue_type = %s;""",
                (check_name,)
            )
            count = cur.fetchone()[0]
            print(f" Inserted rows for {check_name}: {count}\n")

        print(f" Line QA completed at {datetime.now()}\n")

    except Exception as e:
        print(f" Error in Line QA: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_line_qa()
