-- ST_Equals() compares geometry shapes, not just coordinates.

INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)

SELECT
  'osm2pgsql_polygon',
  a.osm_id,
  'Duplicate Geometry',
  'Identical geometry to another feature',
  a.geom

FROM
  osm2pgsql_polygon a

JOIN
  osm2pgsql_polygon b
  
  ON ST_Equals(a.geom, b.geom) AND a.osm_id < b.osm_id;