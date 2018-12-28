![SingularityNet.io](./images/singnet-logo.jpg?raw=true 'SingularityNET')

[![CircleCI](https://circleci.com/gh/IsraelAbebe/pytorch-hed.svg?style=svg)](https://circleci.com/gh/IsraelAbebe/pytorch-hed)

# Holistically-Nested Edge Detection


## Welcome

This service provides age detection service for given images using pytoch frameworks based on the paper [
Holistically-Nested Edge Detection](https://arxiv.org/abs/1504.06375).

The main difference from Canny edge detection is that this approch provides better edge detection for training 
since it picks up useful edges rather than providing all edges that exist and it reduces noice in that way.

## How does it work?
- The user must provide image that is either 3 Channel or 2 Channel which is `PIL.Image` type
- Image then be converted to 480 * 320 like `PIL.Image.resize((480,320))`
- Image then will be converted to byte using 'PIL.Image.tobytes()'

# Using the service on the platform
The returned result has the following form:

        message ImageFile {
	        bytes value = 1;
        }

The returned result image byte with 480 * 320 shape 
To convert to image use :
    
     image = Image.frombytes(data=responce.value,size=(480,320),mode='RGB')
     
Example result after saving the image might look like

![Expected output](./images/client_out.png?raw=true 'SingularityNET')
