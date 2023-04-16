###


import cv2
import argparse
import numpy as np
from flask import Flask,request
from flask_cors import CORS
from base64 import b64decode,b64encode
from PIL import Image
from io import BytesIO
import json

app = Flask(__name__)
CORS(app)

def from_base64(base64_data):
    nparr = np.fromstring(base64_data.decode('base64'), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)





def getOutput(input):

    def get_output_layers(net):
        
        layer_names = net.getLayerNames()
        try:
            output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        except:
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers


    def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        
    image = cv2.imread("temp.jpg")

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open("yolov3.txt", 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    configVariable = "yolov3.cfg"
    net = cv2.dnn.readNet("yolov3.weights", config=configVariable)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]
        
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
        
    cv2.imwrite("object-detection.jpg", image)
    objectsDetected=[]
    for i in list(set(class_ids)):
        objectsDetected.append(classes[i])  
    return json.dumps({
        "objects":objectsDetected,
        "detectedObjectBase64":b64encode(open("object-detection.jpg", "rb").read()).decode("utf-8")
    },default=str)

@app.route("/", methods=['POST'])
def index():
    bimage = request.form['image'];
    image = b64decode(bimage)
    im = Image.open(BytesIO(b64decode(bimage.split(',')[0])))
    rgb_im = im.convert('RGB')
    rgb_im.save("temp.jpg")
    f = open("temp.jpg","wb")
    f.write(image)
    f.close()
    return getOutput("temp.jpg")    

@app.route("/", methods=['get'])
def index2():
    return "<h1>hello</h1>"

if __name__=="__main__":
    app.run(debug=False,host="0.0.0.0")
