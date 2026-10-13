---
name: ancient-rap-battle
description: 古人说唱 Battle：把两个历史上的死对头（曹操 vs 刘备、诸葛亮 vs 司马懿……）做成一条 AI 说唱对决短视频，从选题写词、Suno 做歌、Midjourney 定妆、MiniMax H3 逐句生成对口型镜头，到质检、剪辑、字幕包装、封面和发布文案一条龙。用户说"做一期 A vs B"、"古人说唱 battle"、"历史人物说唱"、"rap battle 视频"，或者要改已有一期的歌词、镜头、字幕、封面时使用。Make an AI rap-battle short between two historical rivals, end to end, with MiniMax H3 lip-sync.
---

# 古人说唱 Battle

两个古人在古风地下说唱现场当面 diss。成片约 1 分 40 秒、16:9、1080p，一期视频生成费约 15 美元。

## 0. 先说清楚的三件事

- **用户要有**：Suno 账号、Midjourney 账号、MiniMax API Key（H3 按秒计费，768P 约 $0.08/秒）
- **红线**：不用近现代政治人物、不用在世真人；人物的脸不能像任何真实的人或演员。请求涉及这些时礼貌拒绝，建议换成古人
- **钱**：每次提交生成前，先用 `--estimate` 报价，用户同意了才提交；生成完报实际花费

API Key 只通过环境变量 `MINIMAX_API_KEY` 传入，**绝不写进任何文件、脚本或记忆**。用户在对话里给了 Key，就只在执行命令时临时带上。

## 工作区

每一期一个文件夹（下面叫 `EP`），先 `python scripts/setup_check.py` 检查环境，缺什么按提示装。

```
EP/
  episode.json      ← 本期设定（从 examples/zhouyu-vs-zhugeliang/episode.json 复制改）
  song.mp3          ← 用户从 Suno 下载
  refs/*.png        ← 用户从 Midjourney 生成的 8 张定妆图
  分镜表.md          ← 脚本生成，给用户看
  字幕.srt / 音乐_最终.wav
  preview/  final/  cover/  clips/  work/
```

脚本都在本 Skill 的 `scripts/` 里，下面写作 `S/`。Windows 上用 `python`，不要用 `python3`。

## 流程

### 第 1 步：选题与歌词（Claude 写，用户确认）

按 `references/lyrics-guide.md`：A 先唱 16 句，B 后唱反杀 18 句，一句一个典故，B 接住 A 的原话回击，每 3–4 句留一个能演的动作梗，B 有一个全程在手的标志道具。写进 `episode.json`（名字、外号、服装、声线、变调、道具、歌词、每句动作 `actions`），把歌词表（每句带典故注释）给用户确认。

### 第 2 步：音乐（用户在 Suno 做）

按 `references/suno.md` 把 Lyrics / Styles / Title 三栏填好发给用户。用户挑好一首下载 MP3 存成 `EP/song.mp3`。前奏太长、两段声音太像都不用重做，下一步会处理。

### 第 3 步：歌曲分析（全自动）

```
python S/analyze_song.py EP
```
分离人声、识别逐字时间、测节拍、按歌词找到两段 verse 和每句起点、按小节剪短前奏间奏结尾、给两人分别变调、生成 `音乐_最终.wav` 和 `字幕.srt`。看输出的 "line check"：每句识别到的字（同音错字很正常）要和歌词对得上。把 `音乐_最终.wav` 发给用户听；嫌声音不够分开就调 `episode.json` 里的 `pitch`（半音）重跑，嫌前奏结尾长短用 `--intro-bars` / `--outro-bars`。

### 第 4 步：定妆图（用户在 Midjourney 做）

按 `references/midjourney.md` 填好 8 条提示词发给用户，按文件名存进 `EP/refs/`。逐张看图：脸原创、两人配色分得开、道具清楚。

### 第 5 步：分镜与提示词（全自动）

```
python S/make_clips.py EP
```
按 `references/shot-template.md` 的模板生成 35 条素材的英文提示词、剪辑表和 `分镜表.md`。把分镜表的「剪辑顺序」用中文讲给用户听，动作想改就改 `episode.json` 的 `actions` 重跑。

### 第 6 步：H3 生成（报价 → 用户同意 → 提交）

```
python S/h3run.py EP --all --estimate     # 报价
python S/h3run.py EP A01 --dry-run        # 检查请求格式，不花钱
python S/h3run.py EP A01                  # 先跑一条测试
python S/h3run.py EP --all                # 测试满意后批量，并行提交
```
**先跑一条测试**，拼预览给用户确认口型和画面，再批量。每条出来自动比对声音：合格的自动记进 `work/picks.json`，H3 晚放了歌会自动记进 `work/shifts.json`；不合格的显示 "LIPS WON'T MATCH"，报给用户、征得同意后用同一命令重抽（自动编 take 号）。批量时 Bash 设成后台运行，等通知。

### 第 7 步：质检与修正

```
python S/assemble.py EP                   # 拼草稿 preview/草稿.mp4，没生成的位置是深灰色
```
草稿压成 30MB 以内发给用户看（手机端上限 30MB）。**用户的眼睛是标准**，自动检查只是筛子。用户说哪里不对：

1. 先抽那几秒的帧自己看，找原因（口型？空台？重复？群演太多？景别太远？）
2. 修正优先级：免费的平移画面（`shifts.json`）→ 剪辑表里换成反应/观众镜头 → 换另一个 take（`picks.json`）→ 花钱单句重抽
3. 口型可以用 `python S/lipcheck.py EP B12` 测嘴比声音慢几帧，但只作参考；挪了必须给用户看，用户说原来更好就改回

### 第 8 步：定稿与包装

```
python S/assemble.py EP --out preview/最终剪辑.mp4
python S/package.py EP --watermark "账号名"
```
轻调色、1080p、金色字幕、名字卡、片头片尾标题（含「AI 生成 仅供娱乐」）、水印、观众欢呼。输出 `final/<标题>_成片.mp4` 和手机预览版。字幕时间不对、太暗等问题都在 `package.py` 里调，不用重新生成画面。

### 第 9 步：封面与文案

```
python S/cover.py EP          # 默认取 B5 双人近景的第 2 秒，镜像成 A 在左
```
输出竖版 3:4（抖音）和横版 16:9 封面。文案写：抖音标题 + 正文（一个是……一个是……、各引一句歌词、你站谁）+ 话题；需要的话再写一条讲制作过程的推文。

### 发布前提醒（每期都说）

- 平台上勾选「AI 生成内容」声明
- Suno 免费版的歌不能商用，要开收益就用付费版重做最终那首
- 水印、标题用自己的，不搬别的账号的 logo 和歌词

## 参考

- `references/shot-template.md`：整片排布、M1–M14 运镜、原片拍法规则
- `references/suno.md`、`references/midjourney.md`：给用户的现成提示词
- `references/lyrics-guide.md`：选题清单、写词规则、`actions` 写法
- `references/pitfalls.md`：踩过的坑和对应的默认规则
- `examples/zhouyu-vs-zhugeliang/episode.json`：完整示例
