import psycopg2
from datetime import datetime

DB_PARAMS = {
    "host": "localhost",
    "dbname": "urban_qa",
    "user": "postgres",
    "password": "",  # Replace
}

point_qa_queries = {
    "Duplicate Point": """
        WITH point_data AS (
          SELECT * FROM points
        )
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'points',
          a.node_id,
          'Duplicate Point',
          'Point has exact same location as another',
          a.geom
        FROM point_data a
        JOIN point_data b
        ON ST_Equals(a.geom, b.geom)
           AND a.node_id < b.node_id;
    """,

    "Invalid Geometry (Point)": """
        INSERT INTO pune_qa_log (table_name, feature_id, issue_type, issue_description, geometry)
        SELECT
          'points',
          node_id,
          'Invalid Geometry (Point)',
          ST_IsValidReason(geom),
          geom
        FROM points
        WHERE NOT ST_IsValid(geom);
    """
}

def run_point_qa():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        print(f"\n Point QA checks started at {datetime.now()}\n")

        for check_name, query in point_qa_queries.items():
            print(f" Running: {check_name}")
            cur.execute(query)
            conn.commit()

            cur.execute(
                f"""SELECT COUNT(*) FROM pune_qa_log WHERE issue_type = %s;""",
                (check_name,)
            )
            count = cur.fetchone()[0]
            print(f" Inserted rows for {check_name}: {count}\n")

        print(f" Point QA completed at {datetime.now()}\n")

    except Exception as e:
        print(f" Error in Point QA: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_point_qa()
