# Houdini_Texture_Tools
This script allows you to apply texture images to objects in a few clicks. Specifically, it automatically creates material nodes, changes assignment paths, etc.  

# Installation
1. Download the complete set of tool files.
2. Change the path in **SettingUsdTexture.py** appropriately.  
3. Copy and paste the **SettingUsdTexture.py** code and run it in Houdini's Python Source Editor.  

# Usage
- In the Geometry SOP of the obj context, **select the node you want to import to the stage.**
![image](https://github.com/user-attachments/assets/5e3cad97-c3f9-4ed9-b2e1-3d5886b14e54)  

- Copy and paste the **SettingUsdTexture.py** code and run it in Houdini's Python Source Editor.  
- A node selection window will appear, so **select the material library** for the stage where you want to create a material.  
![image](https://github.com/user-attachments/assets/2ad771de-7d38-4f38-be0e-7fceca3a6784)  

- **Select the folder containing the texture images.**  
If the texture image in the selected folder contains the following channel name or color space name in its name, it will be properly loaded and connected to the MaterialX Standard Surface node. (Supports uppercase and lowercase letters)  

・Supported channel name  
**base_color, roughness, metalness, normal, displacement**

・Supported color space name  
**sRGB, Raw**

・Example of texture image name  
**wood_table_worn_Base_color_2k_sRGB.png**

- The geometry is imported with **SOP Import Node** on the stage and connected to the **Material Library Node.**  
Materials are also assigned to the geometry at the **Material Library Node.**  
If you look inside, a **Subnetwork of MaterialX Builder** has been created.  
Furthermore, if you look at the contents, a texture image is loaded and a material node is assembled.  
![image](https://github.com/user-attachments/assets/7cb7a1f8-f992-4fbb-942c-ade67945cd4b)  
![image](https://github.com/user-attachments/assets/6cef1e1d-a4ea-48fb-bb68-386bdba72389)    
![image](https://github.com/user-attachments/assets/368f9f38-d548-4253-8f28-7bd976fcf1e3)

- The material is now assigned to the geometryv !  
![image](https://github.com/user-attachments/assets/95954ba8-d499-4e1c-b238-92a6f4ddf7db)