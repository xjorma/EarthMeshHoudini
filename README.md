# EarthMeshHoudini
**Generate real world meshes in Houdini using the Google API.**
![title](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/RushMoreHoudini.png)
![turntable](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/StadeOlympiqueTurningTable30.gif)
## Prerequisites

### Google Cloud Account
You need a google account to be able to use this HDA. The process is easy:
1. To begin click-on this [link](https://cloud.google.com/gcp).
2. Click **Start free** on the top left corner, you need to be logged in with a google account like gmail. If start free is nor present it's probably because you already use google cloud, so instead link on **Console** on the top right (should be here if you are logged), then click on the combo box on the top left, and you could jump to the step **6**.
3. Fill your country your organization description (I personally put _Business idea / startup idea_) and agree to terms of service and click _Continue_.
4. Fill your personal information, and your **credit card** (but you should not be charged if you don't abuse, the free tier is relatively big and the Tile API is supposed to be free for a year, but check it yourself) and click _Continue_.
5. Fill the survey.
6. Click on the top-right on **My First Project**, and them click on **Create a new project**.
7. Give-it a name (I personally called it _Geospacial_) and choose _no organization_ a press **Create**.
8. Click on the _Hamburger Icon_ on the top right. choose **API and Service** them **Library**.
9. Search for **Map Tiles API** and Enable it (It should give you a key at this Stage **Keep it** and **do not share** it with anyone).
10. Search for **Maps Elevation API** and Enable it.
11. That's it for the *Google Cloud Account*.

### Additional Python Packages
You need to add 2 additional python packages, **pygltflib** to load gltf files, **DracoPy** to uncompress mesh compression from google used by the 3D tiles.
- Launch Houdini.
- Go to the top menus **Windows** >> **Shell**.
- Type **hython -m pip install pygltflib** to install the pygltflib.
- Type **hython -m pip install DracoPy** to install DracoPy.
- **Quit** Houdini.
- The 2 packages are installed, your are good to go to the mext step.

### SideFX Labs
I use [this node](https://www.sidefx.com/docs/houdini/nodes/sop/labs--quickmaterial-2.0.html) from Labs, so you need to install the Labs Package.
- Launch the **Houdini Laucher** and install the Labs/Packages.

### (Optional) Increase the viewport material setting
If you don't do that, most of the things you will see in the viewport won't be textured. It's optional but very recommended.
- Open the _Display Option_.
- Go to the _Material_ tab.
- Increase the **Single Object Material Limit** to a big number like 5000.

![Material Warning](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Material%20Limit.png)

## How to use the HDA
Place the EarthMesh node in your scene.

- **Cache path** Path of the temp cache (recommended value $HIP/Cache)

![Material Warning](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/EarthMeshNode.png)

Configure the node with the right parameter for your usage. I suggest you to start with the parameters in the screenshot, or use the test scene **EarthMesh_Test.hip** at the root of the repo.

![Material Warning](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/HDA_Parameters.png)

- **Google API Key** Copy your key here.
- **Cache path** Path of the temp cache (recommended value $HIP/Cache)
- **Latitude** Latitude of the area you want to capture, i usually do a copy-paste from _google map_.
- **Longitude** Longitude of the area you want to capture, i usually do a copy-paste from _google map_.
- **Min Error** The highest definition you want to use for your mesh, smaller number means higher definition. 2 is presently the best definition, maybe one day google will enrich their server with more detailed meshes.
- **Max Error** The lowest definition you want to use for your mesh, smaller number means higher definition. 60000 is presently the worst definition.
- **Min Dist** If the bounding box is below this distance the resolution will be set to the MinError resolution. 
- **Max Dist** If the bounding box is Farther this distance the resolution will be set to the MaxError resolution. Is the distance is in-between the chosen resolution will be an interpolation between MinError and MaxError 
- **Show Bounding Boxes** It's mainly an option I used to debug, it builds a mesh with the bounding boxes instead of the actual mesh from google.

## Trouble shooting
To optimize and also limit the number of requests to the _google cloud_, I use a cache in a folder specified in the digital asset. If a file in the cache is corrupted (it never append to me, but for example if Houdini crash or is killed while generating the mesh) it might result to various issues like crashing Houdini, if you suspect the cache to be the source of your problems don't hesitate to delete all the file inside. There is nothing in the cache that can't be downloaded again from the cloud.

## Know issues 
There are presently few warnings related to the labs's QuickMaterials node just after loading the HDA. I will do some follow-up with _SideFX_, and figure out what the solution is.

![Material Warning](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Material_Warning.png)

## Planified Improvement
- Make the download phase interruptible, presently you only rely on the **max_meshes** parameter to avoid a very long wait or an infinite loop while experimenting with LOD parameters.
- Optimize the mesh construction, I already optimized this part a lot. I will re-give it a try. I am open to suggestions.
- Probably a ton based on your feedback.

## Warning
I am not a legal expert, but the meshes from google are copyrighted. Be careful when using them in a project.
