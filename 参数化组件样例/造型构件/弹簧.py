from pyp3d import *
# 扫掠体

class 弹簧(Component):
    def __init__(self):
        Component.__init__(self)
        self['弹簧'] = Attr(None, show=True)
        self['弹簧高度'] = Attr(100, obvious = True)
        self['步长'] = Attr(0.1, obvious=True,)
        self['弹簧螺旋半径'] = Attr(20, obvious=True,)
        self['弹簧半径'] = Attr(2, obvious=True, )
        self['弹簧间距'] = Attr(10, obvious = True)
        self.replace()
    @export
    def replace(self):
        r = self['弹簧半径']
        # 弹簧转过的总角度值（弧度制）
        t = self['弹簧高度'] *2*pi/ self['弹簧间距']
        R = self['弹簧螺旋半径']
        steplength = self['步长']
        space = self['弹簧间距']
        # 绘制弹簧截面
        section = rotate(Vec3(1,0,0), 0.5*pi) * (scale(r,r) * Section(Arc()))
        # 平移到旋转起点
        section = translate(Vec3(R,0,0)) * section 
        # 相邻截面的高度差（每步长截面上升的高度/单位步长截面上升的高度值）
        space_i = space/(2*pi)

        # 旋转截面、螺旋上升
        SectionArray = []
        # 使用linspace，得到总截面数
        for i in linspace(0, t, int(t//steplength)):
        # 旋转、平移截面到指定位置（即i对应的位置上）       
            SectionArray.append(translate(Vec3(0,0,space_i*i)) * (rotate(Vec3(0,0,1), i) * section))
        # 形成Loft几何体
        Test_Loft = Loft(*SectionArray)
        # 设置为光滑
        Test_Loft.smooth = True

        self['弹簧'] = Test_Loft

if __name__ == "__main__":
    place(弹簧())

