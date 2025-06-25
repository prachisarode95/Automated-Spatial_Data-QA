-- Add spatial index for polygon layer
CREATE INDEX IF NOT EXISTS idx_geom_polygon ON osm2pgsql_polygon USING GIST(geom);
ANALYZE osm2pgsql_polygon;

-- For lines
CREATE INDEX IF NOT EXISTS idx_geom_line ON osm2pgsql_line USING GIST(geom);
ANALYZE osm2pgsql_line;

-- For points
CREATE INDEX IF NOT EXISTS idx_geom_point ON osm2pgsql_point USING GIST(geom);
ANALYZE osm2pgsql_point;