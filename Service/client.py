import os
import grpc
import edgedetect_pb2
import edgedetect_pb2_grpc
import base64

from PIL import Image
import sys

from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

# from hed import Network ,estimate
import argparse

parser = argparse.ArgumentParser()


class ClientTest():
    def __init__(self, port='159.69.56.49:50051', image_output='client_out'):
        self.port = port
        self.image_output = image_output

    def open_grpc_channel(self):
        channel = grpc.insecure_channel(self.port)
        stub = edgedetect_pb2_grpc.EdgedetectStub(channel)
        return stub

    def send_request(self, stub, img):
        out_file_name = self.image_output + '.png'
        img = img
        img = img.resize((480, 320))
        img_b = img.tobytes()

        image_file = edgedetect_pb2.ImageFile(value=img_b)

        response = stub.DetectEdge(image_file)

        print(response)
        image = Image.frombytes(data=response.value, size=(480, 320), mode='RGB')

        return image

    def close_channel(self, channel):
        pass

# if __name__ == "__main__":
#     parser.add_argument("--image_input",type=str,help='image path')
#     parser.add_argument("--image_output",type=str,default='client_out',help='output image file name like "client_out"')
#     parser.add_argument("--port",type=str,default='localhost:50051' ,help='port you are using like :   "localhost:50051" ')

#     args = parser.parse_args()

#     if len(sys.argv) == 1:
#     	parser.print_help()
#     	sys.exit()

image = Image.open('images/sample.png')
client_test = ClientTest()
stub = client_test.open_grpc_channel()
image = client_test.send_request(stub, image)
print(type(image))
