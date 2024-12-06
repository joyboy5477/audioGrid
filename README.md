# Distributed Audio Transcription System 🎧✨

**Team Members**  
- **Akash Vishwakarma**  
- **Samarth Khaire**  
- **Gabriel Do**

---

## **🌟 Problem Statement**

Design a highly efficient **distributed audio transcription system** to process large audio files by splitting them into smaller chunks, distributing workloads across cluster nodes using **MPI**, and optimizing processing within nodes through **multithreading**. The system leverages **GPU acceleration** with Faster Whisper or OpenAI Whisper models, ensuring **scalability, fault tolerance**, and efficient result aggregation to minimize transcription time while maintaining **high accuracy**.

---

## **🚀 System Architecture**

<div align="center">
<img src="https://github.com/user-attachments/assets/fd28ac90-f038-4363-ad62-d3c42f3b8138" alt="System Architecture" width="70%">
</div>

The system processes a **1-hour audio file** by dividing it into **12 chunks** of 5 minutes each:

1. **Master Node (Rank 0)**:
   - Splits the audio file into smaller chunks.
   - Distributes these chunks to worker nodes using **MPI**.
   - Aggregates the processed transcriptions into the final output.

2. **Worker Nodes (Ranks 1 to N)**:
   - Use **ProcessPoolExecutor** for parallel processing across multiple CPU cores.
   - Each node transcribes the assigned audio chunks.

3. **Result Aggregation**:
   - Transcriptions of all chunks are gathered back to the master node.
   - The master node combines these results into a **final transcription output**.

This hybrid approach leverages:
- **MPI** for distributed task management.
- **ProcessPoolExecutor** for intra-node parallelism.
- **GPU Acceleration** for faster transcription (optional).

---

## **📊 System Output**

### **⚡ Terminal Log**
Below is an example of the system's performance for a **1-hour audio file**:

<div align="center">
<img src="https://github.com/user-attachments/assets/ada20df2-1085-4cc0-876a-16f56a94a189" alt="Terminal Log" width="90%">
</div>

### **📂 Generated Files**
The system produces:
1. **Intermediate Transcriptions**:
   - `chunk_1_transcription.txt`, `chunk_2_transcription.txt`, ..., `chunk_12_transcription.txt`
2. **Final Combined Transcription**:
   - `final_transcription.txt`

<div align="center">
<img src="https://github.com/user-attachments/assets/ec37b146-7012-4bfc-a117-1204f59f81a0" alt="Generated Files" width="50%">
</div>

---

## **⏱ Performance Metrics**

| **Metric**            | **Value**      |
|------------------------|----------------|
| **Total Transcription Time** | ~5.65 minutes (339.48 seconds) |
| **Chunk Splitting Time**      | 4.69 seconds                 |
| **Chunk Transcription Time**  | 334.79 seconds               |
| **Cores Utilized**            | 4 CPU cores                 |

> **Note**: The results above are achieved without GPU acceleration. Adding GPUs or increasing the number of CPU cores can further optimize performance, showcasing the system's **scalability and efficiency**.

---

## **🌐 Key Features**

- **Scalable Design**:
  - Supports large-scale transcription tasks by distributing workloads across multiple nodes.
- **Fault Tolerance**:
  - Ensures seamless transcription even if some nodes fail.
- **Hybrid Parallelism**:
  - Combines MPI for distributed processing and ProcessPoolExecutor for intra-node multithreading.
- **GPU Acceleration Ready**:
  - Can leverage Faster Whisper or OpenAI Whisper models for faster processing.
- **Result Aggregation**:
  - Efficiently combines partial results into a unified transcription.

---

## **📝 Acknowledgments**

- **MPI4Py** for enabling efficient parallelism.  
- **OpenAI Whisper** for providing state-of-the-art transcription models.  
- **Our Team** for collaborative development and innovation.

---

This project demonstrates the power of distributed systems in solving real-world challenges efficiently. **Together, let's make audio transcription faster and more scalable than ever! 🚀**

---







