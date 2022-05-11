import tensorflow as tf
from tensorflow.contrib import rnn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score


# this function accepts input in the format of [[label, [[numbers, features]...]]...]
# label refers to the type of the contract
# numbers should equal to n_max
# features are the 14 features extracted from transaction records
# this function use long_short_time_memory network to train a model
def network_(data):
    features = data[:, 1]
    labels = data[:, 0]
    x_train, x_test, y_train, y_test = train_test_split(features, labels, 0.3, False, 23)
    x_train, x_validate, y_train, y_validate = train_test_split(x_train, y_train, 0.2, False, 23)
    return
