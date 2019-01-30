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
from io import BytesIO
import tempfile
import cv2

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

from hed import Network, estimate

train_on_gpu = torch.cuda.is_available()


def detectedge(image_in, image_type):
    binary_image = base64.b64decode(image_in)
    f = tempfile.NamedTemporaryFile()
    #TODO Ugly Hack but for now let it be.
    f.write(binary_image)
    x = cv2.imread(f.name)
    y = cv2.resize(x, (480,320))
    resize_img = tempfile.NamedTemporaryFile(suffix='.png')
    cv2.imwrite(resize_img.name,y)
    if image_type == 'RGB':
        image = PIL.Image.open(resize_img)
        IMAGE_TYPE = 'RGB'
    else:
        image = PIL.Image.open(resize_img)
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

    # TODO lets restore the size of the image to original size

    img = base64.b64encode(img_out.convert(IMAGE_TYPE).tobytes()).decode('utf-8')
    return img
