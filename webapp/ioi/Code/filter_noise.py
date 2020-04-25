import pcl

##################################################################################
# This pipeline reduces the statistical noise of the scene 

# port of http://pointclouds.org/documentation/tutorials/statistical_outlier.php
# download http://svn.pointclouds.org/data/tutorials/table_scene_lms400.pcd
def filter_noise(urls_1,url_2):
    point_cloud = pcl.load(urls_1)
    inliers_path = url_2.partition(".")[0] + "_inliers." + url_2.partition(".")[2]
    outliers_path = url_2.partition(".")[0] + "_outliers." + url_2.partition(".")[2]
    noise_filter = point_cloud.make_statistical_outlier_filter()

    # Set the number of neighboring points to analyze for any given point
    noise_filter.set_mean_k(50)

    # Any point with a mean distance larger than global (mean distance+x*std_dev)
    # will be considered outlier
    noise_filter.set_std_dev_mul_thresh(1.0) 
    pcl.save(noise_filter.filter(), inliers_path)

    noise_filter.set_negative(True)
    pcl.save(noise_filter.filter(), outliers_path)


