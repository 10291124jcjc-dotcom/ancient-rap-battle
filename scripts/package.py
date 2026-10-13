# -*- coding: utf-8 -*-
"""Step 9 - final packaging: light grade, 1080p, gold subtitles, name cards, title cards, watermark, crowd cheers.

usage: python scripts/package.py <episode_dir> [--src preview/最终剪辑.mp4] [--watermark "账号名"]
writes final/<title>_成片.mp4 (for upload) and final/<title>_成片_手机预览.mp4 (< 30 MB)
All text is drawn with Pillow into transparent PNGs and overlaid (ffmpeg's drawtext needs fontconfig, often missing).
Grade stays LIGHT: H3 footage is already low-key; a heavy grade made the film ~30% darker.
"""
import argparse
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import font, jload, load_episode  # noqa: E402

W, H = 1920, 1080
GOLD = (255, 210, 64, 255)
STROKE = (40, 22, 0, 255)


def f_sc(size, weight="Black"):
    f = ImageFont.truetype(font("serif_sc"), size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def f_en(size):
    return ImageFont.truetype(font("serif_en_bold"), size)


def canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def runs(img, items, x, y, anchor="ls", stroke=0, alpha=1.0):
    """items = [(text, font)] on one baseline, soft shadow + optional outline"""
    layer = canvas()
    shadow = canvas()
    d, sd = ImageDraw.Draw(layer), ImageDraw.Draw(shadow)
    total = sum(d.textlength(t, font=f) for t, f in items)
    cx = x - total / 2 if anchor == "ms" else (x - total if anchor == "rs" else x)
    x0 = cx
    for t, f in items:
        sd.text((cx + 3, y + 4), t, font=f, fill=(0, 0, 0, 170), anchor="ls")
        cx += d.textlength(t, font=f)
    cx = x0
    for t, f in items:
        d.text((cx, y), t, font=f, fill=GOLD, anchor="ls", stroke_width=stroke, stroke_fill=STROKE)
        cx += d.textlength(t, font=f)
    layer = Image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4)), layer)
    if alpha < 1:
        layer.putalpha(layer.split()[3].point(lambda v: int(v * alpha)))
    img.alpha_composite(layer)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("--src", default="preview/最终剪辑.mp4")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args()
    ep, e = a.ep, load_episode(a.ep)
    work = os.path.join(ep, "work")
    tmp = os.path.join(work, "package")
    os.makedirs(tmp, exist_ok=True)
    lines = jload(os.path.join(work, "lines.json"))
    edl = jload(os.path.join(work, "edl.json"))
    picks = jload(os.path.join(work, "picks.json")) if os.path.exists(os.path.join(work, "picks.json")) else {}
    end = edl[-1]["t1"]
    A, B = e["a"], e["b"]
    wm = a.watermark if a.watermark is not None else e.get("watermark", "")

    layers = []
    img = canvas()
    runs(img, [("Freestyle Battle", f_en(76))], 150, 380, stroke=2)
    runs(img, [(A["name_cn"], f_sc(150)), (" vs ", f_en(90)), (B["name_cn"], f_sc(150))], 144, 560, stroke=4)
    runs(img, [("AI 生成", f_sc(56))], 150, 660, stroke=2)
    runs(img, [("仅供娱乐", f_sc(56))], 150, 735, stroke=2)
    img.save(os.path.join(tmp, "title.png"))
    a1 = next(l for l in lines if l["who"] == "a" and l["n"] == 1)
    b1 = next(l for l in lines if l["who"] == "b" and l["n"] == 1)
    layers += [("title.png", 0.0, a1["start"] - 0.08, 0.25), ("title.png", end - 4.8, end, 0.5)]
    for who, first in (("a", a1), ("b", b1)):
        p = e[who]
        img = canvas()
        runs(img, [(p["name_cn"], f_sc(96))], 150, 860, stroke=3)
        runs(img, [("aka ", f_en(40)), (p.get("aka", ""), f_sc(44))], 154, 920, stroke=2)
        img.save(os.path.join(tmp, "name_%s.png" % who))
        second = next((l for l in lines if l["who"] == who and l["n"] == 2), first)
        layers.append(("name_%s.png" % who, first["start"] - 0.08, second["end"] - 0.1, 0.3))
    for i, l in enumerate(lines):
        img = canvas()
        runs(img, [(l["text"].replace(" ", "  "), f_sc(58))], W / 2, 995, anchor="ms", stroke=3)
        img.save(os.path.join(tmp, "sub_%02d.png" % i))
        last = i + 1 == len(lines) or lines[i + 1]["who"] != l["who"]
        layers.append(("sub_%02d.png" % i, l["start"] - 0.05, l["end"] + 0.6 if last else lines[i + 1]["start"] - 0.07, 0.0))
    if wm:
        img = canvas()
        runs(img, [(wm, f_sc(38))], W - 60, 78, anchor="rs", stroke=2, alpha=0.8)
        img.save(os.path.join(tmp, "watermark.png"))
        layers.append(("watermark.png", 0.0, end, 0.0))

    # crowd sound from the crowd shots H3 generated (laughs, chant, ending)
    cheers = []
    for x in edl:
        cid = x["clip"].split("@")[0]
        if cid in ("LAUGH", "CHANT", "END") and cid in picks:
            cheers.append((os.path.join(ep, "clips", "%s_t%s.mp4" % (cid, picks[cid])), x["in"] or 0.0, x["t0"], x["t1"]))

    inputs = ["-i", os.path.join(ep, a.src), "-i", os.path.join(work, "music_final.wav")]
    fc = ["[0:v]scale=%d:%d:flags=lanczos,eq=contrast=1.06:saturation=0.95:brightness=0.025,colorbalance=rs=0.02:bs=-0.02,"
          "vignette=angle=PI/11,noise=alls=5:allf=t+u,format=yuv420p[base]" % (W, H)]
    last, k = "base", 2
    for idx, (png, st, en, fade) in enumerate(layers):
        dur = max(0.05, en - st)
        inputs += ["-loop", "1", "-t", "%.3f" % dur, "-i", os.path.join(tmp, png)]
        ch = "[%d:v]format=rgba" % k
        if fade:
            ch += ",fade=t=in:st=0:d=%.2f:alpha=1,fade=t=out:st=%.3f:d=%.2f:alpha=1" % (fade, max(0, dur - fade), fade)
        fc += [ch + ",setpts=PTS+%.3f/TB[l%d]" % (st, idx), "[%s][l%d]overlay=0:0:eof_action=pass[o%d]" % (last, idx, idx)]
        last, k = "o%d" % idx, k + 1
    labels = ["[mus]"]
    fc.append("[1:a]volume=1.0[mus]")
    for j, (f, inp, st, en) in enumerate(cheers):
        d = en - st
        inputs += ["-ss", "%.3f" % inp, "-t", "%.3f" % (d + 0.1), "-i", f]
        fc.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.55,afade=t=in:d=0.3,afade=t=out:st=%.3f:d=0.6,"
                  "adelay=%d:all=1[c%d]" % (k, max(0, d - 0.6), int(st * 1000), j))
        labels.append("[c%d]" % j)
        k += 1
    fc.append("%samix=inputs=%d:normalize=0:duration=first,afade=t=out:st=%.3f:d=1.5,alimiter=limit=0.95[aout]"
              % ("".join(labels), len(labels), end - 1.5))
    os.makedirs(os.path.join(ep, "final"), exist_ok=True)
    out = os.path.join(ep, "final", "%s_成片.mp4" % e["title"])
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs +
                   ["-filter_complex", ";".join(fc), "-map", "[%s]" % last, "-map", "[aout]", "-t", "%.3f" % end,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    phone = out.replace("_成片.mp4", "_成片_手机预览.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out, "-c:v", "libx264", "-preset", "slow", "-b:v", "2000k",
                    "-maxrate", "2400k", "-bufsize", "4000k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", phone], check=True)
    print("wrote", out, "and", phone)


if __name__ == "__main__":
    main()
