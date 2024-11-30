import os
import tempfile
from concurrent.futures import ProcessPoolExecutor
import ffmpeg
from faster_whisper import WhisperModel
import multiprocessing
import time
from typing import Tuple


def log_time(message: str, start_time: float):
    """
    Utility to print elapsed time with a message.
    """
    elapsed = time.time() - start_time
    print(f"{message} - Elapsed time: {elapsed:.2f} seconds.")
    return elapsed


def split_audio_fixed_chunks(input_file: str, chunk_duration: int) -> list:
    """
    Split audio into fixed-duration chunks using FFmpeg.
    """
    print("Starting audio splitting...")
    split_start_time = time.time()

    # Get file extension
    file_extension = os.path.splitext(input_file)[1]
    # Get total audio duration
    metadata = ffmpeg.probe(input_file)
    duration = float(metadata["format"]["duration"])  # Total duration of the audio in seconds

    # Create temporary files for chunks
    temp_files = []
    for start in range(0, int(duration), chunk_duration):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
        temp_file.close()
        # Extract audio chunk using FFmpeg
        ffmpeg.input(input_file, ss=start, t=chunk_duration).output(temp_file.name, c="copy").overwrite_output().run()
        temp_files.append(temp_file.name)

    log_time("Audio splitting completed", split_start_time)
    return temp_files

# def split_audio_fixed_chunks(input_file: str, chunk_duration: int) -> list:
#     """
#     Split audio into fixed-duration chunks using FFmpeg.
#     """
#     print("Starting audio splitting...")
#     split_start_time = time.time()

#     # Get file extension
#     file_extension = os.path.splitext(input_file)[1]
#     if file_extension.lower() != ".m4a":
#         raise ValueError("Only .m4a files are supported. Please provide a valid .m4a file.")
    
#     # Get total audio duration
#     metadata = ffmpeg.probe(input_file)
#     duration = float(metadata["format"]["duration"])  # Total duration of the audio in seconds

#     # Create temporary files for chunks
#     temp_files = []
#     for start in range(0, int(duration), chunk_duration):
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".m4a")
#         temp_file.close()
#         # Extract audio chunk using FFmpeg with AAC codec for .m4a files
#         ffmpeg.input(input_file, ss=start, t=chunk_duration).output(temp_file.name, c="aac").overwrite_output().run()
#         temp_files.append(temp_file.name)

#     log_time("Audio splitting completed", split_start_time)
#     return temp_files


def transcribe_file(file_path: str, model_path: str, device: str) -> Tuple[str, float]:
    """
    Transcribe a single audio file using the Whisper model and return the text and time taken.
    """
    transcribe_start_time = time.time()

    # Load the Whisper model
    model = WhisperModel(model_path, device=device)
    segments, _ = model.transcribe(file_path)
    transcription = "".join(segment.text for segment in segments)

    transcription_time = time.time() - transcribe_start_time
    return transcription, transcription_time


def transcribe_audio_with_processes(input_file: str, chunk_duration: int, model_path: str, device: str) -> str:
    """
    Transcribe audio by splitting it into chunks and using multiple processes.
    """
    total_start_time = time.time()
    time_breakdown = {}

    # Step 1: Split the audio into chunks
    temp_files = split_audio_fixed_chunks(input_file, chunk_duration)
    time_breakdown['Audio Splitting'] = time.time() - total_start_time

    # Step 2: Transcribe each chunk in parallel using processes
    print("Starting transcription of chunks...")
    transcription_start_time = time.time()

    results = []
    chunk_times = []
    with ProcessPoolExecutor(multiprocessing.cpu_count()) as executor:
        for idx, (transcription, chunk_time) in enumerate(
            executor.map(transcribe_file, temp_files, [model_path] * len(temp_files), [device] * len(temp_files))
        ):
            # Save intermediate transcription to a file
            results.append(transcription)
            chunk_times.append(chunk_time)
            with open(f"chunk_{idx + 1}_transcription.txt", "w", encoding="utf-8") as f:
                f.write(transcription)
            print(f"Chunk {idx + 1} transcription completed in {chunk_time:.2f} seconds.")

    time_breakdown['Transcription'] = time.time() - transcription_start_time

    # Step 3: Combine the transcription results
    full_transcription = "\n".join(results)

    # Step 4: Clean up temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

    time_breakdown['Total'] = time.time() - total_start_time

    # Log time breakdown
    print("\nTime Breakdown:")
    for step, elapsed in time_breakdown.items():
        print(f"{step}: {elapsed:.2f} seconds.")

    print(f"\nPer-Chunk Times (seconds): {chunk_times}")
    print(f"Total Transcription Time: {sum(chunk_times):.2f} seconds.")

    return full_transcription


if __name__ == "__main__":
    # Input file and configuration
    input_audio = "audio.m4a"
    chunk_duration = 300  # Split into 5-minute chunks (300 seconds)
    model_path = "tiny"  # Whisper model size
    device = "cpu"  # Use CPU for transcription

    # Transcribe the audio
    total_start_time = time.time()
    transcription = transcribe_audio_with_processes(input_audio, chunk_duration, model_path, device)

    # Save the final transcription to a file
    with open("final_transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription)

    print("\nFinal transcription saved to 'final_transcription.txt'.")
    log_time("Thaotal processing time", total_start_time)