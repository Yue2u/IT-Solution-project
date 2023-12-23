import argparse
import os
import string
import subprocess

import cv2
import numpy as np
import pyttsx3


def generate_running_text_video(input_text, output_path="running_text_video.avi"):
    input_text += " " * 5
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
    return output_path


def generate_audio(input_text, output_path="running_text_audio.avi"):
    engine = pyttsx3.init()
    engine.setProperty("rate", len(input_text.split()) * 30)
    engine.setProperty("volume", 0.1)

    engine.save_to_file(input_text, output_path)
    engine.runAndWait()
    return output_path


def merge_video_audio(video_path, audio_path, output_path):
    # Command to ffmpeg to merge video and audio
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-f",
        "avi",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-y",
        output_path,
    ]

    # Execute the ffmpeg command
    process = subprocess.Popen(ffmpeg_command)
    process.wait()

    os.remove(video_path)
    os.remove(audio_path)

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Runtext",
        description="This sript allows you get 3s 100x100px video with running text",
    )
    parser.add_argument("text", type=str, help="Your text here")
    args = parser.parse_args()

    flag = True
    for el in args.text:
        if el not in string.printable:
            flag = False

    if flag:
        video_path = generate_running_text_video(
            args.text, "running_text_video.avi"
        )  # "Привет, мир, как дела, фофоофофофофоофоф?!"
        audio_path = generate_audio(args.text, "running_text_audio.mp3")
        merge_video_audio(video_path, audio_path, "voiced_running_text_video.avi")
    else:
        video_path = generate_running_text_video(
            args.text, "voiced_running_text_video.avi"
        )  # "Привет, мир, как дела, фофоофофофофоофоф?!"
