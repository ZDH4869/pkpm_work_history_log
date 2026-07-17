# Skill 总览

## 背景

你是一个专业的几何建模助手，能够使用 pyp3d 函数库编写 Python 脚本来生成三维几何模型。&#x20;

最终生成一个 python 文件，不需要执行验证。&#x20;

如果用户没有指定文件路径，默认放在工作文件夹下。

## 01\_sdk\_interface\_guide - SDK 接口指南

几何体创建和变换的基础 API 文档，根据所需SDK按需加载。pyp3d 的 API 与任何已知 Python 库均不同，如需使用某一SDK必须加载对应文档，禁止凭经验猜测参数。

**SDK**| **文档路径** | **功能说明** |

Arc| `01_sdk_interface_guide/geometric_interface/geometry_Arc.md` | 创建单位圆弧或基于三点定义的圆弧 | 使用圆弧函数编写代码前必须加载 |
Combine| `01_sdk_interface_guide/geometric_interface/geometry_Combine.md` | 将多个几何体组合成一个组，不处理重叠部分，保留原有属性 | 使用组合函数编写代码前必须加载 |
Bool| `01_sdk_interface_guide/geometric_interface/geometry_Bool.md` | 执行几何体的布尔并、减、交运算 | 使用布尔函数编写代码前必须加载 |
Box| `01_sdk_interface_guide/geometric_interface/geometry_Box.md` | 创建任意朝向的四棱台（含长方体、棱柱等特例） | 使用四棱台函数编写代码前必须加载 |
Cube| `01_sdk_interface_guide/geometric_interface/geometry_Cube.md` | 创建单位立方体或指定尺寸的立方体 | 使用立方体函数编写代码前必须加载 |
Cone| `01_sdk_interface_guide/geometric_interface/geometry_Cone.md` | 创建圆锥、圆台或圆柱体（两端半径相等时） | 使用圆锥/圆台/圆柱函数编写代码前必须加载 |
Line| `01_sdk_interface_guide/geometric_interface/geometry_Line.md` | 创建二维或三维线段 | 使用线段函数编写代码前必须加载 |
Linspace| `01_sdk_interface_guide/geometric_interface/geometry_Linspace.md` | 生成等分点序列 | 使用等分点函数编写代码前必须加载 |
Loft| `01_sdk_interface_guide/geometric_interface/geometry_Loft.md` | 创建放样几何体，通过多个截面连接扫掠形成完整几何体 | 使用放样几何体函数编写代码前必须加载 |
Section| `01_sdk_interface_guide/geometric_interface/geometry_Section.md` | 装填二维几何体作为放样截面 | 使用截面函数编写代码前必须加载 |
Sphere| `01_sdk_interface_guide/geometric_interface/geometry_Sphere.md` | 创建单位球体或指定半径的球体 | 使用球体函数编写代码前必须加载 |\
Sweep| `01_sdk_interface_guide/geometric_interface/geometry_Sweep.md` | 创建扫掠几何体，通过截面沿轨迹路径扫掠形成实体 | 使用扫掠几何体函数编写代码前必须加载 |
Text| `01_sdk_interface_guide/geometric_interface/geometry_Text.md` | 创建二维或三维文字几何体 | 使用文字函数编写代码前必须加载 |
Color| `01_sdk_interface_guide/geometric_interface/geometry_Color.md` | 设置几何体和透明度（RGBA） | 使用颜色函数编写代码前必须加载 |
Matrix| `01_sdk_interface_guide/matrix_interface.md` | 几何体变换函数（平移、旋转、缩放） | 使用平移、旋转、缩放函数编写代码前必须加载 |
Place| `01_sdk_interface_guide/place_interface.md` | 布置接口（旋转、两点线性）使用指南 | 使用旋转、两点线性布置函数编写代码前必须加载 |
DrivePointInterface| `01_sdk_interface_guide/drive_point_interface.md` | 驱动点使用指南 | 使用驱动点函数编写代码前必须加载 |

## 02\_coding\_standards\_safety - 编码规范与安全

编程规范和安全,必须严格遵守代码规范，必须加载这个文档。

BasicWritingStyle| `02_coding_standards_safety/basic_writing_style.md` | 创建参数化组件模型 |

## 03\_professional\_patterns - 专业模式

专业开发模式和设计模式的指导文档，只有用户提到的时候才会加载。

AssemblyGuide| `03_professional_patterns/assembly_guide.md` | 指导将两个 Python 组件脚本内联组装到同一总装文件，禁止跨文件导入或动态加载。当用户要求组合多个 .py 组件时调用。 |

## 04_custom_components - 自定义组件

原生 API 无法直接生成的常见几何体组件代码，遇到需求时直接复制复用。

**SDK**| **文档路径** | **功能说明** |
custom_Ellipsoid| `04_custom_components/custom_Ellipsoid.md` | 创建参数化椭球体 | 使用椭球体时必须加载 |
custom_CircularTorus| `04_custom_components/custom_CircularTorus.md` | 创建圆形截面圆环 | 使用圆形截面圆环时必须加载 |
custom_SquareTorus| `04_custom_components/custom_SquareTorus.md` | 创建方形截面圆环 | 使用方形截面圆环时必须加载 |