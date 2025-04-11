import numpy as np
import pickle
from tensorflow.keras.applications import VGG16, ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Dense, Dropout, Embedding, LSTM, Add
from tensorflow.keras.utils import to_categorical

# Assuming you're loading a Keras model that was compiled in an older Keras version
model = load_model("model_weights/model_9.h5", compile=False)

# Load and prepare the ResNet50 model
model_temp = ResNet50(weights="imagenet", input_shape=(224, 224, 3))
model_resnet = Model(inputs=model_temp.input, outputs=model_temp.layers[-2].output)

def preprocess_image(img):
    img = image.load_img(img, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

def encode_image(img):
    img = preprocess_image(img)
    feature_vector = model_resnet.predict(img)
    feature_vector = feature_vector.reshape(1, feature_vector.shape[1])
    return feature_vector

def predict_caption(photo):
    in_text = "startseq"
    max_len = 35
    for i in range(max_len):
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence], maxlen=max_len, padding='post')
        ypred = model.predict([photo, sequence])
        ypred = ypred.argmax()
        word = idx_to_word[ypred]
        in_text += ' ' + word
        
        if word == 'endseq':
            break

    final_caption = in_text.split()
    final_caption = final_caption[1:-1]  # Remove 'startseq' and 'endseq'
    final_caption = ' '.join(final_caption)
    
    return final_caption

# Load word dictionaries
with open("./storage/word_to_idx.pkl", "rb") as w2i:
    word_to_idx = pickle.load(w2i)

with open("./storage/idx_to_word.pkl", "rb") as i2w:
    idx_to_word = pickle.load(i2w)

def caption_this_image(image):
    enc = encode_image(image)
    caption = predict_caption(enc)
    return caption
