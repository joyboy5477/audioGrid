from mpi4py import MPI
from audio_splitter import split_audio_fixed_chunks
from transcriber import process_files_in_executor
from utils import log_time
import os
import time

import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

def process_single_file(file_path: str, chunk_duration: int, model_path: str, device: str):
    """
    Process a single audio file: split into chunks, transcribe, and save results.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(f"Rank {rank} processing file: {file_path}")

    # Step 1: Split audio file into chunks (only on rank 0)
    if rank == 0:
        temp_files = split_audio_fixed_chunks(file_path, chunk_duration)
    else:
        temp_files = None

    # Broadcast the chunk list to all ranks
    temp_files = comm.bcast(temp_files, root=0)

    # Step 2: Distribute chunks among ranks
    local_files = temp_files[rank::size]

    # Step 3: Transcribe chunks using ProcessPoolExecutor
    local_start_time = time.time()
    local_transcriptions = process_files_in_executor(local_files, model_path, device)
    log_time(f"Rank {rank} transcription for {file_path} completed", local_start_time)

    # Step 4: Gather results from all ranks
    all_transcriptions = comm.gather(local_transcriptions, root=0)

    if rank == 0:
        # Combine all results into a single transcription
        output_file = os.path.splitext(file_path)[0] + "_transcription.txt"
        final_transcription = "\n".join(["\n".join(r) for r in all_transcriptions])
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_transcription)
        print(f"Transcription saved to {output_file}")

        # Cleanup temporary files
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Failed to delete temporary file {temp_file}: {e}")

if __name__ == "__main__":
    input_audio_folder = "audio"  # Folder containing audio files
    audiofile = "10min.mp3"  # Specific file to process
    chunk_duration = 300  # 5-minute chunks
    model_path = "tiny"  # Faster Whisper model
    device = "cpu"  # Use "cuda" if GPU is available

    # Construct full path to the audio file
    input_file = os.path.join(input_audio_folder, audiofile)

    # Check if file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Audio file not found: {input_file}")

    # Process the specified file
    process_single_file(input_file, chunk_duration, model_path, device)
