from ultralytics import YOLO
import cv2
import numpy as np


# TODO: Obtain the meta-data (EXIF details (geolocation and date-time of capture), Bounding box coordinates, Current Image size, Class detected)
# TODO: optical flow and geolocation calculation
# TODO: Send this data (POST) to the firestore database and storage (bounding box img)


def getPredictions(images_to_predict):
    boxes_ = []
    model = YOLO('./api/v8n.pt')
    results = model.predict(images_to_predict)
    cv2.waitKey(0)
    for result in results:
        boxes_.append(result.boxes)
    return boxes_

def extract_exif_data(img_name, images):
    tag_mapping = {'ImageWidth': 40962, 'ImageLength': 40963, 'DateTime': 306, 'GPSInfo': 34853, 'DateTimeOriginal': 36867, 'FocalLength': 37386}
    exif_list = []

    for img_path, img in zip(img_name, images):
        exif_data = img._getexif()
        exif_temp = {}
        for k,v in tag_mapping.items():
            exif_temp[k] = exif_data[v]
        exif_dict = {'filename': img_path, 'exif_data': exif_temp, 'image': img}
        exif_list.append(exif_dict)
    return exif_list

def grouping_data(image_exifs, bboxes, class_decode):
    grouped_data_to_send = []
    opticalflow_format = []
    for image_exif, boxes in zip(image_exifs, bboxes):
        if boxes.cls.numel() == 0:
            continue

        img = image_exif['image']
        filename = image_exif['filename']
        exif_data = image_exif['exif_data']
        for cls, xyxy, conf in zip(boxes.cls.tolist(), boxes.xyxy.tolist(), boxes.conf.tolist()):
            if cls == 48:
                continue
            data_to_send = {
                'filename': filename,
                'exif_data': exif_data,
                'class': cls,
                'bounding_box': xyxy,
                'confidence': conf,
                'image': img
            }

            np_array = np.array(img)
            if np_array.shape[-1] == 4:
                np_array = np_array[:, :, :3]
            cv2_image = cv2.cvtColor(np_array, cv2.COLOR_RGB2BGR)
            
            opticalflow_format.append([cv2_image, class_decode[int(cls)], xyxy, exif_data['DateTime'], filename])
            grouped_data_to_send.append(data_to_send)
    return grouped_data_to_send, opticalflow_format