import argparse
import os
import sys

from pydub import AudioSegment


def convert_m4a_to_mp3(input_file: str, output_file: str, bitrate: str = "192k") -> None:
    """
    Convert an audio file to .mp3 format.

    Parameters
    ----------
    input_file : str
        Path to the source audio file (any format supported by ffmpeg, e.g. .m4a).
    output_file : str
        Destination path for the converted .mp3 file.
    bitrate : str
        MP3 encoding bitrate (default: "192k").

    Raises
    ------
    FileNotFoundError
        If *input_file* does not exist.
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="mp3", bitrate=bitrate)
    print(f"✅ Successfully converted '{input_file}' to '{output_file}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an audio file (e.g. .m4a) to .mp3."
    )
    parser.add_argument("input", help="Path to the source audio file.")
    parser.add_argument("output", help="Path for the output .mp3 file.")
    parser.add_argument(
        "--bitrate",
        default="192k",
        help="MP3 encoding bitrate (default: 192k).",
    )
    args = parser.parse_args()

    try:
        convert_m4a_to_mp3(args.input, args.output, bitrate=args.bitrate)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
