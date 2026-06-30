"""
Pre-split COJADS/GSR-JD utterances into individual WAV clip files.

For each row in the subset CSVs, extracts the (start, end) segment and
saves it as its own WAV file so that nkululeko sees one file per utterance.
GSR-JD rows with NaN timestamps get the whole file copied.

Output filename format:
  {audio_stem}__{speaker}__{N:04d}.wav
  where N is the per-speaker segment counter (0-based).

Output:
  ja-dialect/clips/train/{audio_stem}__{speaker}__{N:04d}.wav  ...
  ja-dialect/clips/test/{audio_stem}__{speaker}__{N:04d}.wav   ...
  ja-dialect/japanese_dialect_train_sub500_clips.csv
  ja-dialect/japanese_dialect_test_sub150_clips.csv
"""

import os
import shutil
from collections import defaultdict
from pathlib import Path

import pandas as pd
import soundfile as sf

AUDIO_BASE = "ja-dialect"
CLIPS_BASE = "ja-dialect/clips"

JOBS = [
    ("ja-dialect/japanese_dialect_train_sub500.csv", "train"),
    ("ja-dialect/japanese_dialect_test_sub150.csv",  "test"),
]

os.makedirs(f"{CLIPS_BASE}/train", exist_ok=True)
os.makedirs(f"{CLIPS_BASE}/test", exist_ok=True)

for csv_path, split in JOBS:
    df = pd.read_csv(csv_path)
    new_files, skipped = [], 0
    speaker_counters = defaultdict(int)  # per-speaker segment index

    print(f"\n[{split}] {csv_path}  ({len(df)} rows)")

    for enum_i, (_, row) in enumerate(df.iterrows()):
        abs_src  = f"{AUDIO_BASE}/{row['file']}"
        audio_stem = Path(row["file"]).stem          # e.g. 32_a_099
        speaker    = str(row["speaker"]).replace("/", "-")  # sanitise
        speaker_counters[speaker] += 1
        seg_idx    = speaker_counters[speaker]

        clip_name = f"{audio_stem}__{speaker}__{seg_idx:04d}.wav"
        clip_rel  = f"clips/{split}/{clip_name}"
        clip_abs  = f"{AUDIO_BASE}/{clip_rel}"

        try:
            start, end = row["start"], row["end"]
            if pd.isna(start) or pd.isna(end):
                # GSR-JD whole-file utterance — copy as-is
                shutil.copy2(abs_src, clip_abs)
            else:
                info = sf.info(abs_src)
                s0 = int(start * info.samplerate)
                s1 = int(end   * info.samplerate)
                data, sr = sf.read(abs_src, start=s0, stop=s1, always_2d=False)
                sf.write(clip_abs, data, sr)
            new_files.append(clip_rel)
        except Exception as e:
            print(f"  SKIP {enum_i} ({row['file']}): {e}")
            new_files.append(None)
            skipped += 1

        if (enum_i + 1) % 500 == 0:
            print(f"  {enum_i + 1}/{len(df)}  skipped={skipped}  speakers={len(speaker_counters)}")

    df["file"]  = new_files
    df["start"] = float("nan")
    df["end"]   = float("nan")
    df = df[df["file"].notna()].reset_index(drop=True)

    out = csv_path.replace(".csv", "_clips.csv")
    df.to_csv(out, index=False)
    print(f"  -> {out}  ({len(df)} rows, {skipped} skipped)")
