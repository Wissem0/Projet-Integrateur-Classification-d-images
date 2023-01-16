import pandas as pd
import numpy as np
import cv2    
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import f1_score
import keras.utils as image
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential, Model 
from tensorflow.keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.utils import np_utils
from tensorflow.keras.optimizers import SGD
from IPython.core.display import display, HTML
from PIL import Image
from io import BytesIO
import base64

# set variables 
main_folder = "./archive/"
images_folder = main_folder + 'img_align_celeba/img_align_celeba/'

TRAINING_SAMPLES = 100
VALIDATION_SAMPLES = 20
TEST_SAMPLES = 200
IMG_WIDTH = 178
IMG_HEIGHT = 218
BATCH_SIZE = 16
NUM_EPOCHS = 5

# import the data set that include the attribute for each picture
df_attr = pd.read_csv(main_folder + 'list_attr_celeba.csv')
df_attr.set_index('image_id', inplace=True)
df_attr.replace(to_replace=-1, value=0, inplace=True) #replace -1 by 0

df_attr = df_attr.drop(columns=[
'5_o_Clock_Shadow',
'Arched_Eyebrows',
'Attractive',
'Bags_Under_Eyes',
'Bangs',
'Big_Lips',
'Big_Nose',
'Blurry',
'Bushy_Eyebrows',
'Double_Chin',
'Goatee',
'Gray_Hair',
'Mustache',
'Narrow_Eyes',
'Pointy_Nose',
'Receding_Hairline',
'Rosy_Cheeks',
'Sideburns',
'Straight_Hair',
'Wavy_Hair',
'Wearing_Earrings',
'Wearing_Hat',
'Wearing_Necklace',
'Wearing_Necktie'])

# Recomended partition
df_partition = pd.read_csv(main_folder + 'list_eval_partition.csv')

# join the partition with the attributes
df_partition.set_index('image_id', inplace=True)
df_par_attr = df_attr.join(df_partition['partition'], how='inner')

def load_reshape_img(fname):
    img = load_img(fname)
    x = img_to_array(img)/255.
    x = x.reshape((1,) + x.shape)
    return x


def generate_df(partition, num_samples):
    df_ = df_par_attr[(df_par_attr['partition'] == partition)].sample(num_samples)

    # for Train and Validation
    if partition != 2:
        x_ = np.array([load_reshape_img(images_folder + fname) for fname in df_.index])
        x_ = x_.reshape(x_.shape[0], IMG_HEIGHT, IMG_WIDTH, 3)
        y_ = np.array(df_.drop(['partition'], axis=1))
    # for Test
    else:
        x_ = []
        y_ = []

        for index, target in df_.iterrows():
            im = cv2.imread(images_folder + index)
            im = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2RGB), (IMG_WIDTH, IMG_HEIGHT)).astype(np.float32) / 255.0
            im = np.expand_dims(im, axis =0)
            x_.append(im)
        y_ = np.array(df_.drop(['partition'], axis=1))
            
    return x_, y_

    # Generate image generator for data augmentation
datagen =  ImageDataGenerator(
  #preprocessing_function=preprocess_input,
  rotation_range=30,
  width_shift_range=0.2,
  height_shift_range=0.2,
  shear_range=0.2,
  zoom_range=0.2,
  horizontal_flip=True
)

#3.2. Build Data Generators

# Train data
x_train, y_train = generate_df(0, TRAINING_SAMPLES)

# Train - Data Preparation - Data Augmentation with generators
train_datagen =  ImageDataGenerator(
  preprocessing_function=preprocess_input,
  rotation_range=30,
  width_shift_range=0.2,
  height_shift_range=0.2,
  shear_range=0.2,
  zoom_range=0.2,
  horizontal_flip=True,
)

train_datagen.fit(x_train)
train_generator = train_datagen.flow(
    x_train, y_train,
    batch_size=BATCH_SIZE,)

# Validation Data
x_valid, y_valid = generate_df(1, VALIDATION_SAMPLES)
x_test, y_test = generate_df(2, TEST_SAMPLES)

#4.1. Set the Model

# Import InceptionV3 Model
inc_model = InceptionV3(weights='imagenet',
                        include_top=False,
                        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))

#Adding custom Layers
x = inc_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
predictions = Dense(len(df_attr.columns), activation="sigmoid")(x)


# creating the final model 
model_ = Model(inputs=inc_model.input, outputs=predictions)

# Lock initial layers to do not be trained
for layer in model_.layers[:52]:
    layer.trainable = False

# compile the model
model_.compile(optimizer=SGD(learning_rate=0.0001, momentum=0.9)
                    , loss='categorical_crossentropy'
                    , metrics=['accuracy'])


# 4.2. Train Model
checkpointer = ModelCheckpoint(filepath='weights.best.inc.male.hdf5', 
                               verbose=1, save_best_only=True)

hist = model_.fit(x = x_train
                  , y = y_train
                     , validation_data = (x_valid, y_valid)
                      , steps_per_epoch= TRAINING_SAMPLES/BATCH_SIZE
                      , epochs= NUM_EPOCHS
                      , callbacks=[checkpointer]
                      , verbose=1
                    )

