import cv2 #For the filters and capturing the screen
import customtkinter as ctk #For the UI
from tkinter import filedialog #For the take a picture functions
import threading #To be able to open and close both screens at once
import numpy as np #For the sharpening function



shutdown_event = threading.Event() #The event which lets us close both screens at once

edge_cam = 0 #To be able to check if we want the edged cam open or not

blur_entry = 1 #For global we need it as 1 for no effects

sharpening_entry = None #For global we need it as none for no effects

contrast_entry = 1 #For global we need it as 1 for no effects

brightness_entry = 0 #For global we need it as 0 for no effects


def take_photo(): #Take a photo button function


     file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  #Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],  #Allowed types
        title="Save photo as..."
    )
     
     if file_path:

        cv2.imwrite(file_path , frame)   
        label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
        label.place(x=450, y=340)  #Position the label
        app.after(4000, lambda: label.place_forget())  #Hide after 4 seconds


def brightness_dialog(): #Brightness button function
    global brightness_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the brightness level make sure to enter a number enter 0 if you dont want to change the level", title="Brightness level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
                return
        
        elif input: #Checks if the input is empty

            try:
                brightness_entry = float(input) #Checks if the input is right and then assigns it
                return brightness_entry
            
            except ValueError: #Asks again if the input was wrong
                continue  


def blur_dialog(): #Blur button function
    global blur_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the blur level make sure its an odd number like 3,5,7 etc: or 1 if you dont want to blur", title="Blur level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
                return 
            
        elif input: #Checks if the input is empty

            try:
                input = float(input)
                if input > 0:
                    if input % 2 != 0:
                        blur_entry = input
                        return blur_entry
                    
            except ValueError: #Asks again if the input was wrong
                continue    


def contrast_dialog(): #Contrast button function
    global contrast_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the contrast level, Dont type 0, Enter 1 if you dont want to change the level", title="Contrast level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
            return
        
        elif input: #Checks if the input is empty

            try:
                input = float(input)
                if input != 0 and input > 0: #We dont want to enter 0 because that would mean just a black screen
                    contrast_entry = input #Checks if the input is right and then assigns it
                    return contrast_entry
                
            except ValueError: #Asks again if the input was wrong
                    continue  


def sharpening_dialog(): #Sharpening button fonction


    global sharpening_entry


    while True:
        dialog = ctk.CTkInputDialog(text="Enter the sharpening level if you dont want to change something enter 0 ", title="Sharpening level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
            return  

        elif input:
            try:
                input = float(input) #Makes sure the input is a number 

                if input == 0: #0 means no change
                    sharpening_entry = None
                    return sharpening_entry
                    
                if 1 <= input: 
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


def take_edged_photo():

    edged = get_edges(frame) #Uses the function which makes the edged cam


    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", #Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")], #Allowed types
        title="Save photo as..."
    )    

    if file_path:
        cv2.imwrite(file_path , edged)   
        label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
        label.place(x=450, y=340) #Position the label
        app.after(4000, lambda: label.place_forget()) #Hide after 4 seconds
    
    
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

    button = ctk.CTkButton(app, text='Take a photo' , command=take_photo) #Take a photo button
    button.place(x = 520 , y = 575)

    button = ctk.CTkButton(app, text='Take edged photo' , command=take_edged_photo) #Take edged photo button
    button.place(x = 520 , y = 530)


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
    
    
    cap = cv2.VideoCapture(0) #0 means the first camera, 1 means webcam etc.


    if not cap.isOpened(): #Checks if the camera opened
        print("Couldn't open camera")
        shutdown_event.set()

    #While the program is running
    while not shutdown_event.is_set():
        ret, frame = cap.read()

        #If no other frame can be returned break the loop
        if not ret:
            print("Can't recieve frame")
            shutdown_event.set()
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


        #When clicked 'q' or X wait for one second and then break
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
            shutdown_event.set()
            break
        
        
    cap.release() #Stops catching the camera
    cv2.destroyAllWindows() #Destroys the camera screen


t1 = threading.Thread(target = window_CTk) #Assigns
t2 = threading.Thread(target = window_CV) #Assigns
t1.start() #Starts
t2.start() #Starts