import numpy as np
import matplotlib.pyplot as plt

x1,y1 = -2,3
x2,y2 = 2,1

a = (y2-y1) / np.cosh((x2-x1) / (2*y1))
b = (x2-x1) / (2*np.arccosh((y2-y1)/a))

x = np.linspace(x1,x2,1000)

y=np.cosh((x-x1)/b)+y1

plt.plot(x,y)

plt.show()