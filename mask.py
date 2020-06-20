import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import time

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
    
    if prediction[0,0] > 0.8:
        print("MASK")
    else:

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