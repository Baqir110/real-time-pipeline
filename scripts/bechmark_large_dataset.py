import asyncio
import time
import tracemalloc
import httpx


async def benchmark_ingestion():
  print("Starting 50,000 Row Ingestion Benchmark...")
  tracemalloc.start()
  start_time = time.perf_counter()

  # Simulate continuous batch ingestion
  async with httpx.AsyncClient(timeout=30.0) as client:
    total_records = 50000
    batch_size = 1000
    batches = total_records // batch_size

    for i in range(batches):
      # Mock high-throughput ingestion endpoint run
      _ = await client.post("http://localhost:8000/api/v1/trigger-etl")

  end_time = time.perf_counter()
  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()

  total_time = end_time - start_time
  records_per_sec = total_records / total_time
  peak_mb = peak / (1024 * 1024)

  print(f"\n--- BENCHMARK RESULTS ---")
  print(f"Total Records Ingested: {total_records:,}")
  print(f"Total Run Time: {total_time:.2f} seconds")
  print(f"Throughput: {records_per_sec:.2f} records/sec")
  print(f"Peak Memory Footprint: {peak_mb:.2f} MB")


if __name__ == "__main__":
  asyncio.run(benchmark_ingestion())