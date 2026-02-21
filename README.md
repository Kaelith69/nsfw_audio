<div align="center">

<!-- SVG Hero Banner -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="800" height="200">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d0d0d;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a0a2e;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#ff4d6d;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#c77dff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#4cc9f0;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <!-- Background -->
  <rect width="800" height="200" fill="url(#bg)" rx="12"/>
  <!-- Decorative waveform bars -->
  <g opacity="0.25" fill="url(#accent)">
    <rect x="20"  y="80"  width="6" height="40" rx="3"/>
    <rect x="32"  y="60"  width="6" height="80" rx="3"/>
    <rect x="44"  y="90"  width="6" height="20" rx="3"/>
    <rect x="56"  y="50"  width="6" height="100" rx="3"/>
    <rect x="68"  y="70"  width="6" height="60" rx="3"/>
    <rect x="80"  y="85"  width="6" height="30" rx="3"/>
    <rect x="700" y="80"  width="6" height="40" rx="3"/>
    <rect x="712" y="55"  width="6" height="90" rx="3"/>
    <rect x="724" y="75"  width="6" height="50" rx="3"/>
    <rect x="736" y="60"  width="6" height="80" rx="3"/>
    <rect x="748" y="88"  width="6" height="24" rx="3"/>
    <rect x="760" y="70"  width="6" height="60" rx="3"/>
  </g>
  <!-- Accent underline -->
  <rect x="200" y="148" width="400" height="3" rx="2" fill="url(#accent)" filter="url(#glow)"/>
  <!-- Title -->
  <text x="400" y="105" font-family="'Segoe UI', Arial, sans-serif" font-size="42" font-weight="800"
        text-anchor="middle" fill="white" filter="url(#glow)">🔊 NSFW Audio</text>
  <!-- Subtitle -->
  <text x="400" y="138" font-family="'Segoe UI', Arial, sans-serif" font-size="16"
        text-anchor="middle" fill="#c77dff">Transcribe · Detect · Protect</text>
  <!-- Tagline -->
  <text x="400" y="170" font-family="'Segoe UI', Arial, sans-serif" font-size="12"
        text-anchor="middle" fill="#888">OpenAI Whisper · pydub · Python 3.10+</text>
</svg>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![pydub](https://img.shields.io/badge/pydub-audio-FF6B6B?style=for-the-badge)](https://github.com/jiaaro/pydub)
[![ffmpeg](https://img.shields.io/badge/ffmpeg-required-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blueviolet?style=for-the-badge)](https://github.com/Kaelith69/nsfw_audio)

</div>

---

## 📑 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Installation](#installation)
7. [Usage](#usage)
   - [Convert Audio](#convert-audio)
   - [Detect NSFW Content](#detect-nsfw-content)
8. [Configuration](#configuration)
9. [How It Works](#how-it-works)
10. [Contributing](#contributing)
11. [License](#license)

---

## Overview

**NSFW Audio** is a lightweight, command-line Python toolkit that:

- 🎵 **Converts** audio files (`.m4a`, `.wav`, `.ogg`, …) to MP3 using `pydub` + `ffmpeg`.
- 🎙️ **Transcribes** audio with [OpenAI Whisper](https://github.com/openai/whisper) — entirely on-device, no API key required.
- 🚨 **Detects** NSFW (Not Safe For Work) language in the resulting transcript using a configurable keyword list.

It is ideal for content moderation pipelines, podcast pre-screening, parental-control filters, or anywhere you need an automated first pass over spoken audio.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        User / Pipeline                       │
└────────────────────────┬─────────────────────────────────────┘
                         │  audio file path
           ┌─────────────▼──────────────┐
           │        convert.py          │  (optional pre-processing)
           │  pydub  ──►  ffmpeg        │  .m4a / .wav / … → .mp3
           └─────────────┬──────────────┘
                         │  .mp3 path
           ┌─────────────▼──────────────┐
           │       detection.py         │
           │  Whisper model             │  speech-to-text (local)
           │       │                    │
           │  NSFW keyword scan         │  configurable word list
           └─────────────┬──────────────┘
                         │
            ┌────────────▼───────────────┐
            │   ✅ Clean  /  🚨 NSFW     │
            └────────────────────────────┘
```

### Key design decisions

| Decision | Rationale |
|---|---|
| Whisper runs locally | No cloud cost or privacy leakage |
| Keyword-based NSFW filter | Fast, transparent, and easily extended |
| pydub + ffmpeg for conversion | Widest format support, battle-tested |
| CLI-first (`argparse`) | Composable with shell scripts & CI/CD |
| `__main__` guard on every module | Modules are safely importable as libraries |

---

## Features

- ✅ Convert any ffmpeg-supported format → MP3 in one command
- ✅ On-device speech-to-text with multiple Whisper model sizes
- ✅ Customisable NSFW keyword list via CLI flag
- ✅ Human-friendly emoji output and non-zero exit codes for automation
- ✅ Cross-platform: Windows, macOS, Linux
- ✅ No cloud API keys — completely offline

---

## Project Structure

```
nsfw_audio/
├── convert.py      # Audio format conversion  (.m4a → .mp3, etc.)
├── detection.py    # Whisper transcription + NSFW keyword detection
└── README.md       # This file
```

---

## Prerequisites

| Dependency | Version | Why |
|---|---|---|
| Python | ≥ 3.10 | Type-hint syntax used throughout |
| [ffmpeg](https://ffmpeg.org/download.html) | any modern | Required by pydub for encoding/decoding |
| [openai-whisper](https://github.com/openai/whisper) | latest | Speech-to-text engine |
| [pydub](https://github.com/jiaaro/pydub) | latest | Audio conversion wrapper |

> 💡 A CUDA-capable GPU is optional but strongly recommended for Whisper's larger models.

---

## Installation

### 1 — Clone the repository

```bash
git clone https://github.com/Kaelith69/nsfw_audio.git
cd nsfw_audio
```

### 2 — Create and activate a virtual environment (recommended)

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3 — Install Python dependencies

```bash
pip install openai-whisper pydub
```

### 4 — Install ffmpeg

| Platform | Command |
|---|---|
| **macOS** | `brew install ffmpeg` |
| **Ubuntu / Debian** | `sudo apt install ffmpeg` |
| **Windows** | [Download from ffmpeg.org](https://ffmpeg.org/download.html), extract, add to `PATH` |

Verify the installation:

```bash
ffmpeg -version
```

---

## Usage

### Convert Audio

Convert any audio file to MP3:

```bash
# Basic conversion
python convert.py input.m4a output.mp3

# Use a higher bitrate for better quality
python convert.py interview.wav podcast.mp3 --bitrate 320k
```

```
positional arguments:
  input        Path to the source audio file.
  output       Path for the output .mp3 file.

optional arguments:
  --bitrate    MP3 encoding bitrate (default: 192k).
```

---

### Detect NSFW Content

Transcribe an audio file and scan for NSFW language:

```bash
# Using the default built-in keyword list
python detection.py podcast_episode.mp3

# Use a lighter Whisper model for speed
python detection.py clip.mp3 --model small

# Provide your own keyword list
python detection.py audio.mp3 --keywords badword1 badword2 badword3
```

```
positional arguments:
  audio        Path to the audio file to analyse.

optional arguments:
  --model      Whisper model to use (default: turbo).
               Choices: tiny | base | small | medium | large | turbo
  --keywords   Custom NSFW keyword list (replaces the built-in list).
```

**Exit codes:**

| Code | Meaning |
|---|---|
| `0` | Clean — no NSFW content detected |
| `1` | NSFW content detected **or** an error occurred |

#### Full pipeline example (convert then detect)

```bash
python convert.py recording.m4a recording.mp3 && \
python detection.py recording.mp3 --model base
```

---

## Configuration

### Whisper model sizes

| Model | Parameters | VRAM | Relative speed |
|---|---|---|---|
| `tiny` | 39 M | ~1 GB | ~32× |
| `base` | 74 M | ~1 GB | ~16× |
| `small` | 244 M | ~2 GB | ~6× |
| `medium` | 769 M | ~5 GB | ~2× |
| `large` | 1550 M | ~10 GB | 1× |
| `turbo` | 809 M | ~6 GB | ~8× |

> `turbo` is the default: a good balance between accuracy and speed.

### Extending the NSFW keyword list

Pass additional words directly on the command line:

```bash
python detection.py audio.mp3 --keywords word1 word2 word3
```

Or import `detect_nsfw` in your own script and supply any list:

```python
from detection import transcribe, detect_nsfw

transcript = transcribe("audio.mp3", model_name="base")
my_keywords = ["custom", "words", "here"]
is_nsfw, matched = detect_nsfw(transcript, my_keywords)
print(is_nsfw, matched)
```

---

## How It Works

```
1. convert.py
   └─ AudioSegment.from_file(input)      # pydub reads any ffmpeg-supported format
   └─ .export(output, format="mp3")      # re-encode to MP3 at chosen bitrate

2. detection.py
   └─ whisper.load_model(name)           # download (first run) or load cached model
   └─ model.transcribe(audio_path)       # run inference → {"text": "...", ...}
   └─ detect_nsfw(text, keywords)        # substring scan (case-insensitive)
   └─ exit(0) if clean, exit(1) if NSFW
```

---

> 🎉 *(Insert your favourite "audio waves" GIF here to break up the wall of text — something like a visualiser reacting to a beat drop works perfectly.)*

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-improvement`
3. Commit your changes: `git commit -m "feat: add my improvement"`
4. Push and open a Pull Request

Please keep PRs focused — one feature or fix per PR.

---

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

*Built with ❤️ and a suspicious number of audio files.*

**Why did the audio engineer get fired?**
*Because he kept raising the bar — and nobody could ever reach it.* 🥁

</div>
