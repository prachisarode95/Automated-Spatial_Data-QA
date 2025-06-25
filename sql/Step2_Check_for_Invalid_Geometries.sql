-- It checks every polygon in osm2pgsql_polygon, and if its geometry is invalid, it logs it in the spatial_qa_log table.--
INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)

SELECT
  'osm2pgsql_polygon' AS table_name,   -- logs the source table name
  osm_id,                              -- unique ID of the feature
  'Invalid Geometry',                  -- QA error type
  ST_IsValidReason(geom),              -- explanation (e.g., 'Self-intersection')
  geom                                 -- the invalid shape

FROM
  osm2pgsql_polygon

WHERE
  NOT ST_IsValid(geom);               -- filters only the invalid shapes

-- Looks for any feature in the polygon table that has geometry errors
-- Logs a human-readable reason (like “Self-intersection”)
-- Saves the problematic geometry for review