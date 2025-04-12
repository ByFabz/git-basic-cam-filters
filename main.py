import cv2
import customtkinter as ctk
from tkinter import filedialog
import threading
import numpy as np



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
     
def brightness_dialog():#brightness button function
    global brightness_entry
    while True:
        dialog = ctk.CTkInputDialog(text="Type in the brightness level make sure to enter a number or a fraction enter 0 if you dont want to change the level", title="Brightness level") #istenen yazar
        deneme = dialog.get_input()

        if deneme:  # içinin boş olmadığından emin olur
                try:
                    deneme = float(deneme)# float olur eğer stringse çalışmamasını sağlar intleri zaten çevirir
                    brightness_entry = float(deneme)#sonrasında kullanmak için bize blur seviyesini bir değere atar
                    return brightness_entry
                except ValueError:
                    continue  

def blur_dialog(): #blur button function
        global blur_entry
        while True:
            dialog = ctk.CTkInputDialog(text="Type in the blur level make sure its an odd number like 3,5,7 etc: or 1 if you dont want to blur", title="Blur level") #istenen yazar
            deneme = dialog.get_input()
            
            if deneme:  # içinin boş olmadığından emin olur
                try:
                    deneme == int(deneme)
                    if int(deneme) > 0:#sıfırdan büyük mü?
                        if int(deneme) % 2 != 0:
                            blur_entry = int(deneme)#sonrasında kullanmak için bize blur seviyesini bir değere atar
                            return blur_entry
                except ValueError:
                    continue    
                    
def contrast_dialog(): #contrast button function
    global contrast_entry
    while True:
        dialog = ctk.CTkInputDialog(text="Type in the contrast level make sure to enter a number or a fraction enter 1 if you dont want to change the level", title="Brightness level") #istenen yazar
        deneme = dialog.get_input()

        if deneme:  # içinin boş olmadığından emin olur
                try:
                    deneme = float(deneme)# int olmasını doğrular
                    if contrast_entry >= 1:
                        contrast_entry = float(deneme)#sonrasında kullanmak için bize blur seviyesini bir değere atar
                        return contrast_entry
                except ValueError:
                    continue  

def sharpening_dialog(): #sharpening button fonction
    global sharpening_entry
    while True:
        dialog = ctk.CTkInputDialog(text="Enter the sharpening level make sure the number is maximum 10 and bigger than 1 to see changes if you dont want to change something enter 0 anything bigger than 10 will look weird and sometimes bug the code", title="Blur level") #istenen yazar
        deneme = dialog.get_input()


        if deneme:  # makes sure there is something
                try:
                    deneme = float(deneme)# makes it float 

                    if float(deneme) == 0: #0 means no change
                        sharpening_entry = None
                        return sharpening_entry
                    

                    if 1 < float(deneme):
                        sharpening_entry = float(deneme)#we will need it as a float
                        return sharpening_entry
                    
                except ValueError:
                    continue  
    


def window_CTk():#its with def because using threads requires it
    #global values
    global blur_entry
    global sharpening_entry
    global contrast_entry
    global brightness_entry

    
    app = ctk.CTk() #scren
    app.title('filters')#title
    app.geometry('1200x625')#geometry
    ctk.set_default_color_theme('blue')#button colors 
    ctk.set_appearance_mode('dark')#background


    button = ctk.CTkButton(app, text='Blur level' , command=blur_dialog) #blur button
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 10)#yeri vb

    button = ctk.CTkButton(app, text='Brightness level' , command=brightness_dialog) #brightness button
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 55)#yeri vb

    button = ctk.CTkButton(app, text='Contrast level' , command=contrast_dialog) #contrast button
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 100)#yeri vb

    button = ctk.CTkButton(app, text='Sharpening level' , command=sharpening_dialog) #sharpness button
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 145)#yeri vb

    button = ctk.CTkButton(app, text='Take a photo' , command=take_photo) #sharpness button
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 575)#yeri vb


    app.mainloop()#loop the screen
    

def window_CV():#its with def because using threads requires it
    global frame
    global blur_entry
    global sharpening_entry
    global contrast_entry
    global brightness_entry
    
    # 0 means first camera, 1 means webcam etc.
    cap = cv2.VideoCapture(0)

    # Check camera
    if not cap.isOpened():
        print("Couldn't open camera")
        exit()

    # While the program is running
    while True:
        ret, frame = cap.read()

        # If no other frame can be returned break the loop
        if not ret:
            print("Can't recieve frame")
            break


        #sharpening kernel
        sharpening_kernel = np.array([
                                        [0, -0.5, 0],
                                        [-0.5, sharpening_entry, -0.5],
                                        [0, -0.5, 0]
                                                    ])
    

        # filters
        frame = cv2.blur(frame, (int(blur_entry), int(blur_entry))) #blur

        frame = cv2.convertScaleAbs(frame, alpha=float(contrast_entry), beta=float(brightness_entry)) #alpha 0-1 means lowering bigger than 1 means adding contrast #negative beta means lowering positive means adding brightness
        
        if sharpening_entry: #needed to see if it was none or not                                                                              
            frame = cv2.filter2D(frame, -1 , sharpening_kernel )

        
        # Show frames
        cv2.imshow('cam', frame) # cam isim frame ise kamera

        # When clicked 'q' wait for one second and then break
        if cv2.waitKey(1) == ord('q'):
            break


    cap.release() # Stop recording
    cv2.destroyAllWindows() # Destroys the page



t1 = threading.Thread(target = window_CTk)#assigns
t2 = threading.Thread(target = window_CV)#assigns
t1.start()#starts
t2.start()#starts