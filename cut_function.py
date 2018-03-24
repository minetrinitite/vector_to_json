import subprocess, os

#subprocess.call("osmosis --read-pbf ..\..\planet_37.65,55.706_37.661,55.71.osm.pbf --write-xml sampleData1.osm")
#need to get the BBox
#TODO: function to read pbf piece and save it to DB(what should it return?)
#TODO: function to get the pbf piece from DB(prolly osmosis wouldn't be able to read from context so it'd need creating file again)
#TODO: function to read pbf piece and write it in xml(osmosis decorator)
#TODO: function to read xml
#TODO: function to translate OSMxml into GEOjson(prolly also write it)


def cutoutpbf(sourceFilename, left, bottom, right, top, osmosis):
    #returns the absolute path with name of extracted pbf file
    #TODO: intercept file writing and get all contents from osmosis right into the context for better speed
    #TODO: clean code
    #TODO: put explanation comments
    cut = []
    if (type(left) is float) & (type(bottom) is float) &\
       (type(right) is float) & (type(top) is float):
        commandstring = osmosis + " --read-pbf " + sourceFilename + " --bounding-box top=" + str(top) + \
                        " left=" + str(left) + " bottom=" + str(bottom) + " right=" + str(
            right) + " --write-pbf file=" + \
                        str(left) + "-" + str(bottom) + "-" + str(right) + "-" + str(top) + ".osm.pbf omitmetadata=true" #inPipe.0=\"w\"
        #print(commandstring)
        #with open(sourceFilename, "rb") as sourcefile:
        proc = subprocess.Popen(commandstring, stdout=subprocess.PIPE)
        proc.wait()
        outputfile = (str(os.path.dirname(os.path.abspath(__file__))) + "\\" + str(left) + "-" + str(bottom) + "-" + str(right) + "-" + str(top) + ".osm.pbf")
        return outputfile
        # for line in proc.stdout:
        #     #cut.append(line)
        # #for line in io.TextIOWrapper(proc.stdout):
        # #for line in iter(proc.stdout.readline, ''):
        #
        #     if line != '':
        #         # the real code does filtering here
        #         cut.append(line)
        #     else:
        #         break
        #cut = proc.communicate()[0]
        #with open(str(left) + "-" + str(bottom) + "-" + str(right) + "-" + str(top) + ".pbf", "rb") as result:



        #print(cut)


#r, w = os.pipe()

