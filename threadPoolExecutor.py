import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
import ffmpeg
from faster_whisper import WhisperModel

def split_audio_fixed_chunks(input_file: str, chunk_duration: int) -> list:
    """
    Split audio into fixed-duration chunks using FFmpeg.
    """
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
    return temp_files

def transcribe_file_with_shared_model(file_path: str, model) -> str:
    """
    Transcribe a single audio file using a shared Whisper model instance.
    """
    segments, _ = model.transcribe(file_path)
    return "".join(segment.text for segment in segments)

def transcribe_audio_with_threads(input_file: str, chunk_duration: int, model_path: str, device: str, max_threads: int) -> str:
    """
    Transcribe audio by splitting it into chunks and using threads for parallel transcription.
    """
    # Step 1: Split the audio into chunks
    temp_files = split_audio_fixed_chunks(input_file, chunk_duration)

    # Step 2: Initialize the Whisper model (shared across threads)
    model = WhisperModel(model_path, device=device)

    # Step 3: Transcribe each chunk in parallel using threads
    with ThreadPoolExecutor(max_threads) as executor:
        results = list(executor.map(transcribe_file_with_shared_model, temp_files, [model] * len(temp_files)))

    # Step 4: Combine the transcription results
    full_transcription = "\n".join(results)

    # Step 5: Clean up temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

    return full_transcription

if __name__ == "__main__":
    # Input file and configuration
    input_audio = "audio.mp3"
    chunk_duration = 300  # Split into 5-minute chunks (300 seconds)
    model_path = "tiny"  # Whisper model size
    device = "cpu"  # Use CPU for transcription
    max_threads = 4  # Number of threads to use (adjust based on system)

    # Transcribe the audio
    transcription = transcribe_audio_with_threads(input_audio, chunk_duration, model_path, device, max_threads)

    # Save the transcription to a file
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription)

    print("Transcription completed and saved to 'transcription.txt'.")
