# Photo-to-Rainbow Ink Diptych · 照片转七彩水墨双联

把同一张照片制作成竖版9:16作品：上方是16:9真实原片裁切，下方是沿用原片光线、主体关系与色彩方向的七彩水墨重构。先生成下方艺术图，再通过脚本把原图裁切缩放后拼接到顶部。

英文目录名：`photo-to-rainbow-ink-diptych`。Diptych 指由两部分组成的双联作品。这个名称同时包含 Photo、Rainbow、Ink 和 Diptych，便于按照片、水墨、彩虹与双联风格检索；上传源码仓库并不等于自动进入公共插件目录。

## 风格分析

参考成品包含枫叶、动物、黄花、树冠、果实、衣物、水面、花园建筑和夜间灯光。共同语言是“真实摄影 + 同一场景的纸上重构”：原片里的枝叶、布料、道路与水波，变成颜料扩散和纸张折面的方向；粗粝纸纤维、湿水彩积色与矿物颗粒构成下方的触感。

参考图颜色并非平均分配。枫叶以红橙与墨色为主，黄花以黄绿为主，水面以蓝青为主，夜间彩灯才更明显地呈现多色。默认遵循七彩提示词，让七种色相以不同强弱出现，原片主色占主导；也可以明确要求“仅原片色系”变体。

上方是完整横向矩形照片，因此撕纸和折叠只出现在下方。参考截图上的平台界面、文字、点赞按钮和水印不是风格内容，不进入成品或本公开项目。

## 适用照片与使用场景

| 照片类型 | 适用度与处理重点 |
| --- | --- |
| 彩灯道路、霓虹街景、夜景倒影 | 很适合：灯光与道路形成明确的色彩方向 |
| 枫叶、树林、植物、花卉、果实 | 很适合：枝叶与花瓣可对应纸面纹理和折叠 |
| 湖海、河流、水波、雨后路面 | 很适合：真实反光转化为湿颜料与纸上留白 |
| 建筑、窗户、店铺、街景、车站 | 适合：保留透视与空间关系，不生成招牌文字 |
| 彩色衣物、旗帜、布料、市集 | 适合：从真实布褶和色块设计纸张卷折 |
| 带环境的动物照片 | 适合：保持物种、姿态与数量，轮廓需检查 |
| 旅行人像、环境人像、多人合照 | 可以：上方保留真脸，下方默认为同姿态的抽象轮廓 |
| 纯面部特写、证件照 | 不优先：上下重构空间有限，浅横向裁切易丢失上下文 |
| 需要准确文字、地图或商品颜色复现的图 | 不属于主要用途：下方是艺术重构 |

适用于旅行纪念、摄影艺术对照、氛围海报和社交平台竖版图片。横向原片更容易保留完整场景；竖片需要先检查顶部裁切。

## 布局和原图保护

默认画布1152×2048；上方1152×648，下方1152×1400。整体严格9:16，上方严格16:9；上方约占31.6%，不是一半。

顶部只使用真实原片的显示方向、等比例缩放与裁切，不调色、不锐化、不磨皮、不改五官、不改变动作。脚本保存PNG后会验证顶部像素与裁切缩放后的原图完全一致。这不意味着未裁切的整张原片仍然全部可见，也不意味着缩放后的像素与原尺寸照片一一相同。

下方默认使用抽象人物轮廓，不凭空生成新五官。如果要求下方也保留真实脸部，需要额外使用受保护的原脸合成流程；仅靠提示词不能保证精确保留。

## 内容与运行条件

完整 Skill 位于 `skills/photo-to-rainbow-ink-diptych/`，共6个文件：

- `SKILL.md`：触发条件与两阶段工作流。
- `agents/openai.yaml`：英文展示名称与调用示例。
- `references/prompt-template.md`：下方生成模板和局部修订方式。
- `references/scene-adaptation.md`：不同照片的色彩与结构选择。
- `references/quality-checks.md`：构图、人物、色彩和原图保护检查。
- `scripts/compose_diptych.py`：裁切预览、上下拼接和顶部像素验证。

生成下方需要支持参考照片的图像生成/编辑工具；拼接需要Python和Pillow。安装skill不会自动安装图像模型或授予工具权限。缺少图像工具时只能先得到提示词；缺少确定性编辑工具时，顶部原片保护还未完成。

安装脚本依赖：

```bash
python -m pip install "Pillow>=10"
```

安装完整 Skill 文件夹到宿主支持的技能目录，或使用其导入流程。不同AI宿主的安装方式不同，不能只上传单个提示词就假定所有脚本可运行。

调用示例：

```text
使用 $photo-to-rainbow-ink-diptych，将我的照片制作成9:16七彩水墨双联。
上方是真实原图的16:9裁切，不调色、不重绘。
先生成下方七彩水墨艺术图，再把原图拼接到顶部。
不要文字、水印、边框、星空或烟雾特效。
```

如果自行运行，先从仓库根目录检查裁切：

```bash
python skills/photo-to-rainbow-ink-diptych/scripts/compose_diptych.py --source original.jpg --prepare-only --output work/top_preview.png
```

得到下方艺术图后，再使用相同的裁切设置：

```bash
python skills/photo-to-rainbow-ink-diptych/scripts/compose_diptych.py --source original.jpg --art lower_art.png --output output/final_diptych.png
```

生成图像的实际观感依赖模型，须核对下方主体、折叠和色彩。本包已验证拼接、比例、原片不变和输入保护；没有把这些验证用的测试图片当作公开成品示例。

## English project description

**Photo-to-Rainbow Ink Diptych** turns a photo into a vertical 9:16 artwork pairing an untouched 16:9 source-photo crop with a scene-inspired rainbow ink and watercolor reconstruction on rough, torn or folded paper. Generate the lower art first, then composite the real photograph above using a lossless, pixel-verified assembly helper. Best suited to neon streets, night lights, reflections, landscapes, foliage, flowers, textiles, architecture, animals and environmental portraits.

Suggested search terms: photo editing, rainbow ink, ink wash, watercolor, photo diptych, torn paper, folded paper, mixed media, agent skills.

Skill instructions and code follow the repository MIT license. User photos and third-party style screenshots are not distributed in this project and are not covered by that license.
