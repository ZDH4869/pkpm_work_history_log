from pyp3d import *


class 环形阵列长方体(Component):
    def __init__(self):
        Component.__init__(self)
        self['模式'] = Attr('按个数', obvious=True, combo=['按个数', '按角度'])
        self['X方向长'] = Attr(1000, obvious=True)
        self['Y方向宽'] = Attr(500, obvious=True)
        self['Z方向高'] = Attr(800, obvious=True)
        self['阵列半径'] = Attr(2500, obvious=True)
        self['阵列个数'] = Attr(8, obvious=True)
        self['间隔角度'] = Attr(45, obvious=True)
        self['长方体阵列'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        L = self['X方向长']
        W = self['Y方向宽']
        H = self['Z方向高']
        R = self['阵列半径']

        # 根据模式计算角度步长和个数
        mode = self['模式']
        if mode == '按个数':
            N = int(self['阵列个数'])
            if N < 1:
                N = 1
            angle_step = 2 * pi / N
        else:
            angle_step = self['间隔角度'] * pi / 180
            if angle_step <= 0:
                angle_step = 2 * pi
            N = int(2 * pi / angle_step)
            if N < 1:
                N = 1

        # 基础长方体（形心居中，X=长度=径向，Y=宽度=切向）
        # Cube() 原点在角点，先平移使形心位于原点
        cuboid = translate(-L/2, -W/2, -H/2) * scale(L, W, H) * Cube()

        # 环形阵列（圆心=插入点，绕Z轴，第一个长方体在正上方）
        # 变换顺序：scale → rotate(θ)使X指向圆心 → translate到圆周位置
        arr = Array(cuboid)
        for i in range(N):
            theta = pi / 2 + i * angle_step
            arr.append(translate(R * cos(theta), R * sin(theta), 0) * rotate(Vec3(0, 0, 1), theta))

        self['长方体阵列'] = arr


if __name__ == "__main__":
    FinalGeometry = 环形阵列长方体()
    place(FinalGeometry)
