# Vehicle Classifier — Assignment Submission
 
## Overview
CNN-based vehicle image classifier using **MobileNetV2** transfer learning.
Classifies street images into 5 categories under a strict 5 MB model size constraint.
 
## Class Mapping
| Index | Class |
|-------|-------|
| 0     | Bus   |
| 1     | Truck |
| 2     | Car   |
| 3     | Bike  |
| 4     | None  |
 
## Submission Files
```
Assignment_Submission/
├── vehicle_classifier.py   ← inference class (do not rename)
├── student_model.pth       ← trained weights (4.978 MB)
├── report.pdf              ← full report
└── README.md               ← this file
```
 
## How to Run Inference
```python
from vehicle_classifier import VehicleClassifier, CLASS_IDX
 
clf = VehicleClassifier(model_path="student_model.pth")
idx = clf.predict("test_image.jpg")   # returns int 0-4
print(CLASS_IDX[idx])
```
 
## Model Details
| Property            | Value                              |
|---------------------|------------------------------------|
| Architecture        | MobileNetV2 + custom 5-class head  |
| Pretrained on       | ImageNet (transfer learning)       |
| Input size          | 224×224 (handles up to 256×256)    |
| Model size          | 4.978 MB (float16)                 |
| Best val accuracy   | 93.6%                              |
| Inference device    | CPU only                           |
| Training epochs     | 5 (head warmup) + 30 (fine-tune)   |
 
## Dependencies
```
torch>=1.13
torchvision>=0.14
Pillow
```
 
## Training
Training was done on Kaggle with GPU (T4).
Dataset: 35,013 images from ImageNet Winter21 across 5 classes.
See `report.pdf` for full training methodology and results.
