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
import magic
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
    file_format = magic.from_buffer(binary_image, mime=True).split('/')[1]
    print(file_format)
    # This could be improved more
    f = tempfile.NamedTemporaryFile(suffix='*.' + str(file_format))
    f.write(binary_image)
    x = cv2.imread(f.name)
    y = cv2.resize(x, (480,320))
    image = PIL.Image.fromarray(y)
    IMAGE_TYPE = 'RGB'
    if y.shape == 2:
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

    img_out = img_out.convert(IMAGE_TYPE)
    result = tempfile.NamedTemporaryFile(suffix="*." + str(file_format))
    img_out.save(result)

    with open(result.name, 'rb') as f:
        img = base64.b64encode(f.read()).decode('utf-8')
    return img, file_format
