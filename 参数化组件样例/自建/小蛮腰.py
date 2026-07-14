from pyp3d import *

# 小蛮腰（广州塔）参数化外壳模型
# 特征：椭圆截面 + 中间收腰 + 逐层扭转

class 小蛮腰(Component):
    def __init__(self):
        Component.__init__(self)
        self['底部长轴'] = Attr(350.0, obvious=True)
        self['底部短轴'] = Attr(230.0, obvious=True)
        self['顶部长轴'] = Attr(280.0, obvious=True)
        self['顶部短轴'] = Attr(180.0, obvious=True)
        self['腰部收缩'] = Attr(0.70, obvious=True)
        self['总高'] = Attr(2000.0, obvious=True)
        self['截面数'] = Attr(15, obvious=True)
        self['每层扭转角'] = Attr(15.0, obvious=True)
        self['塔身'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        BaseX = self['底部长轴']
        BaseY = self['底部短轴']
        TopX = self['顶部长轴']
        TopY = self['顶部短轴']
        Shrink = self['腰部收缩']
        H = self['总高']
        N = int(self['截面数'])
        TwistDeg = self['每层扭转角']

        # 基准椭圆截面（单位圆，后续通过 scale 拉伸为椭圆）
        base_section = Section(Arc(2 * pi))

        sections = []
        for i in range(N):
            t = i / (N - 1)          # 0 → 1，归一化高度位置
            z = t * H                 # Z 向高度

            # 抛物线收腰：t=0.5 处收缩最大
            mid = 1.0 - 4.0 * (t - 0.5) ** 2  # t=0.5 时 mid=1，t=0/1 时 mid=0

            # 椭圆尺寸：线性插值 + 腰部收缩
            scaleX = (BaseX + (TopX - BaseX) * t) * (1.0 - Shrink * mid)
            scaleY = (BaseY + (TopY - BaseY) * t) * (1.0 - Shrink * mid)

            # 本节扭转角度（弧度）
            angle_rad = i * TwistDeg * pi / 180.0

            # 截面：缩放为椭圆 → 平移到高度 → 绕 Z 轴旋转
            section = rotz(angle_rad) * translate(0, 0, z) * scale(scaleX, scaleY) * base_section
            sections.append(section)

        # 放样生成外壳
        self['塔身'] = Loft(*sections)


if __name__ == "__main__":
    FinalGeometry = 小蛮腰()
    place(FinalGeometry)
