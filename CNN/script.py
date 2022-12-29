import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import log

main_folder = "C:/Users/Rostom/Videos/5SDBD/Projet_Intégrateur/archive/"
ATTR_PATH = main_folder + "list_attr_celeba.csv"  
PARTITION_PATH = main_folder + "list_eval_partition.csv" 
IMAGES_PATH = main_folder + "img_align_celeba/img_align_celeba/"  
MODEL_HANDLE = "./model" 
IMAGE_SIZE = (220, 220)

# Performance
# BATCH_SIZE = 128
BATCH_SIZE = 150
TRAIN_SAMPLE = 200
VALIDATION_SAMPLE = 40
NUM_EPOCHS = 3
# NUM_EPOCHS = 50

def select_best_features():
    df1 = pd.read_csv(ATTR_PATH, delimiter=',')
    df1.dataframeName = 'list_attr_celeba.csv'
    scores=[]
    for column in df1:
        if column != 'image_id':
            a = len(df1[df1[column] == 1])
            b = len(df1[df1[column] == -1])
            score = abs(a-b)/(a+b)
            scores.append((column,1/score))
    scores.sort(reverse = True)
    scores.sort(key=lambda a: a[1])
    scores.reverse()
    N=22
    scores_subset = [x for index, x in enumerate(scores) if index < N]
    selected_features = [scores_subset[i][0] for i in range(len(scores_subset))]
    
    #Manual tweaking
    selected_features.remove('Attractive')
    selected_features.append('Chubby')
    selected_features.append('Bald')
    return selected_features

select_best_features()

df = pd.merge(pd.read_csv(PARTITION_PATH), pd.read_csv(ATTR_PATH), on="image_id")
df.head()
for column in df:
    print(column)
features_str = select_best_features()  

def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, IMAGE_SIZE)
    return image

def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)

def load_and_preprocess_from_path_label(path, 
    Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose, Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald):
    images = load_and_preprocess_image(path)
    return images, Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose,Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald

def init_dataset(df,features_str):
    a = ([IMAGES_PATH + image_id for image_id in df["image_id"]],)
    for feature in features_str:
        b =  list(df[feature].replace(-1,0))
        a = a + (b,)
    return a

def build_dataset_from_df(df):
    ds = tf.data.Dataset.from_tensor_slices(init_dataset(df,features_str))
    ds = ds.map(load_and_preprocess_from_path_label)
    ds = ds.shuffle(buffer_size=1000)
    ds = ds.repeat()
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(buffer_size=tf.data.AUTOTUNE)
    return ds

train_df = df.loc[df["partition"] == 0].head(TRAIN_SAMPLE)
train_ds = build_dataset_from_df(train_df)

val_df = df.loc[df["partition"] == 1].head(VALIDATION_SAMPLE)
val_ds = build_dataset_from_df(val_df)

#val_df

image, Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose, Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald = next(iter(train_ds))
features = [ Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose, Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald]
plt.figure(figsize=(10, 10))
for i in range(9):
#     ax = plt.subplot(3, 3, i + 1)
#     plt.imshow(image[i].numpy().astype("uint8"))
    s = ""
    for j in range(len(features)):
        s+= str(features_str[j]) +" : "
        s+= str(features[j][i].numpy())
        s+= '\n'
#     plt.title(s)
#     plt.axis("off")

normalization_layer = tf.keras.layers.Rescaling(1. / 255)
preprocessing_model = tf.keras.Sequential([normalization_layer])
do_data_augmentation = False
if do_data_augmentation:
    preprocessing_model.add(tf.keras.layers.RandomRotation(0.2))
    preprocessing_model.add(tf.keras.layers.RandomTranslation(0, 0.2))
    preprocessing_model.add(tf.keras.layers.RandomTranslation(0.2, 0))
    preprocessing_model.add(tf.keras.layers.RandomZoom(0.2, 0.2))
    preprocessing_model.add(tf.keras.layers.RandomFlip(mode="horizontal"))
train_ds = train_ds.map(lambda images,  Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose, Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald:
                        (preprocessing_model(images), ( Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose, Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald)))

val_ds = val_ds.map(lambda images,  Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose, Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald:
                    (normalization_layer(images), ( Mouth_Slightly_Open, Smiling, Wearing_Lipstick, High_Cheekbones, Male, Heavy_Makeup, Wavy_Hair, Oval_Face, Pointy_Nose, Arched_Eyebrows, Big_Lips, Black_Hair, Big_Nose, Young, Straight_Hair, Brown_Hair, Bags_Under_Eyes, Wearing_Earrings, No_Beard, Bangs, Blond_Hair, Chubby, Bald)))


do_fine_tuning = False
input = tf.keras.Input(shape=IMAGE_SIZE + (3,))
x = hub.KerasLayer(MODEL_HANDLE, trainable=do_fine_tuning)(input)
x = tf.keras.layers.Dropout(rate=0.2)(x)
x = tf.keras.layers.Dense(128, activation="relu")(x)

outs = []

for feature in features_str:
    out = tf.keras.layers.Dense(1, kernel_regularizer=tf.keras.regularizers.l2(0.0001), activation="sigmoid", name=feature)(x)
    outs.append(out)


model = tf.keras.Model( inputs = input, outputs = outs)
# model.summary()

model.compile(
    loss = {           
        "Mouth_Slightly_Open": tf.keras.losses.BinaryCrossentropy(),
        "Smiling": tf.keras.losses.BinaryCrossentropy(),
        "Wearing_Lipstick": tf.keras.losses.BinaryCrossentropy(),
        "High_Cheekbones": tf.keras.losses.BinaryCrossentropy(),
        "Male": tf.keras.losses.BinaryCrossentropy(),
        "Heavy_Makeup": tf.keras.losses.BinaryCrossentropy(),
        "Wavy_Hair": tf.keras.losses.BinaryCrossentropy(),
        "Oval_Face": tf.keras.losses.BinaryCrossentropy(),
        "Pointy_Nose": tf.keras.losses.BinaryCrossentropy(),
        "Arched_Eyebrows": tf.keras.losses.BinaryCrossentropy(),
        "Big_Lips": tf.keras.losses.BinaryCrossentropy(),
        "Black_Hair": tf.keras.losses.BinaryCrossentropy(),
        "Big_Nose": tf.keras.losses.BinaryCrossentropy(),
        "Young": tf.keras.losses.BinaryCrossentropy(),
        "Straight_Hair": tf.keras.losses.BinaryCrossentropy(),
        "Brown_Hair": tf.keras.losses.BinaryCrossentropy(),
        "Bags_Under_Eyes": tf.keras.losses.BinaryCrossentropy(),
        "Wearing_Earrings": tf.keras.losses.BinaryCrossentropy(),
        "No_Beard": tf.keras.losses.BinaryCrossentropy(),
        "Bangs": tf.keras.losses.BinaryCrossentropy(),
        "Blond_Hair": tf.keras.losses.BinaryCrossentropy(),
        "Chubby": tf.keras.losses.BinaryCrossentropy(),
        "Bald": tf.keras.losses.BinaryCrossentropy() 
    },
    metrics = {
        "Mouth_Slightly_Open": 'accuracy',
        "Smiling": 'accuracy',
        "Wearing_Lipstick": 'accuracy',
        "High_Cheekbones": 'accuracy',
        "Male": 'accuracy',
        "Heavy_Makeup": 'accuracy',
        "Wavy_Hair": 'accuracy',
        "Oval_Face": 'accuracy',
        "Pointy_Nose": 'accuracy',
        "Arched_Eyebrows": 'accuracy',
        "Big_Lips": 'accuracy',
        "Black_Hair": 'accuracy',
        "Big_Nose": 'accuracy',
        "Young": 'accuracy',
        "Straight_Hair": 'accuracy',
        "Brown_Hair": 'accuracy',
        "Bags_Under_Eyes": 'accuracy',
        "Wearing_Earrings": 'accuracy',
        "No_Beard": 'accuracy',
        "Bangs": 'accuracy',
        "Blond_Hair": 'accuracy',
        "Chubby": 'accuracy',
        "Bald": 'accuracy'
    },
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
)

steps_per_epoch = len(train_df) // BATCH_SIZE
validation_steps = len(val_df) // BATCH_SIZE
hist = model.fit(
    train_ds,
    epochs=NUM_EPOCHS, steps_per_epoch=steps_per_epoch,
    validation_data=val_ds,
    validation_steps=validation_steps).history


# fig, ax = plt.subplots(len(features_str), 2, figsize=(35, 35))
# for i, c in enumerate(features_str):
#     ax[i, 0].plot(hist[f"{c}_loss"], label="train")
#     ax[i, 0].plot(hist[f"val_{c}_loss"], label="val")
#     ax[i, 0].set_title(f"Loss ({c})")
#     ax[i, 0].legend()
#     ax[i, 1].plot(hist[f"{c}_accuracy"], label="train")
#     ax[i, 1].plot(hist[f"val_{c}_accuracy"], label="val")
#     ax[i, 1].set_title(f"Accuracy ({c})")
#     ax[i, 1].legend()
# plt.show()

x, y = next(iter(val_ds))
image = x[0, :, :, :]
plt.imshow(image)
plt.axis('off')
plt.show()
#print(x)

prediction_scores = model.predict(np.expand_dims(image, axis=0))
for i, label in enumerate(features_str):
    pred = prediction_scores[i][0][0]
    print(f"{label}: actual {y[i][0]}, predicted {1 if pred > 0.5 else 0} ({format(pred, '.4f')})")


def open_images(inference_folder: str) -> np.ndarray:
    images = []
    for img in os.listdir(inference_folder):
        img_location = os.path.join(inference_folder, img)  
        with Image.open(img_location) as img:  
            img = np.array(img)
            img = img[:, :, :3]
            img = np.expand_dims(img, axis=0)  
        images.append(img)
    images_array = np.vstack(images) 
    return images_array

from PIL import Image
import os, sys

path = "./image_samples/"
dirs = os.listdir( path )
resized_path = "./images_resized/"

def resize():
    for item in dirs:
        print(item)
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            im = im.convert('RGB')
            f, e = os.path.splitext(path+item)
            imResize = im.resize((220,220), Image.ANTIALIAS)
            imResize.save(resized_path + item + '_resized.jpg', 'JPEG', quality=90)

resize()

def display_image(image,s):

    plt.imshow(image)
    plt.title(s)
    plt.figure()

def image_prediction(prediction_score):

    s = ""
    for i, label in enumerate(features_str):
        pred = prediction_score[i][0][0]
        s += f"{label}: predicted {1 if pred > 0.5 else 0} ({format(pred, '.4f')})"
        s +="\n"
    return s      

import os
from PIL import Image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
images = open_images(resized_path)
c=0
for image in images:
    #img_batch = np.expand_dims(image * 10e-4, axis=0)
    img_batch = np.expand_dims(image, axis=0)
    #print(img_batch)
    normalizedData = (img_batch-np.min(img_batch))/(np.max(img_batch)-np.min(img_batch))
    #print(normalizedData)
    prediction_score= model.predict(normalizedData)
    s = image_prediction(prediction_score)
    display_image(image,s)