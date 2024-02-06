# vtk-viz
This is designed to create an interactive volume visualization using the Visualization Toolkit (VTK) library in Python. Its primary purpose is to load a volumetric dataset from a file, such as a .vti file, and render it in a three-dimensional space. The visualization allows users to manipulate various parameters, including color transfer function, opacity, camera angles, background color, and animation speed. Additionally, it provides interactive features like picking points in the volume, toggling the visibility of a plane widget, and displaying information about picked points. It facilitates the exploration and analysis of volumetric data through an interactive and customizable visualization interface.

## Video Demo:
[![Video Demo](https://img.youtube.com/vi/Z9kYDPtN3ms/0.jpg)](https://www.youtube.com/watch?v=Z9kYDPtN3ms)

## UI Example:
![UI example](https://github.com/abulalarabi/vtk-viz/blob/main/1.png)

## Installation Instructions for VTK Visualization Script

### 1. Ensure Required Dependencies:
   - Verify that you have the VTK (Visualization Toolkit) library installed. If not, follow the steps below to install it:
     - For pip installation:
       ```
       pip install vtk
       ```
     - For conda installation:
       ```
       conda install -c conda-forge vtk
       ```
   - Ensure that Python is installed on your system.

### 2. Download the Code:
   - Copy the provided code into a Python script file, e.g., "vtk_visualization.py".

### 3. Update File Path:
   - If you intend to load a specific VTI file, uncomment one of the file_path lines and specify the path to your VTI file. Alternatively, you can pass the file path as a command-line argument.

### 4. Execute the Script:
   - Run the script using a Python interpreter. If you're providing the file path as a command-line argument, execute the script as follows:
     ```
     python vtk_visualization.py <file_path>
     ```

### 5. Interact with the Visualization:
   - After executing the script, a window should appear displaying the rendered volume visualization.
   - Use the sliders to control various aspects of the visualization:
     - Adjust the color transfer function isovalue with the "Color Transfer Function Isovalue" slider.
     - Modify the azimuth and elevation angles using the respective sliders for camera control.
     - Change the background color with the "Background" slider.
     - Adjust the opacity of the volume using the "Opacity" slider.
     - Control the animation speed with the "Animation Speed" slider.
   - Click on the visualization to retrieve information about the picked position, cell ID, and isovalue.

### 6. Additional Features:
   - Toggle the visibility of a plane widget by clicking the button widget.
   - Animate camera movement based on the specified animation speed.

### 7. Exit the Application:
   - Close the application window to exit the visualization environment.

Ensure that your system meets the requirements for running VTK-based applications and that you have the necessary permissions to execute Python scripts.

