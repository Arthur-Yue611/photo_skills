# 照片转像素扫描 · Photo to Pixel Scan

把建筑或风景照片做成一张连续的融合图：一部分是真实原片，另一部分是清楚的二维像素画，中间用发亮的方形像素扫描连接。

[English](README.md) · [处理指令](SKILL.md) · [许可证](LICENSE)

**英文名称：** `photo-to-pixel-scan`

**简短描述：** 建筑与风景照片转原片、二维像素融合图。主体和整图尽量对半，分界轻微起伏，扫描颜色跟随局部景物，建筑也有明显的大方块像素感。

## 本次更新

沿用约20%的颗粒放大目标，不要每次处理再叠加放大。扫描保留半透明彩色方块和细窄亮芯，避免纯白粗光带。像素按景物形状组织成块，避免细碎杂色。分界不稳定时，先做整张像素图，与真实原片按确定位置合成，再只给交界添加扫描效果。详见[分步处理方法](references/staged-workflow.md)。

[完整中英文提示词](references/prompt-template.md)

## 适用照片

建筑、街景、乡村房屋群、树林、花朵、田野、山景、湖景，以及气球形景观等风景场景。**不用于人像、人物合照、宠物照或动物主题照片。**

建筑群横跨画面时，完整建筑群才是主体，包括塔楼、屋顶、墙面和台阶，不只挑最高的部分。小房子或气球形景观等独立主体，要让主体本身一部分为原片、一部分为像素。树林等没有独立主体的照片按整幅画面划分。

## 这个版本的规则

- 保留原片比例、取景、主体结构和位置。
- 主体内部和整张图都尽量做到原片、像素各占一半。
- 分界整体接近直线，只带轻微平滑起伏；可以调角度和位置，不使用折线、突然偏折或大弧线。
- 扫描由发亮的方形像素组成，完整贯穿画面，颜色随经过的局部景物变化。
- 使用明显的大方块；建筑墙面、屋顶、弧形和门窗也必须看得出像素感，不保留平滑绘画或细密写实纹理。
- 小物件使用稍小但清楚的像素，像素侧不能留下未处理的物件。
- 通过原片回填保留真实摄影区域，不靠一句提示词保证原图不变。

## 使用方法

上传原始照片，然后输入：

```text
使用 $photo-to-pixel-scan 处理这张建筑或风景照片。
主体和整张图都尽量做到原片、像素各占一半。
使用明显的大像素块，建筑也要处理；
分界只带轻微起伏，扫描颜色跟随局部景物。
保留真实原片摄影区，保留原比例和取景，每张单独输出。
```

AI 需要能查看照片，并有图像生成或编辑功能。**Skill 提供方法，不会自动安装图像模型。**不同模型的效果可能不同。

附带的回填工具需要 Python 3、Pillow 和 ImageMagick。安装 Pillow 后，先检查分界计划，再合成：

```bash
python -m pip install -r requirements.txt
python scripts/compose_pixel_scan.py --source original.jpg --plan reviewed-plan.json --check-plan
python scripts/compose_pixel_scan.py --source original.jpg --art generated.png --plan reviewed-plan.json --output final.png
```

分界计划的写法见 [composition.md](references/composition.md)。工具支持上下边缘之间或左右边缘之间的扫描，内部处理后会恢复原方向。它会核对面积和保留区原片像素，但不能自动判断衔接是否好看；合成后仍要检查扫描是否被截断或出现额外切线。不能回填原片时，应说明结果是生成试图，不保证摄影部分完全没变化。

## 下载文件夹

在已上传的 GitHub 合集首页选择 **Code → Download ZIP**，解压后打开 `skills/`，取出完整的 `photo-to-pixel-scan/` 文件夹。按所用 AI 工具支持的方法导入，不要只拿一个提示词文件而漏掉参考资料和脚本。

## 上传到 photo_skills

1. 在仓库中打开 `skills/`，选择 **Add file → Upload files**。
2. 上传整个 `photo-to-pixel-scan` 文件夹，保留内部目录。
3. 确认路径为 `skills/photo-to-pixel-scan/SKILL.md`，不要把文件散放到仓库根目录，也不要重复套两层同名文件夹。
4. 把 `assets/project-readmes/` 中的 `README.md` 和 `README.zh-CN.md` 放到仓库根目录，更新合集介绍。这两份说明保留了六个 Skill 的介绍。
5. 确认 `.gitignore` 名称正确，没有变成 `.gitignore.txt`；它可以跟随 Skill 文件夹上传。
6. 保存后检查 `SKILL.md`、`agents/`、`references/` 和 `scripts/` 都在同一个 Skill 文件夹里。

## 文件内容

| 文件或文件夹 | 用途 |
| --- | --- |
| `SKILL.md` | AI 执行的处理指令 |
| `agents/openai.yaml` | 显示名称和调用示例 |
| `references/` | 完整提示词、主体判断、颗粒大小、回填和检查规则 |
| `scripts/compose_pixel_scan.py` | 面积检查与真实原片回填 |
| `requirements.txt` | 回填工具的 Python 依赖 |
| `README.md`、`README.zh-CN.md` | 通俗的使用、下载和上传说明 |
| `assets/project-readmes/` | 中英文合集介绍，放到仓库根目录 |
| `.gitignore` | 排除缓存、本地原片和输出文件夹 |
| `LICENSE` | 指令与代码的 MIT 许可证 |

目前用房屋、乡村房屋群、城堡、树林和气球形景观做过效果试验，帮助确定这套风格；不能据此保证所有照片和所有模型都得到相同效果。

公开文件不附带私人照片、人物试图或第三方视频截图。指令与代码采用附带的 MIT 许可证，私人照片和第三方图片不属于这份授权。
