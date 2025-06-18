#%% Imports
import keras_nlp
import keras
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
np.set_printoptions(suppress=True)
import pickle
from datasets import load_dataset
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from keras_nlp.models.task import Task
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import re
#%%

#%% Global Variables
CLASSIFYING_THRESHOLD=0.7
LYRICS_RETRIEVAL_TRYS=5
genius = lyricsgenius.Genius("0NcFEOg-YopNwxBQrZjTvZ5Cqm07LUvIerQOsxYL6pKcqjtvzZycw1Wc5H97j1-J")
#%%

#%% Global Functions
def classifySong(songName,artist):
    songLyrics=getLyrics(songName,artist)
    if songLyrics is not None :
        songLyrics = songLyrics.split()
        n = 100
        inputModel = [' '.join(songLyrics[i:i+n]) for i in range(0,len(songLyrics),n)]
        return getLabel(inputModel)
    else:
        return "Not Found"
def remove_marks(input_string):
    marks = ['!', '?','@','$','%','^','&','*','(',')','[',']']

    return "".join((char for char in input_string if char not in marks and not char.isdigit()))


def getLabel(inputModel): # Takes Lyrics Segments and return label
    Preprocessed_Inputs=preprocessor(inputModel)
    Prediction_Inputs = classifier.predict(Preprocessed_Inputs)
    for prediction in Prediction_Inputs :
        if prediction > CLASSIFYING_THRESHOLD:
            return "True"
    return "False"

def getPredictions(inputModel):
  Preprocessed_Inputs=preprocessor(inputModel)
  Predictions = classifier.predict(Preprocessed_Inputs)
  for i in range(0,len(Predictions)):
    print(inputModel[i],"->",Predictions[i],"->","True" if Predictions[i] > CLASSIFYING_THRESHOLD else "False","\n")
  print("Average : ",np.sum(Predictions)/len(Predictions))


def delete_text_in_parentheses(text):
    pattern = r'\([^)]*\)'
    return re.sub(pattern, '', text)
def delete_text_in_brackets(text):
    pattern = r'\[[^\]]*\]'
    return re.sub(pattern, '', text)
def PreprocessInput(lyrics):
  return delete_text_in_parentheses(delete_text_in_brackets(lyrics))
#%%

#%% Model Stuff
def distilbert_kernel_initializer(stddev=0.02):
    return keras.initializers.TruncatedNormal(stddev=stddev)

class myClassifier(Task):
  def __init__(
      self,backbone,dropout=0.45,preprocessor=None,**kwargs
  ):

    inputs = backbone.input

    cls = backbone(inputs)[:, backbone.cls_token_index, :]

    x = keras.layers.Dense(
              768,
              activation="relu",
              kernel_initializer=distilbert_kernel_initializer(),
              name="pooled_dense",
          )(cls)

    x = keras.layers.Dense(
              512,
              activation="relu",
              kernel_initializer=distilbert_kernel_initializer(),
              name="pooled_dense1",
          )(cls)

    x = keras.layers.Dropout(dropout, name="classifier_dropout")(x)

    outputs = keras.layers.Dense(
              1,
              kernel_initializer=distilbert_kernel_initializer(),
              name="output_layer",
              activation="sigmoid"
          )(x)
    super().__init__(
              inputs=inputs,
              outputs=outputs,
              include_preprocessing=preprocessor is not None,
              **kwargs,
          )
    self.backbone = backbone
    self.preprocessor = preprocessor

backbone = keras_nlp.models.DistilBertBackbone.from_preset("distil_bert_base_en_uncased")

classifier.backbone.trainable = False

classifier = myClassifier(backbone,preprocessor=None,dropout=0.2)

classifier.compile(
    loss=keras.losses.BinaryCrossentropy(),
    optimizer=keras.optimizers.SGD(),
    metrics=['accuracy','Recall'],
)
#%%

#%% Load weights
classifier.load_weights("D:\\college\\GP\\HateSpeech-5-NoBackbone\\")
#%%

classifySong("Woman", "Doja Cat")

