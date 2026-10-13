# Suno 做歌

用户在 suno.com 操作。Claude 先把下面三栏的内容按本期歌词填好发给用户。

## 操作

1. 左侧 **Create** → 顶部切到 **Advanced**（Simple 模式不能填歌词）
2. 填 **Lyrics**、**Styles**、**Title** 三栏；`+ Voice` 第一次不选（选了两段会变成同一个声音）
3. 模型选最新的非 mini 版本，用不了就用 mini
4. 点 Create，一次出 2 首；多点几次，挑「歌词唱全、咬字清楚、两段声音分得开」的
5. 下载 **MP3** 就够（免费版 WAV 和分轨要付费；人声由脚本自己分离），存成 `<期数文件夹>/song.mp3`

时长不用设。前奏间奏结尾太长也不用重做，`analyze_song.py` 会按小节剪短；两段声音太像也不用重做，`episode.json` 里的 `pitch` 会给两人分别变调。

## Lyrics 栏

```
[Short Intro: 2 bars DJ scratch]

[Verse 1: {A 的拼音名}, {A 的声线}]
{A 的 16 句，一句一行，句中停顿用空格}

[Short Break: 2 bars DJ scratch]

[Verse 2: {B 的拼音名}, {B 的声线}]
{B 的 18 句}

[Outro: crowd chanting]
{B 的外号} {B 的外号} {B 的外号}
[End]
```

## Styles 栏

```
Chinese battle rap, old school boom bap, 92 BPM, dark cinematic, hard punchy drums, vinyl scratches, guqin and guzheng samples, war drums, deep sub bass, live crowd hype, two male rappers trading verses, clear Mandarin diction, short intro, minimal instrumental breaks, short ending
```

朝代不同可以换乐器：唐宋换 `pipa and dizi`，春秋换 `bronze bells and drums`。

## Title 栏

`{A}vs{B}`

## 声线搭配（两段一定要反差大）

| 人设 | 写法 |
| --- | --- |
| 年轻、高傲、武将 | proud young male rapper, sharp bright voice, fast confident flow |
| 沉稳、谋士、老成 | calm cool male rapper, smooth low deep voice, slow mocking delivery |
| 粗人、猛将 | aggressive male rapper, deep powerful voice, shouting energy |
| 文人、诗人 | smooth melodic male rapper, playful flow |
| 帝王 | cold commanding male rapper, slow heavy delivery |

## 版权

Suno **免费版生成的歌不能商用**。只发着玩没问题；要开收益、接推广，先用付费版重新生成最终那一版。每期都提醒用户一次。
