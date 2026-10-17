import cv2 #Get_edges function uses it

import state #To be able to use the main variables

def get_edges(img): #The function which turns the img to edged version of it

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blurred, 100, 200)

def choose_internal_camera_mode(): #To change the variable which tells opencv to read which camera
    
    state.camera_mode = 0
    state.camera_change_event.set()

def choose_external_camera_mode():
    
    state.camera_mode = 1
    state.camera_change_event.set()