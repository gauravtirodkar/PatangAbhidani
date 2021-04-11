from numpy import loadtxt
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
# load model
def model():
    model = load_model('E:/Project_TE/testing/PatangAbhidani/model.h5')
    # summarize model.
    model.summary()
    # load dataset
    path = 'C:/xampp/htdocs/butterfly/589-7.jpg'
    img = image.load_img(path, target_size=(64, 64))
    x = image.img_to_array(img)
    # plt.imshow(x/255.)
    x = np.expand_dims(x, axis=0)
    # images = np.vstack([x])

    classes = model.predict(x)
    print(classes[0])
    if classes[0]<0.5:
        print("is a skipper")
        return True
    else:
        print("is non skipper")
        return False
