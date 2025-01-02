# Training YOLOv8 Model in Google Colab

This document provides a step-by-step guide to train a YOLOv8 model in Google Colab, including instructions to troubleshoot and locate the `best.pt` file if it is not saved in the expected directory.

---

## **1. Setup Colab Environment**

### **1.1 Select Hardware Accelerator**
1. Navigate to **Runtime > Change Runtime Type**.
2. Set **Hardware Accelerator** to **GPU**.
3. Click **Save**.

### **1.2 Install Required Libraries**
Install the YOLOv8 package and required dependencies:
```bash
!pip install ultralytics
```

### **1.3 Verify GPU availability**
```bash
!nvidia-smi
```

---

## **2. Prepare the Dataset**

### **2.1 Upload the Dataset to Google Drive**
Ensure your dataset is structured as follows:
```
dataset/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
```
Upload the dataset folder to your Google Drive.

### **2.2 Mount Google Drive**
Mount your Google Drive to access the dataset:
```python
from google.colab import drive
drive.mount('/content/drive')
```

### **2.3 Verify your dataset location in Google Drive**
```bash
!ls /content/drive/MyDrive/Datasets/final_fortnite_color_yolov8_dataset
```

### **2.4 Copy Dataset to Local Storage**
Copy the dataset from Google Drive to Colab's local storage for faster access:
```bash
!cp -r /content/drive/MyDrive/Datasets/final_fortnite_color_yolov8_dataset /content/dataset
```

### **2.5 Optional: Copy Existing Model to Local Storage**
```bash
!cp -r /content/drive/MyDrive/models/yolo_model.pt /content
```

### **2.6 Verify Dataset Structure**
List files to confirm:
```bash
!ls /content/dataset/train/images
!ls /content/dataset/train/labels
!ls /content/dataset/val/images
!ls /content/dataset/val/labels
```

---

## **3. Configure the Training Process**

### **3.1 Create the `data.yaml` File**
Ensure the `data.yaml` file is present in the dataset directory or create it:
```python
data_yaml = """
train: /content/dataset/train/images
val: /content/dataset/val/images

nc: 3
names: ['eliminated', 'knocked', 'victory_royale']
"""

with open('/content/data.yaml', 'w') as f:
    f.write(data_yaml)
```

### **3.2 Verify the contents of the data.yaml file**
```bash
!cat /content/data.yaml
```

### **3.3 Train the Model**
Run the following code to train the model:
```python
from ultralytics import YOLO

# Load the pretrained YOLOv8 model
model = YOLO('yolov8s.pt')  # Path to the pretrained weights

# Train the model
model.train(
    data='/content/data.yaml',  # Path to dataset configuration
    epochs=25,                  # Number of training epochs
    batch=8,                    # Batch size
    imgsz=1920,                 # Image resolution
    device=0,                   # Use GPU
    cos_lr=True
)
```

---

## **4. Locate the `best.pt` File**

### **4.1 Expected Save Location**
By default, the trained weights are saved in:
```
/content/runs/train/exp/weights/best.pt
```

Sometimes bash commands stop working after training. To list content in a directory with python:
```python
import os

items = os.listdir("/content/runs/detect/train")
for item in items:
    print(item)
```

### **4.2 Check for Missing `best.pt`
If the file is not in the expected directory, check the `/content/runs/detect/` folder:
1. List the `detect` folder contents:
   ```bash
   !ls /content/runs/detect/
   ```
2. If subfolders like `train` or `train2` exist in `detect`, check their `weights/` directory:
   ```bash
   !ls /content/runs/detect/train/weights/
   ```
   ```bash
   !ls /content/runs/detect/train2/weights/
   ```

3. If `best.pt` is found, move it to the proper location for organization:
   ```bash
   !mkdir -p /content/runs/train/train
   !mv /content/runs/detect/train/weights /content/runs/train/train/
   ```

4. To search for `best.pt` globally:
   ```bash
   !find /content -name "best.pt"
   ```

---

## **5. Validate the Trained Model**

### **5.1 Load and Test the Model**
Use the following code to validate the model:
```python
from ultralytics import YOLO

# Load the trained model
model = YOLO('/content/runs/train/train/weights/best.pt')

# Test on a validation image
results = model.predict(source='/content/dataset/val/images/example.jpg', imgsz=1920)

# Display the result
results[0].show()
```

### **5.2 Save Predictions**
To save the predictions:
```python
results = model.predict(source='/content/dataset/val/images/', imgsz=1920, save=True)
```
The annotated images will be saved in:
```
/content/runs/predict/exp/
```

---

## **6. Backup Your Model**

### **6.1 Download the Model to Local Machine**
```python
from google.colab import files
files.download('/content/runs/detect/train/weights/best.pt')
```

### **6.2 Save the Model to Google Drive**
```bash
!cp /content/runs/detect/train/weights/best.pt /content/drive/MyDrive/best.pt
```

---

## **7. Troubleshooting**

### **Common Issues:**
1. **FileNotFoundError:** Ensure the dataset path in `data.yaml` is correct.
2. **Low Performance:**
    - Check if the images and annotations are correctly labeled.
    - Fine-tune the model by running additional epochs.
3. **Missing `best.pt` File:** Follow the steps in Section 4.2 to locate it.

