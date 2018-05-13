import db
import cut_function as cut
import pbf_to_osm as pbf
import osm_to_geojson as osm

startfile = "planet_37.65,55.706_37.661,55.71.osm.pbf"
osmosisFile = "osmosis\\bin\osmosis.bat"
left = 37.654
bottom = 55.707
right = 37.659
top = 55.709

host = "192.168.99.100"
port = 6379

r = db.init_redis(host, port, 0)
key = db.put_in_db(cut.cutoutpbf(startfile, left, bottom, right, top, osmosisFile), r)
print(key)
pbffile = db.get_from_db(key, r)
osmfile = pbf.pbf_to_osm(pbffile, osmosisFile)
osm.parseOSM(osmfile)




