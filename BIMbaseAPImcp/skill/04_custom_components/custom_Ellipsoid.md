---
name: "自定义组件：椭球体"
description: "由于原生API无椭球体，此组件通过 Loft 和 Section 组合生成参数化椭球体类"
---

# 椭球体 (Ellipsoid)

由于 `pyp3d` 基础几何中没有直接生成椭球体的 API，在遇到生成椭球体的需求时，请**直接复制并复用以下自定义类代码**。
该代码通过计算椭圆各高度层的截面，并使用 `Loft` (放样) 拟合平滑曲面实现。

## Python 源码参考

```python
from pyp3d import *
import math

class 椭球体(Component):
    def __init__(self):
        Component.__init__(self)
        self["X半轴"] = Attr(1000.0, obvious=True)
        self["Y半轴"] = Attr(700.0, obvious=True)
        self["Z半轴"] = Attr(500.0, obvious=True)
        self["截面数"] = Attr(25, obvious=True)
        self["旋转角度"] = Attr(0.0, obvious=True)
        self["X"] = Attr(0.0, obvious=True)
        self["Y"] = Attr(0.0, obvious=True)
        self["Z"] = Attr(0.0, obvious=True)
        self["椭球"] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        ax = max(float(self["X半轴"]), 1e-3)
        by = max(float(self["Y半轴"]), 1e-3)
        cz = max(float(self["Z半轴"]), 1e-3)
        n = max(int(self["截面数"]), 5)
        if n % 2 == 0:
            n += 1

        sections = []
        eps = 1e-3
        for i in range(n):
            t = -1.0 + 2.0 * i / (n - 1)
            z = cz * t
            scale_xy = math.sqrt(max(0.0, 1.0 - t * t))
            rx = max(ax * scale_xy, eps)
            ry = max(by * scale_xy, eps)
            sec = translate(0, 0, z) * scale(rx, ry) * Section(Arc(2 * math.pi))
            sections.append(sec)

        solid = Loft(*sections)
        solid.smooth = True

        ang = float(self["旋转角度"]) * math.pi / 180.0
        x = float(self["X"])
        y = float(self["Y"])
        z = float(self["Z"])
        self["椭球"] = translate(x, y, z) * rotation(ang) * solid


if __name__ == "__main__":
    FinalGeometry = 椭球体()
    place(FinalGeometry)
```