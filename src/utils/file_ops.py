import os
import cv2
import csv


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_frame(frame, path, filename):
    """
    Save single frame as image
    """
    create_dir(path)
    full_path = os.path.join(path, filename)
    cv2.imwrite(full_path, frame)
    return full_path


def save_attention_log(csv_path, data):
    """
    Save attention logs in CSV format
    data format:
    [timestamp, attention_state]
    """

    create_dir(os.path.dirname(csv_path))

    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp", "attention_state"])

        writer.writerow(data)