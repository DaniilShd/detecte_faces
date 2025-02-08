
import cv2
import os
from detecte_faces.detecte import CascadeHaara


def extract_frames(video_path, start=-1, end=-1, every=1):
    """
    Extract frames from a video using OpenCV's VideoCapture.
    """

    video_path = os.path.normpath(video_path)

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    capture = cv2.VideoCapture(video_path)

    if start < 0:
        start = 0
    if end < 0:
        end = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    capture.set(cv2.CAP_PROP_POS_FRAMES, start)

    cascade = CascadeHaara('../detecte_faces/classifier/haarcascade_frontalface_alt.xml')


    list_frames = []

    for frame in range(start, end):
        ret, image = capture.read()

        if not ret:
            break

        if frame % every == 0:
            cascade.load_image(image)
            list_frames.append(cascade.return_result())

    capture.release()
    return list_frames

def detected_faces(video_path, output_path, every=1, chunk_size=1000):
    """
    Extract frames from a video using multiprocessing.
    """
    video_path = os.path.normpath(video_path)

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    capture = cv2.VideoCapture(video_path)
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()

    if total_frames < 1:
        raise ValueError("Video has no frames. Check your OpenCV installation.")

    list_frames = extract_frames(video_path, every)


    frames_to_video(list_frames, output_path, fps=30, reverse=False)


def frames_to_video(list_frames, output_path, fps=30, reverse=False):
    """
    Create a video from a sequence of frames.
    """
    # frames_dir = os.path.normpath(frames_dir)
    # output_path = os.path.normpath(output_path)

    # frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    # if reverse:
    #     frame_files = frame_files[::-1]

    if not list_frames:
        raise ValueError("No frames found in the directory.")

    first_frame = list_frames[0]
    height, width, _ = first_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in list_frames:
        out.write(frame)

    out.release()
    print(f"Video saved to {output_path}")

if __name__ == '__main__':
    # Test frame extraction
    detected_faces(video_path='../repository/origin_video/test_3.mp4', output_path='../repository/detected_video/test.mp4',  every=5, chunk_size=1000)
