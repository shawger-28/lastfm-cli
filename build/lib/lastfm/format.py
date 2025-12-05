from datetime import datetime


def format_tracks(tracks):
    lines = []

    for track in tracks:
        artist = track.get("artist", {}).get("#text", "Unknown Artist")
        title = track.get("name", "Unknown Track")
        album = track.get("album", {}).get("#text", "")
        now_playing = track.get("@attr", {}).get("nowplaying")

        if now_playing == "true":
            time_str = "Now Playing"
        else:
            date_info = track.get("date")
            if date_info and "uts" in date_info:
                ts = int(date_info["uts"])
                dt = datetime.fromtimestamp(ts)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            else:
                time_str = "Unknown Time"

        block = f"{artist} — {title}"

        if album:
            block += f"\n  Album: {album}"

        block += f"\n {time_str}"

        lines.append(block)

    return lines
