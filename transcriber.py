from concurrent.futures import ProcessPoolExecutor, TimeoutError
from faster_whisper import WhisperModel


def transcribe_file(file_path: str, model_path: str, device: str) -> str:
    """
    Transcribe a single audio file using the Whisper model.
    """
    model = WhisperModel(model_path, device=device)
    segments, _ = model.transcribe(file_path)
    return "".join(segment.text for segment in segments)


def _transcribe_wrapper(args):
    file_path, model_path, device = args
    print(f"Processing file: {file_path}")
    return transcribe_file(file_path, model_path, device)



def process_files_in_executor(files: list, model_path: str, device: str) -> list:
    """
    Use ProcessPoolExecutor to transcribe files in parallel within a single process.
    Handles errors gracefully.
    """
    max_workers = 1  # Limit the number of workers per rank
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        try:
            results = list(executor.map(_transcribe_wrapper, [(f, model_path, device) for f in files]))
        except Exception as e:
            print(f"Error during transcription: {e}")
            results = []
    return results
