import os
import numpy as np
import pydicom


def load_ct_scan(path):
    dcm_files = []
    for file in os.listdir(path):
        _, file_extension = os.path.splitext(file)
        if file_extension == ".dcm":
            dcm_files.append(os.path.join(path, file))
    try:
        slices = [pydicom.read_file(dcm) for dcm in dcm_files]
        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))

        print("load_ct_scan|Info ==> loaded", str(len(slices)), "slices from:", path)

        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

        for s in slices:
            if slice_thickness > 0.0:
                s.SliceThickness = slice_thickness
            else:
                print("load_ct_scan|Error: Invalid slice thickness:", slice_thickness)
        spacing = np.array([slices[0].SliceThickness] + list(slices[0].PixelSpacing), dtype=np.float32)
        return slices, spacing
    except Exception as e:
        print("load_ct_scan|Error:", str(e))


def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    # Convert to int16 (from sometimes int16),
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0

    # Convert to Hounsfield units (HU)
    for slice_number in range(len(slices)):

        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope

        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)

        image[slice_number] += np.int16(intercept)

    return np.array(image, dtype=np.int16)



def extract_slice_metadata(slice, delimiter):

    metadata = []

    try:
        metadata.append(str(slice['SpecificCharacterSet']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ImageType']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['InstanceCreationDate']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['InstanceCreationTime']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SOPClassUID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SOPInstanceUID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['StudyDate']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['AcquisitionDate']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ContentDate']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['AcquisitionDateTime']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['StudyTime']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['AcquisitionTime']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ContentTime']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['AccessionNumber']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['Modality']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['Manufacturer']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['InstitutionName']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['InstitutionAddress']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ReferringPhysicianName']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['StationName']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['StudyDescription']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SeriesDescription']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['InstitutionalDepartmentName']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    # try:
    #     metadata.append(str(slice['OperatorName']).split(":")[1].strip())
    # except:
    #     metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ManufacturerModelName']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['IrradiationEventUID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PatientName']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PatientID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PatientBirthDate']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PatientSex']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PatientAge']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['MedicalAlerts']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ScanOptions']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SliceThickness']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['KVP']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SpacingBetweenSlices']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['DataCollectionDiameter']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SoftwareVersions']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ProtocolName']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ReconstructionDiameter']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['GantryDetectorTilt']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['TableHeight']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['RotationDirection']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ExposureTime']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['XRayTubeCurrent']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['Exposure']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['FilterType']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ConvolutionKernel']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PatientPosition']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ExposureModulationType']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['EstimatedDoseSaving']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['CTDIvol']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['StudyInstanceUID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SeriesInstanceUID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['StudyID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SeriesNumber']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['AcquisitionNumber']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['InstanceNumber']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    # try:
    #     metadata.append(str(slice['ImagePosition']).split(":")[1].strip())
    # except:
    #     metadata.append("_NO_VAL_")
    #
    # try:
    #     metadata.append(str(slice['ImageOrientation']).split(":")[1].strip())
    # except:
    #     metadata.append("_NO_VAL_")
    #
    # try:
    #     metadata.append(str(slice['FrameOfReferenceUID']).split(":")[1].strip())
    # except:
    #     metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['Laterality']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PositionReferenceIndicator']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SliceLocation']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['ImageComments']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['SamplesPerPixel']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PhotometricInterpretation']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['Rows']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['Columns']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PixelSpacing']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['BitsAllocated']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['BitsStored']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['HighBit']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PixelRepresentation']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['WindowCenter']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['WindowWidth']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['RescaleIntercept']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['RescaleSlope']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['LossyImageCompression']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['RequestedContrastAgent']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PreMedication']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    try:
        metadata.append(str(slice['PerformedProcedureStepID']).split(":")[1].strip())
    except:
        metadata.append("_NO_VAL_")

    return delimiter.join(metadata)


METADATA_HEADER = ['dcm_file',
                   'SpecificCharacterSet',
                   'ImageType',
                   'InstanceCreationDate',
                   'InstanceCreationTime',
                   'SOPClassUID',
                   'SOPInstanceUID',
                   'StudyDate',
                   'AcquisitionDate',
                   'ContentDate',
                   'AcquisitionDateTime',
                   'StudyTime',
                   'AcquisitionTime',
                   'ContentTime',
                   'AccessionNumber',
                   'Modality',
                   'Manufacturer',
                   'InstitutionName',
                   'InstitutionAddress',
                   'ReferringPhysicianName',
                   'StationName',
                   'StudyDescription',
                   'SeriesDescription',
                   'InstitutionalDepartmentName',
                   'ManufacturerModelName',
                   'IrradiationEventUID',
                   'PatientName',
                   'PatientID',
                   'PatientBirthDate',
                   'PatientSex',
                   'PatientAge',
                   'MedicalAlerts',
                   'ScanOptions',
                   'SliceThickness',
                   'KVP',
                   'SpacingBetweenSlices',
                   'DataCollectionDiameter',
                   'SoftwareVersions',
                   'ProtocolName',
                   'ReconstructionDiameter',
                   'GantryDetectorTilt',
                   'TableHeight',
                   'RotationDirection',
                   'ExposureTime',
                   'XRayTubeCurrent',
                   'Exposure',
                   'FilterType',
                   'ConvolutionKernel',
                   'PatientPosition',
                   'ExposureModulationType',
                   'EstimatedDoseSaving',
                   'CTDIvol',
                   'StudyInstanceUID',
                   'SeriesInstanceUID',
                   'StudyID',
                   'SeriesNumber',
                   'AcquisitionNumber',
                   'InstanceNumber',
                   'Laterality',
                   'PositionReferenceIndicator',
                   'SliceLocation',
                   'ImageComments',
                   'SamplesPerPixel',
                   'PhotometricInterpretation',
                   'Rows',
                   'Columns',
                   'PixelSpacing',
                   'BitsAllocated',
                   'BitsStored',
                   'HighBit',
                   'PixelRepresentation',
                   'WindowCenter',
                   'WindowWidth',
                   'RescaleIntercept',
                   'RescaleSlope',
                   'LossyImageCompression',
                   'RequestedContrastAgent',
                   'PreMedication',
                   'PerformedProcedureStepID']


def save_metadata(path, log_fh, delimiter):
    dcm_files = []
    for file in os.listdir(path):
        _, file_extension = os.path.splitext(file)
        if file_extension == ".dcm":
            dcm_files.append(os.path.join(path, file))
    try:
        for dcm in dcm_files:
            slice = pydicom.read_file(dcm)
            slice_metadata = extract_slice_metadata(slice, delimiter)
            log_fh.write(dcm + ";" + slice_metadata + "\n")
    except:
        print("save_metadata error")
