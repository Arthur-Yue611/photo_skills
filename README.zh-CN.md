# Photo Skills · 照片技能合集

收集可复用的 AI 照片编辑、创意转换与视觉叙事 Skill。

[English](README.md) · [开源许可证](LICENSE)

每个 Skill 独立存放在 `skills/` 下，可以单独安装。这个仓库从第一个 Skill 开始，后续可以持续增加其他照片处理功能。

## 当前 Skill

| 名称 | 功能 | 文件 |
| --- | --- | --- |
| **Photo-to-Sketch Storytelling · 让照片长进画里** | 保留上方摄影现场感，让原片主体向下延伸成暖白纸上的细腻手绘，并加入有明确动作关系的小人物。 | [进入 Skill](skills/photo-to-sketch-storytelling/SKILL.md) |

## 第一个 Skill 如何工作

按“原片元素 → 幻想形态 → 小人物动作”设计故事，例如围巾变成针织小路、藤编圆环延伸成桥、树林动感变成可以卷起来的风。

默认采用 2:3 竖幅、细腻铅笔或墨线、少量淡彩与暖白留白。根据照片本身选择情节和色彩，不机械套用同一个故事。也可以指定其他比例、风格或动作。

它包括完整流程、提示词模板、情节选择库与成图检查规则。会核对主体连续性、手脚接触、人物面貌和植物叶形，发现问题时做有针对性的修订。

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
