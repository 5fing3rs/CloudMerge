import pcl

# Returns Downsampled version of a point cloud
# The bigger the leaf size the less information retained
def do_voxel_grid_filter(point_cloud, LEAF_SIZE = 0.01):
  voxel_filter = point_cloud.make_voxel_grid_filter()
  voxel_filter.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE) 
  return voxel_filter.filter()

# Returns only the point cloud information at a specific range of a specific axis
def do_passthrough_filter(point_cloud, name_axis = 'z', min_axis = 0.6, max_axis = 1.1):
  pass_filter = point_cloud.make_passthrough_filter()
  pass_filter.set_filter_field_name(name_axis);
  pass_filter.set_filter_limits(min_axis, max_axis)
  return pass_filter.filter()

# Use RANSAC planse segmentation to separate plane and not plane points
# Returns inliers (plane) and outliers (not plane)
def do_ransac_plane_segmentation(point_cloud, max_distance = 0.01):

  segmenter = point_cloud.make_segmenter()

  segmenter.set_model_type(pcl.SACMODEL_PLANE)
  segmenter.set_method_type(pcl.SAC_RANSAC)
  segmenter.set_distance_threshold(max_distance)

  #obtain inlier indices and model coefficients
  inlier_indices, coefficients = segmenter.segment()

  inliers = point_cloud.extract(inlier_indices, negative = False)
  outliers = point_cloud.extract(inlier_indices, negative = True)

  return inliers, outliers



##################################################################################
# This pipeline separates the objects in the table from the given scene

# Load the point cloud in memory
def filter_downsampled_objects(url1 , url_2):
  cloud = pcl.load_XYZRGB(url1)

  downsampled_path = url_2.partition(".")[0] + "_downsampled." + url_2.partition(".")[2]
  roi_path = url_2.partition(".")[0] + "_roi." + url_2.partition(".")[2]
  backgroud_path = url_2.partition(".")[0] + "_backgroud." + url_2.partition(".")[2]
  objects_path = url_2.partition(".")[0] + "_objects." + url_2.partition(".")[2]

  # Downsample the cloud as high resolution which comes with a computation cost
  downsampled_cloud = do_voxel_grid_filter(point_cloud = cloud, LEAF_SIZE = 0.01)
  pcl.save(downsampled_cloud, downsampled_path )

  # Get only information in our region of interest, as we don't care about the other parts
  filtered_cloud = do_passthrough_filter( point_cloud = downsampled_cloud, 
                                          name_axis = 'z', min_axis = 0.6, max_axis = 1.1)
  pcl.save(filtered_cloud, roi_path)

  # Separate the table from everything else
  table_cloud, objects_cloud = do_ransac_plane_segmentation(filtered_cloud, max_distance = 0.01)
  pcl.save(table_cloud, backgroud_path)
  pcl.save(objects_cloud, objects_path)

