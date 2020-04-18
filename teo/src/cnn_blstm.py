"""
Implements a BLSTM convolutional neural network.

Based on modelwrapper to avoid unnecessary confusion, only overrides build method
"""
from tensorflow import keras as K
import embed_utils
from modelwrapper import ModelWrapper, TRAINABLE_GLOVE


class BlstmCnnUtility(ModelWrapper):
    """
    just shutting up pylint
    """
    ##############################################
    # Constructor
    # def __init__(self, data, labels, sequence_length, GLOVE=False, glove_dir=None):
    #    super().__init__(data, labels, sequence_length, GLOVE, glove_dir)

    # BUILD MODEL, COMPILE
    def build_model(self, embedding_size,
                    filter_sizes, num_filters, num_cells=100):
        print("building model...")

        self.model = K.Sequential()
        # EMBEDDING

        if self.GLOVE:
            print("\tcreating embedding matrix with glove values...")
            print('\t', end='')

            # maybe should try random vs zeros. you never know [scratch that]
            embedding_matrix = embed_utils.pretrained_embedding_matrix(
                embedding_size, self.tokenizer.word_index, self.embeddings_index)
            print("\tembedding matrix created!")
        else:
            # create embedding_matrix with word2vec
            pass

        self.model.add(K.layers.Embedding(len(self.tokenizer.word_index) + 1, embedding_size,
                                          input_length=self.sequence_length, weights=[
                                              embedding_matrix],
                                          trainable=TRAINABLE_GLOVE))

        # self.model.add(K.layers.Bidirectional(K.layers.LSTM(
        #   units=num_cells, dropout=0.4, recurrent_dropout=0.4,return_sequences=True)))

        print("\t adding convolution layers...")
        for i, size in enumerate(filter_sizes):
            self.model.add(K.layers.Conv1D(
                filters=num_filters[i], kernel_size=size,
                padding='same', activation='relu'))
            self.model.add(K.layers.MaxPool1D(pool_size=2))
        print("\t ..added convolution!")

        self.model.add(K.layers.LSTM(
            units=num_cells, dropout=0.2))
        # self.model.add(K.layers.Dropout(0.2))

        self.model.add(K.layers.BatchNormalization())
        # self.model.add(K.layers.Flatten())
        self.model.add(K.layers.Dense(256))
        self.model.add(K.layers.Dense(128))
        # self.model.add(K.layers.Dense(128, activation='relu'))
        self.model.add(K.layers.Dense(1, activation='sigmoid'))

        # K.optimizers.Adam(lr=0.0001) to experiment with convergence speeds
        self.model.compile(loss='binary_crossentropy',
                           optimizer='adam', metrics=['accuracy'])

        print("..model built!")

        self.model.summary()
