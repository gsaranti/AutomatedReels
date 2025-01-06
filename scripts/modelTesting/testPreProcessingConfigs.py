import subprocess
import numpy as np
from collections import defaultdict
from ultralytics import YOLO
import torch

# Paths
VIDEO_PATH = "../../../../../../PostProcessTestClip.mp4"
MODEL_PATH = "../../../../local_models/best_isolated_local.pt"
OUTPUT_FILE = "../../docs/ffmpeg-pre-process-ranked.txt"

# YOLO Model
model = YOLO(MODEL_PATH)

ccm_values = [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27,
              0.28, 0.29, 0.3]  # Example grayscale weights
con_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]  # Example contrast values
br_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Example brightness values

def stream_frames_and_detect(video_path, fps=2):
    """Streams pre-processed frames from the video using FFmpeg and analyzes objects with multiple parameter combinations."""
    overall_results = []

    # Initialize baselines
    best_ccm_sum = -float("inf")

    for ccm in ccm_values:
        best_con_sum = -float("inf")  # Reset for each new `ccm`
        con_baseline_tested = False  # Ensure at least one test for each `con`

        for con in con_values:
            best_br_sum = -float("inf")  # Reset for each new `con`
            br_baseline_tested = False  # Ensure at least one test for each `br`

            for br in br_values:
                print(f"Testing combination: ccm={ccm}, con={con}, br={br}")

                object_data = defaultdict(lambda: {
                    "frame_count": 0,
                    "confidence_sum": 0.0,
                    "confidence_breakdown": {
                        "0-24": 0,
                        "25-49": 0,
                        "50-74": 0,
                        "75-100": 0
                    }
                })

                # FFmpeg command for processing frames
                ffmpeg_command = [
                    "ffmpeg",
                    "-i", video_path,
                    "-vf", (
                        f"fps={fps},format=bgr24,"
                        f"colorchannelmixer={ccm}:{ccm}:{ccm}:0:{ccm}:{ccm}:{ccm}:0:{ccm}:{ccm}:{ccm}:0,"
                        f"eq=saturation=0.0:contrast={con}:brightness={br},"
                        "format=yuv420p"
                    ),
                    "-f", "rawvideo",
                    "-pix_fmt", "bgr24",
                    "-hide_banner",
                    "-loglevel", "error",
                    "pipe:1"
                ]

                process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, bufsize=10**8)
                frame_size = (1920, 1080)  # Adjust based on video resolution
                frame_bytes = frame_size[0] * frame_size[1] * 3  # Width * Height * Channels (BGR)

                while True:
                    frame_data = process.stdout.read(frame_bytes)
                    if not frame_data:
                        break

                    frame = np.frombuffer(frame_data, np.uint8).reshape((frame_size[1], frame_size[0], 3))

                    results = model(frame, conf=0.5, device='mps')

                    detected_objects = {}
                    for box in results[0].boxes:
                        obj_name = model.names[int(box.cls)] if hasattr(model, "names") else f"class_{int(box.cls)}"
                        confidence = float(box.conf) * 100

                        if obj_name not in detected_objects or detected_objects[obj_name] < confidence:
                            detected_objects[obj_name] = confidence

                    for obj_name, confidence in detected_objects.items():
                        object_data[obj_name]["frame_count"] += 1
                        object_data[obj_name]["confidence_sum"] += confidence

                        if confidence < 25:
                            object_data[obj_name]["confidence_breakdown"]["0-24"] += 1
                        elif confidence < 50:
                            object_data[obj_name]["confidence_breakdown"]["25-49"] += 1
                        elif confidence < 75:
                            object_data[obj_name]["confidence_breakdown"]["50-74"] += 1
                        else:
                            object_data[obj_name]["confidence_breakdown"]["75-100"] += 1

                process.terminate()

                current_conf_sum = float(sum(data["confidence_sum"] for data in object_data.values()))

                print(f"Results for combination: ccm={ccm}, con={con}, br={br}")
                print(f"  Total Confidence Sum: {current_conf_sum:.2f}")

                # Store the results
                overall_results.append({
                    "ccm": ccm,
                    "con": con,
                    "br": br,
                    "confidence_sum": current_conf_sum,
                    "object_data": object_data
                })

    return overall_results

def format_results(results):
    """Formats the results into a human-readable string."""
    formatted_results = []

    for result in results:
        formatted_results.append(f"Combination: ccm={result['ccm']}, con={result['con']}, br={result['br']}")
        formatted_results.append(f"  Total Confidence Sum: {result['confidence_sum']:.2f}")
        for obj_name, data in result["object_data"].items():
            formatted_results.append(f"  Object: {obj_name}")
            formatted_results.append(f"    Frames Containing Object: {data['frame_count']}")
            formatted_results.append(f"    Sum of Confidence Scores: {data['confidence_sum']:.2f}")
            formatted_results.append(f"    Confidence Breakdown:")
            for range_name, count in data["confidence_breakdown"].items():
                formatted_results.append(f"      {range_name}: {count}")
        formatted_results.append("")  # Add a blank line for separation

    return "\n".join(formatted_results)

def write_results_to_file(results, output_file):
    """Writes formatted results to a text file."""
    formatted_results = format_results(results)
    with open(output_file, "w") as f:
        f.write(formatted_results)
    print(f"Results written to {output_file}")

def main():
    results = stream_frames_and_detect(VIDEO_PATH, fps=2)

    # Sort results by confidence sum in descending order
    results.sort(key=lambda x: x['confidence_sum'], reverse=True)

    write_results_to_file(results, OUTPUT_FILE)

if __name__ == "__main__":
    main()
