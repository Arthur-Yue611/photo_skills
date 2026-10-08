# Complete prompts

Replace the scene, boundary direction, region orientation and local colors using the actual original. Never send unfilled placeholders. Use approved images only for style; do not copy their content or boundary coordinates.

## 中文 Prompt

请根据我上传的原始照片，制作一张独立的“真实摄影与二维像素画融合”的作品。保留原图宽高比例、取景、地平线、主体位置、结构、比例、姿态和主要配色，每张单独输出，不做对比图、上下两栏或多图拼接。

先识别完整主体。建筑群、大片建筑立面或横跨画面的景物，应把整组场景当作主体，不只选择最高的塔楼；小房子、气球形景观等独立主体，则让分界穿过主体本身。没有独立主体的树林、山水或田野按整幅画面划分。

一侧保留真实原片，另一侧全部转成清楚的二维像素画。主体内部尽量一半原片、一半像素，整张图也尽量各占一半。允许调整分界的位置和角度，不移动、拉伸主体来凑比例。

分界是一条整体接近直线、只带轻微平滑起伏的曲线，像幅度很小的小波浪。根据构图贯穿一组相对的画面边缘，不固定竖直或斜向。不要完全笔直，不要折线、突然偏折、明显大弧线或绕着主体描边。与景物轮廓贴合只是可选项，不能因此破坏自然走向。

交界处保留清楚的“像素扫描”效果：连续发亮的方形像素、中等大小的半透明彩色方块、少量短方块拖尾与更小的外围亮点。透明度不能洗掉颜色，高亮只集中在分界附近；允许少量浅色亮点，不允许连续的纯白粗光带。没有参考图时，可从亮芯约占图宽0.4%—0.5%、整个扫描带约占图宽3%—4%开始，再根据观感调整。提供已认可参考图时，沿用其扫描宽度、亮度、颗粒形式和轻微起伏，不自行改成另一种效果。颜色随经过的局部景物变化：红墙用红色像素、黄墙用黄色像素、草地用绿色、天空用蓝色、白云用暖白色；不同颜色自然连接，不统一套用某种霓虹色。

像素部分使用明显的大方块、平面色组和阶梯轮廓。相邻像素组成有目的的形状和明暗色块，避免随机棋盘格、迷彩状碎片和细小多边形。使用统一的方格单位及其整数倍组合；前景轮廓较清楚，远景适当简化，天空和大墙面保留安静的平面区域，不强行画满格线。颗粒边长以此前的同一基准放大约20%，替代放大30%的设置；若以30%版本为参考，只将艺术区域的颗粒边长调整为当前的约92.3%，也就是缩小约7.7%。不缩小扫描边界的颗粒，不改变其位置、角度、起伏、颜色、透明度、宽度或亮度。大块面使用较大的像素，小物件使用稍小但清楚的像素。允许牺牲一些细节分辨度，不要退回细碎颗粒。可按1536像素画宽，先尝试背景与简单形体约34—48像素方块、建筑表面约24—36像素、小细节约12—19像素，并按实际物体大小调整。

建筑必须与周围景物一样有明确的像素感。墙面、屋顶与塔身使用清楚可见的方块和少量原片色调表现明暗；弧形、屋檐和斜坡采用阶梯状轮廓。门窗、栏杆可使用稍小的像素，但不能保留细密写实纹理、平滑材质或光滑细线。保留建筑结构、比例、位置、门窗关系和核心配色，允许删去细小材质纹理。像素侧的天空、地面、建筑和小物件都要处理，不能只处理草木。

保留原片中的真实景物与光线，不从风格参考图复制云朵、建筑或装饰；原片晴空保持晴空。不要新增人物、动物或无关物体，不修改可辨认的人脸。此方法适用于建筑与风景，不用于人像、合照、宠物或动物主题照片。

不要MC三维方块、立体积木、模糊马赛克、霓虹描边、星空、浓烟、无关装饰、文字、Logo、水印和边框。

先生成与原片对齐的像素艺术部分，再用真实原片恢复摄影区域，保持扫描自然衔接。若一次针对性的分界修正仍失败，改用分步流程：先生成整张纯像素图，按检查后的分界与真实原片合成，再只在既有交界上生成扫描效果；最后仅保留经检查的扫描带，其余区域从合成底图恢复。不要移动遮罩去掩盖原本错误的摄影/像素划分。摄影区域不调色、不美化、不重绘。无法回填原片时，应说明这是生成试图，不能声称摄影部分完全没有变化。

## English prompt

Create one continuous photograph-and-2D-pixel-art fusion from the uploaded original. Preserve its aspect ratio, framing, viewpoint, horizon, geometry, object positions, proportions, lighting and core palette. Output one image per source, without comparison panels or collage.

Identify the complete subject. Treat a wide building complex or facade as one whole subject, including its towers, roofs, pavilions, walls and stairs. For a separate small building or balloon-shaped attraction, pass the boundary through the object itself. For scenery without a separate subject, divide the whole view.

Keep one connected photographic region and one connected pixel-art region. Aim for approximately half of the complete subject and half of the entire frame on each side. Adjust boundary angle and position without moving or stretching the subject.

Use one complete boundary between opposing frame edges. Its overall direction must be nearly straight but have tiny smooth wave-like undulations. Choose its orientation for this composition, without a fixed diagonal. Avoid a ruler-straight line, angular polyline, abrupt roof kink, pronounced bow, large S-curve or object outline. Following scene contours is optional and must not spoil the simple natural route.

Keep a clearly visible pixel scan front made from neighboring luminous SQUARE cells, medium translucent colored squares, short square-cell trails and sparse smaller outer glints. Keep color visible through transparency. Use a thin colored bright core (starting around 0.4–0.5 percent image width) and a total band around 3–4 percent; judge visually. Allow a few pale highlights, never a broad continuous white ribbon. Concentrate highlights near the junction. When an approved reference is supplied, retain its scanner width, intensity, square-cell appearance and slight waviness. Change scan colors with the local source material: red at red walls, yellow at yellow walls, green over grass, blue over sky and ivory over real clouds. Do not apply one fixed neon or unrelated rainbow color.

Target cell side lengths about 20 percent larger than the same earlier baseline, replacing the previous 30 percent setting. When editing that 30 percent version, reduce only artwork cell side lengths to about 92.3 percent of their current size (about 7.7 percent smaller). Lock the scanner particles, route, waves, colors, transparency, width and brightness.

Make the entire pixel region obvious coarse 2D pixel art: large crisp square cells, flat source-color groups and stepped outlines. Group neighboring cells into purposeful shapes and light/shadow masses using a consistent square unit and integer-multiple clusters. Keep foreground edges clearer and distant forms simpler. Allow quiet sky and wall areas without artificial grid lines. Avoid random checkerboards, camouflage fragments and tiny polygon facets. Accept reduced fine detail. As starting guides at 1536-pixel width, try 34–48-pixel background/simple-shape clusters, 24–36-pixel architectural cells and 12–19-pixel small details, adjusted for apparent object size. Do not return to tiny grains or leave smooth photographic patches inside the pixel region.

Buildings must look as visibly pixel-painted as their surroundings. Use coarse square shading groups on walls, roofs and towers; step curves, roof slopes, arches and eaves. Make windows and rails from visible pixel cells rather than thin realistic lines. Keep recognizable structure, position, proportions, door/window relationships and palette, while simplifying stone, plaster and brick micro-texture. Do not paint buildings as smooth illustrations with tiny facets. Pixel-paint every edited sky, ground and small object too.

Keep the source scene and light. Do not copy buildings, clouds or objects from style references. A clear source sky must stay clear. Do not add people, animals or decorations, or repaint recognizable faces. Use this method for architecture and scenery, not portrait, group-photo, pet or animal-theme sources.

No Minecraft cubes, voxel models, plastic gloss, blurred mosaic, neon outlines, stars, smoke, captions, logos, watermarks, borders or multi-image layouts.

Generate aligned pixel art, then restore the actual original photographic region and inspect the scan join. If one targeted route correction fails, generate a complete pixel-art image first, deterministically assemble it with the original along the checked route, then generate the scan ONLY on the existing join. Retain only the reviewed scan band from that edit; restore everything else from the assembly. Never move a mask across a wrongly divided mixed-style image. Do not recolor, enhance or redraw that region. If source restoration is unavailable, label the output a generated preview rather than an untouched-photo composite.

## Local revisions

- Building still looks smooth: revise only pixel-side architecture with coarse square shading and stepped window/roof contours; keep scanner and other regions fixed.
- Grain too small: enlarge the specified region's cells without changing source geometry or scanner style.
- Grain needs a slight reduction: use the current 20 percent enlargement setting; when revising a 30 percent version, target 1.20/1.30 of its artwork cell side lengths. Keep the scanner and photo exactly unchanged, restoring them from the approved image after generation.
- Boundary too straight or too wavy: preserve its position and overall angle while adding or reducing only tiny smooth undulations.
- Scan color wrong: match the affected scan cells to their local source material; retain route, width and brightness.
- Added clouds or objects: remove only the invented content, preserving real source elements and scanner squares.
