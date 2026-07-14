from pyp3d import *


class ResidentialBuilding(Component):
    def __init__(self):
        Component.__init__(self)
        self['应用场景'] = Attr('隧道穿越', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('被穿越物', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('居民楼', obvious=True, group='构件分类')
        self['楼体长'] = Attr(6000.0, obvious=True, group='楼体尺寸')
        self['楼体宽'] = Attr(4000.0, obvious=True, group='楼体尺寸')
        self['楼体高'] = Attr(readonly=True, obvious=True, group='楼体尺寸')
        self['单元数'] = Attr(1, obvious=True, group='楼体尺寸')
        self['层高'] = Attr(2500.0, obvious=True, group='楼层尺寸')
        self['层数'] = Attr(12, obvious=True, group='楼层尺寸')
        self['门高'] = Attr(2100.0, obvious=True, group='单元门')
        self['门宽'] = Attr(900.0, obvious=True, group='单元门')
        self['窗户高'] = Attr(1500.0, obvious=True, group='窗户尺寸')
        self['窗户宽'] = Attr(1800.0, obvious=True, group='窗户尺寸')
        self['ResidentialBuildingGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        # Active Parameters
        BuildingLength = self['楼体长']
        BuildingWidth = self['楼体宽']
        StoreyHeight = self['层高']
        StoreyCount = self['层数']
        DoorHeight = self['门高']
        DoorWidth = self['门宽']
        WindowHeight = self['窗户高']
        WindowWidth = self['窗户宽']
        UnitCount = self['单元数']

        # Limited Parameters
        if DoorHeight > StoreyHeight:
            DoorHeight = StoreyHeight
            self['门高'] = DoorHeight
        if DoorWidth > BuildingLength:
            DoorWidth = BuildingLength
            self['门宽'] = DoorWidth
        if WindowHeight > StoreyHeight - 900:
            WindowHeight = StoreyHeight - 900
            self['窗户高'] = WindowHeight
        if WindowWidth > BuildingLength/2 - DoorWidth/2:
            WindowWidth = BuildingLength/2 - DoorWidth/2
            self['窗户宽'] = WindowWidth
        # Passive Parameters
        self['楼体高'] = StoreyHeight*StoreyCount

        # Geometry
        # 首层建筑
        GroundFloorOut = scale(BuildingLength, BuildingWidth, StoreyHeight)*Cube()
        GroundFloorIn = translate(5, 5, 5)*scale(BuildingLength - 10, BuildingWidth - 10, StoreyHeight - 10)*Cube()
        GroundFloorBuilding = Fusion(GroundFloorOut - GroundFloorIn)
        # 首层窗
        GroundFloorWindowLeft = translate((BuildingLength/2 - DoorWidth/2)/2 - WindowWidth/2, 0, 900)\
                            *scale(WindowWidth, 20, WindowHeight)*Cube()
        GroundFloorWindowLeftSub = translate((BuildingLength/2 - DoorWidth/2)/2 - WindowWidth/2 + 20, 0, 920)\
                            *scale(WindowWidth - 40, 20, WindowHeight - 40)*Cube().color(148/255, 195/255, 230/255, 0.5)
        GroundFloorBuilding = Fusion(GroundFloorBuilding - GroundFloorWindowLeft).color(176/255, 178/255, 165/255, 1)
        GroundFloorWindowLeft = Fusion(GroundFloorWindowLeft - GroundFloorWindowLeftSub).color(0, 0, 0, 1)
        GroundFloorWindowRight = translate((3*BuildingLength/2 + DoorWidth/2)/2 - WindowWidth/2, 0, 900)\
                            *scale(WindowWidth, 20, WindowHeight)*Cube()
        GroundFloorBuilding = Fusion(GroundFloorBuilding - GroundFloorWindowRight).color(176/255, 178/255, 165/255, 1)
        GroundFloorWindowRightSub = translate((3*BuildingLength/2 + DoorWidth/2)/2 - WindowWidth/2 + 20, 0, 920)\
                            *scale(WindowWidth - 40, 20, WindowHeight - 40)*Cube().color(148/255, 195/255, 230/255, 0.5)
        GroundFloorWindowRight = Fusion(GroundFloorWindowRight - GroundFloorWindowRightSub).color(0, 0, 0, 1)
        # 高层
        BaseSingle_Geometry_List = [GroundFloorBuilding, GroundFloorWindowLeft, GroundFloorWindowLeftSub,
                                    GroundFloorWindowRight, GroundFloorWindowRightSub]
        BaseSingle_Geometry = combine(*BaseSingle_Geometry_List)
        Base_Building = Array(BaseSingle_Geometry)
        for point in linspace(Vec3(0, 0, 0), Vec3(0, 0, (StoreyCount - 1)*StoreyHeight), StoreyCount):
            Base_Building.append(translate(point))

        # 首层门
        GroundFloorDoor = translate(BuildingLength/2 - DoorWidth/2, -5)*scale(DoorWidth, 20, DoorHeight)*Cube()
        GroundFloorDoorSub = translate(BuildingLength/2 - DoorWidth/2 + 50, -5)*\
                             scale(DoorWidth - 100, 20, DoorHeight - 50)*Cube()
        GroundFloorDoor = Fusion(GroundFloorDoor - GroundFloorDoorSub).color(0, 0, 0, 1)
        Single_Geo = combine(Base_Building, GroundFloorDoor, GroundFloorDoorSub)
        All_Geometry = Array(Single_Geo)
        for point in linspace(Vec3(0, 0, 0), Vec3(BuildingLength*(UnitCount - 1), 0, 0), UnitCount):
            All_Geometry.append(translate(point))
        # 多单元
        self['ResidentialBuildingGeo'] = All_Geometry


if __name__ == "__main__":
    Final_Geometry = ResidentialBuilding()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)