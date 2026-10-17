#Libraries
import customtkinter as ctk
from tkinter import filedialog
import cv2

#Modularization
from EdgeDetection_and_extras import get_edges
import state

def show_message(app, message):  # Displays a message for 5 seconds
    label = ctk.CTkLabel(app, text=message)
    label.place(x=220, y=235)
    app.after(5000, lambda: label.destroy())

def save_photo(app, photo):  # Handles the photo saving process
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
        title="Save photo as..."
    )

    if not file_path:
        return

    try:
        saved = cv2.imwrite(file_path, photo)

        if saved:
            show_message(app, f"{file_path} is saved")
        else:
            show_message(app, "Photo could not be saved")

    except cv2.error as e:
        show_message(app, f"Error saving photo as: {e}")

def take_normal_photo(app): #Take a normal photo button function

    current = state.original_frame #To stop getting a None error

    if current is None: #Makes sure the camera has opened
        show_message(app, "No camera image available")
        return

    normal_photo = current.copy() #Makes sure we get the exact moment they click the button
    save_photo(app,normal_photo)
    
def take_filtered_photo(app): #Take a photo button function

    current = state.frame #To stop getting a None error

    if current is None: #Makes sure the camera has opened
        show_message(app, "No camera image available")
        return

    photo = current.copy() #Makes sure we get the exact moment they click the button
    save_photo(app,photo)

def take_edged_photo(app):

    current = state.frame #To stop getting a None error

    if current is None: #Makes sure the camera has opened
        show_message(app, "No camera image available")
        return
    
    edged = get_edges(current) #Uses the function which makes the edged cam also makes sure we get the moment where they click the button
    save_photo(app,edged)