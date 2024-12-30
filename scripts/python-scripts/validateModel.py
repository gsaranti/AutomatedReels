# This script is to perform model validation on an M1 mac.

from ultralytics import YOLO
import torch

# Check and set device to MPS (Metal Performance Shaders)
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

# Load the model
model = YOLO('../../models/best.pt')

# Run validation
results = model.val(
    data='../../resources/fortnite/Datasets/fortnite_elimination_count_logo/data.yaml',
    imgsz=1280,    # Adjust resolution
    batch=4,       # Reduce batch size for M1 memory limitations
    device=device  # Use MPS if available
)

# Print metrics
print(results.metrics)
