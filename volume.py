import vtk

#file_path = str(sys.argv[1])

# Reader to load the .vti file
#file_path = 'foot.vti' 
file_path = 'mri_ventricles.vti'



# Initial camera azimuth and elevation values
initial_azimuth = 0
initial_elevation = 0

scalar_range = [0, 0]

# Global variable for animation speed
animation_speed = 0

# Callback function for the slider
def animation_slider_callback(obj, event):
    global animation_speed
    slider_rep = obj.GetRepresentation()
    animation_speed = slider_rep.GetValue()
    # round to 1 decimal place
    animation_speed = round(animation_speed, 1)

# Callback function for the animation
def animate_camera(obj, event):
    global animation_speed
    if animation_speed != 0:
        camera.Azimuth(animation_speed)
        render_window.Render()

# Callback function for the mouse click
def click_callback(obj, event):
    click_pos = render_window_interactor.GetEventPosition()

    picker = vtk.vtkCellPicker()
    picker.Pick(click_pos[0], click_pos[1], 0, renderer)

    if picker.GetCellId() != -1:
        world_position = picker.GetPickPosition()
        # for each element in the world position, round to 2 decimal places and convert to string
        world_position = [str(round(x, 2)) for x in world_position]
        # join the list of strings into one string
        world_position = ', '.join(world_position)
        
        data = volume_mapper.GetInput()
        point_data = data.GetPointData()
        scalars = point_data.GetScalars()
        point_id = picker.GetPointId()
        isovalue = scalars.GetTuple1(point_id)
        
        cell_id = picker.GetCellId()
        # Display information
        info_text = f"Picked position: {world_position}\nCell ID: {cell_id}\nIsovalue: {isovalue}"
        text_actor.SetInput(info_text)
        render_window.Render()

# Callback function for the azimuth slider
def azimuth_slider_callback(obj, event):
    global initial_azimuth
    slider_rep = obj.GetRepresentation()
    new_azimuth = slider_rep.GetValue()
    delta_azimuth = new_azimuth - initial_azimuth
    initial_azimuth = new_azimuth
    camera.Azimuth(-delta_azimuth)
    render_window.Render()

# Callback function for the elevation slider
def elevation_slider_callback(obj, event):
    global initial_elevation
    slider_rep = obj.GetRepresentation()
    new_elevation = slider_rep.GetValue()
    delta_elevation = new_elevation - initial_elevation
    initial_elevation = new_elevation
    camera.Elevation(delta_elevation)
    camera.OrthogonalizeViewUp()
    render_window.Render()

# callback function for the 

# Callback function for the iso slider
def slider_callback(obj, event):
    slider_rep = obj.GetRepresentation()
    pos = slider_rep.GetValue()
    color_transfer_function.RemoveAllPoints()
    color_transfer_function.AddRGBPoint(pos - int((scalar_range[0]+scalar_range[1])/2), 1.0, 0.0, 0.0)  # Red
    color_transfer_function.AddRGBPoint(pos, 0.0, 1.0, 0.0)        # Green
    color_transfer_function.AddRGBPoint(pos + int((scalar_range[0]+scalar_range[1])/2), 0.0, 0.0, 1.0)  # Blue
    volume_property.SetColor(color_transfer_function)
    render_window.Render()


# Callback function for the opacity slider
def opacity_slider_callback(obj, event):
    slider_rep = obj.GetRepresentation()
    value = slider_rep.GetValue()
    # Assuming you have a linear opacity function, adjust as needed
    opacity_transfer_function.RemoveAllPoints()
    opacity_transfer_function.AddPoint(0, 0.0)   # Fully transparent
    opacity_transfer_function.AddPoint(500, 0.3 * value) # Semi-transparent
    opacity_transfer_function.AddPoint(1000, 0.6 * value)
    opacity_transfer_function.AddPoint(1500, 1.0 * value) # Opaque
    volume_property.SetScalarOpacity(opacity_transfer_function)
    render_window.Render()

# Callback function for the background slider
def background_slider_callback(obj, event):
    slider_rep = obj.GetRepresentation()
    pos = slider_rep.GetValue()
    renderer.SetBackground(pos, pos, pos)
    render_window.Render()

# Callback function for the plane widget
def plane_widget_callback(obj, event):
    obj.GetPlane(plane)
    volume_mapper.SetClippingPlanes(plane)
    render_window.Render()

# Callback function for the show/hide button
def button_callback(obj, event):
    if plane_widget.GetEnabled():
        plane_widget.EnabledOff()
    else:
        plane_widget.EnabledOn()
    render_window.Render()

# Function to create a solid color texture
def create_texture(color):
    image_data = vtk.vtkImageData()
    image_data.SetDimensions(10, 10, 1)
    image_data.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 3)
    
    for i in range(10):
        for j in range(10):
            image_data.SetScalarComponentFromFloat(i, j, 0, 0, color[0])
            image_data.SetScalarComponentFromFloat(i, j, 0, 1, color[1])
            image_data.SetScalarComponentFromFloat(i, j, 0, 2, color[2])
    
    return image_data

# Create textures for 'On' (green) and 'Off' (red) states
on_texture = create_texture([0, 255, 0])
off_texture = create_texture([255, 0, 0])

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(file_path)
reader.Update()

# get the scalar range of the data
scalar_range = reader.GetOutput().GetScalarRange()

# divide the scalar range into three colors red, green, blue
range_1 = int((scalar_range[1] + scalar_range[0]) / 3)
range_2 = int((scalar_range[1] + scalar_range[0]) * 2 / 3)
range_3 = int(scalar_range[1])

# Create color transfer function
color_transfer_function = vtk.vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(range_1, 1.0, 0.0, 0.0)  # Red
color_transfer_function.AddRGBPoint(range_2, 0.0, 1.0, 0.0)  # Green
color_transfer_function.AddRGBPoint(range_3, 0.0, 0.0, 1.0)  # Blue

# Create opacity transfer function
opacity_transfer_function = vtk.vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(0, 0.0)   # Fully transparent
opacity_transfer_function.AddPoint(500, 0.3) # Semi-transparent
opacity_transfer_function.AddPoint(1000, 0.6)
opacity_transfer_function.AddPoint(1500, 1.0) # Opaque

# Volume properties
volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)
volume_property.SetInterpolationTypeToLinear()
volume_property.ShadeOn()

# Create a volume mapper
volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

# Create a volume
volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
#render_window.FullScreenOn()
#render_window.SetSize(2000, 2000)

# Create a camera
camera = renderer.GetActiveCamera()

# Get the object volume
object_volume = volume_mapper.GetInput()

# Set the camera based on the object volume
bounds = object_volume.GetBounds()
center = object_volume.GetCenter()
camera.SetPosition((center[0] + bounds[1])*1.5, (center[1] + bounds[3])*1.5, (center[2] + bounds[5])*1.5)
camera.SetFocalPoint(center)
camera.SetViewUp(0, 1, 0)
camera.OrthogonalizeViewUp()

# Set the initial azimuth and elevation
camera.Azimuth(initial_azimuth)
camera.Elevation(initial_elevation)



# Add the volume to the renderer
renderer.AddVolume(volume)
renderer.SetBackground(0, 0, 0)  # Background color black

# Create the slider widget
iso_slider_widget = vtk.vtkSliderWidget()
iso_slider_widget.SetInteractor(render_window_interactor)
iso_slider_widget.SetRepresentation(vtk.vtkSliderRepresentation2D())

# Configure slider representation
iso_slider = iso_slider_widget.GetRepresentation()

# Position the slider at the top right
iso_slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
iso_slider.GetPoint1Coordinate().SetValue(0.7, 0.9)  # Top right, adjust if necessary

iso_slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
iso_slider.GetPoint2Coordinate().SetValue(0.9, 0.9)  # Top right, adjust if necessary

# Set the minimum and maximum values and the initial value
iso_slider.SetMinimumValue(scalar_range[0])
iso_slider.SetMaximumValue(scalar_range[1])
iso_slider.SetValue(int(scalar_range[0] + (scalar_range[1] - scalar_range[0]) / 2))
iso_slider.SetTitleText("Color Transfer Function Isovalue")

# Increase the size of the slider components
iso_slider.SetSliderLength(0.02)
iso_slider.SetSliderWidth(0.03)
iso_slider.SetEndCapLength(0.01)
iso_slider.SetEndCapWidth(0.03)
iso_slider.SetTubeWidth(0.005)
iso_slider.SetLabelFormat("%3.0lf")
iso_slider.SetTitleHeight(0.02)
iso_slider.SetLabelHeight(0.02)

iso_slider_widget.AddObserver("InteractionEvent", slider_callback)

# Create the azimuth slider widget
azimuth_slider_widget = vtk.vtkSliderWidget()
azimuth_slider_rep = vtk.vtkSliderRepresentation2D()
azimuth_slider_widget.SetInteractor(render_window_interactor)
azimuth_slider_widget.SetRepresentation(azimuth_slider_rep)
azimuth_slider_rep.SetMinimumValue(-180.0)
azimuth_slider_rep.SetMaximumValue(180.0)
azimuth_slider_rep.SetValue(initial_azimuth)
azimuth_slider_rep.SetTitleText("Azimuth")

# Set the position for the azimuth slider in the top left corner
azimuth_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
azimuth_slider_rep.GetPoint1Coordinate().SetValue(0.01, 0.9)
azimuth_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
azimuth_slider_rep.GetPoint2Coordinate().SetValue(0.3, 0.9)

# Set the size of the slider components
azimuth_slider_rep.SetSliderLength(0.02)
azimuth_slider_rep.SetSliderWidth(0.03)
azimuth_slider_rep.SetEndCapLength(0.01)
azimuth_slider_rep.SetEndCapWidth(0.03)
azimuth_slider_rep.SetTubeWidth(0.005)
azimuth_slider_rep.SetLabelFormat("%3.0lf")
azimuth_slider_rep.SetTitleHeight(0.02)
azimuth_slider_rep.SetLabelHeight(0.02)

azimuth_slider_widget.AddObserver("InteractionEvent", azimuth_slider_callback)

# Create the elevation slider widget
elevation_slider_widget = vtk.vtkSliderWidget()
elevation_slider_rep = vtk.vtkSliderRepresentation2D()
elevation_slider_widget.SetInteractor(render_window_interactor)
elevation_slider_widget.SetRepresentation(elevation_slider_rep)
elevation_slider_rep.SetMinimumValue(-180.0)
elevation_slider_rep.SetMaximumValue(180.0)
elevation_slider_rep.SetValue(initial_elevation)
elevation_slider_rep.SetTitleText("Elevation")

# Set the position for the elevation slider in the top left corner
elevation_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
elevation_slider_rep.GetPoint1Coordinate().SetValue(0.01, 0.80)
elevation_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
elevation_slider_rep.GetPoint2Coordinate().SetValue(0.3, 0.80)  # Adjust the y-coordinate to make it vertical

# Set the size of the slider components (same as azimuth slider)
elevation_slider_rep.SetSliderLength(0.02)
elevation_slider_rep.SetSliderWidth(0.03)
elevation_slider_rep.SetEndCapLength(0.01)
elevation_slider_rep.SetEndCapWidth(0.03)
elevation_slider_rep.SetTubeWidth(0.005)
elevation_slider_rep.SetLabelFormat("%3.0lf")
elevation_slider_rep.SetTitleHeight(0.02)
elevation_slider_rep.SetLabelHeight(0.02)

elevation_slider_widget.AddObserver("InteractionEvent", elevation_slider_callback)

# add a background color slider
background_slider_widget = vtk.vtkSliderWidget()
background_slider_rep = vtk.vtkSliderRepresentation2D()
background_slider_widget.SetInteractor(render_window_interactor)
background_slider_widget.SetRepresentation(background_slider_rep)
background_slider_rep.SetMinimumValue(0.0)
background_slider_rep.SetMaximumValue(1.0)
background_slider_rep.SetValue(0.0)
background_slider_rep.SetTitleText("Background")

# Set the position for the background slider in the top right corner
background_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
background_slider_rep.GetPoint1Coordinate().SetValue(0.7, 0.8)
background_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
background_slider_rep.GetPoint2Coordinate().SetValue(0.9, 0.8)  # Adjust the y-coordinate to make it vertical

# Set the size of the slider components (same as azimuth slider)
background_slider_rep.SetSliderLength(0.02)
background_slider_rep.SetSliderWidth(0.03)
background_slider_rep.SetEndCapLength(0.01)
background_slider_rep.SetEndCapWidth(0.03)
background_slider_rep.SetTubeWidth(0.005)
background_slider_rep.SetLabelFormat("%3.1lf")
background_slider_rep.SetTitleHeight(0.02)
background_slider_rep.SetLabelHeight(0.02)

background_slider_widget.AddObserver("InteractionEvent", background_slider_callback)

# add a transparency slider
transparency_slider_widget = vtk.vtkSliderWidget()
transparency_slider_rep = vtk.vtkSliderRepresentation2D()
transparency_slider_widget.SetInteractor(render_window_interactor)
transparency_slider_widget.SetRepresentation(transparency_slider_rep)
transparency_slider_rep.SetMinimumValue(0.0)
transparency_slider_rep.SetMaximumValue(1.0)
transparency_slider_rep.SetValue(1.0)
transparency_slider_rep.SetTitleText("Opacity")

# Set the position for the transparency slider in the top right corner
transparency_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
transparency_slider_rep.GetPoint1Coordinate().SetValue(0.7, 0.7)
transparency_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
transparency_slider_rep.GetPoint2Coordinate().SetValue(0.9, 0.7)  # Adjust the y-coordinate to make it vertical

# Set the size of the slider components (same as azimuth slider)
transparency_slider_rep.SetSliderLength(0.02)
transparency_slider_rep.SetSliderWidth(0.03)
transparency_slider_rep.SetEndCapLength(0.01)
transparency_slider_rep.SetEndCapWidth(0.03)
transparency_slider_rep.SetTubeWidth(0.005)
transparency_slider_rep.SetLabelFormat("%3.1lf")
transparency_slider_rep.SetTitleHeight(0.02)
transparency_slider_rep.SetLabelHeight(0.02)

transparency_slider_widget.AddObserver("InteractionEvent", opacity_slider_callback)




# add horizontal scale ruler   
ruler = vtk.vtkScalarBarActor()
ruler.SetLookupTable(color_transfer_function)
ruler.SetTitle("Color Scale")
ruler.SetNumberOfLabels(3)
ruler.SetMaximumWidthInPixels(50)
ruler.SetMaximumHeightInPixels(200)
ruler.SetPosition(0.9, 0.1)
#ruler.SetOrientationToVertical()
ruler.SetLabelFormat("%3.0lf")
ruler.SetTitleRatio(1)
ruler.SetDrawAnnotations(1)
ruler.SetAnnotationTextScaling(1)
# set font size
ruler.GetLabelTextProperty().SetFontSize(12)

renderer.AddActor(ruler)

# Create a plane widget to slice the volume
plane = vtk.vtkPlane()
plane_widget = vtk.vtkImplicitPlaneWidget()
plane_widget.SetInteractor(render_window_interactor)
plane_widget.SetPlaceFactor(2.0)
plane_widget.PlaceWidget(volume.GetBounds())
plane_widget.AddObserver("InteractionEvent", plane_widget_callback)
#plane_widget.On()


# Create the button representation
show_hide_plane = vtk.vtkTexturedButtonRepresentation2D()
show_hide_plane.SetNumberOfStates(2)
show_hide_plane.SetButtonTexture(0, off_texture)  # off_texture is a vtkImageData for 'Off' state
show_hide_plane.SetButtonTexture(1, on_texture)   # on_texture is a vtkImageData for 'On' state

# Create the button widget
show_hide_plane_widget = vtk.vtkButtonWidget()
show_hide_plane_widget.SetInteractor(render_window_interactor)
show_hide_plane_widget.SetRepresentation(show_hide_plane)
show_hide_plane_widget.On()

# Set the callback for the button
show_hide_plane_widget.AddObserver("StateChangedEvent", button_callback)


# Create a text actor to display the information
text_actor = vtk.vtkTextActor()
text_actor.GetTextProperty().SetFontSize(14)
text_actor.GetTextProperty().SetColor(1, 1, 1)  # White color
text_actor.SetPosition(60, 5)
renderer.AddActor2D(text_actor)
render_window_interactor.AddObserver("LeftButtonPressEvent", click_callback)

# Create the slider widget for animation control
animation_slider_rep = vtk.vtkSliderRepresentation2D()
animation_slider_rep.SetMinimumValue(-3)
animation_slider_rep.SetMaximumValue(3)
animation_slider_rep.SetValue(0)
animation_slider_rep.SetTitleText("Animation Speed")
animation_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
animation_slider_rep.GetPoint1Coordinate().SetValue(0.01, 0.7)
animation_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
animation_slider_rep.GetPoint2Coordinate().SetValue(0.3, 0.7)

# Set the size of the slider components
animation_slider_rep.SetSliderLength(0.02)
animation_slider_rep.SetSliderWidth(0.03)
animation_slider_rep.SetEndCapLength(0.01)
animation_slider_rep.SetEndCapWidth(0.03)
animation_slider_rep.SetTubeWidth(0.005)
animation_slider_rep.SetLabelFormat("%3.1lf")
animation_slider_rep.SetTitleHeight(0.02)
animation_slider_rep.SetLabelHeight(0.02)

animation_slider = vtk.vtkSliderWidget()
animation_slider.SetInteractor(render_window_interactor)
animation_slider.SetRepresentation(animation_slider_rep)
animation_slider.AddObserver("InteractionEvent", animation_slider_callback)


render_window_interactor.Initialize()

# Set up a timer for the animation
render_window_interactor.AddObserver("TimerEvent", animate_camera)
timer_id = render_window_interactor.CreateRepeatingTimer(10)

# Render and interact
render_window.Render()
iso_slider_widget.EnabledOn()
azimuth_slider_widget.EnabledOn()
elevation_slider_widget.EnabledOn()
background_slider_widget.EnabledOn()
transparency_slider_widget.EnabledOn()
animation_slider.EnabledOn()
render_window_interactor.Start()


