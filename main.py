import cv2
import customtkinter as ctk
import threading
import numpy as np



blur_entry = 1 #sonrasında globale eklemek için atar etkilemeyen hali 1dir

sharpening_entry = None #sonrasında globale eklemek için atar etki etmeyen bir değer yok o yüzden şu anda none

contrast_entry = 1 #sonrasında globale eklemek için atar etkilemeyen hali 1

brightness_entry = 0#sonrasında globale eklemek için atar etkilemeyen hali 0dır


def brightness_dialog():#brightness ekleme tuşuna basılınca bu açılacak  
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

def blur_dialog(): #blur ekleme tuşuna basıldığında bu ekran açılacak ve blur seviyesi girilecek
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
                    
def contrast_dialog():
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

def sharpening_dialog():
    global sharpening_entry
    while True:
        dialog = ctk.CTkInputDialog(text="Enter the sharpening level make sure the number is maximum 10 and bigger than 1 to see changes if you dont want to change something enter 0 anything bigger than 10 will look weird", title="Blur level") #istenen yazar
        deneme = dialog.get_input()


        if deneme:  # içinin boş olmadığından emin olur
                try:
                    deneme = float(deneme)# float olur eğer stringse çalışmamasını sağlar intleri zaten çevirir

                    if 0 < float(deneme):
                        sharpening_entry = float(deneme)#sonrasında kullanmak için bize blur seviyesini bir değere atar
                        return sharpening_entry
                    if float(deneme) == 0:
                        sharpening_entry = None
                        return sharpening_entry
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

    button = ctk.CTkButton(app, text='Brightness level' , command=brightness_dialog) #blur değerini almamız için gereken tuş
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 55)#yeri vb

    button = ctk.CTkButton(app, text='Contrast level' , command=contrast_dialog) #blur değerini almamız için gereken tuş
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 100)#yeri vb

    button = ctk.CTkButton(app, text='Sharpening level' , command=sharpening_dialog) #blur değerini almamız için gereken tuş
    button.pack(side='top' , padx=10, pady=10)#yeri vb
    button.place(x = 520 , y = 145)#yeri vb


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
        sharpening_kernel = np.array([
                                        [0, -0.5, 0],
                                        [-0.5, sharpening_entry, -0.5],
                                        [0, -0.5, 0]
                                                    ])
    

        # filters
        frame = cv2.blur(frame, (int(blur_entry), int(blur_entry))) #blur

        frame = cv2.convertScaleAbs(frame, alpha=float(contrast_entry), beta=float(brightness_entry)) #alpha 0-1 ise azaltır 1den büyükse artırır contrast #beta negatif ise azaltır pozitif ise artırır brightness
        
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

