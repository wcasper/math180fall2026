#!/usr/bin/python

import numpy as np

error_max = 100
best_m = 1
best_n = 1

errors = np.zeros([1000,999])

for m in range(0,1000):
  for n in range(1,1000):
    error = np.abs(np.pi - m/n)
    errors[m,n-1] = error
    if (error < error_max):
      error_max = error
      best_m = m
      best_n = n
     
print(best_m, best_n, error_max)

from matplotlib import pyplot as plt

plt.contourf(errors,levels=np.arange(-4,4,.02))
plt.colorbar()
plt.show()
