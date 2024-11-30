import os
import tempfile
import ffmpeg

# Splits the audio file into smaller chunks of a fixed duration (e.g., 5 minutes).
# Outputs the temporary chunk files for processing.

import os
import tempfile
import ffmpeg


def split_audio_fixed_chunks(input_file: str, chunk_duration: int) -> list:
    """
    Split the input audio file into fixed-duration chunks.
    """
    # Validate input file extension
    valid_extensions = ['.mp3', '.m4a', '.wav']
    file_extension = os.path.splitext(input_file)[1].lower()
    if file_extension not in valid_extensions:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats are {valid_extensions}.")

    metadata = ffmpeg.probe(input_file)
    duration = float(metadata["format"]["duration"])
    temp_files = []

    for start in range(0, int(duration), chunk_duration):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
        temp_file.close()
        ffmpeg.input(input_file, ss=start, t=chunk_duration).output(temp_file.name, c="copy").overwrite_output().run()
        temp_files.append(temp_file.name)

    return temp_files
