''' Note at bottom '''

# Listing all the imports
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import imutils
import math
# pipeline is the module which has all the below functions written
import pipeline as ppl 

# image height and image width ----> GLOBAL
img_ht = 512
img_wd = 512
path_toCollect =  './test_images'
path_toSave = './prc_test_images'
train_data = pd.read_csv('sample_submission.csv')
newDataframe_cols = ['id_code','diagnosis'] 
trained_data = pd.DataFrame(columns=newDataframe_cols)

# The earlier csv file does not have images with its extention
def appendPNG(img_id):
    return str(img_id) + '.png'

def feedToPipeline(image_name,diagnosis_type):
    global path_toCollect
    global path_toCollect
    global img_ht,img_wd
    global trained_data, train_data
    
    try:
        # print(train_data[train_data['id_code']== image_name].index.item(),image_name,diagnosis_type)
        # print(train_data[train_data['id_code']== image_name].index.item())
        image_name = appendPNG(image_name)
        image = cv2.imread(os.path.join(path_toCollect,image_name))
        image = ppl.imageResize(image, img_ht, img_wd)
        org_copy = image.copy()
        image_crop = ppl.crop_black(image)
        image_clahe = ppl.imageHistEqualization(image_crop)
        sub_med = ppl.subtract_median_bg_image(image_clahe)
        image_final = ppl.colorEnhancement(sub_med, image_clahe)
        count = ppl.processed_test_save(path_toSave,image_final,img_ht,img_wd)
        count = str(count) + '.png'
        len_trained_data = len(trained_data)
        trained_data.loc[len_trained_data]   = [count,diagnosis_type]
    except:
        print("================")
        pass
    

def main():
    start = time.time()

    # Vectorize approach took 846 seconds and the for loop took 905 seconds to process more than 3 thousand images
    # 
    # np.vectorize(feedToPipeline)(train_data['id_code'],train_data['diagnosis'])
    # 
    for i in range(len(train_data)): 
        print(i,train_data['id_code'][i],train_data['diagnosis'][i])
        feedToPipeline(train_data['id_code'][i],train_data['diagnosis'][i])
    # 
    trained_data.to_csv('prc_test.csv')

    end = time.time()
    print(end - start)

# --------------------

if __name__ == "__main__":
    main()

# --------------------

''' NO USE CODE 

# This code below is used to append png to each image_id
train_data['id_code'] = train_data['id_code'].apply(appendPNG)

# This code below was used to remove anomaly in the image_id such as the + sign .

anomaly_id = []
for i in range(len(train_data)):
    image_name_temp = train_data['id_code'][i]
    if('+' in image_name_temp):
        print(i,image_name_temp,train_data['diagnosis'][i])
        anomaly_id.append(image_name_temp)
        train_data = train_data.drop( train_data[train_data['id_code']== image_name_temp].index)
        print('anomaly')
        train_data.to_csv('train.csv')

'''

# NOTE : 
# If some functionality not working properly, then please refer prac_preprocessing.py from the practice folder .