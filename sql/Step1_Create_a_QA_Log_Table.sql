-- This is like a master error log — all QA results from various checks go here.

CREATE TABLE spatial_qa_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    feature_id BIGINT,
    issue_type TEXT,
    issue_description TEXT,
    geometry GEOMETRY,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Instead of checking data visually or manually, you're setting up an automated system to log errors with geometry for easy review, mapping, or reporting later.