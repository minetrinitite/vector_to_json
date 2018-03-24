import subprocess, os
import db

def pbf_to_osm(file, osmosis):

commandstring = osmosis + " --read-pbf " + readName + " --write-xml " + writeName + ".osm"

proc = subprocess.Popen(commandstring, stdout=subprocess.PIPE)