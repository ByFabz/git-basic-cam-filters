import customtkinter as ctk

import state
import button_commands
import photo_functions
from EdgeDetection_and_extras import (choose_external_camera_mode , choose_internal_camera_mode)

def window_CTk(): #The UI 


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
    button = ctk.CTkButton(app, text='Take a filtered photo' , command=lambda:photo_functions.take_filtered_photo(app)) #Take a normal photo button
    button.place(x = 470 , y = 145)

    button = ctk.CTkButton(app, text='Take a normal photo' , command=lambda:photo_functions.take_normal_photo(app)) #Take a photo with the filters button
    button.place(x = 470 , y = 100)

    button = ctk.CTkButton(app, text='Take an edged photo' , command=lambda:photo_functions.take_edged_photo(app)) #Take an edged photo button
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