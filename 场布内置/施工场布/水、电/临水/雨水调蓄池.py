from pyp3d import *


class Tank(Component):
    def __init__(self):
        Component.__init__(self)
        self['场布类型'] = Attr('临水', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('其他', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('雨水调蓄池', obvious=True, group='构件分类')
        self['长度'] = Attr(4000.0, obvious=True, group='尺寸')
        self['宽度'] = Attr(2500.0, obvious=True, group='尺寸')
        self['高度'] = Attr(1500.0, obvious=True, group='尺寸')
        self['壁厚'] = Attr(200.0, readonly=True, obvious=True, group='尺寸')
        self['TankGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        # Active Parameters
        Length = self['长度']
        Width = self['宽度']
        Height = self['高度']
        WallThick = self['壁厚']
        # Geometry
        # 主体
        BaseBody = scale(Length, Width, Height)*Cube()
        BaseBody_Sub = translate(WallThick, WallThick, WallThick)*\
                       scale(Length - 2*WallThick, Width - 2*WallThick, Height - WallThick)*Cube()
        RealBaseBody = Fusion(BaseBody - BaseBody_Sub).color(0.5, 0.5, 1, 1)
        self['TankGeo'] = RealBaseBody


if __name__ == "__main__":
    Final_Geometry = Tank()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)