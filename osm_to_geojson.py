# -*- coding: utf-8 -*-
from lxml import etree
from geojson import Feature, FeatureCollection, Point, Polygon, LineString, dump, GeometryCollection
import json
from pympler import asizeof
import re


#augmentation block
def featureenter(self):
    return self
def featureexit(self, type, value, traceback):
    pass

Feature.__enter__ = featureenter
Feature.__exit__ = featureexit

#additional stuff
def definegeometry(coordinates):
    if (len(coordinates) != 0):
        if ((coordinates[0] == coordinates[len(coordinates) - 1]) & (len(coordinates) > 1)):
            dummycoordinates = []
            dummycoordinates.append(coordinates)
            return Polygon(dummycoordinates)
        return LineString(coordinates)


def parseOSM(osmFile):
    xmltag = re.compile(r"<\?.*xml.*\?>", re.IGNORECASE)
    with open(osmFile, 'r', encoding='utf-8') as fobj:
        xml = fobj.read()
        xml = xmltag.sub("", string=xml)

    root = etree.fromstring(xml)
    print(str(asizeof.asizeof(xml)) + " xml")
    points = {}
    realfuturecollection = []
    counter = 0
    accomodationinfo = {}
    savedforlater = []
    geojsonfile = osmFile[:-3] + "geojson"
    with open(geojsonfile, 'w', encoding='utf-8') as resultfile:
        for appt in root.getchildren():
            props = {}

            if appt.tag == "node":
                id = int(appt.get("id"))
                lon = float(appt.get("lon"))
                lat = float(appt.get("lat"))
                for elem in appt.getchildren():
                    key = elem.get("k")
                    value = "" + elem.get("v")
                    props.update({key: value})
                with Feature(geometry=Point((lon, lat)), id=id, properties=props) as feature:
                    realfuturecollection.append(feature)
                    accomodationinfo.update({str(id): counter})
                    counter += 1
                        #dump(feature, resultfile)
                points[str(id)] = Point((lon, lat))
                    #points.append(Feature(geometry=Point((lon, lat)), id=id))



            elif appt.tag == "way":
                id = int(appt.get("id"))
                coordinates = []
                for elem in appt.getchildren():
                    if elem.tag == "nd":
                        ref = elem.get("ref")
                        if str(ref) in points:
                            coordinates.append(points[str(ref)]["coordinates"])
                    else:
                        key = elem.get("k")
                        value = "" + elem.get("v")
                        props.update({key: value})
                geometry = definegeometry(list(coordinates))
                with Feature(geometry=geometry, id=id, properties=props) as feature:
                    realfuturecollection.append(feature)
                    accomodationinfo.update({str(id): counter})
                    counter += 1
                    #dump(feature, resultfile)

            elif appt.tag == "relation":
                id = int(appt.get("id"))
                members = []
                faulty = 0
                geometries = []
                for elem in appt.getchildren():  # role outer role inner
                    if elem.tag == "member":
                        ref = elem.get("ref")
                        if str(ref) not in accomodationinfo:
                            savedforlater.append(appt)
                            faulty = 1
                            break
                        members.append(tuple((elem.get("ref"), elem.get("role"))))
                    else:
                        key = elem.get("k")
                        value = elem.get("v")
                        props.update({key: value})

                if not faulty:
                    for member in members:
                        geometries.append(realfuturecollection[accomodationinfo[member[0]]]["geometry"])
                    geometry = GeometryCollection(list(geometries))
                    with Feature(geometry=geometry, id=id, properties=props) as feature:
                        realfuturecollection.append(feature)
                        accomodationinfo.update({str(id): counter})
                        counter += 1

        for appt in savedforlater:
            id = int(appt.get("id"))
            members = []
            geometries = []
            for elem in appt.getchildren():  # role outer role inner
                if elem.tag == "member":
                    members.append(tuple((elem.get("ref"), elem.get("role"))))
                else:
                    key = elem.get("k")
                    value = elem.get("v")
                    props.update({key: value})
            for member in members:
                if member[0] in accomodationinfo:
                    geometries.append(realfuturecollection[accomodationinfo[member[0]]]["geometry"])
            geometry = GeometryCollection(list(geometries))
            with Feature(geometry=geometry, id=id, properties=props) as feature:
                realfuturecollection.append(feature)
                accomodationinfo.update({str(id): counter})
                counter += 1

        features = FeatureCollection(realfuturecollection)
        dump(features, resultfile)
    print(geojsonfile + " is ready")
    print(str(asizeof.asizeof(points)) + " points")
    print(str(asizeof.asizeof(features)) + " features")
    print(str(asizeof.asizeof(realfuturecollection)) + " realfuturcollection")
    print(features["features"][0] is realfuturecollection[0])
    with open(geojsonfile, encoding="utf8") as f:
        obj = json.load(f)

    outfile = open('resultbeauty.geojson', "w", encoding="utf8")
    outfile.write(json.dumps(obj, ensure_ascii=False, indent=4))
    outfile.close()
    return geojsonfile

#if __name__ == "__main__":
#    parseOSM("sampleData1.osm")