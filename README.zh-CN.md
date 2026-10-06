# Photo Skills · 照片技能合集

收集可复用的 AI 照片编辑、创意转换与视觉叙事 Skill。

[English](README.md) · [开源许可证](LICENSE)

每个 Skill 独立存放在 `skills/` 下，可以单独安装。这个仓库从第一个 Skill 开始，后续可以持续增加其他照片处理功能。

## 当前 Skill

| 名称 | 功能 | 文件 |
| --- | --- | --- |
| **Photo-to-Sketch Storytelling · 让照片长进画里** | 保留上方摄影现场感，让原片主体向下延伸成暖白纸上的细腻手绘，并加入有明确动作关系的小人物。 | [进入 Skill](skills/photo-to-sketch-storytelling/SKILL.md) |
| **Photo-to-Watercolor Journal · 照片转水彩旅行手账** | 保持原片比例，将场景整体转为钢笔淡彩插画，配氛围纸底、四个纯色色卡与英文手写标题短句。 | [进入 Skill](skills/photo-to-watercolor-journal/SKILL.md) |

## 第一个 Skill 如何工作

按“原片元素 → 幻想形态 → 小人物动作”设计故事，例如围巾变成针织小路、藤编圆环延伸成桥、树林动感变成可以卷起来的风。

默认采用 2:3 竖幅、细腻铅笔或墨线、少量淡彩与暖白留白。根据照片本身选择情节和色彩，不机械套用同一个故事。也可以指定其他比例、风格或动作。

它包括完整流程、提示词模板、情节选择库与成图检查规则。会核对主体连续性、手脚接触、人物面貌和植物叶形，发现问题时做有针对性的修订。

## Photo-to-Watercolor Journal · 照片转水彩旅行手账

将整个照片场景转为黑色细钢笔与柔和通透水彩的手账插画，保留原始宽高比。景物边缘不规则晕染、自然淡入同一纸面；纸面按夜景、暖日景、冷色风景调整底色，底部留白不与景物割裂。

右下角放恰好四个圆角方形纯色色卡，颜色取自原片；底部添加一行英文手写标题和一行短句，不额外添加边框、分栏、贴纸或微型人物。

| 照片类型 | 适用说明 |
| --- | --- |
| 街景、建筑、城市天际线 | 主要适用类型，保留建筑轮廓和空间关系 |
| 城市夜景、蓝调时刻、灯光倒影 | 主要适用类型，深调纸底呼应原片光色 |
| 自然风景、山野、乡村、湖海 | 适用，不强行添加城市元素 |
| 火车、车站、桥梁等旅行场景 | 适用，保留主体走向和真实透视 |
| 带环境的旅行人像、合照 | 可以使用；保留人物服饰姿态，需核对面貌 |
| 证件照、纯商品图、精确地图 | 不属于主要用途 |

调用示例：

```text
使用 $photo-to-watercolor-journal，把这张照片制作成钢笔淡彩旅行手账。
保留原比例，添加四个原片纯色色卡，以及英文手写标题和短句。
```

完整安装 `skills/photo-to-watercolor-journal` 文件夹，方法与第一个 Skill 相同。包含提示词模板、成图检查规则和可选取色脚本 `scripts/extract_palette.py`。脚本需要 Pillow，会返回原片像素中实际存在的四个候选主色；不可运行时可目视取色。生成模型不保证最终色卡严格等于指定 RGB，英文手写文字也需要核对。

## 使用条件

需要支持 Agent Skills、能查看上传图片的智能体环境。真正生成图片还需要该环境提供图像生成或编辑工具；安装 Skill 不会自动安装图像模型或获得工具权限。

没有图像工具时，可让它只编写完整提示词。当前包不包含外部 API 程序、密钥或固定模型依赖。

## 安装

### 通过 Skill Installer

在提供 `$skill-installer` 的 Codex 环境中输入：

```text
$skill-installer 从 https://github.com/Arthur-Yue611/photo_skills
安装 skills/photo-to-sketch-storytelling 目录中的 Skill。
```

### 下载后安装

点击 GitHub 的 **Code → Download ZIP** 下载，或执行：

```bash
git clone https://github.com/Arthur-Yue611/photo_skills.git
```

将完整的 `skills/photo-to-sketch-storytelling` 文件夹复制到宿主支持的 Skill 目录，保留其中的主文件、参考资料与图标。Codex 本地用户级目录为 `~/.agents/skills/`，项目级目录为目标项目下的 `.agents/skills/`。

使用提供导入或上传功能的宿主时，遵循其支持的安装方式。GitHub 上提供的是源文件，不会因为上传仓库就自动进入公共插件目录。

官方文档：[Build skills](https://learn.chatgpt.com/docs/build-skills)。

## 调用

安装后上传照片，输入：

```text
使用 $photo-to-sketch-storytelling，把这张照片制作成摄影与手绘
自然衔接的竖版作品，根据照片设计一个小人物参与的故事。
```

ChatGPT 可通过 `@` 选择已安装的 Skill；Codex CLI 或 IDE 扩展可通过 `$` 提及它。

还可以要求“只写提示词，不生成图片”“每张原片各生成一张”或“只修复小人物的手部接触，保留其他部分”。

生成式编辑可能重绘脸部及细节；Skill 会检查并尽量修正，但不能保证逐像素保留原片。

## 继续添加其他 Skill

为新功能创建独立的 `skills/技能名称/` 文件夹，编写自己的 `SKILL.md` 与必要资源，更新中英文首页的索引，验证后再发布。

仓库不包含用户私人照片。只有明确选择公开、并有权分发的示例图，才应加入公开仓库。

## 许可证

Skill 指令、文档和附带图标采用 [MIT License](LICENSE)。用户上传的照片及第三方图片输入不属于本仓库许可证的授权范围。
