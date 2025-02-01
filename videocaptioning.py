"""
Module Name: videocaptioning.py
Author: Glenn Yaniero
Date: 2025-01-31
Description: This module extracts audio from a video file using MoviePy, transcribes the audio using Azure Speech SDK, and creates captions in SRT format to display on the video.
Dependencies: moviepy, azure-cognitiveservices-speech

Usage:
    python videocaptioning.py
"""

import moviepy as mp
import azure.cognitiveservices.speech as speechsdk
from datetime import timedelta

def extract_audio(video_path, audio_path):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    video_clip.close()
    audio_clip.close()

def transcribe_audio(audio_path, subscription_key, region):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return [{"start_time": 0.0, "end_time": len(result.text.split())/2.5, "text": result.text}]
    else:
        return []

def write_srt(transcription, output_path):
    with open(output_path, 'w') as file:
        for i, segment in enumerate(transcription):
            start_time = segment["start_time"]
            end_time = segment["end_time"]
            text = segment["text"]

            start_srt_time = str(timedelta(seconds=start_time)).replace('.', ',')[:-3]
            end_srt_time = str(timedelta(seconds=end_time)).replace('.', ',')[:-3]

            file.write(f"{i+1}\n")
            file.write(f"{start_srt_time} --> {end_srt_time}\n")
            file.write(f"{text}\n\n")

if __name__ == "__main__":
    video_path = input("Please enter the path to your video file: ")
    audio_path = input("Please enter the path to save the audio file (including the file name and extension, e.g., output.mp3): ")
    srt_path = input("Please enter the path to save the SRT file (including the file name and extension, e.g., subtitles.srt): ")
    subscription_key = "YourSubscriptionKey"
    region = "YourServiceRegion"

    extract_audio(video_path, audio_path)
    transcription = transcribe_audio(audio_path, subscription_key, region)
    write_srt(transcription, srt_path)

    print(f"Audio extracted to: {audio_path}")
    print(f"SRT file created at: {srt_path}")
    print(f"Use the following command to add subtitles to your video using ffmpeg:")
    print(f"ffmpeg -i {video_path} -vf \"subtitles={srt_path}\" output_video_with_subtitles.mp4")
