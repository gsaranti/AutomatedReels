import subprocess
import os
import numpy as np
from ultralytics import YOLO

# Paths
VIDEO_PATH = "../../../../../../fort4.mp4"
MODEL_PATH = "../../../../local_models/best_isolated_local.pt"
OUTPUT_VIDEO_PATH = "../../../../../../output_video_3.mp4"
TEMP_CLIPS_DIR = "../python-scripts/temp_clips"

# YOLO Model
model = YOLO(MODEL_PATH)

def stream_frames_and_detect(video_path, fps=2):
    """Streams pre-processed frames from the video using FFmpeg and detects objects."""
    detected_timestamps = []

    # ffmpeg_command = [
    #     "ffmpeg",
    #     "-i", video_path,
    #     "-vf", (
    #         f"fps={fps},format=bgr24,"  # Set FPS and output format
    #         "colorchannelmixer=.3:.3:.3:0:.3:.3:.3:0:.3:.3:.3:0,"  # Convert to grayscale
    #         "eq=saturation=0.0:contrast=1.5:brightness=0.1,"  # Adjust brightness/contrast
    #         "format=yuv420p"
    #     ),
    #     "-f", "rawvideo",
    #     "-pix_fmt", "bgr24",
    #     "-hide_banner",
    #     "-loglevel", "error",
    #     "pipe:1"
    # ]

    # Darker frames than above
    ffmpeg_command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", (
            f"fps={fps},format=bgr24,"  # Set FPS and output format
            "colorchannelmixer=.2:.2:.2:0:.2:.2:.2:0:.2:.2:.2:0,"  # Adjust grayscale weights
            "eq=saturation=0.0:contrast=3.0:brightness=0.1,"  # Increase contrast and brighten whites
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

    frame_count = 0
    fps_interval = 1 / fps

    while True:
        frame_data = process.stdout.read(frame_bytes)
        if not frame_data:
            break

        # Convert raw bytes to NumPy array
        frame = np.frombuffer(frame_data, np.uint8).reshape((frame_size[1], frame_size[0], 3))

        # Run inference on the pre-processed frame
        results = model(frame, conf=0.5)

        # If any objects are detected, log the timestamp
        if len(results[0].boxes) > 0:
            timestamp = frame_count * fps_interval
            detected_timestamps.append(timestamp)

        frame_count += 1

    process.terminate()
    return detected_timestamps


def merge_overlapping_timestamps(timestamps, segment_duration=3, video_duration=None):
    """Merges overlapping timestamps into unified segments, accounting for video start and end."""
    if not timestamps:
        return []

    timestamps.sort()
    merged_segments = []
    start = max(0, timestamps[0] - segment_duration)
    end = timestamps[0] + segment_duration

    for timestamp in timestamps[1:]:
        if timestamp - segment_duration <= end:
            # Extend the current segment
            end = max(end, timestamp + segment_duration)
        else:
            # Start a new segment
            merged_segments.append((start, min(end, video_duration)))
            start = max(0, timestamp - segment_duration)
            end = timestamp + segment_duration

    # Add the last segment, accounting for video end
    merged_segments.append((start, min(end, video_duration)))
    return merged_segments


def create_clips(video_path, segments, output_dir):
    """Cuts segments from the video and saves as individual clips."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, (start_time, end_time) in enumerate(segments):
        duration = end_time - start_time
        ffmpeg_command = [
            "ffmpeg",
            "-i", video_path,
            "-ss", f"{start_time:.2f}",
            "-t", f"{duration:.2f}",
            "-c:v", "libx264",  # Re-encode video using H.264 codec
            "-c:a", "aac",      # Re-encode audio using AAC codec
            "-strict", "experimental",
            f"{output_dir}/clip_{i:03d}.mp4",
            "-hide_banner",
            "-loglevel", "error"
        ]
        subprocess.run(ffmpeg_command)



def merge_clips(output_dir, output_video_path):
    """Merges all the clips into a single video."""
    clips = sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.mp4')])

    if not clips:
        print("No clips to merge.")
        return

    # Create a temporary text file with the list of clips
    with open("clips_list.txt", "w") as f:
        for clip in clips:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    # Merge clips using FFmpeg
    ffmpeg_command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "clips_list.txt",
        "-c", "copy",
        output_video_path,
        "-hide_banner",
        "-loglevel", "error"
    ]
    subprocess.run(ffmpeg_command)

    # Clean up
    os.remove("clips_list.txt")


def get_video_duration(video_path):
    """Returns the duration of the video in seconds."""
    ffprobe_command = [
        "ffprobe",
        "-i", video_path,
        "-show_entries", "format=duration",
        "-v", "quiet",
        "-of", "csv=p=0"
    ]
    result = subprocess.run(ffprobe_command, stdout=subprocess.PIPE, text=True)
    return float(result.stdout.strip())


def main():
    # Get video duration
    video_duration = get_video_duration(VIDEO_PATH)

    # Step 1: Stream pre-processed frames and detect objects
    timestamps = stream_frames_and_detect(VIDEO_PATH, fps=2)

    if not timestamps:
        print("No objects detected in the video.")
        return

    print(f"Detected timestamps: {timestamps}")

    # Step 2: Merge overlapping timestamps into segments
    segments = merge_overlapping_timestamps(timestamps, segment_duration=3, video_duration=video_duration)
    print(f"Merged segments: {segments}")

    # Step 3: Create video clips for detected segments
    create_clips(VIDEO_PATH, segments, TEMP_CLIPS_DIR)

    # Step 4: Merge all clips into a single video
    merge_clips(TEMP_CLIPS_DIR, OUTPUT_VIDEO_PATH)

    print(f"Processed video saved to: {OUTPUT_VIDEO_PATH}")


if __name__ == "__main__":
    main()
