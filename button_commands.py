#Libraries
import customtkinter as ctk
import state
import math

def brightness_dialog(): #Brightness button function
    


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the brightness level between -255 and 255. Make sure to enter a number. Enter 0 if you dont want to change the level", title="Brightness level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
                return
        
        elif input: #Checks if the input is empty

            try:
                input = float(input) #Checks if the input is right and then assigns it
                if -255 <= input <= 255 and math.isfinite(input):
                    state.brightness_entry = input
                    state.brightness_label.configure(text = f'Brightness: {state.brightness_entry}')
                    return 
            except ValueError: #Asks again if the input was wrong
                continue  

def blur_dialog(): #Blur button function


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
                        state.blur_entry = input
                        state.blur_label.configure(text = f'Blur: {state.blur_entry}')
                        return 
                    
            except ValueError: #Asks again if the input was wrong
                continue  

def contrast_dialog(): #Contrast button function
    


    while True:
        dialog = ctk.CTkInputDialog(text="Type in the contrast level between 1 and 10. Enter 1 if you dont want to change the level", title="Contrast level") #Dialog
        input = dialog.get_input()


        if input is None or not input: #To be able to close the input when the user clicks cancel or ok
            return
        
        elif input: #Checks if the input is empty

            try:
                input = float(input)
                if math.isfinite(input) and 1<= input <= 10: #Makes sure the input is right
                    state.contrast_entry = input #Assigns it
                    state.contrast_label.configure(text = f'Contrast: {state.contrast_entry}')
                    return 
                
            except ValueError: #Asks again if the input was wrong
                    continue  

def sharpening_dialog(): #Sharpening button fonction

    


    


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
                    state.sharpening_entry = None
                    state.sharpening_label.configure(text = f'Sharpening: 0')
                    return 
                    
                if 0 < input <= 50: 
                    state.sharpening_entry = input #Assigns the value
                    state.sharpening_label.configure(text = f'Sharpening: {state.sharpening_entry}')
                    return 
                    
            except ValueError: #Asks again if the input was wrong
                continue 

def edge_detection_button(): #Turns the edge detection on or of
    


    if state.edge_cam == 0:
            state.edge_cam = 1
            state.edge_label.configure(text = 'Edge detection is open')

    elif state.edge_cam == 1:
        state.edge_cam = 0
        state.edge_label.configure(text = 'Edge detection is closed')

def reset_button(): #Turns every valuable back to how they were by assigning them to their base values to reset the filters
    
    

    state.blur_entry = 1
    state.contrast_entry = 1
    state.sharpening_entry = None
    state.brightness_entry = 0
    state.edge_cam = 0

    state.blur_label.configure(text = "Blur: 1")
    state.contrast_label.configure(text = "Contrast: 1")
    state.sharpening_label.configure(text = "Sharpening: 0")
    state.brightness_label.configure(text = "Brightness: 0")
    state.edge_label.configure(text= "Edge detection is closed")                     