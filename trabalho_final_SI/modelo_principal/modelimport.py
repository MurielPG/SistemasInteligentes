import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras
from script import plot_the_model


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
    plt.savefig("graficos/modelo_dados_teste.png")
    plt.show()
    plt.close()

new_model = keras.models.load_model('modelo_completo/')


test_dataset = np.genfromtxt('dadosTeste.csv', delimiter=",", names=["x", "y"])
inputs = test_dataset['x']
outputs = test_dataset['y']

test_results = new_model.evaluate(
    test_dataset['x'], test_dataset['y'],
    verbose=0)

print(test_results)
plot_the_model(new_model, inputs, outputs)

new_model.summary()