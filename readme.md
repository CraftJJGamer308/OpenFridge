* OpenFridge Project 2025
Jeongjoo Lim, Aron Feher, Marie Schrotter, Jakub Stanczyk

* Usage: 

run "node server" on the console
visit http://localhost:3000 in your browser of your choice
upload a picture of your fridge contents
edit the extracted list if necessary
wait until the recipes and images are generated. You will be redirected to the starting page at completion.
Note: during runtime, the webpage may seem unreactive - in this case do not leave the website as it is retrieving information from the API in the backend. On average the runtime is ~1 min. A demonstration is to be seen in the "./OpenFridgeDemo.mp4" file (sped up for time saving purposes).

* Explanation:

This web app is implemented with node.js expressjs. It is there designed to be as a server - client devices can connect to this web app via its IP address.
After upload of the image, it is stored at "./uploads/bild.*" and then used for image recognition. 
In addition, "./productList.txt" and "/public/recipes/*.*" files are generated.
"./productList.txt" stores the product present in the fridge so that it could be reused if necessary.
"/public/recipes/*.*" are the image and HTML files that are shown in the starting page (at the initial state empty). 


