# import firebase_admin
# from firebase_admin import credentials, firestore, storage
from PIL import Image, ImageDraw
# from google.cloud.firestore import GeoPoint
from model_integration import getPredictions, extract_exif_data, grouping_data
from optical_flow import get_filtered_images
from geolocation_calculation import calculate_geolocation, get_location_details
from io import BytesIO
import os
# import time

# start_time = time.time()

# cred = credentials.Certificate("C:/SD/api/key.json")
# firebase_app = firebase_admin.initialize_app(cred, {'storageBucket': 'traffic-50c49.appspot.com'})
# db = firestore.client()

# bucket = storage.bucket()
# storage_index = len(list(bucket.list_blobs()))

# ## mapping of the classes
class_decode = {0: 'R7-1', 1: 'W11-2', 2: 'S1-1', 3: 'R4-7c', 4: 'M3-2', 5: 'M1-5', 6: 'M6-1R', 7: 'R7-3', 8: 'W16-9P', 9: 'D11-1', 10: 'M6-3', 11: 'R4-7', 12: 'W17-1', 13: 'R1-3P', 14: 'W16-7PL', 15: 'W3-1', 16: 'D1-1', 17: 'R3-7R', 18: 'OM1-3', 19: 'R1-2', 20: 'M6-1L', 21: 'W14-2', 22: 'M6-4', 23: 'W13-1P', 24: 'R5-1', 25: 'W11-1', 26: 'R6-1R', 27: 'W3-3', 28: 'R10-19aP', 29: 'R4-11', 30: 'R3-5R', 31: 'R3-6L', 32: 'M3-4', 33: 'W16-2P', 34: 'S4-3P', 35: 'W1-2L', 36: 'R3-5L', 37: 'R10-3b', 38: 'R6-2R', 39: 'W16-7PR', 40: 'D1-2', 41: 'OM2-2H', 42: 'D1-1e', 43: 'R10-3e', 44: 'R7-8', 45: 'M3-3', 46: 'R1-1', 47: 'D3-1', 48: 'other', 49: 'R2-1'}
# mutcd_dict = {'R7-1': 'No Parking any Time', 'W11-2': 'Pedestrian', 'S1-1': 'School', 'R4-7c': 'Narrow Keep Right', 'M3-2': 'Cardinal Direction - East (Auxiliary)', 'M1-5': 'State Route Sign', 'M6-1R': 'Right Turn Arrow (Auxiliary)', 'R7-3': 'No Parking Except (Days)', 'W16-9P': 'Ahead (plaque)', 'D11-1': 'Bike Route', 'M6-3': 'Straight Arrow (Auxiliary)', 'R4-7': 'Keep Right', 'W17-1': 'Speed Hump', 'R1-3P': 'All Way (plaque)', 'W16-7PL': 'Downward Diagonal Left Arrow (plaque)', 'W3-1': 'Stop Ahead', 'D1-1': 'Destination (1 line)', 'R3-7R': 'Right Lane Must Turn Right', 'OM1-3': 'Type 1 Object Marker (yellow )', 'R1-2': 'Yield', 'M6-1L': 'Left Turn Arrow (Auxiliary)', 'W14-2': 'No Outlet', 'M6-4': 'Two-Direction Left/Right Turn Arrow (Auxiliary)', 'W13-1P': 'Advisory Speed (plaque)', 'R5-1': 'Do Not Enter', 'W11-1': 'Bicycle', 'R6-1R': 'One Way Right Sign', 'W3-3': 'Signal Ahead', 'R10-19aP': 'Photo Enforced (word message) (plaque)', 'R4-11': 'Bicycles May use Full Lane', 'R3-5R': 'Turn Only (Right)', 'R3-6L': 'Optional Movement (Left)', 'M3-4': 'Cardinal Direction - West (Auxiliary)', 'W16-2P': 'XX Feet', 'S4-3P': 'School (plaque)', 'W1-2L': 'Curve (Left)', 'R3-5L': 'Turn Only (Left)', 'R10-3b': 'Pedestrian Signal Information (Symbol)', 'R6-2R': 'One Way Right Sign', 'W16-7PR': 'Downward Diagonal Right Arrow (plaque)', 'D1-2': 'Destination (2 lines)', 'OM2-2H': 'Type 2 Object Marker', 'D1-1e': 'Exit Destination Sign', 'R10-3e': 'Pedestrian Signal Information (Countdown)', 'R7-8': 'Parking Restrictions', 'M3-3': 'Cardinal Direction - South (Auxiliary)', 'R1-1': 'Stop', 'D3-1': 'Street Name', 'other': 'Non-MUTCD sign', 'R2-1': 'Speed Limit'}
# geolocation_object_height = {'D3-1': 304.8, 'Other/Unidentified/Unclear': 750.0, 'R1-1': 750.0, 'R2-1': 750.0, 'R7-1': 457.2, 'D11-1': 450.0, 'W11-2': 914.4, 'S1-1': 914.4, 'W16-7PL': 304.8, 'R4-7': 609.6, 'W14-2': 609.6, 'R5-1': 750.0, 'R1-3P': 152.4, 'M1-5': 609.6, 'M6-1L': 381.0, 'W17-1': 914.4, 'R3-5L': 914.4, 'M6-3': 381.0, 'W16-9P': 457.2, 'R6-1R': 304.8, 'R7-3': 450.0, 'W3-1': 762.0, 'M6-4': 381.0, 'R1-2': 900.0, 'R4-7c': 762.0, 'R7-8': 457.2, 'M6-1R': 381.0, 'D1-1': 304.8, 'D1-1e': 304.8, 'W11-1': 600.0, 'S4-3P': 203.2, 'R3-5R': 914.4, 'R10-3b': 304.8, 'W16-7PR': 450.0, 'R3-7R': 762.0, 'R10-19aP': 457.2, 'W3-3': 914.4, 'R4-11': 762.0, 'M3-2': 304.8, 'M3-4': 304.8, 'R10-3e': 375.0, 'OM1-3': 457.2, 'W16-2P': 450.0, 'R3-6L': 914.4, 'OM2-2H': 300.0, 'D1-2': 762.0, 'W1-2L': 762.0, 'W13-1P': 457.2, 'M3-3': 304.8, 'R6-2R': 457.2, 'M3-1': 304.8, 'M1-4': 609.6}
# sign_to_url = {'D1-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/D1-1.png', 'D1-1e': 'https://storage.googleapis.com/traffic-50c49.appspot.com/D1-1e.png', 'D1-2': 'https://storage.googleapis.com/traffic-50c49.appspot.com/D1-2.png', 'D11-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/D11-1.png', 'D3-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/D3-1.png', 'M1-5': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M1-5.png', 'M3-2': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M3-2.png', 'M3-3': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M3-3.png', 'M3-4': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M3-4.png', 'M6-1L': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M6-1L.png', 'M6-1R': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M6-1R.png', 'M6-3': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M6-3.png', 'M6-4': 'https://storage.googleapis.com/traffic-50c49.appspot.com/M6-4.png', 'OM1-3': 'https://storage.googleapis.com/traffic-50c49.appspot.com/OM1-3.png', 'OM2-2H': 'https://storage.googleapis.com/traffic-50c49.appspot.com/OM2-2H.png', 'other': 'https://storage.googleapis.com/traffic-50c49.appspot.com/other.png', 'R1-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R1-1.png', 'R1-2': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R1-2.png', 'R1-3P': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R1-3P.png', 'R10-19aP': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R10-19aP.png', 'R10-3b': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R10-3b.png', 'R10-3e': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R10-3e.png', 'R2-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R2-1.png', 'R3-5L': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R3-5L.png', 'R3-5R': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R3-5R.png', 'R3-6L': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R3-6L.png', 'R3-7R': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R3-7R.png', 'R4-11': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R4-11.png', 'R4-7': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R4-7.png', 'R4-7c': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R4-7C.png', 'R5-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R5-1.png', 'R6-1R': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R6-1R.png', 'R6-2R': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R6-2R.png', 'R7-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R7-1.png', 'R7-3': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R7-3.png', 'R7-8': 'https://storage.googleapis.com/traffic-50c49.appspot.com/R7-8.png', 'S1-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/S1-1.png', 'S4-3P': 'https://storage.googleapis.com/traffic-50c49.appspot.com/S4-3P.png', 'W1-2L': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W1-2L.png', 'W11-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W11-1.png', 'W11-2': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W11-2.png', 'W13-1P': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W13-1P.png', 'W14-2': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W14-2.png', 'W16-2P': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W16-2P.png', 'W16-7PL': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W16-7PL.png', 'W16-7PR': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W16-7PR.png', 'W16-9P': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W16-9P.png', 'W17-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W17-1.png', 'W3-1': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W3-1.png', 'W3-3': 'https://storage.googleapis.com/traffic-50c49.appspot.com/W3-3.png'}

# # data = request.files.getlist("images")
# path = './sd_/'
path = './sd_/'
data = os.listdir(path)[30:80]
img_names = []
images = []
img_bytes_list = []

for file_name in data:
    file_path = os.path.join(path, file_name)
    with open(file_path, "rb") as file:
        img_bytes = file.read()
        img_bytes_obj = BytesIO(img_bytes)
        img_names.append(file_name)
        img_bytes_list.append(img_bytes)
        images.append(Image.open(img_bytes_obj))
        
grouped_data_to_send, optical_flow_images = grouping_data(extract_exif_data(img_names, images), getPredictions(images), class_decode)
optical_flow_images = get_filtered_images(optical_flow_images)
print(optical_flow_images)
# for data in grouped_data_to_send:
#     img = data['image']
#     isCrossed = False if data['filename'] in optical_flow_images else True
            
#     xmin, ymin, xmax, ymax = map(int, data['bounding_box'])
#     draw = ImageDraw.Draw(img)
#     draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=(0, 0, 255), width=15)
#     img = img.resize((1200, 1200))
    
#     img_bytes_ = BytesIO()
#     img.save(img_bytes_, format='JPEG')
#     img_bytes_.seek(0)

#     ## send to img storage and get the url
#     blob = bucket.blob(f'{storage_index}.jpg')
#     blob.upload_from_file(img_bytes_, content_type='image/jpeg')
#     blob.make_public()
#     storage_index += 1

#     firestore_collection = {}
#     firestore_collection['name'] = blob.public_url
#     firestore_collection['sign'] = class_decode[data['class']]
#     firestore_collection['imgurl'] = sign_to_url[firestore_collection['sign']] if not isCrossed else 'https://storage.googleapis.com/traffic-50c49.appspot.com/crossed.png'

#     x = data['exif_data']['GPSInfo'] # geolocation
#     latitude = float(x[2][0] + x[2][1] / 60 + x[2][2] / 3600)
#     longitude = float(x[4][0] + x[4][1] / 60 + x[4][2] / 3600)
#     if x[1] == 'S':
#         latitude = -latitude
#     if x[3] == 'W':
#         longitude = -longitude
    
#     if firestore_collection['sign'] in geolocation_object_height and isCrossed == False:
#         latitude, longitude = calculate_geolocation(latitude, longitude, geolocation_object_height[firestore_collection['sign']], ymin, ymax)
    
#     firestore_collection['geolocation'] = GeoPoint(latitude, longitude)
#     firestore_collection['lats'] = "{:.5f}".format(latitude)
#     firestore_collection['longs'] = "{:.5f}".format(longitude)
#     firestore_collection['mutcd'] = mutcd_dict[firestore_collection['sign']]
#     firestore_collection['confidence'] = "{:.1f}".format(data['confidence']*100)
#     firestore_collection['area'] = get_location_details(latitude, longitude)
#     firestore_collection['isCrossed'] = isCrossed
#     print(firestore_collection)
                            
#     ## send to firestore
#     _, sendRef = db.collection("image_details").add(firestore_collection)
#     print(f'send the image - {sendRef}')

# end_time = time.time()
# print(f'\n\nExecution Time - {end_time - start_time} seconds')