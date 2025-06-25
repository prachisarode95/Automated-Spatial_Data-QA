-- Adjust with WHERE building IS NOT NULL if focusing only on buildings.

INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)

SELECT
  'osm2pgsql_polygon',
  a.osm_id,
  'Overlapping Feature',
  'Overlaps with another polygon',
  a.geom

FROM
  osm2pgsql_polygon a

JOIN
  osm2pgsql_polygon b
  
  ON ST_Overlaps(a.geom, b.geom) AND a.osm_id <> b.osm_id;
