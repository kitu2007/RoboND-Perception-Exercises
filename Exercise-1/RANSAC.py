# Import PCL module
import pcl
import ipdb

# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')


# Voxel Grid filter
vox = cloud.make_voxel_grid_filter()
LEAF_SIZE = .01
vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

cloud_filtered = vox.filter()
filename = 'voxel_downsampled.pcd'
pcl.save(cloud_filtered, filename)

# PassThrough filter
passthrough = cloud_filtered.make_passthrough_filter()

# Assign axis and range to the passthrough filter object
filter_axis = 'z'
passthrough.set_filter_field_name(filter_axis)
axis_min = .6; axis_max = 2
passthrough.set_filter_limits(axis_min, axis_max)

#ipdb.set_trace()

cloud_filtered = passthrough.filter()
filename = 'pass_through_filtered.pcd'
pcl.save(cloud_filtered, filename)

# RANSAC plane segmentation
seg = cloud_filtered.make_segmenter()

seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)

#
max_distance = 0.01
seg.set_distance_threshold(max_distance)

# Extract inliers
inliers, coefficients = seg.segment()
extracted_inliers = cloud_filtered.extract(inliers, negative=False)
# Save pcd for table
filename = 'extracted_inliers.pcd'
pcl.save(extracted_inliers, filename)

if 1:
    # Extract outliers
    extracted_outliers = cloud_filtered.extract(inliers, negative=True)

    # Save pcd for tabletop objects
    filename = 'extracted_outliers.pcd'
    pcl.save(extracted_outliers, filename)




