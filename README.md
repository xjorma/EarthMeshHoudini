# EarthMeshHoudini
**Generate real world meshes in Houdini using the Google API.**
![Title](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/RushMoreHoudini.png)
![Turntable](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/StadeOlympiqueTurningTable30.gif)
![Sagrada Familia](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Sagrada.png)
![Chryster Building](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Chrysler.png)
## Prerequisites

### Google Cloud Account
You need a google account to be able to use this HDA. The process is easy:
1. To begin click-on this [link](https://cloud.google.com/gcp).
2. Click **Start free** on the top left corner, you need to be logged in with a google account like gmail. If start free is not present it's probably because you already use google cloud, so instead link on **Console** on the top right (should be here if you are logged), then click on the combo box on the top left, and you could jump to the step **6**.
3. Fill your country, your organization description (I personally put _Business idea / startup idea_) and agree to terms of service and click _Continue_.
4. Fill your personal information and your **credit card** (but you should not be charged if you don't overuse it, the free tier is relatively big and the Tile API is supposed to be free for a year, but check it yourself) and click _Continue_.
5. Fill the survey.
6. Click on the top-right on **My First Project**, and them click on **Create a new project**.
7. Give-it a name (I personally called it _Geospacial_) and choose _no organization_ a press **Create**.
8. Click on the _Hamburger Icon_ on the top right. choose **API and Service** then **Library**.
9. Search for **Map Tiles API** and Enable it (It should give you a key at this Stage **Keep it** and **do not share** it with anyone).
10. Search for **Maps Elevation API** and Enable it.
11. You can test if your key supports the _Map Tiles API_ by trying this link on your favorite browser **https://tile.googleapis.com/v1/3dtiles/root.json?key=YOUR_API_KEY**, replace **YOUR_API_KEY** by your key, if you see an error message it's not good, and you need to check again your account.
12. You can test if your key supports the _Elevation API_ by trying this link on your favorite browser **https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536%2C-104.9847034&key=YOUR_API_KEY**, replace **YOUR_API_KEY** by your key, if you see an error message it's not good, and you need to check again your account.

### Additional Python Packages
You need to add 2 additional python packages, **pygltflib** to load gltf files, **DracoPy** to uncompress mesh compression from google used by the 3D tiles.
- Launch Houdini.
- Go to the top menus **Windows** >> **Shell**.
- To install **pygltflib** type:
   ```sh
   hython -m pip install pygltflib
- To install **DracoPy** type:
   ```sh
   hython -m pip install DracoPy
- **Quit** Houdini.
- The 2 packages are installed, your are good to go to the next step.

Note: Some user had to install **PIP**, in this case follow the instruction [here](http://wordpress.discretization.de/houdini/home/advanced-2/installing-and-using-scipy-in-houdini/).

### SideFX Labs
I use [this node](https://www.sidefx.com/docs/houdini/nodes/sop/labs--quickmaterial-2.0.html) from Labs, so you need to install the Labs Package.
- Launch the **Houdini Laucher** and install the Labs/Packages.

### (Optional) Increase the viewport material setting
If you don't do that, most of the things you will see in the viewport won't be textured. It's optional but very recommended.
- Open the _Display Option_.
- Go to the _Material_ tab.
- Increase the **Single Object Material Limit** to a big number like _5000_.
- instantiate a new Scene Viewer or quit and restart Houdini.

![Material Warning](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Material%20Limit.png)

# Installation
- Download the repo.
- Place the **EarthMeshHoudini** folder somewhere on your local drive. It's important that you do not install **EarthMeshHoudini** directly into your $HOME/houdiniXX.X directory or into any other default Houdini installation directory, or else it may not properly be loaded when you start Houdini.
- Configure the **Google API Key** in the **EarthMesh.json** file and change the **EARTHMESH_PATH** to the path where you placed the **EarthMeshHoudini** folder.
- Copy the **EarthMesh.json** file to your $HOME/houdiniXX.X/packages folder.

## How to use the HDA

### EarthMesh
Place the EarthMesh node in your scene.

![Earth Mesh Node](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/EarthMeshNode.png)

Configure the node with the right parameter for your usage. I suggest you start with the parameters in the screenshot, or use the test scene **EarthMesh_Test.hip** at the root of the repo.

![HDA Parameters EarthMesh Node](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/HDA_Parameters.png)

- **Google API Key** Copy your key here, you can replace the whole _`$Google_Cloud_Api_Key`_ string with your key, or set an environment variable named _Google_Cloud_Api_Key_ and set your key as value.
- **Cache path** Path of the temp cache (recommended value $HIP/Cache). **Make sure this folder exists on your drive**
- **Latitude** Latitude of the area you want to capture, i usually do a copy-paste from _google map_.
- **Longitude** Longitude of the area you want to capture, i usually do a copy-paste from _google map_.
- **Min Error** The highest definition you want to use for your mesh, smaller number means higher definition. 2 is presently the best definition, maybe one day google will enrich their server with more detailed meshes.
- **Max Error** The lowest definition you want to use for your mesh, smaller number means higher definition. 60000 is presently the worst definition.
- **Min Dist** If the bounding box is below this distance, the resolution will be set to the MinError resolution. 
- **Max Dist** If the bounding box is farther from this distance the resolution will be set to the MaxError resolution. If the distance is in-between the chosen resolution will be an interpolation between MinError and MaxError 
- **Max Meshes** Limit the number of GLB loaded, to avoid scraping the whole google database and explode your budget and also avoid being trapped in an infinite loop.
- **Show Bounding Boxes** It's mainly an option I used to debug, it builds a mesh with the bounding boxes instead of the actual mesh from google.
- **Remove Skirt** _Skirts_ are small polygons used to avoid gaps between meshes. For most common usage it's better to keep polygons, but if you want to display your mesh in additive or generate a point cloud, this option  might be useful.
- **Clear Cache** Press this button to clear your cache.

Be patient it takes couple of minutes to dowwnload and build the meshes.

1 unit in Houdini, is 1 meter in real live, the X axis point to the North, the Z axis point to the East.

### TextureAtlas

Using countless lots of 256x256 textures, it is not practical and also slow to render (Too many draw calls), this node is here to help you..

![HDA Parameters TextureAtlas_Node](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/HDA_Parameters_Atlas.png)

- **TextureDirectory** Folder where all the atlas textures will be exported. **Make sure this folder exists on your drive**
- **Prefix** All the texture filename will start with this.
- **Padding** Number of pixels used to separate the little textures block inside the big texture. Useful to avoid seams when using mipmaps. Too big value will reduce the resolution of the texture.
- **Extension** File format used to export atlas textures.
- **Max Atlas Size** Dimension of generated atlas textures. (don't use a size bigger than _8192_ for Unreal)

If you don't want to see pixelated textured in your houdini viewport, you probably want to uncheck **Limit Resolution** on the **Texture** tab of **Display Option**  .

![Display Option Limit Resolution](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/LimitResolution.png)

## Trouble shooting
To optimize and also limit the number of requests to the _google cloud_, I use a cache in a folder specified in the digital asset. If a file in the cache is corrupted (it's never happened to me, but for example if Houdini crashes or is killed while generating the mesh) it might result in various issues like crashing Houdini, if you suspect the cache to be the source of your problems don't hesitate to delete all the files inside. There is nothing in the cache that can't be downloaded again from the cloud.

## Know issues 
There are currently a few warnings related to the labs's QuickMaterials node just after loading the HDA. I'll do some follow-up with _SideFX_, and figure out what the solution is.

![Material Warning](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Material_Warning.png)

## Planified Improvement
- <s>Make the download phase interruptible, presently you only rely on the **max_meshes** parameter to avoid a very long wait or an infinite loop while experimenting with LOD parameters.</s> **(Done)**
- <s>Optimize the mesh construction, I already optimized this part a lot. I will try to optimize it more. I am open to suggestions.</s> **(Done)**
- Probably a ton based on your feedback.

## Warning
I am not a legal expert, but the meshes from google are copyrighted. Be careful when using them in a project.
