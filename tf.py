import tensorflow as tf
import CardLib as cl
import tables
import numpy as np
import h5py

# TODO
# Data set works and can be made
# Need to figure out how to input that into the algorithm
# Need to figure out how to make the algorithm use my input
# Need to figure out how to interpret results in a usable way

infile = 'indata.h5'
outfile = 'outdata.h5'

# printable dataset
i = tables.open_file(infile, mode = 'r')
if len(i.root.data) == 4:
    print(i.root.data[0: 4])
for index in range(4, len(i.root.data), 4):
    print(i.root.data[index - 4: index])

# printable dataset
o = tables.open_file(outfile, mode = 'r')
if len(o.root.data) == 4:
    print(o.root.data[0: 4])
for index in range(4, len(o.root.data), 4):
    print(o.root.data[index - 4: index])

# print("TensorFlow version:", tf.__version__)

# print(np.load("output_file.npy"))
# print(np.load("input_file.npy"))



# deck_matrix = np.array([
#         #    A  2  3  4  5  6  7  8  9  10 J  Q  K
#             [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Diamonds
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Hearts
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Clubs
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Spades
#         ])



# train_labels = [
#     [ 4,  5,  4, 0 , 4,  0  ,0  ,0  ,2,  4,  4 ,-1 ,-1],
#  [ 0 , 3,  4 , 2 ,-1 , 2 , 2 , 2  ,0 , 0  ,0  ,2 , 2],
#  [ 4, -1 ,-1 , 6 ,-1 , 4,  2, 2  ,0  ,0  ,0  ,3 , 5],
#  [ 2,  3 ,-1 , 2 , 4,  2 , 0 , 0 , 0,  0 , 0 , 2,  3]]

# BATCH_SIZE = 64
# SHUFFLE_BUFFER_SIZE = 100

# train_dataset = tf.data.Dataset.from_tensor_slices((train_examples, train_labels))

# train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)

# model = tf.keras.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(10)
# ])

# model.compile(optimizer=tf.keras.optimizers.RMSprop(),
#               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#               metrics=['sparse_categorical_accuracy'])
            
# model.fit(train_dataset, epochs=10)

# dataset2 = tf.convert_to_tensor(deck_matrix)
# for element in dataset2:
#     print(element)
# dataset = tf.data.Dataset.from_tensor_slices(deck_matrix)
# for element in dataset:
#     print(element)

# wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
# sudo dpkg -i cuda-keyring_1.0-1_all.deb