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

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        continue
    cv2.imwrite('test_photo2.jpg',frame)
    
    cv2.imshow("Video Frame",frame)

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
        print("NO MASK")
    
    key_pressed = cv2.waitKey(1) & 0xFF
    #gives ASCII value of pressed key 
    if key_pressed == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()