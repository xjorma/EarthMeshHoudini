# EarthMeshHoudini
**Generate real-world meshes in Houdini using the Google API.**
![Title](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/RushMoreHoudini.png)
![Turntable](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/StadeOlympiqueTurningTable30.gif)
![Sagrada Familia](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Sagrada.png)
![Chrysler Building](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Chrysler.png)
## Prerequisites

### Google Cloud Account
You need a Google account to use this HDA. The process is straightforward:
1. Start by clicking on this [link](https://cloud.google.com/gcp).
2. Click **Start free** on the top left corner; you need to be logged in with a Google account, such as Gmail. If "Start free" is not visible, it's probably because you're already using Google Cloud, so instead, click on **Console** on the top right, then click on the combo box on the top left, and you can proceed to step **6**.
3. Fill in your country, organization description (I personally put _Business idea / startup idea_), agree to the terms of service, and click _Continue_.
4. Fill in your personal information and **credit card details** (although you shouldn't be charged if you don't exceed the free tier; the Tile API is supposed to be free for a year, but verify this yourself) and click _Continue_.
5. Fill out the survey.
6. Click on the top-right **My First Project**, then click on **Create a new project**.
7. Give it a name (I called mine _Geospatial_) and choose _No organization_, then press **Create**.
8. Click on the _Hamburger Icon_ on the top right, choose **APIs & Services**, then **Library**.
9. Search for **Map Tiles API** and enable it (you should receive a key at this stage; **keep it** and **do not share** it with anyone).
10. Search for **Maps Elevation API** and enable it.
11. Test if your key supports the _Map Tiles API_ by trying this link in your favorite browser: **https://tile.googleapis.com/v1/3dtiles/root.json?key=YOUR_API_KEY**, replacing **YOUR_API_KEY** with your key. If you see an error message, something is wrong, and you should check your account settings again.
12. Test if your key supports the _Elevation API_ by trying this link in your favorite browser: **https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536%2C-104.9847034&key=YOUR_API_KEY**, replacing **YOUR_API_KEY** with your key. If you see an error message, something is wrong, and you should check your account settings again.

### Additional Python Packages
You need to add two additional Python packages: **pygltflib** to load GLTF files and **DracoPy** to decompress mesh compression used by Google's 3D Tiles.
- Launch Houdini.
- Go to the top menus **Windows** >> **Shell**.
- To install **pygltflib**, type:
  ```sh
  hython -m pip install pygltflib
- To install **DracoPy**, type:
  ```sh
  hython -m pip install DracoPy
- **Quit** Houdini.
- The two packages are installed; you're ready to proceed to the next step.

Note: Some users had to install **PIP**; in this case, follow the instructions [here](http://wordpress.discretization.de/houdini/home/advanced-2/installing-and-using-scipy-in-houdini/).

### SideFX Labs
I use [this node](https://www.sidefx.com/docs/houdini/nodes/sop/labs--quickmaterial-2.0.html) from Labs, so you need to install the Labs package.
- Launch the **Houdini Launcher** and install the Labs/Packages.

### (Optional) Increase the viewport material setting
If you don't do this, most of the objects you see in the viewport won't be textured. It's optional but highly recommended.
- Open the _Display Options_.
- Go to the _Material_ tab.
- Increase the **Single Object Material Limit** to a large number, such as _5000_.
- Instantiate a new Scene Viewer or quit and restart Houdini.

![Material Warning](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/Material%20Limit.png)

## How to use the HDA

### EarthMesh
Place the EarthMesh node in your scene.

![Earth Mesh Node](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/EarthMeshNode.png)

Configure the node with the right parameters for your usage. I suggest starting with the parameters in the screenshot or using the test scene **EarthMesh_Test.hip** at the root of the repository.

![HDA Parameters EarthMesh Node](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/HDA_Parameters.png)

- **Google API Key**: Copy your key here; you can replace the entire _`$Google_Cloud_Api_Key`_ string with your key or set an environment variable named _Google_Cloud_Api_Key_ with your key as the value.
- **Cache path**: Path of the temporary cache (recommended value: $HIP/Cache). **Make sure this folder exists on your drive**.
- **Latitude**: Latitude of the area you want to capture; I usually copy-paste from _Google Maps_.
- **Longitude**: Longitude of the area you want to capture; I usually copy-paste from _Google Maps_.
- **Min Error**: The highest definition you want to use for your mesh; a smaller number means higher definition. 2 is currently the best definition; maybe one day Google will enrich their servers with more detailed meshes.
- **Max Error**: The lowest definition you want to use for your mesh; a smaller number means higher definition. 60000 is currently the worst definition.
- **Min Dist**: If the bounding box is below this distance, the resolution will be set to the MinError resolution. 
- **Max Dist**: If the bounding box is farther than this distance, the resolution will be set to the MaxError resolution. If the distance is between the two, the chosen resolution will be an interpolation between MinError and MaxError.
- **Max Meshes**: Limit the number of GLB files loaded to avoid scraping the entire Google database and exploding your budget, as well as avoiding being trapped in an infinite loop.
- **Show Bounding Boxes**: This is mainly an option I used for debugging; it builds a mesh with the bounding boxes instead of the actual mesh from Google.
- **Remove Skirt**: _Skirts_ are small polygons used to avoid gaps between meshes. For most common use cases, it's better to keep these polygons, but if you want to display your mesh in additive mode or generate a point cloud, this option might be useful.
- **Clear Cache**: Press this button to clear your cache.

Be patient, as it can take a couple of minutes to download and build the meshes.

1 unit in Houdini is equivalent to 1 meter in real life. The X-axis points North, and the Z-axis points East.

### TextureAtlas

Using numerous 256x256 textures is impractical and slow to render due to too many draw calls. This node helps solve that issue.

![HDA Parameters TextureAtlas_Node](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/HDA_Parameters_Atlas.png)

- **TextureDirectory**: The folder where all atlas textures will be exported. **Make sure this folder exists on your drive**.
- **Prefix**: All texture filenames will start with this prefix.
- **Padding**: The number of pixels used to separate the smaller texture blocks within the larger atlas texture. This is useful for avoiding seams when using mipmaps. A value that is too large will reduce the final texture resolution.
- **Extension**: File format used to export atlas textures.
- **Max Atlas Size**: The dimensions of the generated atlas textures. (Do not use a size larger than 8192 for Unreal Engine).

If you don't want to see pixelated textures in your Houdini viewport, you should uncheck **Limit Resolution** on the **Texture** tab of **Display Options**.

![Display Option Limit Resolution](https://github.com/xjorma/EarthMeshHoudini/blob/main/Image/LimitResolution.png)

## Troubleshooting
To optimize performance and limit the number of requests to Google Cloud, this HDA uses a cache stored in the folder specified in the digital asset's parameters. If a file in the cache becomes corrupted (which has never happened to me but could occur if Houdini crashes or is terminated while generating a mesh), it might cause various issues, including Houdini crashing. If you suspect the cache is the source of your problems, feel free to delete all the files inside it. There is nothing in the cache that cannot be downloaded again from the cloud.

## Known Issues 
- <s>I have some certificate issues on Mac and Linux. Any help fixing them is welcome.</s>
- It seems there is an issue with atlasing when too many meshes are loaded.

## Planned Improvements
- <s>Make the download phase interruptible. Currently, you can only rely on the max_meshes parameter to avoid a very long wait or an infinite loop while experimenting with LOD parameters.</s> **(Done)**
- <s>Optimize mesh construction. I have already optimized this part significantly, but I will continue to improve it. I am open to suggestions.</s> **(Done)**
- More improvements based on your feedback.

## Warning
I am not a legal expert, but be aware that the meshes from Google are copyrighted. Please be cautious when using them in a project.
