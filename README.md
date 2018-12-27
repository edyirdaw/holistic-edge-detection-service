# pytorch-hed
This is implementation of Holistically-Nested Edge Detection [1] using PyTorch. Should you be making use of this work, please cite the paper accordingly. Also, make sure to adhere to the licensing terms of the authors. Should you be making use of this particular implementation, please acknowledge it appropriately.

<a href="https://arxiv.org/abs/1504.06375" rel="Paper"><img src="http://www.arxiv-sanity.com/static/thumbs/1504.06375v2.pdf.jpg" alt="Paper" width="100%"></a>

For the original version of this work, please see: https://github.com/s9xie/hed
<br />
For another reimplementation based on Caffe, please see: https://github.com/zeakey/hed


## Install prerequisites
### Using conda

	conda env create -f environment.yml
	conda activate edge-detection-snet-agent


## Using pip
	#To install requirements for the project 
	$ pip install -r requirements.txt
	
	$ pip install grpcio
	$ pip install grpcio-tools
	
## Download pretrained models

	bash download.bash
         

## Setup
- run the following command to generate gRPC classes for Python
    
      # only in Service folder run
      $ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Service/edgedetect.proto


## Using docker with GPU

If you have a [nvidia-docker2](https://github.com/NVIDIA/nvidia-docker) installed, we have Dockerfile.gpu which you can use to build your image.

     docker build --file Dockerfile.gpu . -t singnet:hed

## Using docker with CPU

You can also build an image which has only the CPU dependecies to evaluate the models provided.

	docker build --file Dockerfile . -t singnet:hed-cpu
	

## How to Use the docker image
	
	# this will open port 50051 and run the service 
	docker run -it --rm -p 50051:50051 hed:0.1
	
	

## Usage
To run it on your own image, use the following command. Please make sure to see their paper / the code for more details.


	

	# on project directory this will start the server 
	$ python Service/server.py



	#on other terminal run 
	$ python Service/client.py [-h] [--image_input IMAGE_INPUT]
                       [--image_output IMAGE_OUTPUT] [--port PORT]

         optional arguments:
            -h, --help            show this help message and exit
            --image_input IMAGE_INPUT
                                  image path
            --image_output IMAGE_OUTPUT
                                  output image file name like "client_out"
            --port PORT           port you are using like : "localhost:50051" [The server must run on the port you specify ]






 It achieves an ODS=0.774  on the BSDS500 dataset, evaluated using [this code](https://github.com/zeakey/edgeval). Please feel free to contribute to this repository by submitting issues and pull requests.

## Comparison
<p align="center"><img src="comparison/comparison.gif?raw=true" alt="Comparison"></p>

## References
```
[1]  @inproceedings{Xie_ICCV_2015,
         author = {Saining Xie and Zhuowen Tu},
         title = {Holistically-Nested Edge Detection},
         booktitle = {IEEE International Conference on Computer Vision},
         year = {2015}
     }
```
