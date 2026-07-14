from pathlib import Path
import re


def time_to_milliseconds(time_text: str) -> int:
    """Convert HH:MM:SS,mmm into milliseconds."""
    hours, minutes, rest = time_text.split(":")
    seconds, milliseconds = rest.replace(".", ",").split(",")

    return (
        int(hours) * 3_600_000
        + int(minutes) * 60_000
        + int(seconds) * 1_000
        + int(milliseconds)
    )


def user_time_to_milliseconds(
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
) -> int:
    return (
        hours * 3_600_000
        + minutes * 60_000
        + seconds * 1_000
    )


def extract_subtitles(
    srt_file: str,
    from_hours: int = 0,
    from_minutes: int = 0,
    from_seconds: int = 0,
    to_hours: int = 0,
    to_minutes: int = 0,
    to_seconds: int = 0,
) -> str:
    content = Path(srt_file).read_text(encoding="utf-8-sig")

    start_limit = user_time_to_milliseconds(
        from_hours,
        from_minutes,
        from_seconds,
    )

    end_limit = user_time_to_milliseconds(
        to_hours,
        to_minutes,
        to_seconds,
    )

    subtitle_blocks = re.split(r"\n\s*\n", content.strip())
    selected_text = []

    for block in subtitle_blocks:
        lines = block.splitlines()

        timestamp_line = next(
            (line for line in lines if "-->" in line),
            None,
        )

        if not timestamp_line:
            continue

        start_text, end_text = [
            value.strip() for value in timestamp_line.split("-->")
        ]

        subtitle_start = time_to_milliseconds(start_text)
        subtitle_end = time_to_milliseconds(end_text)

        # Include subtitles that overlap the selected range.
        if subtitle_end >= start_limit and subtitle_start <= end_limit:
            timestamp_index = lines.index(timestamp_line)
            text_lines = lines[timestamp_index + 1 :]
            selected_text.append(" ".join(text_lines).strip())

    return "\n".join(selected_text)


result = extract_subtitles(
    srt_file="subtitles.srt",
    from_hours=0,
    from_minutes=10,
    from_seconds=30,
    to_hours=0,
    to_minutes=15,
    to_seconds=0,
)

print(result)

Path("extracted_text.txt").write_text(
    result,
    encoding="utf-8",
)