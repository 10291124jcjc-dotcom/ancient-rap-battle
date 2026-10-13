# 古人说唱 Battle · ancient-rap-battle

**一句话做一期：「做一期 曹操 vs 刘备」。** 一个 [Claude Code](https://claude.com/claude-code) Skill，把两个历史上的死对头做成一条 AI 说唱对决短视频：选题写词、做歌、定妆、逐句生成对口型镜头、质检、剪辑、字幕包装、封面文案，一条龙。

完全免费、开源（MIT）。

## 成片示例：周瑜 vs 诸葛亮

周瑜拿正史打，诸葛亮拿演义还手。1 分 42 秒，34 句原创歌词，视频生成花了约 16 美元。

[![周瑜 vs 诸葛亮](assets/cover-16x9.jpg)](assets/demo.mp4)

▶ 点上图看完整视频（[assets/demo.mp4](assets/demo.mp4)）

| | |
| --- | --- |
| ![](assets/frame-1.jpg) | ![](assets/frame-2.jpg) |

## 它帮你做什么

| 步骤 | 谁来做 |
| --- | --- |
| 1. 选题、写两段 battle 歌词（一句一个典故，后唱的一方接住原话反杀） | Claude 写，你确认 |
| 2. 做歌 | 你在 Suno 生成（Claude 给好三栏提示词） |
| 3. 分离人声、识别每句时间、按小节剪短、给两人变调区分声线 | 全自动 |
| 4. 定妆图 8 张 | 你在 Midjourney 生成（Claude 给好提示词） |
| 5. 照原片拆好的分镜模板，生成 35 条素材的提示词和剪辑表 | 全自动 |
| 6. MiniMax H3 逐句生成对口型镜头，并行提交、自动检查口型 | 全自动，花钱前先报价 |
| 7. 拼草稿给你看，按你的意见修 | Claude 修，你拍板 |
| 8. 调色、金色字幕、名字卡、片头片尾、水印、观众欢呼 | 全自动 |
| 9. 抖音封面（竖版 + 横版）和发布文案 | 全自动 |

这些经验都写进了默认规则：一句一条（两句一条时 H3 常从第 2 秒开始自己重唱）、近景用半身参考图（给全身图会被拍成远景）、唱的人永远站画面左边、观众镜头里台上不能空、气氛组最多出现 3 次……完整清单见 [references/pitfalls.md](references/pitfalls.md)。

## 需要什么

- [Claude Code](https://claude.com/claude-code)
- Suno 账号、Midjourney 账号
- MiniMax API Key（H3 视频模型，768P 约 $0.08/秒，一期约 $15）
- Python 3.9+ 和 ffmpeg（要带 rubberband，Windows 用 `winget install Gyan.FFmpeg`）
- 本地 Python 包：`pip install demucs faster-whisper soundfile scipy numpy pillow`（第一次会下载约 2GB 的模型）

## 安装

```bash
git clone https://github.com/10291124jcjc-dotcom/ancient-rap-battle.git ~/.claude/skills/ancient-rap-battle
```

Windows 上把 `~/.claude/skills` 换成 `%USERPROFILE%\.claude\skills`。然后在 Claude Code 里说：

> 做一期 诸葛亮 vs 司马懿

Claude 会先跑环境检查，再一步步带你做完。

## 目录

```
SKILL.md                    Claude 的操作手册
scripts/                    analyze_song / make_clips / h3run / qa / lipcheck / assemble / package / cover
references/                 分镜模板、Suno 和 Midjourney 提示词、写词规则、踩坑清单
examples/zhouyu-vs-zhugeliang/episode.json   示例期的完整设定
```

## 注意

- 片头已经标了「AI 生成 仅供娱乐」，发布时还要在平台勾选 AI 生成内容声明
- Suno 免费版生成的歌**不能商用**，要开收益请用付费版生成最终那首
- 只做古人：不用近现代政治人物和在世真人，脸也不要做得像任何演员

## 作者

硅基废话（X：[@DDJCXX](https://x.com/DDJCXX)）。做出来的视频欢迎 @ 我。
