import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Dense, Dropout, BatchNormalization, GaussianNoise,
    LeakyReLU, Conv2D, MaxPooling2D, Flatten, Activation
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l1



# Tensorflow GPU setup
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)



def create_model(input_dim=(64, 64, 1), output_dim=4, dropout_rate=0.2, noise=0.1, learning_rate=0.001, scale=1):
    # Input
    input_layer = Input(shape=input_dim)

    # Tree structure, units are getting smaller 32-16-8-4
    units = int(32 * scale)

    while units >= 4:
        # Analyze
        x = Conv2D(filters=units, kernel_size=(3, 3), padding='same')(input_layer)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = BatchNormalization()(x)
        x = Dropout(dropout_rate)(x)

        # Flatten
        x = Flatten()(x)

        # Brain
        x = Dense(units, kernel_regularizer=l1(0.00001))(x)
        x = GaussianNoise(stddev=noise)(x)
        x = BatchNormalization()(x)
        x = Activation('sigmoid')(x)
        x = Dropout(dropout_rate)(x)

        # Scale units
        units = int(float(units) / 2)
    
    # Output
    output_layer = Dense(output_dim, activation='sigmoid')(x)

    # Compilation
    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', 'mean_absolute_error'])    
    return model

def test_model(input_dim=(64, 64, 1), output_dim=4, dropout_rate=0.2, noise=0.1, learning_rate=0.001, scale=1):
    print("Start test_model()...")
    try:
        model = create_model(input_dim, output_dim, dropout_rate, noise, learning_rate, scale)

        train_input = np.random.rand(4, *input_dim).astype('float32')
        train_output = np.random.rand(4, output_dim).astype('float32')

        model.fit(train_input, train_output, epochs=5, batch_size=2, verbose=1)

        eval_input = np.random.rand(4, *input_dim).astype('float32')
        eval_output = np.random.rand(4, output_dim).astype('float32')

        evaluation = model.evaluate(eval_input, eval_output, verbose=1)
        print("test_model() Evaluation:", evaluation)

        predict_input = np.random.rand(4, *input_dim).astype('float32')

        # Run predictions
        predictions = model.predict(predict_input)
        print("test_model() Prediction:", predictions)

        print("Success test_model()!\n")
    except Exception as e:
        print(f"Error in test_model(): {e}")
        exit(1)


# Run test when import
test_model()


