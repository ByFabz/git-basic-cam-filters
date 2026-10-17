#libraries
import cv2 #For the filters and capturing the screen
import customtkinter as ctk #For the UI
from tkinter import filedialog #For the take a picture functions
import threading #To be able to open and close both screens at once
import numpy as np #For the sharpening function


#modularization
import state
import button_commands 




def choose_internal_camera_mode(): #To change the variable which tells opencv to read which camera
    
    state.camera_mode = 0
    state.camera_change_event.set()

def choose_external_camera_mode():
    
    state.camera_mode = 1
    state.camera_change_event.set()


def take_normal_photo(): #Take a normal photo button function

    current = state.original_frame #To stop getting a None error

    if current is None: #Makes sure the camera has opened
        print('No camera image available')
        return

    normal_photo = current.copy() #Makes sure we get the exact moment they click the button
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
        title='Save photo as...'
    )

    if file_path: #Checks if we got a path
            try: #We will check if the user choose another file type then we listed
                saved = cv2.imwrite(file_path , normal_photo) 
    
                if saved: #If it saved we will print the normal saved answer
                    label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
                    label.place(x=220, y=235)  #Position the label
                    app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds
    
                else:
                    label = ctk.CTkLabel(app, text="Photo could not be saved")
                    label.place(x=220, y=235)  #Position the label
                    app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds
    
            except cv2.error as e: #If they did change the file type then it will not work
                label = ctk.CTkLabel(app, text=f"Error saving photo: {e}")
                label.place(x=220, y=235)  #Position the label
                app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds


def take_filtered_photo(): #Take a photo button function

    current = state.frame #To stop getting a None error

    if current is None: #Makes sure the camera has opened
        print("No camera image available")
        return

    photo = current.copy() #Makes sure we get the exact moment they click the button

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  #Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],  #Allowed types
        title="Save photo as..."
    )
     
    if file_path: #Checks if we got a path
        try: #We will check if the user choose another file type then we listed
            saved = cv2.imwrite(file_path , photo) 

            if saved: #If it saved we will print the normal saved answer
                label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
                label.place(x=220, y=235)  #Position the label
                app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds

            else:
                label = ctk.CTkLabel(app, text="Photo could not be saved")
                label.place(x=220, y=235)  #Position the label
                app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds

        except cv2.error as e: #If they did change the file type then it will not work
            label = ctk.CTkLabel(app, text=f"Error saving photo: {e}")
            label.place(x=220, y=235)  #Position the label
            app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds


def take_edged_photo():

    current = state.frame #To stop getting a None error

    if current is None: #Makes sure the camera has opened
        print("No camera image available")
        return
    
    edged = get_edges(current) #Uses the function which makes the edged cam also makes sure we get the moment where they click the button


    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", #Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")], #Allowed types
        title="Save photo as..."
    )    

    if file_path: #Checks if we got a path
            try: #We will check if the user choose another file type then we listed
                saved = cv2.imwrite(file_path , edged) 
    
                if saved: #If it saved we will print the normal saved answer
                    label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
                    label.place(x=220, y=235)  #Position the label
                    app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds
    
                else:
                    label = ctk.CTkLabel(app, text="Photo could not be saved")
                    label.place(x=220, y=235)  #Position the label
                    app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds
    
            except cv2.error as e: #If they did change the file type then it will not work
                label = ctk.CTkLabel(app, text=f"Error saving photo: {e}")
                label.place(x=220, y=235)  #Position the label
                app.after(5000, lambda: label.destroy())  #Destorys after 5 seconds


def get_edges(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blurred, 100, 200)

    
def window_CTk(): #The UI 

    global app

    app = ctk.CTk() #Scren
    app.title('filters') #Title
    app.geometry('700x350') #Geometry
    ctk.set_default_color_theme('blue') #Button colors 
    ctk.set_appearance_mode('dark') #Background

    #Filter buttons
    button = ctk.CTkButton(app, text='Blur level' , command=button_commands.blur_dialog) #Blur button
    button.place(x = 30 , y = 10) 

    button = ctk.CTkButton(app, text='Brightness level' , command=button_commands.brightness_dialog) #Brightness button
    button.place(x = 30 , y = 55)

    button = ctk.CTkButton(app, text='Contrast level' , command=button_commands.contrast_dialog) #Contrast button
    button.place(x = 30 , y = 100)

    button = ctk.CTkButton(app, text='Sharpening level' , command=button_commands.sharpening_dialog) #Sharpness button
    button.place(x = 30 , y = 145)

    button = ctk.CTkButton(app, text='Edge detection' , command=button_commands.edge_detection_button) #Edge detection button
    button.place(x = 30 , y = 190)

    button = ctk.CTkButton(app, text='Reset the filters' , command=button_commands.reset_button) #Reset the filters button
    button.place(x = 30 , y = 235)


    #Take a photo buttons
    button = ctk.CTkButton(app, text='Take a filtered photo' , command=take_filtered_photo) #Take a normal photo button
    button.place(x = 470 , y = 145)

    button = ctk.CTkButton(app, text='Take a normal photo' , command=take_normal_photo) #Take a photo with the filters button
    button.place(x = 470 , y = 100)

    button = ctk.CTkButton(app, text='Take an edged photo' , command=take_edged_photo) #Take an edged photo button
    button.place(x = 470 , y = 190)


    #Camera mode buttons
    button = ctk.CTkButton(app, text='Internal Camera' , command=choose_internal_camera_mode) #Choose internal camera button
    button.place(x = 470 , y = 10)

    button = ctk.CTkButton(app, text='External Camera' , command=choose_external_camera_mode) #Choose external camera button
    button.place(x = 470 , y = 55)


    #Indicator labels
    state.blur_label = ctk.CTkLabel(app, text="Blur: 1")
    state.blur_label.place(x=220, y=10)

    state.contrast_label = ctk.CTkLabel(app, text="Contrast: 1")
    state.contrast_label.place(x=220, y=100)

    state.sharpening_label = ctk.CTkLabel(app, text="Sharpening: 0")
    state.sharpening_label.place(x=220, y=145)

    state.brightness_label = ctk.CTkLabel(app, text="Brightness: 0")
    state.brightness_label.place(x=220, y=55)

    state.edge_label = ctk.CTkLabel(app, text="Edge detection is closed")
    state.edge_label.place(x=220, y=190)

    


    def on_close(): #To start the shutdown event

        state.shutdown_event.set()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close) #Calls the function which starts the shutdown event       

    def check_shutdown(): #Checks if the shutdown event has been started every 100 milliseconds 

        if state.shutdown_event.is_set():
            app.destroy()
        else:
            app.after(100, check_shutdown)

    check_shutdown() #Calls the function to check the shutdown event

    app.mainloop() #Starts the screen


def window_CV(): #The camera


    cap = None #We will use it for the finally part

    try: #We use try and finally just so that if we get an unexpected error we can make sure to close tkinkter
        #Outer loop to check the cam
        while not state.shutdown_event.is_set():

            cap = cv2.VideoCapture(state.camera_mode) #Decides if the camera is external or internal


            if not cap.isOpened(): #Checks if the camera opened
                print("Can't open camera")
                cap.release() #We could not open it so we use release

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
                while not state.shutdown_event.is_set():
                    if state.camera_change_event.wait(timeout=0.1):
                        state.camera_change_event.clear()
                        break

                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("q") or cv2.getWindowProperty(
                        "Camera", cv2.WND_PROP_VISIBLE
                    ) < 1:
                        state.shutdown_event.set()
                        break

                    if state.shutdown_event.is_set():
                        break

                continue


            #Inside loop to add filters
            while not state.shutdown_event.is_set():


                ret, raw_frame = cap.read()
                

                if not ret: #Checks if we can receive the frames
                    print("Can't receive frame")

                    state.frame = None #This clears the old frame if the camera suddenly stops working
                    state.original_frame = None #This clears the old frame if the camera suddenly stops working

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


                    while not state.shutdown_event.is_set():
                        if state.camera_change_event.wait(timeout=0.1):
                            state.camera_change_event.clear()
                            break

                        key = cv2.waitKey(1) & 0xFF

                        if key == ord("q") or cv2.getWindowProperty(
                            "Camera", cv2.WND_PROP_VISIBLE
                        ) < 1:
                            state.shutdown_event.set()
                            break

                    if state.shutdown_event.is_set():
                        break

                    break


                state.original_frame = raw_frame.copy() #Keeps the original camera as a copy to use it later if needed


                #Filters
                filtered = raw_frame
                #Sharpening kernel
                if state.sharpening_entry is not None:

                    amount = float(state.sharpening_entry) / 10

                    sharpening_kernel = np.array([
                                                    [0, -amount, 0],
                                                    [-amount, 1 + 4 * amount, -amount],
                                                    [0, -amount, 0]
                                                                ], dtype=np.float32)
                    
                    filtered = cv2.filter2D(filtered, -1 , sharpening_kernel )


                filtered = cv2.blur(filtered, (int(state.blur_entry), int(state.blur_entry))) #Blur

                filtered = cv2.convertScaleAbs(filtered, alpha=float(state.contrast_entry), beta=float(state.brightness_entry))
                #bigger than 1 means adding contrast 
                #negative beta means lowering positive means adding brightness

                state.frame = filtered
                
                                                                                            
                
                
                #We use display on the screen and frame to take photos
                display = filtered

                if state.edge_cam == 1: #Checks if the user switched on the edge detection
                    display = get_edges(filtered)


                #Shows display
                cv2.imshow('Camera', display) 

                #Checks if the user clicked the change the camera button after the camera has opened for once
                if state.camera_change_event.is_set():
                    state.camera_change_event.clear()
                    break


                #When clicked 'q' or X wait for one second and then break
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
                    state.shutdown_event.set()
                    break
            
            
            cap.release() #Stops catching the camera

    finally:
        if cap is not None:
            cap.release()
        state.shutdown_event.set()
        cv2.destroyAllWindows()        





t1 = threading.Thread(target = window_CTk) #Assigns
t2 = threading.Thread(target = window_CV) #Assigns
t1.start() #Starts
t2.start() #Starts