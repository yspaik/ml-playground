#!/usr/binb/env python

'''
Martin Kersner, m.kersner@gmail.com
2016/08/09

Draw eigen vectors and error ellipses representing covariance matrices.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import Arrow

chi_square_prob = {}
chi_square_prob[99] = 9.210
chi_square_prob[95] = 5.991
chi_square_prob[90] = 4.605

def main():
  mean  = np.array([0.0, 0.0])
  C = np.array([[1.0, 0.8],
                [0.8, 1.5]])
  n_samples = 1000

  plt.ylim([-8, 8])
  plt.xlim([-8, 8])

  data = np.random.multivariate_normal(mean, C, size=n_samples)
  data_std = np.std(data, axis=0)
  vals, vecs = np.linalg.eig(C)

  print "Eigenvalues: \n", vals
  print "Eigenvectors: \n", vecs

  ax = plt.axes()

  plot_data(data)
  plot_arrow(ax, vals, vecs, mean, C)
  plot_ellipse(ax, vals, vecs, mean, data_std, 99, 'r', data)
  plot_ellipse(ax, vals, vecs, mean, data_std, 95, 'g', data)
  plot_ellipse(ax, vals, vecs, mean, data_std, 90, 'b', data)

  plt.show()

def plot_arrow(ax, vals, vecs, mean, C):
  sqrt_vals  = np.sqrt(np.abs(vals))

  head_width  = 0.05
  head_length = 0.1
  fc = ec = "aqua"

  #alpha_0 = np.arctan(vecs[1, 0]/vecs[0, 0])
  #dx_0 = np.cos(alpha_0)*sqrt_vals[0]
  #dy_0 = np.sin(alpha_0)*sqrt_vals[0]

  #alpha_1 = np.arctan(vecs[1, 1]/vecs[0, 1])
  #dx_1 = np.cos(alpha_1)*sqrt_vals[1]
  #dy_1 = np.sin(alpha_1)*sqrt_vals[1]

  #ax.arrow(mean[0], mean[1], dx_0, dy_0, head_width=head_width, head_length=head_length, fc=fc, ec=ec)
  #ax.arrow(mean[0], mean[1], dx_1, dy_1, head_width=head_width, head_length=head_length, fc=fc, ec=ec)

  ax.arrow(mean[0], mean[1], vecs[0, 0]*sqrt_vals[0], vecs[1, 0]*sqrt_vals[0], head_width=head_width, head_length=head_length, fc='g', ec='g')
  ax.arrow(mean[0], mean[1], vecs[0, 1]*sqrt_vals[1], vecs[1, 1]*sqrt_vals[1], head_width=head_width, head_length=head_length, fc='g', ec='g')

def plot_ellipse(ax, vals, vecs, mean, data_std, prob_val, edgecolor, data):
  width  = 2*np.sqrt(chi_square_prob[prob_val]*vals[0])
  height = 2*np.sqrt(chi_square_prob[prob_val]*vals[1])

  # according to http://www.visiondummy.com/2014/04/draw-error-ellipse-representing-covariance-matrix/ we should emply max value 
  min_idx = np.argmin(vals)
  angle = np.degrees(np.arctan(vecs[1, min_idx]/vecs[0, min_idx]))

  el = Ellipse(xy=mean, width=width, height=height, angle=angle, edgecolor=edgecolor, fc='None', lw=1)
  ax.add_patch(el)

def plot_data(data):
  plt.scatter(data[:, 0], data[:, 1], 1.0)

if __name__ == "__main__":
  main()
