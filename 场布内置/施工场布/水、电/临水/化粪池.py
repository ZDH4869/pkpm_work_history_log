from pyp3d import *


class SepticTank(Component):
    def __init__(self):
        Component.__init__(self)
        self['场布类型'] = Attr('临水', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('其他', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('化粪池', obvious=True, group='构件分类')
        self['长度'] = Attr(2700.0, obvious=True, group='尺寸')
        self['宽度'] = Attr(1500.0, obvious=True, group='尺寸')
        self['高度'] = Attr(1500.0, obvious=True, group='尺寸')
        self['三格比例'] = Attr('2:1:3', readonly=True, obvious=True, group='其他')
        self['盖板厚'] = Attr(100.0, readonly=True, obvious=True, group='其他')
        self['化粪池顶盖透明度'] = Attr(0.5, obvious=True, group='其他')
        self['壁厚'] = Attr(240.0, readonly=True, obvious=True, group='其他')
        self['SepticTankGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        # Active Parameters
        Length = self['长度']
        Width = self['宽度']
        Height = self['高度']
        WallThick = self['壁厚']
        BoardThick = self['盖板厚']
        t = self['化粪池顶盖透明度']
        # Limited Parameters
        if Height < 700:
            self['高度'] = Height = 700.0
        if Length < 1500:
            self['长度'] = Length = 1500.0
        # Passive Parameters
        # 1格长度
        OneLength = (Length - 3*WallThick)/6
        # Geometry
        # 主体
        BaseBody = scale(Length, Width, Height)*Cube()
        BaseBody_Sub = translate(WallThick, WallThick, BoardThick)*\
                       scale(Length - 2*WallThick, Width - 2*WallThick, Height - BoardThick)*Cube()
        RealBaseBody = Fusion(BaseBody - BaseBody_Sub).color(200/255, 201/255, 206/255, 1)
        # 内墙
        LeftIndoorWall = translate(WallThick + 2*OneLength, 0)*scale(WallThick/2, Width, Height)*Cube()
        RealBaseBody = Fusion(RealBaseBody + LeftIndoorWall).color(200/255, 201/255, 206/255, 1)
        RightIndoorWall = translate(1.5*WallThick + 3*OneLength, 0)*scale(WallThick/2, Width, Height)*Cube()
        RealBaseBody = Fusion(RealBaseBody + RightIndoorWall).color(200/255, 201/255, 206/255, 1)
        # 盖板
        Board = translate(0, 0, Height)*scale(Length, Width, BoardThick)*Cube().color(200/255, 201/255, 206/255, t)
        # 水管
        PipeBaseSection0 = Section(scale(50)*Arc(pi*2))
        PipeBaseSection90 = rotate(Vec3(0, 1, 0), pi/2)*Section(scale(50)*Arc(pi*2))
        WaterPipe_left1 = translate(0, Width - 350, Height-100)\
                         *Loft(translate(-130, 0)*PipeBaseSection90, translate(420, 0)*PipeBaseSection90)
        WaterPipe_left2 = translate(0, Width - 350, Height-100)\
                         *Loft(translate(370, 0)*PipeBaseSection0, translate(370, 0, -400)*PipeBaseSection0)
        WaterPipe_left = Fusion(WaterPipe_left1 + WaterPipe_left2)
        WaterPipe_Middle1 = translate(WallThick + 2*OneLength, 350, Height-410)*rotate(Vec3(0, 1, 0), -60/180*pi)\
                         *Loft(translate(-150, 0)*PipeBaseSection90, translate(370, 0)*PipeBaseSection90)
        WaterPipe_Middle2 = translate(1.5*WallThick + 3*OneLength, Width - 350, Height-410)*\
                            rotate(Vec3(0, 1, 0), -60/180*pi)\
                         *Loft(translate(-150, 0)*PipeBaseSection90, translate(370, 0)*PipeBaseSection90)
        WaterPipe_Right1 = translate(Length - 240, 350, Height-100)\
                         *Loft(translate(-130, 0)*PipeBaseSection90, translate(420, 0)*PipeBaseSection90)
        WaterPipe_Right2 = translate(Length - 240, 350, Height-100) \
                           * Loft(translate(370, 0) * PipeBaseSection0, translate(370, 0, -400) * PipeBaseSection0)
        WaterPipe_Right = Fusion(WaterPipe_Right1 + WaterPipe_Right2)
        WaterPipe = combine(WaterPipe_left, WaterPipe_Middle1, WaterPipe_Middle2, WaterPipe_Right).color(0.3, 0.3, 1, 1)
        self['SepticTankGeo'] = combine(RealBaseBody, Board, WaterPipe)


if __name__ == "__main__":
    Final_Geometry = SepticTank()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)