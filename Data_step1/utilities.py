import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import scipy.misc
import scipy.ndimage

import skimage
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import disk, binary_erosion, binary_closing
from skimage.filters import roberts
from scipy import ndimage as ndi

np.set_printoptions(precision=2)


def check_paths_validity(path_lst):
    for path in path_lst:
        if os.path.isdir(path):
            print(path, " --> OK")
        else:
            print(path, " --> Error!")


def build_patient_list(ct_scans_path,subfolder=''):
    folders = os.listdir(ct_scans_path)
    patients = []
    for folder in folders:
        if os.path.isdir(ct_scans_path + folder):  # process only folders
            dcm_files = []
            files = os.listdir(ct_scans_path + folder + subfolder ) # \1 or \RS_3
            for file in files:
                if file.endswith(".dcm"):
                    dcm_files.append(file)
            if len(dcm_files) > 0:
                patients.append(folder)
                print("build_patient_list|Info: patient <{}> found with {} dcm files".format(ct_scans_path + folder, len(dcm_files)))
            else:
                print("build_patient_list|Warn: empty patient data folder ", ct_scans_path + folder)
    print("Patients detected:{}".format(str(len(patients))))
    return sorted(patients)


def read_annotation_data(annotation_csv):
    df_annotation = pd.read_csv(annotation_csv).dropna()
    annotation_count = df_annotation.ID.count()
    patient_count = df_annotation['ID'].nunique()
    print("read_annotation_data|Info: {} annotations for {} patients {}".format(annotation_count, patient_count,
                                                                                annotation_csv))
    return df_annotation


def plot_ct_image(scan):
    num_slices = scan.shape[0]
    print("viz_ct_scan|Info ==> Slices:", num_slices)
    cols = 6
    rows = int(num_slices / cols) + 1

    fig, axs = plt.subplots(rows, cols, tight_layout=True, figsize=(12, 1.3 * rows))
    for i in range(rows * cols):
        axs[i // cols, i % cols].axis('off')
    for i in range(num_slices):
        axs[i // cols, i % cols].imshow(scan[i], cmap='gray', vmin=np.min(scan), vmax=np.max(scan))
    # fig.suptitle(viz_title, fontsize=10)
    plt.subplots_adjust(wspace=0.01, hspace=0.01)
    plt.show()
    plt.close('all')


def resample_ct_pixels(ct_pixels, ct_pixel_spacing, new_spacing=[1, 1, 1]):
    resize_factor = ct_pixel_spacing / new_spacing
    new_real_shape = ct_pixels.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / ct_pixels.shape
    new_spacing = ct_pixel_spacing / real_resize_factor
    ct_resampled = scipy.ndimage.interpolation.zoom(ct_pixels, real_resize_factor, mode='nearest')
    print("resample_ct_pixels|Info ==>",
          "Original shape  :", str(ct_pixels.shape),
          "New shape  :", str(ct_resampled.shape))
    print("resample_ct_pixels|Info ==>",
          "Original spacing:", ct_pixel_spacing,
          "New spacing:", new_spacing)
    return ct_resampled


MIN_BOUND_HU = -1000.0
MAX_BOUND_HU = 400.0


def truncate_hu(ct_img_array):
    # set all hu values outside the range [-1000,400] to -1000 (corresponds to air)
    ct_img_array[ct_img_array > MAX_BOUND_HU] = -1000
    ct_img_array[ct_img_array < MIN_BOUND_HU] = -1000
    return ct_img_array


def normalize(ct_img_array):
    ct_img_array = (ct_img_array - MIN_BOUND_HU) / (MAX_BOUND_HU - MIN_BOUND_HU)
    ct_img_array[ct_img_array > 1] = 1.
    ct_img_array[ct_img_array < 0] = 0.
    return ct_img_array


def compute_lung_mask(ct_img_array, threshold=-350):
    num_slices = ct_img_array.shape[0]
    lung_mask = []
    for i in range(num_slices):
        img = ct_img_array[i]
        '''
        Step 1: Convert into a binary image. 
        '''
        binary_mask = img < threshold
        '''
        Step 2: Remove the blobs connected to the border of the image.
        '''
        cleared = clear_border(binary_mask)
        '''
        Step 3: Label the image.
        '''
        label_image = label(cleared)
        '''
        Step 4: Keep the labels with 2 largest areas.
        '''
        areas = [r.area for r in regionprops(label_image)]
        areas.sort()
        if len(areas) > 2:
            for region in regionprops(label_image):
                if region.area < areas[-2]:
                    for coordinates in region.coords:
                        label_image[coordinates[0], coordinates[1]] = 0
        binary_mask = label_image > 0
        '''
        Step 5: Closure operation with a disk of radius 10. This operation is 
        to keep nodules attached to the lung wall.
        '''
        selem = disk(10)
        binary_mask = binary_closing(binary_mask, selem)
        '''
        Step 5: Fill in the small holes inside the binary mask of lungs.
        '''
        edges = roberts(binary_mask)
        binary_mask = ndi.binary_fill_holes(edges)
        lung_mask.append(binary_mask)

    return np.asarray(lung_mask)


def apply_lung_mask(ct_img_array, lung_mask):
    ct_lung_seg = ct_img_array.copy()
    ct_lung_seg[lung_mask == 0] = 0
    return ct_lung_seg


def viz_ct_scan(scan, out_pdf_file):
    num_slices = scan.shape[0]
    print("viz_ct_scan|Info ==> Slices:", num_slices)
    cols = 6
    rows = int(num_slices / cols) + 1

    fig, axs = plt.subplots(rows, cols, tight_layout=True, figsize=(8, 1.3 * rows))
    for i in range(rows * cols):
        axs[i // cols, i % cols].axis('off')
    for i in range(num_slices):
        axs[i // cols, i % cols].imshow(scan[i], cmap='gray', vmin=np.min(scan), vmax=np.max(scan))
    # fig.suptitle(viz_title, fontsize=10)
    plt.subplots_adjust(wspace=0.01, hspace=0.01)
    plt.savefig(out_pdf_file)
    plt.close('all')


def first_nonzero(arr, axis, invalid_val=-1):
    mask = arr != 0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


def last_nonzero(arr, axis, invalid_val=-1):
    mask = arr != 0
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


def crop_ct_lungs(scan, mask, margin=32):
    num_slices = mask.shape[0]
    h_min = mask.shape[1]
    h_max = 0
    v_min = mask.shape[2]
    v_max = 0

    crop_slices = []

    for i in range(num_slices):
        img = mask[i, :, :]
        img_x_min = max(0, np.min(first_nonzero(img, axis=1, invalid_val=img.shape[1])) - margin)
        img_x_max = min(img.shape[1], np.max(last_nonzero(img, axis=1, invalid_val=0)) + margin)
        img_y_min = max(0, np.min(first_nonzero(img, axis=0, invalid_val=img.shape[0])) - margin)
        img_y_max = min(img.shape[0], np.max(last_nonzero(img, axis=0, invalid_val=0)) + margin)
        if img_x_min < h_min:
            h_min = img_x_min
        if img_x_max > h_max:
            h_max = img_x_max
        if img_y_min < v_min:
            v_min = img_y_min
        if img_y_max > v_max:
            v_max = img_y_max

    for i in range(num_slices):
        crop_slices.append(scan[i, v_min:v_max, h_min:h_max])
    scan_crop = np.asarray(crop_slices)
    print("lung_seg_crop|Info ==> original shape {} --> cropped shape {}".format(scan.shape, scan_crop.shape))
    return scan_crop


def export_normal_patches(lung_seg_cropped, patch_shape, stride, out_path, patch_npy_prefix, patient_id):
    patches = []
    depth = lung_seg_cropped.shape[0]
    height = lung_seg_cropped.shape[1]
    width = lung_seg_cropped.shape[2]

    dd = patch_shape[0]
    hh = patch_shape[1]
    ww = patch_shape[2]

    stride_d = stride[0]
    stride_h = stride[1]
    stride_w = stride[2]

    for d in range(0, depth - dd, stride_d):
        for h in range(0, height - hh, stride_h):
            for w in range(0, width - ww, stride_w):
                d1 = d + dd
                h1 = h + hh
                w1 = w + ww
                if (d1 <= depth) and (h1 <= height) and (w1 <= width):
                    patches.append(lung_seg_cropped[d:d1, h:h1, w:w1])
    if len(patches) > 0:
        patch = np.asarray(patches)
        assert patch.dtype == 'float64'
        out_normal_patch_npy = out_path + patch_npy_prefix + "_" + str(len(patches)).zfill(4) + "_" + \
                               str(dd).zfill(3) + "_" + str(hh).zfill(3) + "_" + str(ww).zfill(3) + "_" + \
                               patient_id + ".npy"
        np.save(out_normal_patch_npy, patch)
        print("export_normal_patches|Info: saved patch:", out_normal_patch_npy)
    else:
        print('export_normal_patches|Error: no data to export as patch')

def export_normal_slices(lung_seg_cropped, patch_shape, stride, out_path, patch_npy_prefix, patient_id):
    depth = lung_seg_cropped.shape[0]
    height = lung_seg_cropped.shape[1]
    width = lung_seg_cropped.shape[2]

    if depth > 0:
        out_normal_patch_npy = out_path + patch_npy_prefix  + "_" + \
                               str(depth).zfill(3) + "_" + str(height).zfill(3) + "_" + str(width).zfill(3) + "_" + \
                               patient_id + ".npy"
        np.save(out_normal_patch_npy, lung_seg_cropped)
        print("export_normal_patches|Info: saved patch:", out_normal_patch_npy)
    else:
        print('export_normal_patches|Error: no data to export as patch')




def export_centered_patches(lung_seg,
                            patient_ct_spacing, patient_ct_orig_shape,
                            df_patient_annot, output_shape,
                            out_path,
                            patch_npy_prefix, patient_id):
    depth, height, width = patient_ct_orig_shape
    patch_count = 0
    centered_patches = []

    for node_idx, cur_row in df_patient_annot.iterrows():
        node_x = cur_row["Center_x (px)"]
        node_y = cur_row["Center_y (px)"]
        node_z = cur_row["Center_z (px)"]
        out_array = np.zeros((output_shape[0], output_shape[1], output_shape[2]))
        center = np.array([int(depth) - node_z, node_y, node_x])
        v_center = np.rint(center * patient_ct_spacing)
        try:
            out_array[:, :, :] = lung_seg[[int(v_center[0] - 1), int(v_center[0]), int(v_center[0] + 1)],
                                 int(v_center[1] - output_shape[1] / 2):int(v_center[1] + output_shape[1] / 2),
                                 int(v_center[2] - output_shape[2] / 2):int(v_center[2] + output_shape[2] / 2)]
            centered_patches.append(out_array)
            patch_count += 1
        except:
            # print(node_x,node_y,node_z,"<- The coordinates are out of range!")
            continue

    print("Total centered patches extracted:", patch_count)
    if len(centered_patches) > 0:
        output_patch = np.asarray(centered_patches)
        out_center_patch_npy = out_path + patch_npy_prefix + "_" +str(len(centered_patches)).zfill(4) + "_" + \
                               str(output_shape[0]) + "_" + \
                               str(output_shape[1]) + "_" + \
                               str(output_shape[2]) + "_" + patient_id + ".npy"

        assert output_patch.dtype == 'float64'
        np.save(out_center_patch_npy, output_patch)
        print("export_center_patches|Info: saved patch:", out_center_patch_npy)
    else:
        print('export_center_patches|Error: no data to export as patch')


def export_random_centered_patches(lung_seg,
                            patient_ct_spacing, patient_ct_orig_shape,
                            df_patient_annot, output_shape,
                            out_path,
                            patch_npy_prefix, patient_id):
    depth, height, width = patient_ct_orig_shape
    patch_count = 0
    centered_patches = []

    for node_idx, cur_row in df_patient_annot.iterrows():
        node_x1 = cur_row["Center_x (px)_1"]
        node_y1 = cur_row["Center_y (px)_1"]
        node_z1 = cur_row["Center_z (px)_1"]
        node_x2 = cur_row["Center_x (px)_2"]
        node_y2 = cur_row["Center_y (px)_2"]
        out_array = np.zeros((output_shape[0], output_shape[1], output_shape[2]))
        for i in range(20): # 20 random patches for each slice!
            node_x = np.random.randint(node_x1,node_x2)
            node_y = np.random.randint(node_y1,node_y2)
            center = np.array([int(depth) - node_z1, node_y, node_x])
            v_center = np.rint(center * patient_ct_spacing)
            try:
                out_array[:, :, :] = lung_seg[[int(v_center[0] - 1), int(v_center[0]), int(v_center[0] + 1)],
                                     int(v_center[1] - output_shape[1] / 2):int(v_center[1] + output_shape[1] / 2),
                                     int(v_center[2] - output_shape[2] / 2):int(v_center[2] + output_shape[2] / 2)]
                centered_patches.append(out_array)
                patch_count += 1
            except:
                # print(node_x,node_y,node_z,"<- The coordinates are out of range!")
                continue

    print("Total centered patches extracted:", patch_count)
    if len(centered_patches) > 0:
        output_patch = np.asarray(centered_patches)
        out_center_patch_npy = out_path + patch_npy_prefix + "_" +str(len(centered_patches)).zfill(4) + "_" + \
                               str(output_shape[0]) + "_" + \
                               str(output_shape[1]) + "_" + \
                               str(output_shape[2]) + "_" + patient_id + ".npy"

        assert output_patch.dtype == 'float64'
        np.save(out_center_patch_npy, output_patch)
        print("export_random_centered_patches|Info: saved patch:", out_center_patch_npy)
    else:
        print('export_random_centered_patches|Error: no data to export as patch')


