from pyp3d import *


class PowerLineRectangle(Component):
    def __init__(self):
        Component.__init__(self)
        self['应用场景'] = Attr('隧道穿越', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('被穿越物', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('石油管线', obvious=True, group='构件分类')
        self['外径'] = Attr(1000.0, obvious=True, group='管线尺寸')
        self['壁厚'] = Attr(15.0, obvious=True, group='管线尺寸')
        self['大小'] = Attr(150.0, obvious=True, group='字体')
        self['默认长度'] = Attr(150.0, obvious=False, group='管线尺寸')
        self['PowerLineRectangleGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        # Active Parameters
        OutDiameter = self['外径']
        WallThick = self['壁厚']
        Size = self['大小']/2
        DefaultLength = self['默认长度']

        # Geometry
        # 管线
        PipeSecStart = rotate(Vec3(0, 1, 0), pi/2)*Section(scale(OutDiameter/2)*Arc(pi*2))
        PipeSecEnd = translate(DefaultLength, 0)*PipeSecStart
        PipeSecStart_Sub = rotate(Vec3(0, 1, 0), pi/2)*Section(scale(OutDiameter/2 - WallThick)*Arc(pi*2))
        PipeSecEnd_Sub = translate(DefaultLength, 0)*PipeSecStart_Sub
        Pipe = Loft(PipeSecStart, PipeSecEnd)
        Pipe_Sub = Loft(PipeSecStart_Sub, PipeSecEnd_Sub)
        RealPipe = Fusion(Pipe - Pipe_Sub).color(0.3, 0.3, 0.3, 1)

        # 文字
        SingleText = translate(100, -Size/2, OutDiameter/2 + 0.1)*Text('石油管线', Size, Size).color(1, 1, 1, 1)
        SizeLength = len('石油管线')
        Count = int((DefaultLength - 200)/(SizeLength*(Size + 100/150*Size) + 2000))
        if DefaultLength - 200 - Count*(SizeLength*(Size + 100/150*Size) + 2000) > SizeLength*(Size + 100/150*Size):
            Count += 1
        AllText = Array(SingleText)
        for point in linspace(Vec3(0, 0, 0), Vec3((Count - 1)*(SizeLength*(Size + 100/150*Size) + 2000), 0, 0), Count):
            AllText.append(translate(point))
        self['PowerLineRectangleGeo'] = combine(RealPipe, AllText)


if __name__ == "__main__":
    Final_Geometry = PowerLineRectangle()
    TwoPointPlace.linearize(Final_Geometry, '默认长度')
    place(Final_Geometry)
