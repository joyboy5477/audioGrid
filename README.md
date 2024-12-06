# Distributed Audio Transcription System

**📜 Problem Statement:**

Design a highly efficient distributed audio transcription system to process large audio files by splitting them into smaller chunks, distributing workloads across cluster nodes using MPI, and optimizing processing within nodes through multithreading. The system will leverage GPU acceleration with Faster Whisper or OpenAI Whisper models, ensuring scalability, fault tolerance, and efficient result aggregation to minimize transcription time while maintaining high accuracy.


**🚀 Diagram:**

<img width="398" alt="audioGrid" src="https://github.com/user-attachments/assets/fd28ac90-f038-4363-ad62-d3c42f3b8138">

The diagram shows the process of a 1-hour audio file by dividing it into 12 chunks of 5 minutes each, leveraging MPI for distributed processing and ProcessPoolExecutor for parallel processing on each node. The master node (Rank 0) splits the audio into chunks and scatters them across four worker nodes (Ranks 0 to 3), with each node receiving three chunks.
On each node, multiple CPU cores process these chunks in parallel using Python’s ProcessPoolExecutor, ensuring efficient resource utilization. After processing, the transcriptions of all chunks (T1 to T12) are gathered back to the master node using MPI. The master node then combines these results into a final transcription output. This setup combines the power of MPI for distributed task management and ProcessPoolExecutor for intra-node parallelism, greatly reducing the processing time.


**📊 Output:**

<img width="576" alt="image" src="https://github.com/user-attachments/assets/ada20df2-1085-4cc0-876a-16f56a94a189">
<img width="263" alt="image" src="https://github.com/user-attachments/assets/ec37b146-7012-4bfc-a117-1204f59f81a0">


Above output demonstrates the results of our transcription system. The terminal log shows that a 1-hour audio file was split into 12 chunks, each processed independently. The total time for transcription was approximately 5.65 minutes (339.48 seconds), including just 4.69 seconds for splitting and 334.79 seconds for chunk transcription.

The files section highlights the intermediate chunk-level transcriptions (chunk_1_transcription.txt, etc.) and the final combined result saved as final_transcription.txt. This setup currently runs on 4 CPU cores without GPU acceleration, achieving this performance efficiently.

With GPU acceleration or more cores, this time could be further reduced, showcasing the potential scalability and optimization of the system.





