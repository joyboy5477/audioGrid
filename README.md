# audioGrid

**Problem Statement:**

Design a highly efficient distributed audio transcription system to process large audio files by splitting them into smaller chunks, distributing workloads across cluster nodes using MPI, and optimizing processing within nodes through multithreading. The system will leverage GPU acceleration with Faster Whisper or OpenAI Whisper models, ensuring scalability, fault tolerance, and efficient result aggregation to minimize transcription time while maintaining high accuracy.

**Diagram:**

<img width="398" alt="audioGrid" src="https://github.com/user-attachments/assets/fd28ac90-f038-4363-ad62-d3c42f3b8138">

**Output:**
<img width="576" alt="image" src="https://github.com/user-attachments/assets/ada20df2-1085-4cc0-876a-16f56a94a189">
<img width="263" alt="image" src="https://github.com/user-attachments/assets/ec37b146-7012-4bfc-a117-1204f59f81a0">

Above output demonstrates the results of our transcription system. The terminal log shows that a 1-hour audio file was split into 12 chunks, each processed independently. The total time for transcription was approximately 5.65 minutes (339.48 seconds), including just 4.69 seconds for splitting and 334.79 seconds for chunk transcription.

The files section highlights the intermediate chunk-level transcriptions (chunk_1_transcription.txt, etc.) and the final combined result saved as final_transcription.txt. This setup currently runs on 4 CPU cores without GPU acceleration, achieving this performance efficiently.

With GPU acceleration or more cores, this time could be further reduced, showcasing the potential scalability and optimization of the system.





