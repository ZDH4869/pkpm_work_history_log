from pyp3d import *


class 四棱锥三角形截面(Component):
    def __init__(self):
        Component.__init__(self)
        self['底边(X)'] = Attr(1000, obvious=True, description='三角形底边长度，也作为正方形内接圆半径')
        self['高度(Y)'] = Attr(800, obvious=True, description='三角形高度，也作为棱锥沿轴高度')
        self['旋转轴'] = Attr('Z', obvious=True, combo=['X', 'Y', 'Z'], description='棱锥顶点延伸方向（右手法则）')
        self['四棱锥'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        base_leg = self['底边(X)']  # 三角形底边 = 正方形内接圆半径
        height_val = self['高度(Y)']  # 三角形高 = 棱锥高度
        axis = self['旋转轴']
        half = base_leg  # 正方形半边长

        # 用 Loft 放样创建四棱锥
        # 三角形截面在 XOY 平面（直角在原点=插入点，底边沿X，高沿Y）
        # 底边长度 = 正方形内接圆半径，高度值 = 棱锥沿轴高度
        n_sec = 4  # 截面数量（越多越平滑）
        sections = []
        for i in range(n_sec):
            t = i / (n_sec - 1)  # 0 → 1
            sz = half * (1.0 - t) + 0.001  # 从半边长缩小到趋于0
            sq = Section(Vec2(-sz, -sz), Vec2(sz, -sz), Vec2(sz, sz), Vec2(-sz, sz))

            if axis == 'Z':
                # 底面在XOY平面，顶点沿Z轴上升
                sections.append(translate(0, 0, t * height_val) * sq)
            elif axis == 'X':
                # 底面在YOZ平面，顶点沿X轴延伸
                sections.append(translate(t * height_val, 0, 0) * rotate(Vec3(0, 1, 0), pi / 2) * sq)
            else:  # 'Y'
                # 底面在XOZ平面，顶点沿Y轴延伸
                sections.append(translate(0, t * height_val, 0) * rotate(Vec3(1, 0, 0), pi / 2) * sq)

        pyramid = Loft(*sections)
        self['四棱锥'] = pyramid


if __name__ == "__main__":
    FinalGeometry = 四棱锥三角形截面()
    place(FinalGeometry)
