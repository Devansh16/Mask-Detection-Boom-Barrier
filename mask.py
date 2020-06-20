# Mask Detection Boom Barrier
# Author: Muskan Jain and Devansh Chawla
# Date Created: June 20, 2020 (Last Updated: June 20, 2020)

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import time
import serial
from serial.tools import list_ports

port_name = []

print('Connect Device and press c')
c = input()
if c == 'c':
    ports = list(list_ports.comports())
    for p in ports:
        port_name.append(p[0])
        
    #get a serial instance as ser and configure later
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.timeout = 1
    ser.port = port_name[0]
    
    for p in port_name:
        try:
            ser.port = p
            ser.open()
            print("connected to " + ser.port)
            break
        except:
            print(p + " Already Opend ! Retrying... ")

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cap= cv2.VideoCapture(0)

classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        continue
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    faces = classifier.detectMultiScale(gray, 1.5, 5) 

    X_test = [] 
    
    cv2.imwrite('test_photo2.jpg',frame)

    # Replace this with the path to your image
    image = Image.open('test_photo2.jpg')

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    #image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    
    if prediction[0,0] > 0.9:
        print("MASK")
        ser.write('o'.encode())                      #send 1 to the arduino's Data code                
    else:
        ser.write('c'.encode())
        for face in faces: 
            x, y, w, h = face 
            im_face = gray[y:y + h, x:x + w] 
            im_face = cv2.resize(im_face, (224, 224)) 
            X_test.append(im_face.reshape(-1))
        
        for i, face in enumerate(faces): 
            x, y, w, h = face 

            # drawing a rectangle on the detected face 
            cv2.rectangle(frame, (x, y), (x + w, y + h), 
                          (0, 0, 255), 3) 

            # adding detected/predicted name for the face 
            cv2.putText(frame, "NO MASK", (x-50, y-50), 
                            cv2.FONT_HERSHEY_DUPLEX, 2, 
                                    (0, 0, 255), 3)
    
    cv2.imshow("Video Frame",frame)
    
    key_pressed = cv2.waitKey(1) & 0xFF
    #gives ASCII value of pressed key 
    if key_pressed == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()