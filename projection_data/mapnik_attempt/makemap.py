
import os
import json

def Project(name):
    return {
        "bounds": [-180,-85.0511,180,85.0511],
        "center": [0,0,2],
        "format": "png8",
        "srs": "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0.0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs +over",
        "Stylesheet": [],
        "Layer": [],
        "name": '{}'.format(name)
    }

def Layer(name, path, geometry='polygon'):
    return {
        "geometry": "{}".format(geometry),
        "id": "{}".format(name),
        "class": "",
        "Datasource": {
            "file": "{}".format(path),
            "srs": WGS84,
        },
        "srs": WGS84,
        "advanced": {},
        "name": "{}".format(name),
        "status": "on"
    }

WGS84 = '+proj=longlat +ellps=WGS84 +datun=WGS84 +no_defs'

