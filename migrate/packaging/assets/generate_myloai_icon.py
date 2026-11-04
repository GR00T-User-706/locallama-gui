from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ICO = ROOT / "MyLoAI.ico"
PNG = ROOT / "MyLoAI.png"

SIZE = 1024
img = Image.new("RGBA", (SIZE, SIZE), (11, 16, 32, 255))
draw = ImageDraw.Draw(img)

# Soft inset panel.
draw.rounded_rectangle((32, 32, SIZE - 32, SIZE - 32), radius=220, fill=(17, 27, 50, 255))
draw.rounded_rectangle((48, 48, SIZE - 48, SIZE - 48), radius=205, outline=(63, 82, 118, 255), width=8)

# Stylized M / signal path.
points = [(220, 730), (220, 300), (512, 620), (804, 300), (804, 730)]
draw.line(points, fill=(96, 226, 255, 255), width=82, joint="curve")

# Inner signal path gives the mark depth without making it noisy at small sizes.
inner = [(270, 690), (270, 390), (512, 650), (754, 390), (754, 690)]
draw.line(inner, fill=(151, 116, 255, 255), width=24, joint="curve")

# AI nodes and connections.
node_r = 34
nodes = [(220, 300), (512, 620), (804, 300)]
for a, b in ((nodes[0], nodes[1]), (nodes[1], nodes[2])):
    draw.line((a, b), fill=(202, 211, 255, 220), width=12)
for x, y in nodes:
    draw.ellipse((x - node_r, y - node_r, x + node_r, y + node_r), fill=(236, 249, 255, 255))
    draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(96, 226, 255, 255))

# Central control node.
draw.ellipse((466, 574, 558, 666), fill=(236, 249, 255, 255))
draw.ellipse((490, 598, 534, 642), fill=(151, 116, 255, 255))

# Export both a Windows icon and a preview asset.
img.save(PNG)
img.save(
    ICO,
    format="ICO",
    sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)
print(f"Generated {ICO}")
