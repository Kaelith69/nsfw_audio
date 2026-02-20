"""
NSFW Audio Detection
====================
Transcribes an audio file using OpenAI Whisper and scans the transcript for
NSFW (Not Safe For Work) content by matching against a keyword list.

Usage
-----
    python detection.py <audio_file> [--model MODEL] [--keywords KEYWORDS]
"""

import argparse
import os
import sys

import whisper

# ---------------------------------------------------------------------------
# Default NSFW keyword list (extend or replace via --keywords flag)
# ---------------------------------------------------------------------------
DEFAULT_NSFW_KEYWORDS: list[str] = [
    "fuck", "shit", "bitch", "asshole", "cunt", "dick", "pussy",
    "cock", "whore", "slut", "nigger", "faggot", "retard",
    "kill yourself", "kys",
]


def transcribe(audio_path: str, model_name: str = "turbo") -> str:
    """
    Transcribe *audio_path* using Whisper and return the plain-text transcript.

    Parameters
    ----------
    audio_path : str
        Path to the audio file to transcribe.
    model_name : str
        Whisper model size to use (e.g. "tiny", "base", "small", "medium",
        "large", "turbo").  Default: "turbo".

    Returns
    -------
    str
        The transcribed text.

    Raises
    ------
    FileNotFoundError
        If *audio_path* does not exist.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result["text"]


def detect_nsfw(text: str, keywords: list[str]) -> tuple[bool, list[str]]:
    """
    Check whether *text* contains any NSFW keywords.

    Parameters
    ----------
    text : str
        The transcript to scan.
    keywords : list[str]
        Ordered list of forbidden words / phrases.

    Returns
    -------
    tuple[bool, list[str]]
        A tuple of (is_nsfw, matched_keywords).
    """
    lowered = text.lower()
    matched = [kw for kw in keywords if kw.lower() in lowered]
    return bool(matched), matched


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe audio and detect NSFW content using Whisper."
    )
    parser.add_argument("audio", help="Path to the audio file to analyse.")
    parser.add_argument(
        "--model",
        default="turbo",
        help="Whisper model to use (default: turbo).",
    )
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=None,
        metavar="WORD",
        help="Custom NSFW keyword list (replaces the built-in list).",
    )
    args = parser.parse_args()

    keywords = args.keywords if args.keywords is not None else DEFAULT_NSFW_KEYWORDS

    try:
        print(f"🎙️  Transcribing '{args.audio}' with model '{args.model}' …")
        transcript = transcribe(args.audio, model_name=args.model)
        print(f"\n📝 Transcript:\n{transcript}\n")

        is_nsfw, matched = detect_nsfw(transcript, keywords)
        if is_nsfw:
            print(f"🚨 NSFW content detected!  Matched keywords: {matched}")
            sys.exit(1)
        else:
            print("✅ No NSFW content detected.")
    except FileNotFoundError as exc:
        print(f"❌ {exc}")
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Unexpected error: {exc}")
        sys.exit(1)
