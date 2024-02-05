from PIL import Image
import numpy as np

pic = Image.open("convert_image/sigma.jpg").convert('RGB')
pic.show()
pix = np.array(pic.getdata()).reshape(pic.size[1], pic.size[0], 3)
im = Image.fromarray(np.sum(pix*np.array([0.299, 0.587, 0.114]), axis=2).astype(np.uint8))
im.save('convert_image/converted_sigma.jpg')