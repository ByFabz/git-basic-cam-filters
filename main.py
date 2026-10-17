#Libraries
import threading 

#Modularization
import tkUI 
import camera    

t1 = threading.Thread(target = tkUI.window_CTk) #Assigns
t2 = threading.Thread(target = camera.window_CV) #Assigns
t1.start() #Starts
t2.start() #Starts