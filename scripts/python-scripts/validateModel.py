from ultralytics import YOLO

# Load the model (fine-tuned or pre-trained)
model = YOLO('../../models/best.pt')  # Replace with your model's path

# Run validation
results = model.val(data='../../resources/fortnite/Datasets/fortnite_elimination_count_logo/data.yaml', imgsz=640, batch=16)

# Access metrics
print(results.metrics)  # Includes mAP, Precision, Recall
