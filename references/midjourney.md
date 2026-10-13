# Midjourney 定妆图

一期 8 张，用户在 Midjourney 生成，存进 `<期数文件夹>/refs/`，文件名必须照下表。Claude 先把 `{...}` 按本期角色填好再发给用户。

| 文件名 | 内容 | 比例 |
| --- | --- | --- |
| a_sheet.png | A 三视图 | 16:9 |
| a_face.png | A 表情四宫格 | 1:1 |
| b_sheet.png | B 三视图（手里拿着标志道具） | 16:9 |
| b_face.png | B 表情四宫格 | 1:1 |
| dj.png | DJ | 16:9 |
| hecklers.png | 气氛组 3 人 | 16:9 |
| crowd.png | 群众 | 16:9 |
| venue.png | 场景 | 16:9 |

`make_clips.py` 会从三视图左边的正面像自动裁出**腰部以上的半身图**，近景都用半身图：参考图给全身，H3 就会拍成全身远景。裁得不好时，用户可以自己放一张 `a_bust.png` / `b_bust.png`。

## 挑图标准

- 脸要原创，**不能像任何真实人物或演过这个角色的演员**，像就重抽
- 两个主角的配色和轮廓一眼分得开（例：红黑铠甲 vs 白鹤氅）
- B 的标志道具要清楚，定稿后整期都用这一套，不再换

## 提示词

### A / B 三视图
```
cinematic photoreal character turnaround sheet, front view, side view and back view of the same man standing full body side by side, plain grey studio background, soft even studio light. {名字（拼音）}, {一句话身份：朝代、身份、年龄、体型}, {脸型、眉眼、胡须、发型、头饰}, {表情气质}. {服装：材质、颜色、配件}. Holding a silver corded microphone in his right hand{B 加：and {道具} in his left hand}. realistic skin texture, ultra detailed, 35mm film still --ar 16:9 --style raw
```

### A / B 表情四宫格
```
2x2 grid of close-up portraits of the same man, cinematic photoreal, plain grey background: top left shouting a rap line into a silver microphone, top right smug confident smirk, bottom left mocking side-eye, bottom right {第四个表情}. {名字}, {脸和发型的简述}, {服装简述} --ar 1:1 --style raw
```
支持 Omni Reference 的话，把定稿的三视图加成 `--oref`，脸更一致。

### DJ
```
cinematic photoreal portrait, front and side half-body views of the same young Asian man, plain grey background. Black knit beanie, big black over-ear headphones, oversized modern black t-shirt with a Chinese pattern print, thick silver chain, tattooed forearms, cool focused expression --ar 16:9 --style raw
```

### 气氛组
```
cinematic photoreal group portrait, three {朝代} commoner men with arms over each other's shoulders, plain grey background, front half-body. Left: tall thin man in his 20s with a grey cloth headband and rough grey cross-collar tunic. Middle: round-faced chubby man about 30 with a brown head wrap and earth-yellow short tunic, laughing with mouth wide open. Right: young man with a topknot in a dark blue rough tunic wearing modern black sunglasses. Excited exaggerated expressions --ar 16:9 --style raw
```

### 群众
```
cinematic photoreal medium shot of a packed crowd of {朝代} commoners inside a dim wooden hall, about twenty people, varied faces aged 18 to 50, mostly men with a few women, rough hemp cross-collar tunics in earth tones of grey, brown, ochre and faded indigo, cloth headbands, head wraps or simple topknots, raising fists and cheering wildly toward the left, warm red lantern light from above, haze, shallow depth of field, 35mm film grain --ar 16:9 --style raw
```

### 场景
```
cinematic photoreal wide shot, no main characters. A two-story wooden hall of the {朝代} era converted into an underground rap battle club: dark timber pillars and second-floor wooden railings, rows of red lanterns glowing warm orange, hanging plain red and black battle banners without text, a raised DJ booth at the far end with modern turntables, a mixer and vertical blue-white LED tubes, a single cold white spotlight beam from the ceiling cutting through thick haze, an empty circle in the center surrounded by a packed crowd of {朝代} commoners raising their fists. Low-key lighting, warm orange against cool blue-white, shallow depth of field, 35mm film grain --ar 16:9 --style raw
```
DJ、气氛组、群众、场景这四张可以跨期复用，同一朝代不用重做。
