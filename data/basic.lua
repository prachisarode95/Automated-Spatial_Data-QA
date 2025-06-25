-- basic.lua: Minimal Lua config file for osm2pgsql flex output
-- Imports points, lines, and polygons with common tags

local tables = {}

tables.nodes = osm2pgsql.define_node_table('osm2pgsql_point', {
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'point', projection = 4326 },
})

tables.ways = osm2pgsql.define_way_table('osm2pgsql_line', {
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'linestring', projection = 4326 },
})

tables.areas = osm2pgsql.define_area_table('osm2pgsql_polygon', {
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'geometry', projection = 4326 },
})

function osm2pgsql.process_node(object)
    tables.nodes:insert({
        tags = object.tags,
        geom = object:as_point()
    })
end

function osm2pgsql.process_way(object)
    if object.is
