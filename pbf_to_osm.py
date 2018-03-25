import subprocess

def pbf_to_osm(file, osmosis):

    commandstring = osmosis + " --read-pbf " + file + " --write-xml " + file[:-8] + ".osm"

    proc = subprocess.Popen(commandstring, stdout=subprocess.PIPE)
    proc.wait()
    return file[:-4]