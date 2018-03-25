import db
import cut_function as cut
import os

file = "planet_37.65,55.706_37.661,55.71.osm.pbf"
osmosisFile = "osmosis\\bin\osmosis.bat"
left = 37.654
bottom = 55.707
right = 37.659
top = 55.709


key = db.put_in_db(cut.cutoutpbf(file, left, bottom, right, top, osmosisFile), 'localhost',6379,0)
os.remove(key + '.osm.pbf')
db.get_from_db(key,  'localhost',6379,0)




