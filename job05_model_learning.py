import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *
import datetime

x_train = np.load('./data/x_train_wordsize12375_20260608.npy', allow_pickle=True)
y_train = np.load('./data/y_train_wordsize12375_20260608.npy', allow_pickle=True)
x_test = np.load('./data/x_test_wordsize12375_20260608.npy', allow_pickle=True)
y_test = np.load('./data/y_test_wordsize12375_20260608.npy', allow_pickle=True)
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

model = Sequential()
model.add(Embedding(12375, 300))
model.build(input_shape=(None, 26))
model.add(Conv1D(32, 5, padding='same', activation='relu'))
model.add(MaxPooling1D(1))
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(6, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(x_train, y_train, batch_size=128, epochs=10, validation_data=(x_test, y_test), verbose=1)
score = model.evaluate(x_test, y_test, verbose=0)
print('Final test loss:', score[0])
print('Final test accuracy:', score[1])
model.save('./models/news_section_classifier_{}_{}.h5'.format(datetime.datetime.now().strftime('%Y%m%d'), score[1]))
plt.plot(fit_hist.history['val_accuracy'], label='val accuracy')
plt.plot(fit_hist.history['accuracy'], label='train accuracy')
plt.legend(loc='lower right')
plt.show()