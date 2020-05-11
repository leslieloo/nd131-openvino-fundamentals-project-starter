# Project Write-Up

This documentation explain some of the details of the performance and model conversion/selection

## Explaining Custom Layers

The IR model used is converted from trained TensorFlow SSD MobileNet V2 COCO model. No custom layers handling is required, as the IR model's layers is fully supported by the OpenVino engine and it's CPU extension

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations were running both models manually and record their inference time, and accuracy

The difference between model accuracy pre- and post-conversion was 0.85 and 0.72

The size of the model pre- and post-conversion was 122MB and 65MB

The inference time of the model pre- and post-conversion was roughly 0.005 and 0.02 seconds

There will be significant cost/charges and network involved if the similar solution is done using cloud services. Data/Image from the camera is required to transmit to cloud, in order to do inference, which incurred some latency. Using edge to do inference locally will remove unnecessary data travel, with contribute to much better inference performance.

## Assess Model Use Cases

Some of the potential use cases of the people counter app are manufacturing smart monitoring system to monitor the people flow in the production line, and retail queueing system to monitor customer's queue

Each of these use cases would be useful because it's allow to detect people flow, and act accordingly, by redirect customer to not fully occupied queue in case of retail queueing system, or inform on-duty-manager to distribute more workers on more busy production line.

## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows:-

1) IR model performance may varies on different ambient lighting environment (eg. light vs dark)
2) Model accuracy may dropped slightly when converted to IR model, and further reduced when using quantization to reduce the IR model's size
3) The IR model is expecting the input images to have certain width and height. Image reprocessing is required to transform images (shape and cropping) before feeding into the model
