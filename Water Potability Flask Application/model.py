import pandas as pd
import numpy as np
import tensorflow as tf


model = tf.keras.models.load_model("potability.model")

pred = model.predict([[1,2,3,4,5,6,7,8,9]])

print(pred)
