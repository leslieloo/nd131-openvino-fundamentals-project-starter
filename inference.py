#!/usr/bin/env python3
"""
 Copyright (c) 2018 Intel Corporation.

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import logging as log
from openvino.inference_engine import IENetwork, IECore


class Network:
    """
    Load and configure inference plugins for the specified target devices 
    and performs synchronous and asynchronous modes for the specified infer requests.
    """

    def __init__(self):
        ### TODO: Initialize any class variables desired ###
        self.plugin = IECore()
        self.net_plugin = None
        self.input_blob = None
        self.output_blob = None
        self.exec_network = None
        self.infer_request_handle = None

    def load_model(self, model, device="CPU", extension=None):
        ### TODO: Load the model ###
        model_xml = model
        model_bin = os.path.splitext(model_xml)[0] + ".bin"
        
        self.net_plugin = IENetwork(model=model_xml, weights=model_bin)
        self.input_blob = next(iter(self.net_plugin.inputs))
        self.output_blob = next(iter(self.net_plugin.outputs))
                
        ### TODO: Check for supported layers ###
        supported_layers = self.plugin.query_network(network=self.net_plugin, device_name=device)
        unsupported_layers = [l for l in self.net_plugin.layers.keys() if l not in supported_layers]
        if len(unsupported_layers) != 0 and extension is None:
            print("Unsupported layers found in model: {}".format(unsupported_layers))
            print("Please provide extension to support the layers")
            exit(1)
        
        ### TODO: Add any necessary extensions ###
        if extension:
            self.plugin.add_extension(extension, device)
            
        ### TODO: Return the loaded inference plugin ###              
        ### Note: You may need to update the function parameters. ###
        self.exec_network = self.plugin.load_network(self.net_plugin, device)        
        return self.exec_network

    def get_input_shape(self):
        ### TODO: Return the shape of the input layer ###
        return self.net_plugin.inputs[self.input_blob].shape

    def async_inference(self, image):
        ### TODO: Start an asynchronous request ###
        ### TODO: Return any necessary information ###
        ### Note: You may need to update the function parameters. ###
        self.exec_network.start_async(request_id=0, inputs={self.input_blob: image})
        return

    def wait(self):
        ### TODO: Wait for the request to be complete. ###
        ### TODO: Return any necessary information ###
        ### Note: You may need to update the function parameters. ###
        status = self.exec_network.requests[0].wait(-1)
        return status

    def get_output(self):
        ### TODO: Extract and return the output results
        ### Note: You may need to update the function parameters. ###
        return self.exec_network.requests[0].outputs[self.output_blob]
