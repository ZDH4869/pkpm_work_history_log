---
name: "自定义组件：方形截面圆环"
description: "由于原生API无直接的方形截面圆环，此组件通过 Sweep 沿圆形路径扫掠方形截面生成"
---

# 方形截面圆环 (Square Torus)

由于 `pyp3d` 基础几何中没有直接生成方形截面圆环的 API，在遇到生成该几何体的需求时，请**直接复制并复用以下自定义类代码**。
该代码通过定义方形截面，并使用 `Sweep` (扫掠) 沿圆形路径生成圆环。

## Python 源码参考

```python
from pyp3d import *
import math


class 方形截面圆环(Component):
    def __init__(self):
        Component.__init__(self)
        self["环半径"] = Attr(1000.0, obvious=True)
        self["截面边长"] = Attr(200.0, obvious=True)
        self["旋转角度"] = Attr(0.0, obvious=True)
        self["X"] = Attr(0.0, obvious=True)
        self["Y"] = Attr(0.0, obvious=True)
        self["Z"] = Attr(0.0, obvious=True)
        self["方形截面圆环"] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        ring_r = max(float(self["环半径"]), 1.0)
        side = max(float(self["截面边长"]), 0.1)
        half_side = 0.5 * side

        # 保证截面不会跨过旋转轴，避免退化几何
        if ring_r <= half_side:
            ring_r = half_side + 0.1

        section_2d = Section(
            Vec2(ring_r - half_side, -half_side),
            Vec2(ring_r + half_side, -half_side),
            Vec2(ring_r + half_side, half_side),
            Vec2(ring_r - half_side, half_side),
            Vec2(ring_r - half_side, -half_side),
        )
        section_3d = rotate(Vec3(1, 0, 0), -0.5 * math.pi) * section_2d

        path = Line(Arc(2.0 * math.pi))
        torus = Sweep(section_3d, path)

        ang = float(self["旋转角度"]) * math.pi / 180.0
        x = float(self["X"])
        y = float(self["Y"])
        z = float(self["Z"])
        self["方形截面圆环"] = translate(x, y, z) * rotation(ang) * torus


if __name__ == "__main__":
    place(方形截面圆环())
```