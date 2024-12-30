# Fine-Tuning Metrics and Desired Trends

When fine-tuning a model like YOLOv8, the goal is to improve its performance on the dataset. Here's what to monitor and how to interpret the metrics:

---

## Key Metrics and Desired Trends

### Metrics You Want to See Increase
- **mAP@50**: Mean Average Precision at a 50% IoU threshold.
    - Higher mAP@50 indicates the model is detecting objects accurately at a basic level.

- **mAP@50:95**: Average mAP across IoU thresholds from 50% to 95%.
    - This measures both localization and confidence accuracy. An increase shows better overall model performance.

- **Precision**:
    - Measures the proportion of correct positive detections.
    - A higher precision means fewer false positives.

- **Recall**:
    - Measures the proportion of true positives detected out of all actual positives.
    - A higher recall means the model is missing fewer true detections.

### Metrics You Want to See Decrease
- **Box Loss**:
    - Lower box loss indicates the model is predicting bounding boxes more accurately.

- **Objectness Loss**:
    - Lower objectness loss means the model is improving its ability to detect objects confidently and distinguish them from the background.

- **Classification Loss**:
    - Lower classification loss indicates the model is assigning the correct class to detected objects more consistently.

---

## During Fine-Tuning

When fine-tuning your YOLOv8 model:

- **mAP Metrics**:
    - These should improve for both the new class (e.g., Victory Royale) and the existing class (e.g., elimination count logo).
    - If mAP for the existing class drops, it may indicate **catastrophic forgetting**.

- **Precision and Recall**:
    - Precision may initially decrease if the model begins to over-detect the new class (false positives), but it should stabilize.
    - Recall should improve for the new class as the model learns to detect it.

---

## Common Scenarios and Actions

| **Scenario**                      | **Metric Behavior**                  | **Action**                                     |
|-----------------------------------|--------------------------------------|-----------------------------------------------|
| **New class improves, old class worsens** | mAP/Recall drop for old class       | Reduce learning rate, check for overfitting.  |
| **Both classes improve**          | All metrics increase, losses decrease | Continue fine-tuning as planned.             |
| **Metrics stagnate**              | No significant changes               | Increase dataset diversity, adjust weights.  |
| **Loss increases, mAP decreases** | Poor localization or misclassification | Check annotations, reduce learning rate.     |

---

## How to Monitor During Fine-Tuning

### Validation Metrics
- After each epoch, YOLOv8 logs mAP, Precision, Recall, and Loss metrics. Use these to track progress.

### Use Visualization Tools
- Tools like **Weights & Biases (W&B)** or **TensorBoard** can help you visualize trends over epochs.

---

## Ideal Trends

- Loss metrics (Box, Objectness, Classification) should **decrease** consistently.
- mAP, Precision, and Recall should **increase** for both classes.
- Any degradation in performance for the elimination count logo class should be minimal.
