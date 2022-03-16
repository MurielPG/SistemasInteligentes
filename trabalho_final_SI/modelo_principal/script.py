# Example based on https://colab.research.google.com/github/google/eng-edu/blob/main/ml/cc/exercises/linear_regression_with_synthetic_data.ipynb?utm_source=mlcc&utm_campaign=colab-external&utm_medium=referral&utm_content=linear_regression_synthetic_tf2-colab&hl=en#scrollTo=QF0BFRXTOeR3

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras
import os


learning_rate=0.00015
epochs=3000
batch_size=13


def build_model(learning_rate):
    """Create and compile a simple linear regression model."""
    # Most simple tf.keras models are sequential. 
    # A sequential model contains one or more layers.
    model = tf.keras.models.Sequential()

    # Describe the topography of the model.
    # The topography of a simple linear regression model
    # is a single node in a single layer. 
    model.add(tf.keras.layers.Dense(50, activation='selu', 
                                    input_shape=(1,)))
    model.add(tf.keras.layers.Dense(50, activation='elu'))
    model.add(tf.keras.layers.Dense(30, activation='selu'))
    model.add(tf.keras.layers.Dense(20, activation='selu'))
    model.add(tf.keras.layers.Dense(1))

    # Compile the model topography into code that 
    # TensorFlow can efficiently execute. Configure 
    # training to minimize the model's mean squared error. 
    model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=learning_rate),
                  loss="mean_squared_error",
                  metrics=[tf.keras.metrics.RootMeanSquaredError()])

    return model           


def train_model(model, feature, label, epochs, batch_size):
    """Train the model by feeding it data."""
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=100)

    # Feed the feature values and the label values to the 
    # model. The model will train for the specified number 
    # of epochs, gradually learning how the feature values
    # relate to the label values. 
    history = model.fit(x=feature,
                        y=label,
                        batch_size=batch_size,
                        epochs=epochs,
                        callbacks=[early_stop])

    # Gather the trained model's weight and bias.
    trained_weight = model.get_weights()[0]
    trained_bias = model.get_weights()[1]

    # The list of epochs is stored separately from the 
    # rest of history.
    epochs = history.epoch
    
    # Gather the history (a snapshot) of each epoch.
    hist = pd.DataFrame(history.history)

    # Specifically gather the model's root mean 
    #squared error at each epoch. 
    rmse = hist["root_mean_squared_error"]

    return trained_weight, trained_bias, epochs, rmse

def plot_the_model(model, feature, label):
    """Plot the trained model against the training feature and label."""

    # Label the axes.
    plt.figure()
    plt.xlabel('Input')
    plt.ylabel('Output')
    plt.plot(feature, label, '-b',
             label='Dataset')
    plt.plot(feature, model.predict(feature), '-r',
             label='Model')

    # Render the scatter plot and the red line.
    plt.savefig("graficos/modelo.png")
    plt.show()
    plt.close()
    
def plot_the_loss_curve(epochs, rmse):
    """Plot the loss curve, which shows loss vs. epoch."""

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Root Mean Squared Error")

    plt.plot(epochs, rmse, label="Loss")
    plt.legend()
    plt.ylim([rmse.min()*0.97, rmse.max()])
    plt.savefig("graficos/erro.png")
    plt.show()
    plt.close()


train_dataset = np.genfromtxt('dadosTreino.csv', delimiter=",", names=["x", "y"])
test_dataset = np.genfromtxt('dadosTeste.csv', delimiter=",", names=["x", "y"])
inputs = train_dataset['x']
outputs = train_dataset['y']

model = build_model(learning_rate)
trained_weight, trained_bias, epochs, rmse = train_model(model, inputs, 
                                                         outputs, epochs,
                                                         batch_size)
plot_the_model(model, inputs, outputs)
plot_the_loss_curve(epochs, rmse)
# print(trained_weight, trained_bias)


test_results = model.evaluate(
    test_dataset['x'], test_dataset['y'],
    verbose=0)




checkpoint_path = "cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

model.save("modelo_completo/")
# model.save_weights("nn_weights.h5")


# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


print(test_results)

print(model.summary())

