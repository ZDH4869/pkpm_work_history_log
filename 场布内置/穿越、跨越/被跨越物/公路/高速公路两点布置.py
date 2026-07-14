from pyp3d import *


class Freeway(Component):
    def __init__(self):
        Component.__init__(self)
        self['应用场景'] = Attr('施工线路三跨', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('被跨越物—公路', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('高速公路（双向）', obvious=True, group='构件分类')
        self['单车道宽'] = Attr(3750.0, obvious=True, group='道路')
        self['总车道数'] = Attr(4, obvious=True, group='道路')
        self['路面厚度'] = Attr(220.0, obvious=True, group='道路')
        self['紧急停车带宽度'] = Attr(3250.0, obvious=True, group='道路')
        self['分道线长度'] = Attr(6000.0, readonly=True, obvious=True, group='道路')
        self['分道线宽度'] = Attr(150.0, readonly=True, obvious=True, group='道路')
        self['分道线间距'] = Attr(9000.0, readonly=True, obvious=True, group='道路')
        self['默认长度'] = Attr(5000.0, obvious=False, group='道路')
        self['分隔带宽度'] = Attr(5000.0, obvious=True, group='中央分隔带')
        self['防撞栏高度'] = Attr(1500.0, readonly=True, obvious=True, group='防撞栏')
        self['立柱间距'] = Attr(4000.0, readonly=True, obvious=True, group='防撞栏')
        self['立柱直径'] = Attr(140.0, readonly=True, obvious=True, group='防撞栏')
        self['FreewayGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        def point_rotate(geometry, center: Vec3, axis: Vec3, angle: float):
            geometry_Temp = translate(Vec3(0, 0, 0) - center)*geometry
            geometry_Temp = rotate(axis, angle)*geometry_Temp
            geometry_New = translate(center)*geometry_Temp
            return geometry_New

        # Active Parameters
        DefaultRoadLength = self['默认长度']
        SingleRoadWidth = self['单车道宽']
        SingleRoadCount = self['总车道数']
        EmergencyRoadWidth = self['紧急停车带宽度']
        DividerWidth = self['分隔带宽度']
        ColumnDiameter = self['立柱直径']
        ColumnHeight = self['防撞栏高度']
        ColumnSpace = self['立柱间距']
        RoadHeight = self['路面厚度']
        LaneWidth = self['分道线宽度']
        LaneHeight = self['分道线长度']
        LaneSpace = self['分道线间距']

        # Limited Parameters
        if int(SingleRoadCount) % 2 != 0:
            SingleRoadCount = int(SingleRoadCount) + 1
            self['总车道数'] = SingleRoadCount

        # Passive Parameters
        DottedLineSingle_SingleCount = int(DefaultRoadLength/(LaneSpace + LaneHeight))
        # 其中500为分隔带两侧的窄空地
        RoadWidth = SingleRoadWidth*SingleRoadCount + EmergencyRoadWidth*2 + 500*2 + DividerWidth + ColumnDiameter*2
        ColumnNumber = int((DefaultRoadLength-ColumnDiameter)/ColumnSpace) + 1

        # Geometry
        # 公路地板
        BaseRoad = translate(0, -RoadWidth/2)*scale(DefaultRoadLength, RoadWidth, RoadHeight)*Cube().\
            color(152/255, 147/255, 145/255, 1)

        # 中间绿植
        # 500为比防护栏高500
        MiddlePlant = translate(0, -DividerWidth/2, RoadHeight)*\
                      scale(DefaultRoadLength, DividerWidth, ColumnHeight + 500)*Cube().\
                      color(151/255, 201/255, 14/255, 1)

        # 上侧内实线
        SolidLineBase = translate(0, -LaneWidth/2, RoadHeight)*\
                          scale(DefaultRoadLength, LaneWidth, 1)*Cube().color(1, 1, 1, 1)
        SolidLineBase_Inside = translate(0, DividerWidth/2 + 500)*SolidLineBase
        # 上侧外实线
        SolidLineBase_Outside = translate(0, DividerWidth/2 + 500 + SingleRoadWidth*SingleRoadCount/2)*SolidLineBase

        # 上侧单虚线
        DottedLineSingle_Single = translate(0, -LaneWidth/2, RoadHeight)*\
                          scale(LaneHeight, LaneWidth, 1)*Cube().color(1, 1, 1, 1)
        DottedLineSingle = Array(DottedLineSingle_Single)
        for point in linspace(Vec3(0, 0, 0), Vec3(DottedLineSingle_SingleCount*(LaneSpace + LaneHeight), 0, 0),
                              DottedLineSingle_SingleCount + 1):
            DottedLineSingle.append(translate(point))
        DottedLineSingle_Sub = translate(DefaultRoadLength, -RoadWidth/2)*\
                               scale(LaneHeight, RoadWidth, RoadHeight*2)*Cube()
        DottedLineSingle = Fusion(DottedLineSingle - DottedLineSingle_Sub).color(1, 1, 1, 1)
        DottedLineSingle_Base = translate(0, DividerWidth/2 + 500 + SingleRoadWidth, 0)*DottedLineSingle

        # 上侧虚线
        DottedLine = Array(DottedLineSingle_Base)
        for point in linspace(Vec3(0, 0, 0), Vec3(0, SingleRoadWidth*(SingleRoadCount//2 - 2), 0),
                              (SingleRoadCount//2 - 1)):
            DottedLine.append(translate(point))

        # 上侧护栏立柱
        Guardrail_Sec = Section(scale(ColumnDiameter/2)*Arc(2*pi))
        Guardrail_Single = Loft(Guardrail_Sec, translate(0, 0, ColumnHeight)*Guardrail_Sec).color(0, 84/255, 31/255, 1)
        Guardrail_Single_Base = translate(ColumnDiameter/2, DividerWidth/2 + ColumnDiameter/2, RoadHeight)*\
                                Guardrail_Single
        Guardrail_Column = Array(Guardrail_Single_Base)
        for point in linspace(Vec3(0, 0, 0), Vec3((ColumnNumber - 1)*ColumnSpace, 0, 0), ColumnNumber):
            Guardrail_Column.append(translate(point))

        # 上侧护栏
        GuardrailUp_Sec1_Single = to_section(Vec3(0, 40, RoadHeight), Vec3(0, 42, RoadHeight),
                                          Vec3(DefaultRoadLength, 42, RoadHeight),
                                          Vec3(DefaultRoadLength, 40, RoadHeight))
        i = 0
        GuardrailUp_Sec1 = []
        while i - 10:
            num = i/4
            if num - int(num) < 0.3:
                if i % 2 == 0:
                    GuardrailUp_Sec1.append(translate(0, 40, 58 + 96*int(i/2) - 8)*GuardrailUp_Sec1_Single)
                else:
                    GuardrailUp_Sec1.append(translate(0, 40, 58 + 96*int(i/2) + 8)*GuardrailUp_Sec1_Single)
            else:
                if i % 2 == 0:
                    GuardrailUp_Sec1.append(translate(0, -40, 58 + 96*int(i/2) - 8)*GuardrailUp_Sec1_Single)
                else:
                    GuardrailUp_Sec1.append(translate(0, -40, 58 + 96*int(i/2) + 8)*GuardrailUp_Sec1_Single)
            i += 1

        GuardrailUp_Sec2 = to_section(Vec3(0, 0, RoadHeight + 2), Vec3(0, 0, RoadHeight),
                                   Vec3(DefaultRoadLength, 0, RoadHeight),
                                   Vec3(DefaultRoadLength, 0, RoadHeight + 2))
        GuardrailUp_Sec3 = to_section(Vec3(0, 8, RoadHeight + 2), Vec3(0, 8, RoadHeight),
                                   Vec3(DefaultRoadLength, 8, RoadHeight),
                                   Vec3(DefaultRoadLength, 8, RoadHeight + 2))
        GuardrailUp_Sec4 = to_section(Vec3(0, 8, RoadHeight + 498), Vec3(0, 8, RoadHeight + 500),
                                   Vec3(DefaultRoadLength, 8, RoadHeight + 500),
                                   Vec3(DefaultRoadLength, 8, RoadHeight + 498))
        GuardrailUp_Sec5 = to_section(Vec3(0, 0, RoadHeight + 498), Vec3(0, 0, RoadHeight + 500),
                                   Vec3(DefaultRoadLength, 0, RoadHeight + 500),
                                   Vec3(DefaultRoadLength, 0, RoadHeight + 498))
        GuardrailUp = Loft(GuardrailUp_Sec2, GuardrailUp_Sec3, *GuardrailUp_Sec1, GuardrailUp_Sec4, GuardrailUp_Sec5).\
                      color(0, 84/255, 31/255, 1)
        GuardrailUp = translate(0, DividerWidth/2 + ColumnDiameter, ColumnHeight - 500)*GuardrailUp
        Guardrail_inside = combine(Guardrail_Column, GuardrailUp)
        Guardrail_Column_outside = translate(0, RoadWidth/2 - (DividerWidth/2 + ColumnDiameter))*Guardrail_Column
        GuardrailUp_outside = point_rotate(GuardrailUp, Vec3(DefaultRoadLength/2,
                                                             (RoadWidth/2 - 2*ColumnDiameter - DividerWidth/2)/2 + DividerWidth/2 +ColumnDiameter,
                                                             0),
                                           Vec3(0, 0, 1), pi)
        # 全模型
        AllGeometry_List_Up = [BaseRoad, MiddlePlant, SolidLineBase_Inside, SolidLineBase_Outside, DottedLine,
                               Guardrail_Column, Guardrail_inside, Guardrail_Column_outside, GuardrailUp_outside]
        AllGeometry_Up = combine(*AllGeometry_List_Up)
        AllGeometry_Down = point_rotate(AllGeometry_List_Up, Vec3(DefaultRoadLength/2, 0, 0),
                                             Vec3(0, 0, 1), pi)
        self['FreewayGeo'] = combine(AllGeometry_Up, AllGeometry_Down)


if __name__ == "__main__":
    Final_Geometry = Freeway()
    TwoPointPlace.linearize(Final_Geometry, '默认长度')
    place(Final_Geometry)
