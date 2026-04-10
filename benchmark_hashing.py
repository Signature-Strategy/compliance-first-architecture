"""
Multi-Algorithm Hashing Benchmark
Empirical throughput measurement for the five-algorithm hash set
described in Compliance-First Data Processing Architecture (Berry, 2026).

Measures single-pass (concurrent) vs individual algorithm throughput
to quantify the marginal cost of computing all five digests.
"""

import hashlib
import os
import time
import statistics
import json
import sys
from datetime import datetime, timezone

ALGORITHMS = ["md5", "sha1", "sha256", "sha512", "sha3_256"]
ALGO_LABELS = {
    "md5": "MD5",
    "sha1": "SHA-1",
    "sha256": "SHA-256",
    "sha512": "SHA-512",
    "sha3_256": "SHA3-256",
}

# Test data sizes: representative of real-world items
DATA_SIZES = [
    (1024,             "1 KB",    "Short email / metadata record"),
    (64 * 1024,        "64 KB",   "Typical email with small attachment"),
    (1024 * 1024,      "1 MB",    "Office document / PDF"),
    (16 * 1024 * 1024, "16 MB",   "Large spreadsheet / presentation"),
    (64 * 1024 * 1024, "64 MB",   "Small PST / archive segment"),
    (256 * 1024 * 1024,"256 MB",  "Large container / disk image chunk"),
]

CHUNK_SIZE = 65536  # 64 KB read buffer, typical for buffered I/O
WARMUP_ROUNDS = 2
BENCH_ROUNDS = 5


def generate_data(size):
    """Generate pseudo-random data block. os.urandom is used to prevent
    any CPU-level compression or shortcut in hash computation."""
    return os.urandom(size)


def hash_single_pass_all(data, chunk_size=CHUNK_SIZE):
    """Single-pass: feed every chunk to all five hashers simultaneously.
    This is how a properly implemented processing engine works."""
    hashers = [hashlib.new(algo) for algo in ALGORITHMS]
    offset = 0
    while offset < len(data):
        chunk = data[offset:offset + chunk_size]
        for h in hashers:
            h.update(chunk)
        offset += chunk_size
    return [h.hexdigest() for h in hashers]


def hash_single_algo(data, algo, chunk_size=CHUNK_SIZE):
    """Single algorithm pass for comparison."""
    h = hashlib.new(algo)
    offset = 0
    while offset < len(data):
        chunk = data[offset:offset + chunk_size]
        h.update(chunk)
        offset += chunk_size
    return h.hexdigest()


def bench_single_algo(data, algo, rounds):
    """Time a single algorithm over multiple rounds, return seconds per run."""
    times = []
    for _ in range(rounds):
        start = time.perf_counter()
        hash_single_algo(data, algo)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return times


def bench_all_five(data, rounds):
    """Time the single-pass five-algorithm hash over multiple rounds."""
    times = []
    for _ in range(rounds):
        start = time.perf_counter()
        hash_single_pass_all(data)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return times


def throughput_gbps(data_size, seconds):
    """Convert to GB/s."""
    if seconds == 0:
        return float("inf")
    return (data_size / (1024 ** 3)) / seconds


def format_time(seconds):
    """Human-readable time."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.0f} us"
    elif seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    else:
        return f"{seconds:.2f} s"


def project_volume(throughput_gbps_val, volume_tb):
    """Project time for a given volume in TB."""
    if throughput_gbps_val == 0:
        return float("inf")
    volume_gb = volume_tb * 1024
    return volume_gb / throughput_gbps_val  # seconds


def format_duration(seconds):
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.1f}m"
    else:
        return f"{seconds / 3600:.1f}h"


def main():
    print("=" * 72)
    print("MULTI-ALGORITHM HASHING BENCHMARK")
    print("Compliance-First Data Processing Architecture (Berry, 2026)")
    print("=" * 72)
    print()

    # System info
    print(f"Date:      {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Python:    {sys.version.split()[0]}")
    print(f"Platform:  {sys.platform}")
    print(f"Rounds:    {BENCH_ROUNDS} (after {WARMUP_ROUNDS} warmup)")
    print(f"Chunk:     {CHUNK_SIZE // 1024} KB read buffer")
    print(f"Algorithms: {', '.join(ALGO_LABELS[a] for a in ALGORITHMS)}")
    print()

    results = {}

    for data_size, size_label, description in DATA_SIZES:
        print(f"--- {size_label} ({description}) ---")
        data = generate_data(data_size)

        # Warmup
        for _ in range(WARMUP_ROUNDS):
            hash_single_pass_all(data)
            for algo in ALGORITHMS:
                hash_single_algo(data, algo)

        # Benchmark each algorithm individually
        algo_results = {}
        for algo in ALGORITHMS:
            times = bench_single_algo(data, algo, BENCH_ROUNDS)
            median = statistics.median(times)
            tp = throughput_gbps(data_size, median)
            algo_results[algo] = {
                "median_s": median,
                "throughput_gbps": tp,
                "times": times,
            }
            print(f"  {ALGO_LABELS[algo]:>10s}:  {format_time(median):>8s}  ({tp:.2f} GB/s)")

        # Benchmark all-five single pass
        all_times = bench_all_five(data, BENCH_ROUNDS)
        all_median = statistics.median(all_times)
        all_tp = throughput_gbps(data_size, all_median)
        print(f"  {'All 5':>10s}:  {format_time(all_median):>8s}  ({all_tp:.2f} GB/s)")

        # Marginal overhead vs SHA-256 alone
        sha256_median = algo_results["sha256"]["median_s"]
        if sha256_median > 0:
            overhead_pct = ((all_median - sha256_median) / sha256_median) * 100
            overhead_abs = all_median - sha256_median
            print(f"  {'Overhead':>10s}:  +{format_time(overhead_abs)} (+{overhead_pct:.1f}% vs SHA-256 alone)")
        print()

        results[size_label] = {
            "data_size": data_size,
            "description": description,
            "algorithms": algo_results,
            "all_five": {
                "median_s": all_median,
                "throughput_gbps": all_tp,
                "times": all_times,
            },
            "overhead_vs_sha256_pct": overhead_pct if sha256_median > 0 else None,
        }

    # Scale projection using the 256 MB throughput (most representative of sustained I/O)
    print("=" * 72)
    print("SCALE PROJECTIONS (based on 256 MB sustained throughput)")
    print("=" * 72)
    large = results["256 MB"]
    sha256_tp = large["algorithms"]["sha256"]["throughput_gbps"]
    all5_tp = large["all_five"]["throughput_gbps"]

    print()
    print(f"  {'Volume':>10s}  {'SHA-256 only':>14s}  {'All 5 hashes':>14s}  {'Added time':>12s}")
    print(f"  {'------':>10s}  {'-' * 14:>14s}  {'-' * 14:>14s}  {'-' * 12:>12s}")

    for vol_tb in [0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]:
        t_sha = project_volume(sha256_tp, vol_tb)
        t_all = project_volume(all5_tp, vol_tb)
        delta = t_all - t_sha
        label = f"{vol_tb:.1f} TB" if vol_tb >= 1 else f"{int(vol_tb * 1000)} GB"
        print(f"  {label:>10s}  {format_duration(t_sha):>14s}  {format_duration(t_all):>14s}  {format_duration(delta):>12s}")

    print()

    # Also compute: what fraction of total processing time is hashing?
    # Real-world eDiscovery processing includes: extraction, OCR, text indexing,
    # metadata extraction, deduplication, classification. Hashing is a tiny slice.
    print("=" * 72)
    print("CONTEXT: HASHING AS FRACTION OF TOTAL PROCESSING")
    print("=" * 72)
    print()
    print("  Real-world eDiscovery/DF processing per item includes:")
    print("    - Container extraction (ZIP, PST, OST, NSF, disk images)")
    print("    - Text extraction and encoding detection")
    print("    - OCR for image-based content")
    print("    - Metadata extraction and normalization")
    print("    - Language detection and indexing")
    print("    - Email threading and deduplication")
    print("    - Classification, NER, privilege detection")
    print()
    print("  Typical observed processing rates (Nuix, single worker):")
    print("    - Simple items (emails, text):     ~50-200 items/sec")
    print("    - Complex items (Office, PDF):      ~5-50 items/sec")
    print("    - OCR-heavy items:                  ~0.5-5 items/sec")
    print()

    # For a 1 MB document, how long does hashing take vs everything else?
    mb1 = results["1 MB"]
    hash_time_1mb = mb1["all_five"]["median_s"]
    # Conservative processing estimate: 20 items/sec = 50ms per item
    typical_processing_ms = 50
    hash_ms = hash_time_1mb * 1000
    hash_fraction = hash_ms / typical_processing_ms * 100
    print(f"  For a 1 MB document (5 hashes): {hash_ms:.2f} ms")
    print(f"  Typical processing time:         ~{typical_processing_ms} ms (extraction + indexing + metadata)")
    print(f"  Hashing fraction:                ~{hash_fraction:.1f}% of total per-item time")
    print()

    # Save raw results as JSON for the study
    output = {
        "benchmark_date": datetime.now(timezone.utc).isoformat(),
        "system": {
            "cpu": "AMD Ryzen Threadripper 7960X 24-Cores",
            "python": sys.version.split()[0],
            "ram_gb": 128,
        },
        "config": {
            "chunk_size": CHUNK_SIZE,
            "warmup_rounds": WARMUP_ROUNDS,
            "bench_rounds": BENCH_ROUNDS,
            "algorithms": ALGORITHMS,
        },
        "results": {},
    }
    for label, r in results.items():
        output["results"][label] = {
            "data_size_bytes": r["data_size"],
            "description": r["description"],
            "sha256_only_gbps": r["algorithms"]["sha256"]["throughput_gbps"],
            "all_five_gbps": r["all_five"]["throughput_gbps"],
            "overhead_vs_sha256_pct": r["overhead_vs_sha256_pct"],
        }

    with open("benchmark_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("Raw results saved to benchmark_results.json")
    print()


if __name__ == "__main__":
    main()
