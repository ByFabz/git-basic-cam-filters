import cv2
import customtkinter as ctk
import threading
import numpy as np



blur_entry = 1 #sonrasında globale eklemek için atar etkilemeyen hali 1dir

sharpening_entry = None #sonrasında globale eklemek için atar etki etmeyen bir değer yok o yüzden şu anda none

contrast_entry = 1 #sonrasında globale eklemek için atar etkilemeyen hali 1

brightness_entry = 0#sonrasında globale eklemek için atar etkilemeyen hali 0dır


    

def blur_dialog(): #blur ekleme tuşuna basıldığında bu ekran açılacak ve blur seviyesi girilecek
        while True:
            global blur_entry 
            dialog = ctk.CTkInputDialog(text="Type in the blur level make sure its an odd number like 3,5,7 etc: or 1 if you dont want to blur", title="Blur level") #istenen yazar
            deneme = dialog.get_input()
            
            if deneme:  # içinin boş olmadığından emin olur
                try:
                    deneme == int(deneme)# int yapar
                    if int(deneme) > 0:#sıfırdan büyük mü?
                        if int(deneme) % 2 != 0:
                            blur_entry = deneme#sonrasında kullanmak için bize blur seviyesini bir değere atar
                            return blur_entry
                except ValueError:
                    continue    
                    


def window_CTk():#def yaptım çünkü thread yapmak için def olmalı
    #tuşların bulunacağı ekran
    global blur_entry
    global sharpening_entry
    global contrast_entry
    global brightness_entry

    
    app = ctk.CTk() #butonların olacağı ekran
    app.title('filters')#ekran ismi
    app.geometry('1200x625')#ekran geometrisi
    ctk.set_default_color_theme('blue')#tuşlar
    ctk.set_appearance_mode('dark')#arka plan



    button = ctk.CTkButton(app, text='Blur level' , command=blur_dialog) #blur değerini almamız için gereken tuş
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 10)#yeri vb







    



    app.mainloop()#ekranın açık olması için
    







def window_CV():#def yaptım çünkü thread yapmak için def olmalı

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
        sharpening_kernel = np.array([[0, -1, 0],
                                      [-1, sharpening_entry, -1],
                                      [0, -1, 0]])


        # filters
        frame = cv2.blur(frame, (int(blur_entry), int(blur_entry))) #blur

        frame = cv2.convertScaleAbs(frame, alpha=contrast_entry, beta=brightness_entry) #alpha 0-1 ise azaltır 1den büyükse artırır contrast #beta negatif ise azaltır pozitif ise artırır brightness
        
        if sharpening_entry: #burada ifle doğrulamam gerekti çünkü etki etmeyen bir değer yok                                                                               
            frame = cv2.filter2D(frame, -1 , sharpening_kernel )

        
        # Show frames
        cv2.imshow('cam', frame) # cam isim frame ise kamera

        # When clicked 'q' wait for one second and then break
        if cv2.waitKey(1) == ord('q'):
            break


    cap.release() # Stop recording
    cv2.destroyAllWindows() # Destroys the page



t1 = threading.Thread(target = window_CTk)#başlatabilmek için atar
t2 = threading.Thread(target = window_CV)#başlatabilmek için atar
t1.start()#başlatır
t2.start()#başlatır
