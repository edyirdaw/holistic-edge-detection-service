import sys

sys.path.insert(0, 'Service/')

from client import ClientTest
from server import *
from PIL import Image
import unittest
import numpy as np
import subprocess
import torch.nn as nn
import torch
import base64


class TestSuiteGrpc(unittest.TestCase):
    def setUp(self):
        with open('images/sample.png', 'rb') as f:
            img = f.read()
            self.image = base64.b64encode(img).decode('utf-8')
            self.image_type = 'RGB'
        self.server = Server()
        self.server.start_server()
        self.client = ClientTest()

    def test_grpc_call(self):
        stub = self.client.open_grpc_channel()
        result_image = self.client.send_request(stub, self.image, self.image_type)

        binary_image = base64.b64decode(result_image.image)
        with open("images/client_out2." + result_image.image_type, 'wb') as f:
            f.write(binary_image)


        img_res = np.asarray(Image.open("images/client_out2." + result_image.image_type).convert('L'))
        img_expected = np.asarray(Image.open("images/client_out.png").convert('L'))
        self.assertEqual(img_res.all(), img_expected.all())

    def tearDown(self):
        # self.client.channel.close()
        self.server.stop_server()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestSuiteGrpc("test_grpc_call"))
    unittest.main()
