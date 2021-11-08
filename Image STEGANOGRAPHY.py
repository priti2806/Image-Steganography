from tkinter import *          
from PIL import Image, ImageTk
from tkinter import filedialog,Tk, Button, Label
import cv2
import numpy as np
import math
import tkinter.font as font

global path_image

image_display_size = 300,300

def on_click():

    # Step 1.5
    global path_image
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    path_image = filedialog.askopenfilename()
    # load the image using the path
    load_image = Image.open(path_image)
    # set the image into the GUI using the thumbnail function from tkinter
    load_image.thumbnail(image_display_size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    img.place(x=100, y=240)

def encrypt_data_into_image():
    # Step 2
    global path_image
    data = txt.get(1.0, "end-1c")
    # load the image
    img = cv2.imread(path_image)
    # break the image into its character level. Represent the characyers in ASCII.
    data = [format(ord(i), '08b') for i in data]  
    _, width, _ = img.shape
    # algorithm to encode the image
    PixReq = len(data) * 3

    RowReq = PixReq/width
    RowReq = math.ceil(RowReq)

    count = 0
    charCount = 0
    # Step 3
    for i in range(RowReq + 1):
        # Step 4
        while(count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            # Step 5
            for index_k, k in enumerate(char):
                if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if(index_k % 3 == 2):
                    count += 1
                if(index_k == 7):
                    if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if(charCount*3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0
    # Step 6
    # Write the encrypted image into a new file
    cv2.imwrite("encrypted_image.png", img)

    # Display the success label.
    success_label = Label(app, text="Encryption Successful!",
                bg='lavender', font=("Times New Roman", 20))
    success_label.place(x=100, y=600)

image_display_size = 500, 350


def decrypt():
    # load the image and convert it into a numpy array and display on the GUI.
    load = Image.open("./encrypted_image.png")
    load.thumbnail(image_display_size, Image.ANTIALIAS)
    load = np.asarray(load)
    load = Image.fromarray(np.uint8(load))
    render = ImageTk.PhotoImage(load)
    img = Label(app, image=render)
    img.image = render
    img.place(x=950, y=240)

    # Algorithm to decrypt the data from the image
    img = cv2.imread("./encrypted_image.png")
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if(stop):
            break

    message = []
    # join all the bits to form letters (ASCII Representation)
    for i in range(int((len(data)+1)/8)):
        message.append(data[i*8:(i*8+8)])
    # join all the letters to form the message.
    message = [chr(int(''.join(i), 2)) for i in message]
    message = ''.join(message)
    message_label = Label(app, text=message, bg='white', font=("Times New Roman", 13))
    message_label.place(x=1270, y=308)

    #Add a label which displays the message
    D_label = Label(app, text="The Hidden message is  :", font=("Times New Roman", 12))
    D_label.place(x=1270, y=260)
       

# Step 1
# Defined the TKinter object app with background lavender, title Encrypt, and app size 2000*800 pixels.
# app is a object of tk and using it we perform all gui operations
app = Tk() 
app.configure(background='pink')
app.title("Encryption and Decryption")
app.geometry('2000x800')

myFont=font.Font(size=10)
myFont=font.Font(weight="bold")

# Add the button to call the function encrypt.
# create a button for calling the function on_click
on_click_button = Button(app, text="ENCRYPT", bg='black', fg='white',width=16,height=3, command=on_click)
on_click_button['font']=myFont
on_click_button.place(x=420, y=80)

# Add the label to which displays the message.
E_label = Label(app, text="Write Your Secret Message Here :", font=("Times New Roman", 13))
E_label.place(x=410, y=280)

# Add the button to call the function encode.
encrypt_button = Button(app, text="Encode", bg='white', fg='black', command=encrypt_data_into_image)
encrypt_button.place(x=490, y=490)

# Add the button to call the function decrypt.
on_click_button = Button(app, text="DECRYPT", bg='black', fg='white',width=16,height=3, command=decrypt)
on_click_button['font']=myFont
on_click_button.place(x=980, y=80)

# add a text box using tkinter's Text function and place it at (340,55). The text box is of height 165pixels.
txt = Text(app, wrap=WORD, width=30, font=("Times New Roman", 13))
txt.place(x=410, y=318, height=165)
    

app.mainloop()



