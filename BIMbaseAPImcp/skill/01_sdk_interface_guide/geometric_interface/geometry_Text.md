---
name: Text
description: 创建二维或三维文字几何体
---


## 功能说明

提供二维文字和三维文字两种创建方式。二维文字为平面图形，可通过 color() 设置颜色；三维文字通过将二维文字沿 Z 轴扫掠形成实体。

**接口形式：**

```python
# 二维文字
Text(content, width, height).color(r, g, b, a)

# 三维文字（通过 Sweep）
text = Text(content, width, height)
TextHightLine = Line(Vec3(0,0,0), Vec3(0,0,height))
ThreeDText = Sweep(text, TextHightLine).color(r, g, b, a)
```

## 接口用例

**二维文字：**

```python
texttest = Text('参数化组件', 10, 10).color(1, 1, 1, 1)
```

**三维文字：**

```python
text = Text('参数化组件 2.0', 100, 100)
TextHight = 20
TextHightLine = Line(Vec3(0,0,0), Vec3(0,0,TextHight))
ThreeDText = Sweep(text, TextHightLine).color(0, 0, 1, 1)
```

## 注意事项

- **Text 参数：** 第一个参数为文字内容（字符串），后两个参数分别为文字宽度和高度
- **颜色设置：** 使用 `.color(r, g, b, a)` 方法设置颜色（RGBA 四元组）
- **三维实现：** 三维文字需通过 `Text()` 配合 `Sweep()` 函数实现，将二维文字沿 Z 轴线段扫掠
- **扫掠轨迹：** 三维文字的扫掠轨迹必须是垂直的 Line，从 (0,0,0) 到 (0,0,height)