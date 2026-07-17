---
name: Attr
description: 设置组件属性及其下拉框选项
---

## 功能说明

在组件类中定义属性并设置其在属性面板中的显示状态、默认值以及是否提供下拉选项。通过在 `__init__` 方法中使用 `Attr` 函数，可以控制属性的可见性（`obvious`）、只读性（`readonly`）以及通过下拉框（`combo`）限制用户的输入值。

**函数签名：**

```python
Attr(value: Any, obvious: bool = False, readonly: bool = False, combo: list = None, show: bool = False) -> AttrObject
```

**参数说明：**

- `value` (Any): 属性的默认数值，可以是数值（如 1000.0）、字符串（如 '类型A'）或特殊占位符 `None`。
- `obvious` (bool, 可选): 属性的可见性。`True` 时在属性面板中可见，`False` 或不填时隐藏。默认为 `False`。
- `readonly` (bool, 可选): 属性的只读性。`True` 时在属性面板中置灰不可调，`False` 或不填时可调。默认为 `False`。
- `combo` (list, 可选): 属性的下拉选项列表。装填的列表元素类型需与 `value` 保持一致，且必须包含 `value` 的默认值。设置后用户只能从列表中选择。
- `show` (bool, 可选): 针对最终模型的特殊参数。当赋值给模型时，`show=True` 表示在场景中显示该模型预留位。

## 接口用例

**创建常规可见可调属性：**

```python
self['宽'] = Attr(300.0, obvious=True)
```

**创建只读属性：**

```python
self['旋转角度'] = Attr(0, obvious=True, readonly=True)
```

**创建带下拉框选项的属性：**

```python
# 默认值为 1000.0，且存在于 combo 列表中
self['长'] = Attr(1000.0, obvious=True, combo=[500, 1000, 2000, 3000])
```

**创建模型预留位属性：**

```python
self['最终模型'] = Attr(None, show=True)
```

## 注意事项

- **标签命名：** 所有控制标签（如 `obvious`、`readonly`、`combo`）必须为**纯小写字母**。
- **Combo 元素匹配：** `combo` 列表中的元素类型必须与 `value`（默认参数）的数据类型完全相同，且列表中必须包含与默认参数完全相同的元素。
- **Combo 输入限制：** 一旦使用了 `combo` 标签，用户在属性面板中只能从下拉列表中选择数值，将无法再随意手动输入其他数值。
- **特殊占位符：** 最终生成的几何模型必须赋值给一个预留的"特殊属性"，其默认值需填入 `None`，并使用 `show=True` 标签。