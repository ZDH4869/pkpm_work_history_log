from pyp3d import *
import math

class 天圆地方(Component):
    def __init__(self):
        Component.__init__(self)
        self['圆直径'] = Attr(1000.0, obvious=True)
        self['矩形长'] = Attr(3000.0, obvious=True)
        self['矩形宽'] = Attr(1000.0, obvious=True)
        self['高度'] = Attr(2000.0, obvious=True)
        self['X偏心(xoy面)'] = Attr(0.0, obvious=True)
        self['Y偏心(xoy面)'] = Attr(0.0, obvious=True)
        self['截面位置'] = Attr('xoy面', obvious=True, combo=['xoy面', 'yoz面', 'xoz面'])
        self['天圆地方'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        D = self['圆直径']
        L = self['矩形长']
        W = self['矩形宽']
        H = self['高度']
        X偏 = self['X偏心']
        Y偏 = self['Y偏心']
        R = D / 2.0

        # 步骤1：圆形截面，圆心(X偏心, Y偏心, 高度)，XOY面
        # 将圆拆分为4段不等长弧，弧端点对齐矩形对角线方向，使连线投影与对角线重合
        # α = atan(W/L) 为矩形对角线半角，L=W时α=π/4退化为等分弧（等效rotz(5π/4)）
        α = math.atan2(W, L)
        circle_sec = translate(X偏, Y偏, H) * Section(
            rotz(math.pi + α) * scale(R) * Arc(math.pi - 2*α),      # 弧1: π+α→2π-α 对应左下
            rotz(2*math.pi - α) * scale(R) * Arc(2*α),              # 弧2: 2π-α→α 对应右下
            rotz(α) * scale(R) * Arc(math.pi - 2*α),                # 弧3: α→π-α 对应右上
            rotz(math.pi - α) * scale(R) * Arc(2*α),                # 弧4: π-α→π+α 对应左上
        )

        # 步骤2：矩形截面，形心(0,0,0)，XOY面，长3000(X方向)，宽1000(Y方向)
        # translate(-L/2, -W/2, 0) 将角点对齐的Section平移至形心在原点
        rect_sec = translate(-L/2, -W/2, 0) * Section(
            Vec2(0, 0), Vec2(L, 0), Vec2(L, W), Vec2(0, W)
        )

        # 步骤3：Loft放样，矩形截面为底面，圆形截面为顶面
        result = Loft(rect_sec, circle_sec)

        # 步骤4：根据截面位置旋转整体模型
        # xoy面：默认不旋转；yoz面：绕Y轴旋转-90°；xoz面：绕X轴旋转90°
        截面位置 = self['截面位置']
        if 截面位置 == 'yoz面':
            result = roty(-math.pi / 2.0) * result
        elif 截面位置 == 'xoz面':
            result = rotx(math.pi / 2.0) * result

        self['天圆地方'] = result

if __name__ == "__main__":
    FinalGeometry = 天圆地方()
    place(FinalGeometry)