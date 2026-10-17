import threading #To be able to define the events

shutdown_event = threading.Event() #The event which lets us close both screens at once
camera_change_event = threading.Event() #The event which lets us change the camera mode

frame = None #This is used to fix the issue of code bugging out when trying to take a photo before camera is ready
original_frame = None #This will be used to take a photo without the filters

camera_mode = 0 #To decide if the camera is internal or external

edge_cam = 0 #To be able to check if we want the edged cam open or not
blur_entry = 1 #For global we need it as 1 for no effects
sharpening_entry = None #For global we need it as none for no effects
contrast_entry = 1 #For global we need it as 1 for no effects
brightness_entry = 0 #For global we need it as 0 for no effects

blur_label = None #Indicator
brightness_label = None #Indicator
contrast_label = None #Indicator
sharpening_label = None #Indicator
edge_label = None #Indicator