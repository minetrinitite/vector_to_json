import subprocess

subprocess.call("osmosis --read-pbf ..\..\planet_37.65,55.706_37.661,55.71.osm.pbf --write-xml sampleData1.osm")
#need to get the BBox

subprocess.call("osmosis --read-pbf FILENAME --bounding-box top=55.709"
                " left=37.654 bottom=55.707 right=37.659 --write-pbf file=LEFT-BOTTOM-RIGHT-TOP",
                stdout=subprocess.STDOUT,
                shell=True)
#37.654 37.659 55.707 55.709

