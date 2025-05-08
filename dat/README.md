# PTB-XL Dataset and ECG Image Processing Workflow

## Dataset Overview

This directory contains data derived from the PTB-XL dataset, a large publicly available electrocardiography dataset.

### PTB-XL Dataset Description

The PTB-XL dataset is a comprehensive collection of 21,799 clinical 12-lead ECGs from 18,869 patients, each with a 10-second duration. Key characteristics of the dataset include:

- **Demographics**: The dataset covers patients of all ages (0-95 years), with a median age of 62 years. Gender distribution is balanced with 52% male and 48% female participants.
- **ECG Recordings**: All ECGs contain the standard 12 leads (I, II, III, AVL, AVR, AVF, V1-V6)
- **Annotations**: Each ECG is annotated by up to two cardiologists with standardized SCP-ECG statements
- **Diagnosis Distribution**:
  - Normal ECG: 9,514 records
  - Myocardial Infarction: 5,469 records
  - ST/T Change: 5,235 records
  - Conduction Disturbance: 4,898 records
  - Hypertrophy: 2,649 records

### Data Format

The original dataset provides waveform files in:
- High resolution (500 Hz) in the `records500/` directory
- Lower resolution (100 Hz) in the `records100/` directory

All files are stored in WaveForm DataBase (WFDB) format with 16-bit precision at a resolution of 1μV/LSB.

## Image Generation Workflow

Our workflow for processing the PTB-XL dataset involves the following steps:

1. **Data Acquisition**: Download the raw signal data from the original PTB-XL dataset
2. **Image Generation**: Generate ECG images from the raw signal data using the ECG-Image-Kit from AlphanumericsLab
3. **Image Cleaning**: Process and clean the generated images
4. **Annotation Mapping**: Map the PTB-XL diagnostic annotations to the generated images
5. **Model Training**: Train machine learning models on the processed images

### ECG-Image-Kit

We use the ECG-Image-Kit toolbox (https://github.com/alphanumericslab/ecg-image-kit) for generating synthetic ECG images. This toolkit enables:

- Plotting ECG time-series data on standard ECG paper-like backgrounds
- Applying realistic distortions to simulate real-world ECG printouts, including:
  - Handwritten text artifacts
  - Paper wrinkles and creases
  - Perspective transforms
  - Various noise and artifact simulations

The ECG-Image-Kit is particularly valuable for generating training data for machine learning models while ensuring patient privacy by producing synthetic, non-identifiable images.

### Image Generation Process

The image generation follows these specific steps:

1. Extract the time-series ECG data from the PTB-XL WFDB files
2. Configure the ECG-Image-Generator with appropriate parameters:
   - Paper grid settings (1mm fine grid, 5mm coarse grid)
   - Lead configuration (standard 12-lead format)
   - Signal gain and paper speed settings
3. Generate synthetic ECG images that simulate printed ECGs
4. Apply realistic artifacts to the images to improve model robustness
5. Save the generated images with appropriate metadata linking back to original diagnostic labels

### Data Cleaning and Preprocessing

After image generation, we perform several cleaning steps:
- Binarization for noise removal
- Deskewing for Orientation correction
- Masking/ Blurring for Grid removal
- Contrast enhancement for grid removal
- Spline reconstruction for reconnecting signal

### Annotation Mapping

The original PTB-XL annotations are mapped to our generated images, maintaining the diagnostic classifications:
- Normal
- Myocardial Infarction
- ST/T Change
- Conduction Disturbance
- Hypertrophy

## Usage Instructions

1. Download the PTB-XL dataset from PhysioNet: https://physionet.org/content/ptb-xl/1.0.3/
2. Follow the installation instructions for ECG-Image-Kit: https://github.com/alphanumericslab/ecg-image-kit
3. Use the ECG-Image-Generator scripts to create ECG images from the downloaded signals
4. Process the generated images using the provided cleaning scripts
5. Train ML models using the images and their corresponding diagnostic labels

## Citation Information

When using the PTB-XL dataset, please cite:
```
Wagner, P., Strodthoff, N., Bousseljot, R., Samek, W., & Schaeffter, T. (2022). 
PTB-XL, a large publicly available electrocardiography dataset (version 1.0.3). 
PhysioNet. https://doi.org/10.13026/kfzx-aw45

Wagner, P., Strodthoff, N., Bousseljot, R.-D., Kreiseler, D., Lunze, F.I., Samek, W., 
Schaeffter, T. (2020), PTB-XL: A Large Publicly Available ECG Dataset. 
Scientific Data. https://doi.org/10.1038/s41597-020-0495-6
```

When using the ECG-Image-Kit, please cite:
```
Kshama Kodthalu Shivashankara, Deepanshi, Afagh Mehri Shervedani, Matthew A. Reyna, 
Gari D. Clifford, Reza Sameni (2024). ECG-image-kit: a synthetic image generation 
toolbox to facilitate deep learning-based electrocardiogram digitization. 
In Physiological Measurement. IOP Publishing. doi: 10.1088/1361-6579/ad4954
```

## License

The PTB-XL dataset is released under a Creative Commons Attribution 4.0 International Public License.

## Contact

For questions regarding the original PTB-XL dataset, please refer to PhysioNet.
For questions regarding the ECG-Image-Kit, contact: ecg-image-kit@dbmi.emory.edu