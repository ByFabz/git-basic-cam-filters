import cv2 #For the filters and capturing the screen
import customtkinter as ctk #For the UI
from tkinter import filedialog #For the take a picture functions
import threading #To be able to open and close both screens at once
import numpy as np #For the sharpening function
import math #To be able to block inputs such as nan or inf
import time


shutdown_event = threading.Event() #The event which lets us close both screens at once

camera_change_event = threading.Event()

frame = None #This is used to fix the issue of code bugging out when trying to take a photo before camera is ready

original_frame = None #This will be used to take a photo without the filters

camera_mode = 0 #To decide if the camera is internal or external

edge_cam = 0 #To be able to check if we want the edged cam open or not

blur_entry = 1 #For global we need it as 1 for no effects

sharpening_entry = None #For global we need it as none for no effects

contrast_entry = 1 #For global we need it as 1 for no effects

brightness_entry = 0 #For global we need it as 0 for no effects

def choose_internal_camera_mode(): #To change the variable which tells opencv to read which camera
    global camera_mode
    camera_mode = 0
    camera_change_event.set()

def choose_external_camera_mode():
    global camera_mode
    camera_mode = 1
    camera_change_event.set()


def take_normal_photo(): #Take a normal photo button function

    if original_frame is None: #Makes sure the camera has opened
        print('Camera has not opened yet')
        return

    normal_photo = original_frame.copy() #Makes sure we get the exact moment they click the button
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
        title='Save photo as...'
    )

    if file_path:
        cv2.imwrite(file_path , normal_photo)
        label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
        label.place(x=450, y=340)  #Position the label
        app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds


def take_filtered_photo(): #Take a photo button function

    if frame is None: #Makes sure the camera has opened
        print("Camera has not opened yet")
        return

    photo = frame.copy() #Makes sure we get the exact moment they click the button

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  #Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],  #Allowed types
        title="Save photo as..."
    )
     
    if file_path:

        cv2.imwrite(file_path , photo)   
        label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
        label.place(x=450, y=340)  #Position the label
        app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds


def take_edged_photo():

    if frame is None: #Makes sure the camera has opened
        print("Camera has not opened yet")
        return
    
    edged = get_edges(frame) #Uses the function which makes the edged cam also makes sure we get the moment where they click the button


    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", #Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")], #Allowed types
        title="Save photo as..."
    )    

    if file_path:
        cv2.imwrite(file_path , edged)   
        label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
        label.place(x=450, y=340) #Position the label
        app.after(5000, lambda: label.destroy()) #Destorys it after 5 seconds


def brightness_dialog(): #Brightness button function
    global brightness_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the brightness level between -255 and 255. Make sure to enter a number. Enter 0 if you dont want to change the level", title="Brightness level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
                return
        
        elif input: #Checks if the input is empty

            try:
                input = float(input) #Checks if the input is right and then assigns it
                if -255 <= input <= 255 and math.isfinite(input):
                    brightness_entry = input
                    return brightness_entry
            except ValueError: #Asks again if the input was wrong
                continue  


def blur_dialog(): #Blur button function
    global blur_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the blur level between 1 and 31. Make sure its a whole and odd number like 3,5,7 etc. Enter 1 if you dont want to blur", title="Blur level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
                return 
            
        elif input: #Checks if the input is empty

            try:
                input = int(input)
                if 1 <= input <= 31:
                    if input % 2 != 0:
                        blur_entry = input
                        return blur_entry
                    
            except ValueError: #Asks again if the input was wrong
                continue    


def contrast_dialog(): #Contrast button function
    global contrast_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the contrast level between 1 and 10. Enter 1 if you dont want to change the level", title="Contrast level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
            return
        
        elif input: #Checks if the input is empty

            try:
                input = float(input)
                if math.isfinite(input) and 1<= input <= 10: #Makes sure the input is right
                    contrast_entry = input #Assigns it
                    return contrast_entry
                
            except ValueError: #Asks again if the input was wrong
                    continue  


def sharpening_dialog(): #Sharpening button fonction


    global sharpening_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Enter the sharpening level between 0 and 50. If you dont want to change something enter 0 ", title="Sharpening level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
            return  

        elif input:
            try:
                input = float(input) #Makes sure the input is a number 

                if not math.isfinite(input): #Makes sure the input is not nan or inf
                    continue

                if input == 0: #0 means no change
                    sharpening_entry = None
                    return sharpening_entry
                    
                if 0 < input <= 50: 
                    sharpening_entry = input #Assigns the value
                    return sharpening_entry
                    
            except ValueError: #Asks again if the input was wrong
                continue  


def edge_detection_button():
    global edge_cam


    if edge_cam == 0:
            edge_cam = 1

    elif edge_cam == 1:
        edge_cam = 0


def get_edges(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blurred, 100, 200)

    
def window_CTk(): #The UI 

    global app


    app = ctk.CTk() #Scren
    app.title('filters') #Title
    app.geometry('1200x625') #Geometry
    ctk.set_default_color_theme('blue') #Button colors 
    ctk.set_appearance_mode('dark') #Background


    button = ctk.CTkButton(app, text='Blur level' , command=blur_dialog) #Blur button
    button.place(x = 520 , y = 10) 

    button = ctk.CTkButton(app, text='Brightness level' , command=brightness_dialog) #Brightness button
    button.place(x = 520 , y = 55)

    button = ctk.CTkButton(app, text='Contrast level' , command=contrast_dialog) #Contrast button
    button.place(x = 520 , y = 100)

    button = ctk.CTkButton(app, text='Sharpening level' , command=sharpening_dialog) #Sharpness button
    button.place(x = 520 , y = 145)

    button = ctk.CTkButton(app, text='Edge detection' , command=edge_detection_button) #Edge detection button
    button.place(x = 520 , y = 190)

    button = ctk.CTkButton(app, text='Reset the filters' , command=reset_button) #Reset the filters button
    button.place(x = 520 , y = 235)

    button = ctk.CTkButton(app, text='Take a photo without the filters' , command=take_normal_photo) #Take a normal photo button
    button.place(x = 520 , y = 495)

    button = ctk.CTkButton(app, text='Take a photo' , command=take_filtered_photo) #Take a photo with the filters button
    button.place(x = 520 , y = 530)

    button = ctk.CTkButton(app, text='Take an edged photo' , command=take_edged_photo) #Take an edged photo button
    button.place(x = 520 , y = 575)

    button = ctk.CTkButton(app, text='Internal Camera' , command=choose_internal_camera_mode) #Choose internal camera button
    button.place(x = 700 , y = 575)

    button = ctk.CTkButton(app, text='External Camera' , command=choose_external_camera_mode) #Choose external camera button
    button.place(x = 700 , y = 610)

    


    def on_close(): #To start the shutdown event

        shutdown_event.set()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close) #Calls the function which starts the shutdown event       

    def check_shutdown(): #Checks if the shutdown event has been started every 100 milliseconds 

        if shutdown_event.is_set():
            app.destroy()
        else:
            app.after(100, check_shutdown)

    check_shutdown() #Calls the function to check the shutdown event

    app.mainloop() #Starts the screen


def window_CV(): #The camera

    global frame
    global original_frame #We put it before applying the filters to have the camera without the filters

    #Outer loop to check the cam
    while not shutdown_event.is_set():

        cap = cv2.VideoCapture(camera_mode) #Decides if the camera is external or internal


        if not cap.isOpened(): #Checks if the camera opened
            print("Can't open camera")
            cap.release #We could not open it so we use release

            #A waiting screen which tells the problem
            waiting_screen = np.zeros((480,640,3), dtype=np.uint8) 

            cv2.putText(
                waiting_screen,
                "Camera not found",
                (150, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.imshow("Camera", waiting_screen)
            while not shutdown_event.is_set():
                if camera_change_event.wait(timeout=0.1):
                    camera_change_event.clear()
                    break

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q") or cv2.getWindowProperty(
                    "Camera", cv2.WND_PROP_VISIBLE
                ) < 1:
                    shutdown_event.set()
                    break

                if shutdown_event.is_set():
                    break

            continue


        #Inside loop to add filters
        while not shutdown_event.is_set():


            
            ret, frame = cap.read()
            original_frame = frame.copy() #Keeps the original camera as a copy to use it later if needed

            

            if not ret: #Checks if we can receive the frames
                print("Can't receive frame")

                #A waiting screen which tells the problem
                waiting_screen = np.zeros((480, 640, 3), dtype=np.uint8)

                cv2.putText(
                    waiting_screen,
                    "No frame received",
                    (150, 220),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )

                cv2.imshow("Camera", waiting_screen)


                while not shutdown_event.is_set():
                    if camera_change_event.wait(timeout=0.1):
                        camera_change_event.clear()
                        break

                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("q") or cv2.getWindowProperty(
                        "Camera", cv2.WND_PROP_VISIBLE
                    ) < 1:
                        shutdown_event.set()
                        break

                if shutdown_event.is_set():
                    break

                break

            
            #Filters

            #Sharpening kernel
            if sharpening_entry is not None:

                amount = float(sharpening_entry) / 10

                sharpening_kernel = np.array([
                                                [0, -amount, 0],
                                                [-amount, 1 + 4 * amount, -amount],
                                                [0, -amount, 0]
                                                            ], dtype=np.float32)
                
                frame = cv2.filter2D(frame, -1 , sharpening_kernel )


            frame = cv2.blur(frame, (int(blur_entry), int(blur_entry))) #Blur

            frame = cv2.convertScaleAbs(frame, alpha=float(contrast_entry), beta=float(brightness_entry)) 
            #Alpha 0-1 means lowering bigger than 1 means adding contrast 
            #negative beta means lowering positive means adding brightness
            
                                                                                        
            
            
            #We use display on the screen and frame to take photos
            display = frame

            if edge_cam == 1: #Checks if the user switched on the edge detection
                display = get_edges(frame)


            #Shows display
            cv2.imshow('Camera', display) 

            #Checks if the user clicked the change the camera button after the camera has opened for once
            if camera_change_event.is_set():
                camera_change_event.clear()
                break


            #When clicked 'q' or X wait for one second and then break
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
                shutdown_event.set()
                break
        
        
        cap.release() #Stops catching the camera




    cv2.destroyAllWindows() #Destroys the camera screen


def reset_button(): #Turns every valuable back to how they were to reset the filters
    global blur_entry
    global contrast_entry
    global sharpening_entry
    global brightness_entry
    global edge_cam

    blur_entry = 1
    contrast_entry = 1
    sharpening_entry = None
    brightness_entry = 0
    edge_cam = 0



t1 = threading.Thread(target = window_CTk) #Assigns
t2 = threading.Thread(target = window_CV) #Assigns
t1.start() #Starts
t2.start() #Starts