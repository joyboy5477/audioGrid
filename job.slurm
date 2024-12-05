#!/bin/bash
#SBATCH --job-name=audio_transcription   # Name of the job
#SBATCH --output=transcription.out       # Standard output log file
#SBATCH --error=transcription.err        # Standard error log file
#SBATCH --nodes=2                        # Request 2 nodes
#SBATCH --ntasks-per-node=4              # 4 MPI ranks (cores) per node
#SBATCH --time=02:00:00                  # Max runtime (adjust as needed)
#SBATCH --partition=main                 # Partition for the job

# Load necessary modules
module load python/3.11.3                # Python 3 module
module load ffmpeg                       # FFmpeg module
module load openmpi/4.1.4                # Specify the exact version of MPI module

# Activate the virtual environment
source venv/bin/activate                 # Activate virtual environment

# Run the transcription job with MPI
srun --mpi=pmi2 python mpi_transcription.py
