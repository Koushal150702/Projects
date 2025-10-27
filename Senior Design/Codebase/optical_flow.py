# import os
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
# from filterpy.kalman import KalmanFilter
# from collections import defaultdict
# import numpy as np
# from datetime import datetime
# import cv2

# def list_to_dict(list_of_images):
#     d = defaultdict(list)
#     for sign in list_of_images:
#         d[sign[1]].append(sign)
#     sequences_of_images = dict(d)
#     return sequences_of_images

# def get_filtered_images(list_of_images):
#     sequences_of_signs = []
#     dict_of_images = list_to_dict(list_of_images)
#     for data in dict_of_images.values():
#         for i in range(len(data)):
#             if len(data) - i < 2:
#                 image_1, _, _, _, filename1 = data[i]
#                 sequences_of_signs.append(filename1)
#             elif len(data) - i >= 2:
#                 image_1, detection_class_1, bbox_1, ts_1, filename1 = data[i]
#                 image_2, detection_class_2, bbox_2, ts_2, filename2 = data[i + 1]
#                 date_format = "%Y:%m:%d %H:%M:%S"
#                 ts_1 = datetime.strptime(ts_1, date_format)
#                 ts_2 = datetime.strptime(ts_2, date_format)
#                 time_difference = abs(ts_2 - ts_1)
#                 time_difference_seconds = time_difference.total_seconds()

#                 avg_vel_vec = optical_flow(image_1, image_2, bbox_1, bbox_2)
#                 if avg_vel_vec is not None:
#                     predicted_roi = predict_points(bbox_2, avg_vel_vec)
#                     if len(data) - i > 2 and predicted_roi is not None:
#                         if check_roi_match(predicted_roi, data[i + 2][2]):
#                             continue
#                         else:
#                             if time_difference_seconds < 2:
#                                 continue
#                             else:
#                                 sequences_of_signs.append(filename2)
#                     else:
#                         sequences_of_signs.append(filename2)
#                 else:
#                     sequences_of_signs.append(filename2)

#     return list(set(sequences_of_signs))


# def check_roi_match(predicted_roi, actual_roi):
#     "if the predicted points are outside the dimensions of the image, it wil anyways not be in the next image and therefore it is not part of the sequence"
#     pred_area = (predicted_roi[2] - predicted_roi[0]) * (predicted_roi[3] - predicted_roi[1])
    
#     intersect_xmin = max(predicted_roi[0], actual_roi[0])
#     intersect_ymin = max(predicted_roi[1], actual_roi[1])
#     intersect_xmax = min(predicted_roi[2], actual_roi[2])
#     intersect_ymax = min(predicted_roi[3], actual_roi[3])
#     # intersect_area = max(0, intersect_xmax - intersect_xmin + 1) * max(0, intersect_ymax - intersect_ymin + 1)
#     # iou = intersect_area / (pred_area + (actual_roi[2] - actual_roi[0]) * (actual_roi[3] - actual_roi[1]) - intersect_area)
    
#     intersection_area = max(0, intersect_xmax - intersect_xmin + 1) * max(0, intersect_ymax - intersect_ymin + 1)
    
#     bbox1_area = (predicted_roi[2] - predicted_roi[0] + 1) * (predicted_roi[3] - predicted_roi[1] + 1)
#     bbox2_area = (actual_roi[2] - actual_roi[0] + 1) * (actual_roi[3] - actual_roi[1] + 1)
    
#     union_area = bbox1_area + bbox2_area - intersection_area
    
#     iou = intersection_area / union_area

#     return iou > 0.05  #adjust later

# def optical_flow(image_1,image_2,bounding_box_1, bounding_box_2):
    
#     x_min1, y_min1, x_max1, y_max1 = map(int, bounding_box_1)
#     x_min2, y_min2, x_max2, y_max2 = map(int, bounding_box_2)
    
#     feature_params = dict( maxCorners = 3, 
#                            qualityLevel = 0.3, 
#                            minDistance = 3, 
#                            blockSize = 5 ) 
    
#     lk_params = dict( winSize = (15, 15), 
#                       maxLevel = 2, 
#                       criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
#                                   10, 0.03)) 
    
    
#     # current_img = cv2.imread(image_1, cv2.IMREAD_COLOR)
#     current_img = image_1
#     current_img_gray = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)
#     roi_img1 = current_img_gray[y_min1:y_max1, x_min1:x_max1]
#     next_img = image_2 #cv2.imread(image_2, cv2.IMREAD_COLOR)
#     next_img_gray = cv2.cvtColor(next_img, cv2.COLOR_BGR2GRAY)
    
#     roi_img2 = next_img_gray[y_min2:y_max2, x_min2:x_max2]
#     corners1 = cv2.goodFeaturesToTrack(roi_img1,**feature_params)
#     corners1[:, 0, 0] += x_min1  #add x_min1 to x coordinates

#     corners1[:, 0, 1] += y_min1  #add y_min1 to y coordinates
    
#     if corners1 is not None:
#         corners1 = np.int0(corners1)
     
#     for i in corners1:
#         x,y = i.ravel()
#         cv2.circle(current_img,(x,y),5,255,-1)
    
#     corners2 = cv2.goodFeaturesToTrack(roi_img2, **feature_params)
    
#     corners2[:, 0, 0] += x_min2  #add x_min1 to x coordinates
#     corners2[:, 0, 1] += y_min2  #add y_min1 to y coordinates
#     # corners1[:, 0, 0] += x_min1
#     # corners1[:, 0, 1] += y_min1
#     # corners2[:, 0, 0] += x_min2
#     # corners2[:, 0, 1] += y_min2
#     if corners2 is not None:
#         corners2 = np.int0(corners2)
     
#     for i in corners2:
#         x,y = i.ravel()
#         cv2.circle(next_img,(x,y),5,255,-1)
    
#     _, st, err = cv2.calcOpticalFlowPyrLK(current_img_gray, 
#                                             next_img_gray, 
#                                             corners1.astype('float32'), corners2.astype('float32'), 
#                                             cv2.OPTFLOW_LK_GET_MIN_EIGENVALS, **lk_params) 
#     # flow = cv2.calcOpticalFlowPyrLK(current_img_gray, 
#     #                                         next_img_gray, 
#     #                                         corners1.astype('float32'), corners2.astype('float32'), 
#     #                                         cv2.OPTFLOW_LK_GET_MIN_EIGENVALS, **lk_params) 
    
#     good_old = corners1[st == True]
#     good_new = corners2[st == True] 
    
#     for i, (new, old) in enumerate(zip(good_new, good_old)):
#         a, b = np.int32(new.ravel())
#         c, d = np.int32(old.ravel())
#         cv2.line(next_img, (a, b), (c, d), (0, 255, 0), 2)  # Green line
#         cv2.circle(next_img, (a, b), 5, (0, 0, 255), -1)  # Red circle
    
#     velocity_vector = good_new - good_old  # This represents the displacement between old and new points
#     magnitude = np.linalg.norm(velocity_vector, axis=1)  # Magnitude of the velocity vector
#     direction = np.arctan2(velocity_vector[:, 1], velocity_vector[:, 0])  # Direction of the velocity vector
    
#     direction_degrees = np.degrees(direction)
#     # print(velocity_vector)
#     velocity_vector = kalman_filter_velocity(velocity_vector)
#     avg_vel_vec = np.mean(velocity_vector, axis = 0)
#     # x = np.percentile(velocity_vector, 25, axis = 0)
#     med = np.median(velocity_vector, axis = 0)
#     # min_vec = np.min(velocity_vector)
#     # avg_mag = np.mean(magnitude)
#     # avg_dir = np.mean(direction_degrees)
    
#     return avg_vel_vec


# def predict_points(bounding_box, avg_vel_vec):
#     x_min, y_min, x_max, y_max = bounding_box

#     dx, dy = avg_vel_vec

#     # next_xmin = x_min + dx
#     # next_xmax = x_max + dx
#     # next_ymin = y_min + dy
#     # next_ymax = y_max + dy
#     next_xmin = x_min + int(round(dx))
#     next_xmax = x_max + int(round(dx))
#     next_ymin = y_min + int(round(dy))
#     next_ymax = y_max + int(round(dy))
#     next_roi = [next_xmin, next_ymin, next_xmax, next_ymax]

#     return next_roi

# def kalman_filter_velocity(velocity_vectors):
#     # Define Kalman filter
#     kf = KalmanFilter(dim_x=2, dim_z=2)
#     kf.x = np.array([0., 0.])  # Initial state estimate
#     kf.F = np.array([[1., 1.], [0., 1.]])  # State transition matrix
#     kf.H = np.array([[1., 0.], [0., 1.]])  # Measurement matrix
#     kf.P *= 1000.  # Initial covariance matrix
#     kf.R = np.diag([1., 1.])  # Measurement noise covariance
#     kf.Q = np.eye(2)  # Process noise covariance

#     filtered_velocities = []

#     for vel in velocity_vectors:
#         kf.predict()
#         kf.update(vel)
#         filtered_velocities.append(kf.x)

#     return np.array(filtered_velocities)