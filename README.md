# EarthMeshHoudini
Generate real world meshes in Houdini using the Google API.

## Prerequisites

### Google Cloud Account
You need a google account to be able to use this HDA. The process is easy:
- to begin click this [link](https://cloud.google.com/gcp).
- click **Start free** on the top left corner, for need to be logger with a google account like gmail.
- Fill your country your organization description (I personally put _Business idea / startup idea_) and agree to terms of service and click _Continue_.
- Fill your personnal information, and your **credit card** (but you should not me charged if you don't abuse, the free tier is relativity big and the Tile API is supposed to be free for a year, but by check yourself) and click _Continue_.
- Fill the survey.
- Click on the top-right on **My First Project**, and them click on **Create a new project**.
- Give-it a name (I personnaly called it _Geospacial_) and choose _no organization_ a press **Create**.
- Click on the _Hamburger Icon_ on the top right. choose **API and Service** them **Library**.
- Search for **Map Tiles API** and Enable it (It should give you a key a this Stage **Keep it** and **do not share** it with anyone).
- Search for **Maps Elevation API** and Enable it.
- That it for the *Google Cloud Account*.

### Additionnal Python Packages
You need to add 2 additionnal python packages, **pygltflib** to load gltf files, **DracoPy** to uncompress to mesh compression from google used by the 3d tiles.
- Launch Houdini.
- Go to the top menus **Windows** >> **Shell**.
- type **hython -m pip install pygltflib** to install the pygltflib.
- type **hython -m pip install DracoPy** to install DracoPy.
- **Quit** Houdini.
- The 2 packages are installed.

### SideFX Labs
I use [this node](https://www.sidefx.com/docs/houdini/nodes/sop/labs--quickmaterial-2.0.html) from Labs, so you need to install the Labs Package.
- Launch the **Houdini Laucher** and install the Labs/Packages.

## How to use the HDA
- **Latitude** Latitude of the area you want to capture, i usualy do a copy-paste from _google map_.
- **Longitude** Longitude of the area you want to capture, i usualy do a copy-paste from _google map_.
- **Cache path** Path of the temp cache (recommended value $HIP/Cache)
- **MinError** The highest definition you want to use for your mesh, smaller number means higher definition. 2 is presently the best definition, maybe on day google will enrich thier server with more detailled meshes.
- **MaxError** The lowest definition you want to use for your mesh, smaller number means higher definition. 60000 is presently the worst definition.
- **MinDist** If the boundingbox is bellow this distance the resolution will be set the the MinError resolution. 
- **MaxDist** If the boundingbox is Farther this distance the resolution will be set the the MaxError resolution. Is the distance is in-between the chosen resolution will be an interpoation between MinError and MaxError 

## Trouble shooting
To optimize and also limit the number of request to the _google cloud_, I use a cache in a folder specified in the digital asset. If a file in the cache is corrupted (it never append to me, but for exemple if Houdini crash or is killed while generating the mesh) it might result to various issues like crashing Houdini, if you suspect the cache to be the source of your problems don't hesitate to delete all the file inside. There is nothing in the cachae that can't be downlaoded again frpm the cloud. 

## Warning
I am not a legal expert, but the mesh from google are copyrighed. Be careful when using them in a project. 
