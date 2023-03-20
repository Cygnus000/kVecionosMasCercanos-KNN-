# datos sacados de https://interactivechaos.com/es/manual/tutorial-de-deep-learning/el-dataset-mnist
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("mnist.csv", header = None)
data_not = data[data[0] < 6]
#data_not.head()
y = data_not.pop(0)
X = data_not
for i in range(500):
#plt.imshow(X.iloc[i, :].values.reshape(28, 28), cmap = "binary_r");
    image = X.iloc[i, :].values.reshape(28, 28)
    name = 'numero'+str(i)+'.png'
    plt.imsave(name,image, cmap = 'gray')
#plt.show()
