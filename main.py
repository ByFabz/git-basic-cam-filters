import cv2
import customtkinter as ctk
from tkinter import filedialog
import threading
import numpy as np



shutdown_event = threading.Event()

edge_cam = 0

blur_entry = 1 #for global we need it as 1 for no effects

sharpening_entry = None #for global we need it as none for no effects

contrast_entry = 1 #for global we need it as 1 for no effects

brightness_entry = 0#for global we need it as 0 for no effects


def take_photo():#take a photo button function

     file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  # Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],  # Allowed types
        title="Save photo as..."
    )
     
     if file_path:

        cv2.imwrite(file_path , frame)   
        label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
        label.place(x=450, y=340)  # Position the label
        app.after(4000, lambda: label.place_forget())  # Hide after 3 seconds


def brightness_dialog():#brightness button function
    global brightness_entry
    while True:
        dialog = ctk.CTkInputDialog(text="Type in the brightness level make sure to enter a number or a fraction enter 0 if you dont want to change the level", title="Brightness level") #istenen yazar
        input = dialog.get_input()

        if input is None or not input:
                return
        
        elif input:  # içinin boş olmadığından emin olur
            try:
                input = float(input)# float olur eğer stringse çalışmamasını sağlar intleri zaten çevirir
                brightness_entry = float(input)#sonrasında kullanmak için bize blur seviyesini bir değere atar
                return brightness_entry
            except ValueError:
                continue  


def blur_dialog(): #blur button function
        global blur_entry
        while True:
            dialog = ctk.CTkInputDialog(text="Type in the blur level make sure its an odd number like 3,5,7 etc: or 1 if you dont want to blur", title="Blur level") #istenen yazar
            input = dialog.get_input()
            
            if input is None or not input:
                return 
            
            elif input:  
                try:
                    input = int(input)
                    if int(input) > 0:#sıfırdan büyük mü?
                        if int(input) % 2 != 0:
                            blur_entry = int(input)#sonrasında kullanmak için bize blur seviyesini bir değere atar
                            return blur_entry
                except ValueError:
                    continue    


def contrast_dialog(): #contrast button function
    global contrast_entry
    while True:
        dialog = ctk.CTkInputDialog(text="Type in the contrast level, Dont type 0, Enter 1 if you dont want to change the level", title="Contrast level") #istenen yazar
        input = dialog.get_input()

        if input is None or not input:
            return
        
        elif input:
            try:
                input = float(input)# int olmasını doğrular
                if input != 0:
                    contrast_entry = float(input)#sonrasında kullanmak için bize blur seviyesini bir değere atar
                    return contrast_entry
            except ValueError:
                    continue  


def sharpening_dialog(): #sharpening button fonction
    global sharpening_entry
    while True:
        dialog = ctk.CTkInputDialog(text="Enter the sharpening level between 1 and 10 if you dont want to change something enter 0 ", title="Sharpening level") #istenen yazar
        input = dialog.get_input()


        if input is None or not input:
            return  # makes sure there is something

        elif input:
            try:
                input = float(input)# makes it float 

                if float(input) == 0: #0 means no change
                    sharpening_entry = None
                    return sharpening_entry
                    

                if 1 <= float(input):
                    sharpening_entry = float(input)#we will need it as a float
                    return sharpening_entry
                    
            except ValueError:
                continue  


def edge_detection_button():
    global edge_cam
    global frame
    global edges

    
                
    if edge_cam == 0:
            edge_cam = 1
    elif edge_cam == 1:
        edge_cam = 0


def get_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blurred, 100, 200)


def take_edged_photo():

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Kernel size (5x5)
    edged = cv2.Canny(blurred, 100, 200)  # The thresholds can be adjusted

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  # Default extension
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],  # Allowed types
        title="Save photo as..."
    )    

    if file_path:
        cv2.imwrite(file_path , edged)   
        label = ctk.CTkLabel(app, text= str(file_path) + ' is saved')
        label.place(x=450, y=340)  # Position the label
        app.after(4000, lambda: label.place_forget())  # Hide after 3 seconds
    
    

def window_CTk():#its with def because using threads requires it
    #global values
    global app


    app = ctk.CTk() #scren
    app.title('filters')#title
    app.geometry('1200x625')#geometry
    ctk.set_default_color_theme('blue')#button colors 
    ctk.set_appearance_mode('dark')#background


    button = ctk.CTkButton(app, text='Blur level' , command=blur_dialog) #blur button
    button.place(x = 520 , y = 10)#yeri vb

    button = ctk.CTkButton(app, text='Brightness level' , command=brightness_dialog) #brightness button
    button.place(x = 520 , y = 55)#yeri vb

    button = ctk.CTkButton(app, text='Contrast level' , command=contrast_dialog) #contrast button
    button.place(x = 520 , y = 100)#yeri vb

    button = ctk.CTkButton(app, text='Sharpening level' , command=sharpening_dialog) #sharpness button
    button.place(x = 520 , y = 145)#yeri vb

    button = ctk.CTkButton(app, text='Edge detection' , command=edge_detection_button) #sharpness button
    button.place(x = 520 , y = 190)

    button = ctk.CTkButton(app, text='Take a photo' , command=take_photo) #sharpness button
    button.place(x = 520 , y = 575)#yeri vb

    button = ctk.CTkButton(app, text='Take edged photo' , command=take_edged_photo) #sharpness button
    button.place(x = 520 , y = 530)#yeri vb

    def on_close():
        shutdown_event.set()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close)       

    def check_shutdown():
        if shutdown_event.is_set():
            app.destroy()
        else:
            app.after(100, check_shutdown)

    check_shutdown()

    app.mainloop()#loop the screen



def window_CV():#its with def because using threads requires it
    global frame
    global blur_entry
    global sharpening_entry
    global contrast_entry
    global brightness_entry
    global edge_cam
    

    # 0 means first camera, 1 means webcam etc.
    cap = cv2.VideoCapture(0)

    # Check camera
    if not cap.isOpened():
        print("Couldn't open camera")
        shutdown_event.set()

    # While the program is running
    while not shutdown_event.is_set():
        ret, frame = cap.read()

        # If no other frame can be returned break the loop
        if not ret:
            print("Can't recieve frame")
            shutdown_event.set()
            break

        # filters


        #sharpening kernel
        if sharpening_entry is not None:

            amount = float(sharpening_entry) / 10

            sharpening_kernel = np.array([
                                            [0, -amount, 0],
                                            [-amount, 1 + 4 * amount, -amount],
                                            [0, -amount, 0]
                                                        ], dtype=np.float32)
            
            frame = cv2.filter2D(frame, -1 , sharpening_kernel )


        frame = cv2.blur(frame, (int(blur_entry), int(blur_entry))) #blur

        frame = cv2.convertScaleAbs(frame, alpha=float(contrast_entry), beta=float(brightness_entry)) #alpha 0-1 means lowering bigger than 1 means adding contrast #negative beta means lowering positive means adding brightness
        
                                                                                     
        
        
        #display to show frame to take photos
        display = frame

        if edge_cam == 1:
            display = get_edges(frame)


        # Show display
        cv2.imshow('cam', display) # cam isim display ise kamera

        # When clicked 'q' or X wait for one second and then break
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('cam', cv2.WND_PROP_VISIBLE) < 1:
            shutdown_event.set()
            break
        
        
        
    cap.release() # Stop recording
    cv2.destroyAllWindows() # Destroys the page



t1 = threading.Thread(target = window_CTk)#assigns
t2 = threading.Thread(target = window_CV)#assigns
t1.start()#starts
t2.start()#starts