import torch
# import torch.utils.serialization

import getopt
import math
import numpy
import os
import PIL
import PIL.Image
import sys
import base64

from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

from hed import Network, estimate

train_on_gpu = torch.cuda.is_available()


def detectedge(image_in):
    IMAGE_TYPE = 'RGB'
    try:
        image = PIL.Image.frombytes(data=image_in, size=(480, 320), mode='RGB')
    except:
        image = PIL.Image.frombytes(data=image_in, size=(480, 320), mode='L')
        image = image.convert('RGB')
        IMAGE_TYPE = 'L'

    if train_on_gpu:
        moduleNetwork = Network().cuda().eval()
    else:
        moduleNetwork = Network().eval()

    img_array = numpy.array(image)
    tensorInput = torch.FloatTensor(img_array[:, :, ::-1].transpose(2, 0, 1).astype(numpy.float32) * (1.0 / 255.0))
    tensorOutput = estimate(tensorInput, moduleNetwork)
    img_out = PIL.Image.fromarray((tensorOutput.clamp(0.0, 1.0).detach().numpy().transpose(1, 2, 0)[:, :, 0] * 255.0))

    img = img_out.convert(IMAGE_TYPE).tobytes()
    return img
