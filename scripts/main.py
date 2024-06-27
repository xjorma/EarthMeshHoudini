from typing import Any
import logging
import os
import sys
import hou

from utils import hash_filename, buildBoundingBoxMatrix, sdfBox, file_from_url, json_from_byte, bytes_from_url, find_key
from utils import CACHE_PATH, GOOGLE_API_KEY

logger = logging.getLogger(__name__)

# log to the console
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# Enum status
class Status:
    SUCCESS = 0
    ERROR = 1
    INTERRUPTED = 2
    MAX_MESHES_REACHED = 3
    DOWNLOAD_ERROR = 4
    DOWNLOADING = 5


class EarthMeshDownloader:
    def __init__(self, max_meshes, cached, center, min_dist, max_dist, min_error, max_error):
        self.tile_url = "https://tile.googleapis.com"
        self.root_cmd = "/v1/3dtiles/root.json"

        assert GOOGLE_API_KEY, "GOOGLE_API_KEY environment variable is not set"
        
        # read Root
        b = bytes_from_url(self.tile_url + self.root_cmd + "?key=" + GOOGLE_API_KEY, False)
        res = json_from_byte(b)
        # find uri
        self.uri = find_key(res["root"], "uri")
        # extract context
        self.context = self.uri.split("?")[-1]

        self.max_meshes = max_meshes
        self.cached = cached
        self.center = center

        self.min_dist = min_dist
        self.max_dist = max_dist

        assert min_dist < max_dist, "min_dist must be less than max_dist"

        self.min_error = min_error
        self.max_error = max_error

        assert min_error < max_error, "min_error must be less than max_error"
        assert min_error >= 0, "min_error must be greater than or equal to 0"
        
        self.interrupted = False
        self.nb_meshes = 0
        self.mesh_list = []
        self.boxes_str = []
        self.errors_str = []
        self.operation = None

        logger.info(f"EarthMeshDownloader initialized with: center {center}, min_dist {min_dist}, max_dist {max_dist}, min_error {min_error}, max_error {max_error}")
    
    @property
    def status(self):
        if self.interrupted:
            return Status.INTERRUPTED
        
        if self.nb_meshes >= self.max_meshes:
            return Status.MAX_MESHES_REACHED
        
        return Status.DOWNLOADING
    
    def _check_exit(self):
        if self.status != Status.DOWNLOADING:
            return True
        
    def _update(self):
        if self.operation is None:
            return
        
        try:
            self.operation.updateLongProgress(float(self.nb_meshes) / float(self.max_meshes), "Loading mesh # %i" % (self.nb_meshes))
        except hou.OperationInterrupted:
            self._exit()

    def _exit(self):
        self.interrupted = True

    def _get_children(self, node):
        if len(node) == 1:
            if "content" not in node[0]:
                logger.info("No content in single child node")
                return node
            
            if node[0]['content']['uri'].split(".")[-1] == "json":
                url = f"{self.tile_url}{node[0]['content']['uri']}?{self.context}&key={GOOGLE_API_KEY}"
                return json_from_byte(bytes_from_url(url, self.cached))["root"]["children"]
        return node
    
    def _download(self, child):
        glb = child["content"]["uri"]
        file_name = CACHE_PATH + "/" + hash_filename(glb.split("/")[-1])
        file_from_url(f"{self.tile_url}{glb}?{self.context}&key={GOOGLE_API_KEY}", file_name, self.cached)
        boxes_str = ",".join([str(x) for x in child["boundingVolume"]["box"]])
        return file_name, boxes_str, str(child["geometricError"])

    def download(self, node):
        self._update()

        if self._check_exit():
            return
        
        if "children" not in node:
            return
        
        children = node["children"]

        if len(children) == 0:
            return
        
        children = self._get_children(children)
        
        for child in children:
            self._update()

            if self._check_exit():
                return
            
            if "content" not in child:
                self.download(child)
                continue

            e = child["geometricError"]

            # if e < self.min_error or e > self.max_error:
            #     logger.info(f"Geometric Error: {e} is out of range [{self.min_error}, {self.max_error}]")
            #     self.download(child)
            #     continue

            bbx = buildBoundingBoxMatrix(child["boundingVolume"]["box"])
            dist = sdfBox(bbx, self.center)

            dist_norm = (dist - self.min_dist) / (self.max_dist - self.min_dist)
            err = dist_norm * (self.max_error - self.min_error) + self.min_error

            l = max(min(err, self.max_error), self.min_error)

            if (l > e) or ("children" not in child):
                logger.info(f"Distance: {dist}, Distance_norm: {dist_norm}, Error: {l}, Geometric Error: {e}")
                mesh, boxes, error = self._download(child)
                self.mesh_list.append(mesh)
                self.boxes_str.append(boxes)
                self.errors_str.append(error)
                self.nb_meshes = self.nb_meshes + 1

                self._update()
            else:
                self.download(child)

        return self.status
            
    def __call__(self):
        node = json_from_byte(bytes_from_url(self.tile_url + self.uri + "&key=" + GOOGLE_API_KEY, self.cached))["root"]
        with hou.InterruptableOperation("Get geometry with Google API...", long_operation_name = "Starting Tasks", open_interrupt_dialog = True) as operation:
            self.operation = operation
            status = self.download(node)

        logger.info(status)

