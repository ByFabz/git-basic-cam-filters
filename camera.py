#Libraries
import cv2
import numpy as np

#Modularization
import state
from EdgeDetection_and_extras import get_edges

def window_CV(): #The camera

    cap = None #We will use it for the finally part

    try: #We use try and finally just so that if we get an unexpected error we can make sure to close tkinkter
        #Outer loop to check the cam
        while not state.shutdown_event.is_set():

            cap = cv2.VideoCapture(state.camera_mode) #Decides if the camera is external or internal

            if not cap.isOpened(): #Checks if the camera opened

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
                filtered = raw_frame #Makes a new variable to apply the filters

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

                state.frame = filtered #Gets the filtered version to take photos 
                                                                                            
                #We use display on the screen 
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