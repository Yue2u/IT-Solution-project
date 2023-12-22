import argparse

import cv2
import numpy as np


def generate_running_text_video(input_text, output_path="running_text_video.avi"):
    if len(input_text) < 10:
        input_text += " " * (11 - len(input_text))
    width, height = 100, 100
    fps = 60
    duration = 3

    video_writer = cv2.VideoWriter(
        output_path, cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height)
    )

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 2
    font_thickness = 3
    text_size, _ = cv2.getTextSize(input_text, font, font_scale, font_thickness)

    text_width = text_size[0]
    text_height = text_size[1]

    text_x = width
    text_y = int((height + text_height) / 2)

    for _ in range(duration * fps):
        background = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.putText(
            background,
            input_text,
            (text_x, text_y),
            font,
            font_scale,
            (255, 255, 255),
            font_thickness,
        )
        video_writer.write(background)

        text_x -= int((width + text_width) / (duration * fps))
    video_writer.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Runtext",
        description="This sript allows you get 3s 100x100px video with running text",
    )
    parser.add_argument("text", type=str, help="Your text here")
    args = parser.parse_args()

    generate_running_text_video(
        args.text, "running_text_video.avi"
    )  # "Привет, мир, как дела, фофоофофофофоофоф?!"
