from PIL import image
import numpy as np


path_to_img = input('Input relative path to imgage: ')
img = image.open(path_to_img).convert('RGB')
img.show()
vectorized_img = np.array(img.getdata()).reshape(img.size[1], img.size[0], 3)
converted_img = imgage.fromarray(np.sum(vectorized_img*np.array([0.299, 0.587, 0.114]), axis=2).astype(np.uint8))
converted_img.show()
path_to_converted_img = input('Input relative save path to converted imgage: ')
converted_img.save(path_to_converted_img)