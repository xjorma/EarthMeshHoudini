import json
import urllib.request
import hashlib
import os
import logging
from pathlib import Path

try:
    import hou
except ImportError:
    pass

logger = logging.getLogger(__name__)


CACHE_PATH = Path(os.environ.get("EARTH_MESH_CACHE", "./cache"))
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", None)

print(f"Cache path: {CACHE_PATH}")

# Filename need to be encoded because filenames provided by google are too long for windows.
def hash_filename(filename):
    name, ext = os.path.splitext(filename)                      # Splitting the filename from its extension
    hashed_name = hashlib.sha256(name.encode()).hexdigest()     # Encoding the filename (without extension) and hashing it
    return hashed_name + ext                                    # Returning the new filename with the original extension


def bytes_from_url(url, cached):
    filename = hash_filename(url.split("?")[0].split("/")[-1])

    if not CACHE_PATH.exists():
        CACHE_PATH.mkdir(parents=True)  # TODO: May want to do this somewhere else

    path = CACHE_PATH / filename

    if cached and path.is_file():
        with open(path, "rb") as file:
            return file.read()
    else:
        with urllib.request.urlopen(url) as response:
            logger.info("Download %s", path)
            bytes = response.read()
            file_from_bytes(bytes, path)
            return bytes
    

def json_from_byte(bytes):
    return json.loads(bytes.decode("utf-8"))
    

def file_from_bytes(bytes, file_name):
    with open(file_name, "wb") as binary_file:
        binary_file.write(bytes)
        

def find_key(root, key):
    children = root["children"]
    for child in children :
        if "content" in child:
            content = child["content"]
            if key in content:
                return content[key]
        r = find_key(child, key)
        if r:
            return r
    return ""


def file_from_url(url, file_name, cached):
    if(cached and os.path.isfile(file_name)):
        return
    file_from_bytes(bytes_from_url(url, cached), file_name)
    

def buildBoundingBoxMatrix(box):
    # Bounding boxes don't have the same axis than the meshes
    boundingbox2mesh = hou.Matrix4([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, -1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
        ])  
    return hou.Matrix4([
        [box[3], box[4], box[5], 0.0],
        [box[6], box[7], box[8], 0.0],
        [box[9], box[10], box[11], 0.0],
        [box[0], box[1], box[2], 1.0]]
        ) * boundingbox2mesh
    

def sdfBox(bbx, ctr):
    bbx = bbx.asTupleOfTuples()
    m = [hou.Vector3(bbx[0][0:3]), hou.Vector3(bbx[1][0:3]), hou.Vector3(bbx[2][0:3]), hou.Vector3(bbx[3][0:3])]
    b = hou.Vector3(m[0].length(), m[1].length(), m[2].length())
    m = [m[0].normalized(), m[1].normalized(), m[2].normalized(), m[3]]
    m = hou.Matrix4([
        [m[0].x(), m[0].y(), m[0].z(), 0.0],
        [m[1].x(), m[1].y(), m[1].z(), 0.0],
        [m[2].x(), m[2].y(), m[2].z(), 0.0],
        [m[3].x(), m[3].y(), m[3].z(), 1.0]
        ])
    mi = m.inverted()
    p = hou.Vector3(ctr) * mi
    # inspired by https://iquilezles.org/articles/distfunctions/
    q = hou.Vector3([abs(p.x()), abs(p.y()), abs(p.z())]) - b
    return hou.Vector3(max(0.0,q.x()), max(0.0,q.y()), max(0.0,q.z())).length() + min(max(q.x(), max(q.y(), q.z())), 0.0)
    