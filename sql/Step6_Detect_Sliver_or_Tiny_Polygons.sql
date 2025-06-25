-- Sometimes, accidental digitizing can create narrow slivers or tiny polygons.

INSERT INTO spatial_qa_log (table_name, feature_id, issue_type, issue_description, geometry)

SELECT
  'osm2pgsql_polygon',
  osm_id,
  'Sliver Polygon',
  'Area below minimum threshold',
  geom

FROM
  osm2pgsql_polygon

WHERE
  ST_Area(geom::geography) < 5; -- Area in square meters
