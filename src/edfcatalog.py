""" edfcatalog.py

creates csv file with edf files metadata, saves it in patient's main directory

"""

# Import standard libraries
import pathlib
import os
import pandas as pd
import numpy as np
import mne
from datetime import datetime, timedelta

# Inputs
patient_id  = "PR06"
stage1_path = "/data_store0/presidio/nihon_kohden"
INDIR       = pathlib.Path(stage1_path, patient_id, patient_id)
OUTDIR      = pathlib.Path(stage1_path, patient_id)

# Custom functions to build catalog
##Get paths to each edf file in patient's directory
def GetFilePaths(FileDirectory, FileFormat):
    FileNames = sorted(filter(lambda x: True if FileFormat in x else False, os.listdir(FileDirectory)))
    FilePaths = []
    for i in range(len(FileNames)):
        FilePaths.append(pathlib.Path(FileDirectory, FileNames[i]))
    return FilePaths

##Create dictionary object with each edf metadata
def ExtractFileMetadata(FilePathList):
    edf_name     = []
    h5_name      = []
    edf_start    = []
    edf_stop     = []
    edf_duration = []
    edf_sfreq    = []
    edf_nsample  = []
    edf_path     = []

    for i in range(len(FilePathList)):
        raw          = mne.io.read_raw_edf(FilePathList[i])
        raw_start    = raw.info['meas_date']
        raw_duration = timedelta(seconds=len(raw)/raw.info['sfreq'])
        raw_n        = len(raw)
        raw_stop      = raw_start + raw_duration

        ##Create name of future h5 file:
        date_string  = raw_start.strftime('%Y%m%d')
        time_string  = raw_start.strftime('%H%M%S')
        h5_string    = f'sub-{patient_id}_ses-stage1_task-continuous_acq-{date_string}_run-{time_string}_ieeg.h5'
        edf_name.append(str(FilePathList[i]).split("/")[-1])
        h5_name.append(h5_string)
        edf_start.append(raw_start.replace(tzinfo=None))
        edf_stop.append(raw_stop.replace(tzinfo=None))
        edf_duration.append(raw_duration)
        edf_nsample.append(raw_n)
        edf_sfreq.append(raw.info['sfreq'])
        edf_path.append(str(FilePathList[i]))

    DictObj = {
            'edf_name': edf_name,
            'h5_name': h5_name,
            'edf_start': edf_start,
            'edf_end': edf_stop,
            'edf_duration': edf_duration,
            'edf_nsample': edf_nsample,
            'edf_sfreq': edf_sfreq,
            'edf_path': edf_path
            }

    return DictObj

# Start of actual code
edf_file_paths = GetFilePaths(INDIR, 'edf')
edf_dict       = ExtractFileMetadata(edf_file_paths)
edf_df         = pd.DataFrame(edf_dict)

edf_df.to_csv(pathlib.Path(OUTDIR, f"{patient_id}_edf_catalog.csv"), index=False)
print("")
print(f"{patient_id}_edf_catalog.csv has been created and saved in {OUTDIR}")

"""

End of code

"""

