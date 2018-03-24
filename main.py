import db
import cut_function as cut


file = "planet_37.65,55.706_37.661,55.71.osm.pbf"
osmosisFile = "osmosis\\bin\osmosis.bat"
left = 37.654
bottom = 55.707
right = 37.659
top = 55.709


key = db.put_in_db(cut.cutoutpbf(file, left, bottom, right, top, osmosisFile), 'localhost',6379,0)
db.get_from_db(key,  'localhost',6379,0)
#37.654 37.659 55.707 55.709




