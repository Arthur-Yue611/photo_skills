# Keep the division stable

Use this workflow when one targeted correction still fails to place the boundary, when architecture has complex eaves, or when the generator keeps changing scene geometry. Use it immediately if precise preservation is important.

1. Inspect the original and record its full subject silhouette. Plan one nearly straight curve with tiny smooth waves. Check both subject and frame areas before generation.
2. Generate a COMPLETE 2D pixel-art version of the original, without a scan, photo region or divider. Keep the exact original framing and geometry. Preserve roof shape, pavilion count, bell position, windows and real clouds. Inspect this artwork before proceeding.
3. Assemble the actual original on the photographic side and the complete pixel artwork on the other side using the checked route. Use a deterministic mask and an ordinary image compositor. This establishes the boundary; do not shift a mask across a previously incorrect mixed-style image.
4. Supply that assembled image to the image editor and ask it to add ONLY the pixel scan directly along the existing join. Supply an approved image only as a scan-texture reference. Explicitly forbid moving the join or copying reference objects.
5. Inspect the actual scan path. Composite only the reviewed narrow scan band back onto the assembly from step 3. Preserve the original photography and the complete pixel artwork outside that band. Feather the outer band only enough to retain colored scan grains without a second hard edge.
6. Verify byte equality outside the intentional edit: the photographic region against the original, and the pixel region outside the scan against the step-3 assembly. Inspect the seam at full size. Reject clipped squares, misaligned roof edges and altered objects.

Use the available image generator for the artwork and scanner. Use ordinary image tools only for masks, assembly and source restoration, subject to the active tool instructions. Do not create the art through a mosaic filter.

The bundled `compose_pixel_scan.py` checks plans and restores original photography for an aligned mixed-style output. It does NOT automate the full-art generation or scan-only overlay steps above. Use an equivalent reviewed compositor for those steps; do not invent unsupported command flags. If this assembly is unavailable, clearly label a generated preview and state which preservation checks were not performed.

## Full-art prompt

Convert the entire original into coarse flat 2D pixel art. Preserve the exact aspect ratio, crop, object locations, proportions, perspective and lighting. Use large crisp square cells, connected source-color groups, stepped silhouettes and simpler distant details. Make architecture visibly pixel-painted, including roofs, walls and windows. Preserve real sky and clouds. No photographic patches, divider, scan, text, extra objects or voxel models.

## Scan-only prompt

Add a pixel scan ONLY along the existing photo/pixel join in this assembly. Keep its route, tiny waves, subject geometry and artwork grain fixed. Use neighboring small luminous squares, medium translucent colored cells, short square trails and sparse outer glints. Follow local source colors along the route. Keep a thin colored bright core, not a broad white ribbon. Do not repaint the scene or copy objects from a style reference. Preserve everything outside the narrow scan band.
