#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import glob
import argparse
import os
import time
import tensorflow as tf

from ioi.Code.model import RPN3D
from ioi.Code.config import cfg
from ioi.Code.utils import *
from ioi.Code.utils.kitti_loader import iterate_data, sample_test_data
from ioi.Code.filter_noise import filter_noise
from ioi.Code.filter_objects import *
from ioi.Code.filter_downsampled_objects import *

def IOI(input_calib_url,
        input_image_2_url,
        input_label_2_url,
        input_velodyne_url,
        output_folder_url):

    MODEL = 'pre_trained_car'
    DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    INPUT_DATA_DIR = [input_calib_url,
                      input_image_2_url,
                      input_label_2_url,
                      input_velodyne_url]
    MODEL_DIR = os.path.join(DATA_DIR, 'model', MODEL)

    with tf.Graph().as_default():

        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=cfg.GPU_MEMORY_FRACTION,
                                    visible_device_list=cfg.GPU_AVAILABLE,
                                    allow_growth=True)
    
        config = tf.ConfigProto(gpu_options=gpu_options,
                                device_count={"GPU": cfg.GPU_USE_COUNT,},
                                allow_soft_placement=True,)

        with tf.Session(config=config) as sess:
            model = RPN3D(cls=cfg.DETECT_OBJ,
                          single_batch_size=1,
                          avail_gpus=cfg.GPU_AVAILABLE.split(','))

            if tf.train.get_checkpoint_state(MODEL_DIR):
                print("Reading model parameters from %s" % MODEL_DIR)
                model.saver.restore(sess, tf.train.latest_checkpoint(MODEL_DIR))
        
            for batch in iterate_data(INPUT_DATA_DIR, 
                                      shuffle=False,
                                      aug=False,
                                      is_testset=False,
                                      batch_size=cfg.GPU_USE_COUNT,
                                      multi_gpu_sum=cfg.GPU_USE_COUNT):

                tags, results, front_images, bird_views, heatmaps = model.predict_step(INPUT_DATA_DIR,
                                                                                       sess,
                                                                                       batch,
                                                                                       summary=False)                
                # ret: A, B
                # A: (N) tag
                # B: (N, N') (class, x, y, z, h, w, l, rz, score)
                for tag, result in zip(tags, results):
                    os.makedirs(os.path.join(output_folder_url, tag), exist_ok=True)
                    of_path = os.path.join(output_folder_url, tag, 'result.txt')
                    with open(of_path, 'w+') as f:
                        labels = box3d_to_label([result[:, 1:8]],
                                                [result[:, 0]],
                                                [result[:, -1]],
                                                coordinate='lidar')[0]
                        for line in labels:
                            f.write(line)
                        print('write out {} objects to {}'.format(len(labels), tag))
                # dump visualizations
                for tag, front_image, bird_view, heatmap in zip(tags, front_images, bird_views, heatmaps):
                    front_img_path = os.path.join( output_folder_url, tag, 'front.jpg'  )
                    bird_view_path = os.path.join( output_folder_url, tag, 'bv.jpg'  )
                    heatmap_path = os.path.join( output_folder_url, tag, 'heatmap.jpg'  )
                    cv2.imwrite( front_img_path, front_image )
                    cv2.imwrite( bird_view_path, bird_view )
                    cv2.imwrite( heatmap_path, heatmap )

def ND( input_cloud_2_url,output_folder_url):
    INPUT_DATA_DIR = input_cloud_2_url
    input_dir = input_cloud_2_url
    OUTPUT_DATA_DIR = output_folder_url
    reverse_input = input_dir[::-1]
    name_input = reverse_input.partition("/")[0]
    Input_file_name = name_input[::-1]
        
    if OUTPUT_DATA_DIR[len(OUTPUT_DATA_DIR)-1]=="/":
        OUTPUT_DATA_DIR +=Input_file_name
    else:
        OUTPUT_DATA_DIR += "/"
        OUTPUT_DATA_DIR += Input_file_name
    print(INPUT_DATA_DIR)
    print(OUTPUT_DATA_DIR)
    filter_noise(INPUT_DATA_DIR , OUTPUT_DATA_DIR)

def OD( input_cloud_2_url,output_folder_url):
    INPUT_DATA_DIR = input_cloud_2_url
    input_dir = input_cloud_2_url
    OUTPUT_DATA_DIR = output_folder_url
    reverse_input = input_dir[::-1]
    name_input = reverse_input.partition("/")[0]
    Input_file_name = name_input[::-1]
        
    if OUTPUT_DATA_DIR[len(OUTPUT_DATA_DIR)-1]=="/":
        OUTPUT_DATA_DIR +=Input_file_name
    else:
        OUTPUT_DATA_DIR += "/"
        OUTPUT_DATA_DIR += Input_file_name
    print(INPUT_DATA_DIR)
    print(OUTPUT_DATA_DIR)
    filter_objects(INPUT_DATA_DIR , OUTPUT_DATA_DIR)

def SD( input_cloud_2_url,output_folder_url):
    INPUT_DATA_DIR = input_cloud_2_url
    input_dir = input_cloud_2_url
    OUTPUT_DATA_DIR = output_folder_url
    reverse_input = input_dir[::-1]
    name_input = reverse_input.partition("/")[0]
    Input_file_name = name_input[::-1]
        
    if OUTPUT_DATA_DIR[len(OUTPUT_DATA_DIR)-1]=="/":
        OUTPUT_DATA_DIR +=Input_file_name
    else:
        OUTPUT_DATA_DIR += "/"
        OUTPUT_DATA_DIR += Input_file_name
    print(INPUT_DATA_DIR)
    print(OUTPUT_DATA_DIR)
    filter_downsampled_objects(INPUT_DATA_DIR , OUTPUT_DATA_DIR)


