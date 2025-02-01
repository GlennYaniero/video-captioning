"""
Module Name: extractaudio.py
Author: Glenn Yaniero
Date: 2025-01-31
Description: This module utilizes MoviePy to extract the audio track from the video.

Usage:
    python extractaudio.py

"""

from moviepy import VideoFileClip

# Prompt the user to enter the video file path
video_path = input("Please enter the path to your video file: ")

# Load the video file
video_clip = VideoFileClip(video_path)

# Extract the audio from the video
audio_clip = video_clip.audio

# Prompt the user to enter the path for saving the audio file
audio_path = input("Please enter the path to save the audio file (including the file name and extension, e.g., output.mp3): ")

# Save the audio to a file
audio_clip.write_audiofile(audio_path)

# Close the clips
video_clip.close()
audio_clip.close()

print("Audio extraction completed and saved to:", audio_path)
