# Fornite Model Notes

---

## **1/1/25:**

**Model name** - `best_isolated.pt`

**Dataset** - `final_fortnite_yolov8_dataset`

Dataset has augmented images with manual overlays of in game text.
Image is then adjusted to be black and white using the white_pixels.py script.
Current script values set for this dataset are:

* value_min=125
* saturation_max=50

Unedited images exists in "final_fortnite_color_yolov8_dataset".
