#!/usr/bin/env python3
"""
reel_edit.py - Turn a 16:9 two-musician video into a 9:16 Instagram Reel.

Features
  * Dynamic reframing: smooth, eased virtual-camera pan (keyframes below)
  * Slow push-in zoom + optional "punch" zooms on beat timestamps
  * Warm-teal cinematic grade that protects window highlights, subtle vignette
  * Audio: gentle EQ + light compression + two-pass loudness normalisation (-14 LUFS)
  * Minimal white centred title with fade in/out, clean fade-out at the end
  * H.264 / AAC export tuned for Instagram (1080x1920, 30 fps, AAC 192k)

Requires only Python 3.8+ (standard library) and FFmpeg/FFprobe on PATH.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# =============================================================================
# CONFIG - tweak these
# =============================================================================
DEFAULT_INPUT = "WhatsApp Video 2026-11-22 at 11.13.47.mp4"
DEFAULT_OUTPUT = "reel_vertical.mp4"

OUT_W, OUT_H, FPS = 1080, 1920, 30

# Horizontal position of each musician as a fraction of the source frame width
# (0.0 = far left edge, 1.0 = far right edge). Tune these after a --preview.
GUITAR_X = 0.27      # guitarist (left side of frame): face + fretting hand
KEYBOARD_X = 0.71    # keyboardist (right side of frame)
MID_X = 0.49         # between the two

# Virtual camera keyframes: (time_in_seconds, centre_x_fraction).
# The camera eases (smoothstep) from each keyframe to the next.
CAMERA_KEYS = [
    (0.0,  KEYBOARD_X),   # 0:00-0:12.3  keyboard intro
    (12.3, KEYBOARD_X),
    (13.5, GUITAR_X),     # glide to guitarist by 0:13.5
    (36.0, GUITAR_X),     # 0:13-0:36 guitar lead
    (46.0, MID_X),        # 0:36-1:39 both playing: slow sweep guitar -> keys -> guitar
    (58.0, KEYBOARD_X),
    (68.0, KEYBOARD_X),
    (80.0, MID_X),
    (92.0, GUITAR_X),
    (99.0, GUITAR_X),
]

# Zoom: slow push-in across the whole clip (0.06 = ends 6% closer)
SLOW_PUSH = 0.06
# Optional beat-drop punch-ins: list of timestamps in seconds, e.g. [13.5, 36.0, 58.0]
PUNCH_TIMES = []
PUNCH_AMOUNT = 0.045   # 4.5% extra zoom at peak
PUNCH_DECAY = 4.0      # higher = faster settle

# Text
TITLE_TEXT = "Acoustic Session"
SUBTITLE_TEXT = "guitar + keys"
TITLE_IN = 0.6         # seconds when title starts fading in
TITLE_OUT = 4.0        # seconds when title starts fading out
TITLE_FADE = 0.8
END_FADE = 1.2         # video + audio fade-out length at the end

# Audio
TARGET_LUFS = -14
TRUE_PEAK = -1.5
LRA = 11

# Colour grade (all gentle; adjust to taste)
GRADE = (
    "eq=gamma=1.12:contrast=1.04:saturation=1.10,"                 # lift dim room, a touch of contrast
    "curves=m='0/0 0.18/0.155 0.50/0.52 0.80/0.83 0.92/0.93 1/0.975',"  # S-curve + highlight roll-off (protects window)
    "colorbalance=rs=-0.04:gs=0.02:bs=0.06:rm=0.02:bm=-0.01:rh=0.07:gh=0.02:bh=-0.07,"  # teal shadows, warm highlights
    "vignette=angle=PI/3.5"                                         # subtle vignette
)

AUDIO_EQ = (
    "highpass=f=60,"
    "afftdn=nr=6:nf=-45,"                       # very light noise reduction
    "equalizer=f=220:t=q:w=1.0:g=-2,"           # trim room mud
    "equalizer=f=3500:t=q:w=0.9:g=1.5,"         # a little presence
    "highshelf=f=9500:g=1.5,"                   # a little air
    "acompressor=threshold=-20dB:ratio=2:attack=20:release=250:makeup=1"
)
# =============================================================================


def run(cmd, capture=False):
    print("\n>", " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd), "\n")
    res = subprocess.run(cmd, stderr=subprocess.PIPE if capture else None, text=True)
    if res.returncode != 0:
        if capture and res.stderr:
            print(res.stderr[-3000:])
        sys.exit(f"FFmpeg failed (exit {res.returncode}).")
    return res.stderr if capture else ""


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,width,height:format=duration", "-of", "json", path],
        capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("ffprobe could not read the file:\n" + out.stderr)
    info = json.loads(out.stdout)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    return int(video["width"]), int(video["height"]), float(info["format"]["duration"]), has_audio


def smooth(a, b):
    """FFmpeg expression: smoothstep 0->1 as t goes a->b."""
    u = f"clip((t-{a})/{b - a},0,1)"
    return f"({u}*{u}*(3-2*{u}))"


def camera_center_expr(keys):
    c0 = keys[0][1]
    expr = f"{c0}"
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t1 > t0 and v1 != v0:
            expr += f"+({v1 - v0:.4f})*{smooth(t0, t1)}"
    return expr


def zoom_expr(duration):
    z = f"1+{SLOW_PUSH}*t/{duration:.3f}"
    for p in PUNCH_TIMES:
        z += (f"+gte(t,{p})*{PUNCH_AMOUNT}*min((t-{p})/0.1,1)*exp(-{PUNCH_DECAY}*(t-{p}))")
    return z


def esc_text(s):
    return (s.replace("\\", "\\\\").replace("'", "\u2019")
             .replace(":", "\\:").replace("%", "\\%"))


def find_font():
    for name in ("segoeuil.ttf", "segoeui.ttf", "arial.ttf"):
        p = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / name
        if p.exists():
            return str(p).replace("\\", "/").replace(":", "\\:")
    return None  # let FFmpeg/fontconfig pick (works on Linux/macOS)


def text_filters(title, subtitle):
    font = find_font()
    fontopt = f"fontfile='{font}':" if font else ""
    a, b, f = TITLE_IN, TITLE_OUT, TITLE_FADE
    alpha = (f"alpha='if(lt(t,{a}),0,if(lt(t,{a + f}),(t-{a})/{f},"
             f"if(lt(t,{b}),1,if(lt(t,{b + f}),1-(t-{b})/{f},0))))'")
    common = f"{fontopt}fontcolor=white:shadowcolor=black@0.45:shadowx=2:shadowy=2:{alpha}:x=(w-text_w)/2"
    parts = []
    if title:
        parts.append(f"drawtext=text='{esc_text(title)}':fontsize=68:y=h*0.68:{common}")
    if subtitle:
        parts.append(f"drawtext=text='{esc_text(subtitle)}':fontsize=34:y=h*0.68+80:{common}")
    return ",".join(parts)


def build_audio_chain(duration, measured=None):
    ln = f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA={LRA}"
    if measured is None:
        return f"{AUDIO_EQ},{ln}:print_format=json"
    ln += (f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
           f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
           f":offset={measured['target_offset']}:linear=true")
    return (f"{AUDIO_EQ},{ln},aresample=48000,"
            f"afade=t=out:st={max(duration - END_FADE, 0):.3f}:d={END_FADE}")


def measure_loudness(src):
    print("Pass 1/2: measuring loudness ...")
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-vn",
               "-af", build_audio_chain(0), "-f", "null", os.devnull], capture=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    if not m:
        sys.exit("Could not parse loudnorm measurement output.")
    return json.loads(m.group(0))


def main():
    ap = argparse.ArgumentParser(description="Convert a 16:9 duo video to a 9:16 Instagram Reel.")
    ap.add_argument("input", nargs="?", default=DEFAULT_INPUT)
    ap.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
    ap.add_argument("--title", default=TITLE_TEXT)
    ap.add_argument("--subtitle", default=SUBTITLE_TEXT)
    ap.add_argument("--no-text", action="store_true", help="disable title overlay")
    ap.add_argument("--preview", action="store_true", help="fast low-quality, no-audio test render")
    ap.add_argument("--preview-start", type=float, default=8.0)
    ap.add_argument("--preview-len", type=float, default=14.0)
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH. Install FFmpeg (see README commands) and reopen the terminal.")
    if not Path(args.input).exists():
        sys.exit(f"Input file not found: {args.input}")

    src_w, src_h, duration, has_audio = probe(args.input)
    print(f"Source: {src_w}x{src_h}, {duration:.1f}s, audio={'yes' if has_audio else 'no'}")

    # Crop window: full source height, 9:16 width, positioned by the virtual camera
    cw = int(src_h * 9 / 16) // 2 * 2
    cx = camera_center_expr(CAMERA_KEYS)
    zoom = zoom_expr(duration)
    scale_up = src_h < OUT_H
    if scale_up:
        print(f"Note: the {cw}x{src_h} crop is upscaled to {OUT_W}x{OUT_H} "
              f"({OUT_H / src_h:.2f}x). A light sharpen is applied.")

    texts = "" if args.no_text else text_filters(args.title, args.subtitle)
    fade_out_start = max(duration - END_FADE, 0)

    vgraph = (
        f"[0:v]fps={FPS},"
        f"crop=w={cw}:h={src_h}:x='clip(({cx})*iw-{cw}/2,0,iw-{cw})':y=0,"
        f"hqdn3d=1.5:1.2:3:3,"
        f"scale={OUT_W}:{OUT_H}:flags=lanczos,"
        f"unsharp=5:5:0.4:5:5:0.0[base];"
        f"[base]scale=w='trunc({OUT_W}*({zoom})/2)*2':h='trunc({OUT_H}*({zoom})/2)*2':"
        f"eval=frame:flags=bicubic[zoomed];"
        f"[1:v][zoomed]overlay=x='(W-w)/2':y='(H-h)/2':shortest=1:format=yuv420,"
        f"{GRADE},"
        + (f"{texts}," if texts else "")
        + f"fade=t=in:st=0:d=0.5,fade=t=out:st={fade_out_start:.3f}:d={END_FADE},"
        f"format=yuv420p[v]"
    )

    cmd = ["ffmpeg", "-y", "-hide_banner", "-i", args.input,
           "-f", "lavfi", "-i", f"color=c=black:s={OUT_W}x{OUT_H}:r={FPS}:d={duration:.3f}"]

    if args.preview:
        cmd += ["-filter_complex", vgraph, "-map", "[v]", "-an",
                "-ss", str(args.preview_start), "-t", str(args.preview_len),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p"]
        out = Path(args.output).with_name(Path(args.output).stem + "_preview.mp4")
    else:
        graph = vgraph
        maps = ["-map", "[v]"]
        if has_audio:
            measured = measure_loudness(args.input)
            graph += f";[0:a]{build_audio_chain(duration, measured)}[a]"
            maps += ["-map", "[a]"]
        else:
            print("No audio stream found; exporting video only.")
        cmd += ["-filter_complex", graph] + maps + [
            "-c:v", "libx264", "-preset", "slow", "-crf", "17",
            "-maxrate", "14M", "-bufsize", "28M",
            "-profile:v", "high", "-level", "4.2", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-fps_mode", "cfr", "-g", str(FPS * 2), "-bf", "2",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart",
        ]
        out = Path(args.output)

    cmd.append(str(out))
    print("Rendering ...")
    run(cmd)
    print(f"\nDone -> {out.resolve()}")


if __name__ == "__main__":
    main()
