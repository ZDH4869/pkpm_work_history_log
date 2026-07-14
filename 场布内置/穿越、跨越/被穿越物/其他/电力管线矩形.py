from pyp3d import *


class PowerLineRectangle(Component):
    def __init__(self):
        Component.__init__(self)
        self['应用场景'] = Attr('隧道穿越', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('被穿越物', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('电力管线（矩形）', obvious=True, group='构件分类')
        self['长'] = Attr(1000.0, obvious=True, group='截面尺寸')
        self['宽'] = Attr(800.0, obvious=True, group='截面尺寸')
        self['壁厚'] = Attr(10.0, obvious=True, group='截面尺寸')
        self['大小'] = Attr(150.0, obvious=True, group='字体')
        self['默认长度'] = Attr(150.0, obvious=False, group='截面尺寸')
        self['PowerLineRectangleGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        # Active Parameters
        Length = self['长']
        Width = self['宽']
        WallThick = self['壁厚']
        Size = self['大小']/2
        DefaultLength = self['默认长度']

        # Geometry
        # 管线
        BaseBody = scale(DefaultLength, Length, Width)*Cube()
        BaseBody_Sub = translate(0, WallThick, WallThick)*\
                       scale(DefaultLength, Length - 2*WallThick, Width - 2*WallThick)*Cube()
        RealBaseBody = translate(0, -Length/2, -Width/2)\
                       *Fusion(BaseBody - BaseBody_Sub).color(0.3, 0.3, 0.3, 1)
        # 文字
        SingleText = translate(100, -Size/2, Width/2 + 1)*Text('电力管线', Size, Size).color(0.01,0.01,0.01,1)
        SizeLength = len('电力管线')
        Count = int((DefaultLength - 200)/(SizeLength*(Size + 100/150*Size) + 2000))
        if DefaultLength - 200 - Count*(SizeLength*(Size + 100/150*Size) + 2000) > SizeLength*(Size + 100/150*Size):
            Count += 1
        AllText = Array(SingleText)
        for point in linspace(Vec3(0, 0, 0), Vec3((Count - 1)*(SizeLength*(Size + 100/150*Size) + 2000), 0, 0), Count):
            AllText.append(translate(point))
        self['PowerLineRectangleGeo'] = combine(RealBaseBody, AllText)


if __name__ == "__main__":
    Final_Geometry = PowerLineRectangle()
    TwoPointPlace.linearize(Final_Geometry, '默认长度')
    place(Final_Geometry)
