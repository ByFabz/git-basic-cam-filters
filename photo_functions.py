import customtkinter as ctk
import state
from tkinter import filedialog
import cv2

import filters


def take_normal_photo(app): #Take a normal photo button function

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


def take_filtered_photo(app): #Take a photo button function

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


def take_edged_photo(app):

    current = state.frame #To stop getting a None error

    if current is None: #Makes sure the camera has opened
        print("No camera image available")
        return
    
    edged = filters.get_edges(current) #Uses the function which makes the edged cam also makes sure we get the moment where they click the button


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