from pyp3d import *


class 环形阵列球(Component):
    def __init__(self):
        Component.__init__(self)
        self['半径'] = Attr(500, obvious=True)
        self['模式'] = Attr('按个数', obvious=True, combo=['按个数', '按角度'])
        self['阵列个数'] = Attr(10, obvious=True)
        self['间隔角度'] = Attr(36, obvious=True)
        self['阵列半径'] = Attr(1500, obvious=True)
        self['环形阵列'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        r = self['半径']
        mode = self['模式']
        R = self['阵列半径']

        # 根据模式计算角度步长和个数
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

        # 基础球体
        sphere = scale(r) * Sphere()

        # 环形阵列（圆心=插入点，绕Z轴，第一个球在正上方）
        arr = Array(sphere)
        for i in range(N):
            theta = pi / 2 + i * angle_step
            arr.append(translate(R * cos(theta), R * sin(theta), 0))

        self['环形阵列'] = arr


if __name__ == "__main__":
    FinalGeometry = 环形阵列球()
    place(FinalGeometry)
