from pyp3d import *


class GateRoom(Component):

    def __init__(self):
        Component.__init__(self)
        self['场布类型'] = Attr("智慧工地", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("闸机房", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("闸机房", obvious=True, group="构件分类")
        self['通道宽'] = Attr(800.0, obvious=True, group="闸机")
        self['通道数量'] = Attr(3, obvious=True, group="闸机")
        self['闸机高'] = Attr(800.0, obvious=True, group="闸机")
        self['闸机宽'] = Attr(200.0, obvious=True, readonly=True, group="闸机")
        self['闸机长'] = Attr(2000.0, obvious=True, readonly=True, group="闸机")
        self['围栏宽度'] = Attr(1000.0, obvious=True, group="闸机")
        self['围栏高度'] = Attr(obvious=True, readonly=True, group="闸机")
        self['进深'] = Attr(3600.0, obvious=True, group="通道房间")
        self['开间'] = Attr(obvious=True, readonly=True, group="通道房间")
        self['高度'] = Attr(3200.0, obvious=True, group="通道房间")
        self['闸机房'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        # active parameters
        W_Aisle = self['通道宽']
        N_Aisle = self['通道数量']
        H_Gate = self['闸机高']
        W_Gate = self['闸机宽']
        L_Gate = self['闸机长']
        W_Fence = self['围栏宽度']
        self['围栏高度'] = self['闸机高']
        W_Room = self['进深']
        H_Room = self['高度']
        # passive parameters
        L_Room = W_Fence + W_Aisle*N_Aisle + W_Gate*(N_Aisle+1) + 200  # 100为单面墙厚, 100为缝隙
        self['开间'] = L_Room
        # limited parameters
        if W_Room < 2000.0:
            W_Room = 2000.0
            self['进深'] = W_Room
        if H_Room < 2600.0:
            H_Room = 2600.0
            self['高度'] = 2600.0
        if H_Gate > H_Room - 500:
            H_Gate = H_Room - 500
            self['闸机高'] = H_Gate
        # Geometry
        def point_rotate(geometry, center: Vec3, axis: Vec3, angle: float):
            geometry_Temp = translate(Vec3(0, 0, 0) - center)*geometry
            geometry_Temp = rotate(axis, angle)*geometry_Temp
            geometry_New = translate(center)*geometry_Temp
            return geometry_New

        # 定义闸机
        def Gates(AisleWidth: float, AisleNumber: float, GateHeight: float, GateWidth: float, GateLength: float):
            # 单个闸机
            SingleGate1 = translate(0, -GateLength/2, 1/20*GateHeight)\
                          *scale(-GateWidth, GateLength, 17/20*GateHeight)*Cube().color(231/255, 222/255, 203/255, 1)
            SingleGate2_Section1 = to_section(Vec3(-GateWidth, -GateLength/2, 9/10*GateHeight),
                                           Vec3(-GateWidth, GateLength/2, 9/10*GateHeight),
                                           Vec3(0, GateLength/2, 9/10*GateHeight),
                                           Vec3(0, -GateLength/2, 9/10*GateHeight))
            SingleGate2_Section2 = scale(9/10, 9/10)*SingleGate2_Section1
            SingleGate2 = Loft(SingleGate2_Section1, translate(-GateWidth/20, 0, 1/10*GateHeight)*SingleGate2_Section2)\
                .color(231/255, 222/255, 203/255, 1)
            SingleGate3 = translate(-10, -GateLength/2+10, 0)\
                          *scale(-GateWidth+20, GateLength-20, 1/20*GateHeight)*Cube().color(0, 0, 0, 1)
            SingleGate4 = translate(-50/2, -GateLength/2 + 200, GateHeight)*\
                          scale(-(GateWidth - 50), 80, 20)*Cube().color(227/255, 174/255, 79/255, 1)
            SingleGate5 = point_rotate(SingleGate4, Vec3(-GateWidth/2, 0, 0), Vec3(0, 0, 1), pi)
            SingleGate6 = translate(-70/2, -10, GateHeight)*\
                          scale(-(GateWidth - 70), 20, 10)*Cube().color(227/255, 174/255, 79/255, 1)
            SingleGate_List = [SingleGate1, SingleGate2, SingleGate3, SingleGate4, SingleGate5, SingleGate6]
            SingleGate = combine(*SingleGate_List)

            # 单个通道
            SingleAisle_R = (AisleWidth/2 - 20)*2
            Section_List = []
            # SingleAisle_SectionPoints = [Vec3(-GateWidth, 10, 200), Vec3(-GateWidth, -10, 200)]
            for theta in linspace(pi/2, 4/6*pi, 10):
                SingleAisle_SectionTemp = [Vec3(-GateWidth, 10, 100), Vec3(-GateWidth, -10, 100)]
                X_Temp = SingleAisle_R*cos(theta) - GateWidth
                Z_Temp = SingleAisle_R*sin(theta)
                for i in [-10, 10]:
                    SingleAisle_SectionTemp.append(Vec3(X_Temp, i, GateHeight - 150 - SingleAisle_R + Z_Temp))
                Section_Temp = to_section(*SingleAisle_SectionTemp)
                Section_List.append(Section_Temp)
            SingleAisle1 = Loft(*Section_List).color(0, 0.5, 1, 0.1)
            SingleAisle2 = point_rotate(SingleAisle1, Vec3(-GateWidth - AisleWidth/2, 0, 0), Vec3(0, 0, 1), pi)
            SingleAisle = combine(SingleAisle1, SingleAisle2)

            # 人脸识别
            FaceIdentify1 = translate(-60, -7.5, -80 + GateHeight + 200)*\
                            scale(120, 15, 160)*Cube().color(231/255, 222/255, 203/255, 1)
            FaceIdentify2_Sec = Section(scale(7)*Arc(2*pi))
            FaceIdentify2 = translate(0, 0, GateHeight)*\
                            Loft(FaceIdentify2_Sec, translate(0, 0, 200)*FaceIdentify2_Sec)\
                                .color(231/255, 222/255, 203/255, 1)
            FaceIdentify1 = point_rotate(FaceIdentify1, Vec3(0, 0, GateHeight + 200), Vec3(1, 0, 0), pi/15)
            FaceIdentify1 = point_rotate(FaceIdentify1, Vec3(0, 0, GateHeight + 200), Vec3(0, 0, 1), pi/9)
            FaceIdentify = Fusion(FaceIdentify1 + FaceIdentify2).color(231/255, 222/255, 203/255, 1)

            FaceIdentify3_1 = translate(-60, 7.5, -80 + GateHeight + 200)*\
                            scale(120, 0.1, 160)*Cube().color(0, 0, 0, 1)
            FaceIdentify3_2 = translate(-55, 7.6, -70 + GateHeight + 200)*\
                            scale(110, 0.1, 140)*Cube().color(55/255, 77/255, 156/255, 1)
            FaceIdentify3 = combine(FaceIdentify3_1, FaceIdentify3_2)
            FaceIdentify3 = point_rotate(FaceIdentify3, Vec3(0, 0, GateHeight + 200), Vec3(1, 0, 0), pi/15)
            FaceIdentify3 = point_rotate(FaceIdentify3, Vec3(0, 0, GateHeight + 200), Vec3(0, 0, 1), pi/9)
            FaceIdentify = combine(FaceIdentify, FaceIdentify3)
            FaceIdentify = translate(-GateWidth/2, GateLength/2-400, 0)*FaceIdentify
            Gate_Part2 = combine(SingleAisle, FaceIdentify)
            Gates_Part1_List = []
            for x_trans in linspace(0, -AisleNumber*(AisleWidth + GateWidth), AisleNumber + 1):
                Gates_Part1_List.append(translate(x_trans, 0, 0)*SingleGate)
            Gates_Part1 = combine(*Gates_Part1_List)

            Gates_Part2_List = []
            for x_trans in linspace(0, -(AisleNumber - 1)*(AisleWidth + GateWidth), AisleNumber):
                Gates_Part2_List.append(translate(x_trans, 0, 0)*Gate_Part2)
            Gates_Part2 = combine(*Gates_Part2_List)

            Gates_List = [Gates_Part1, Gates_Part2]
            GatesGeometry = combine(*Gates_List)
            return GatesGeometry

        # 定义通道房间
        def RoomOfAisle(RoomWidth: float, RoomHeight: float, RoomLength: float, GateHeight: float, FenceWidth: float):
            floor = scale(-RoomLength, RoomWidth, 100)*Cube()
            wall = translate(-RoomLength, 0, 100)*scale(100, RoomWidth, RoomHeight - 200)*Cube()
            roof = translate(0, 0, RoomHeight - 100)*floor
            RollerBlind1 = translate(0, -5, RoomHeight)*scale(-RoomLength, 300, 300)*Cube().color(1, 1, 1, 1)
            RollerBlind2_single = translate(0, 0, RoomHeight)*scale(-RoomLength + 100, -5, -100)\
                                  *Cube().color(1, 1, 1, 1)
            RollerBlind2 = []
            for z in linspace(0, -500, 6):
                RollerBlind2.append(translate(0, 0, z)*RollerBlind2_single)
            RollerBlind = combine(RollerBlind1, *RollerBlind2)
            room = Fusion(wall + floor)
            room = Fusion(room + roof).color(156/255, 150/255, 132/255, 1)
            tv1 = translate(-RoomLength + 100, RoomWidth/2 - 800, 1500)*scale(40, 1600, 1000)*Cube().color(0, 0, 0, 1)
            tv2 = translate(-RoomLength + 140, RoomWidth/2 - 780, 1550)*scale(0.1, 1560, 900)*\
                  Cube().color(55/255, 77/255, 156/255, 1)
            room = combine(room, tv1, tv2)
            fence1_sec = Section(scale(10)*Arc(2*pi))
            fence1_sec2 = translate(0, 0, GateHeight - 50)*fence1_sec
            fence1_sec3_list = []
            for theta in linspace(0, -pi/2, 10):
                fence1_sec3_list.append(point_rotate(fence1_sec2, Vec3(-50, 0, GateHeight - 50), Vec3(0, 1, 0), theta))
            fence1_sec4 = translate(-FenceWidth + 100, 0)*fence1_sec3_list[-1]
            fence1_sec5_list = []
            for theta in linspace(0, -pi/2, 10):
                fence1_sec5_list.append(point_rotate(fence1_sec4, Vec3(-FenceWidth + 50, 0, GateHeight - 50),
                                                     Vec3(0, 1, 0), theta))
            fence1_sec6 = translate(0, 0, 50 - GateHeight)*fence1_sec5_list[-1]

            fence1 = Loft(fence1_sec, fence1_sec2, *fence1_sec3_list, fence1_sec4, *fence1_sec5_list, fence1_sec6)\
                .color(193/255, 184/255, 180/255, 1)
            fence2_single_sec = translate(-100, 0)*Section(scale(10)*Arc(2*pi))
            fence2_single = Loft(translate(0, 0, 100)*fence2_single_sec,
                                 translate(0, 0, GateHeight)*fence2_single_sec) \
                                .color(193/255, 184/255, 180/255, 1)
            fence2_list = []
            for i in linspace(0, -FenceWidth + 200, abs(int((-FenceWidth + 200)/100))):
                fence2_list.append(translate(i, 0)*fence2_single)
            fence2 = combine(*fence2_list)
            fence3_sec = translate(0, 0, 100)*rotate(Vec3(0, 1, 0), pi/2)*fence1_sec
            fence3 = Loft(fence3_sec, translate(-FenceWidth, 0, 0)*fence3_sec).color(193/255, 184/255, 180/255, 1)
            fence = combine(fence1, fence2, fence3)
            fence = translate(-25, RoomWidth/2, 100)*fence
            room = combine(room, fence, RollerBlind)
            return room

        # 门卫室
        def RoomOfGuard(RoomWidth: float, RoomHeight: float, RoomLength: float):
            floor = scale(-RoomLength, RoomWidth, 100)*Cube().color(156/255, 150/255, 132/255, 1)
            roof = translate(0, 0, RoomHeight - 100)*floor
            column1 = translate(0, 0, 100)*scale(-200, 200, RoomHeight - 200)*Cube().color(156/255, 150/255, 132/255, 1)
            column2 = translate(0, RoomWidth - 200)*column1
            wall = translate(-50, 200, 100)*scale(-50, RoomWidth - 400, RoomHeight - 200)*\
                   Cube().color(253/255, 253/255, 240/255, 1)
            wall_part2 = translate(-RoomLength + 50, RoomWidth/2, 100)*\
                         scale(-50, RoomWidth/2 - 100, RoomHeight - 200)*\
                   Cube().color(253/255, 253/255, 240/255, 1)
            door = translate(-RoomLength + 30, 100, 100)*scale(-10, RoomWidth/2 - 100, RoomHeight - 200)*\
                   Cube().color(0, 0.5, 1, 0.1)
            WallWithWindow1 = translate(-200, 50, 100)*scale(-RoomLength + 200, 50, RoomHeight - 200)*\
                   Cube().color(253/255, 253/255, 240/255, 1)
            WallWithWindow2 = translate(-500, 50, 1500)*scale(-1600, 50, 1000)*\
                   Cube().color(0, 0, 0, 1)
            WallWithWindow3 = translate(-520, 50, 1520)*scale(-1560, 50, 960)*\
                   Cube().color(0, 0, 0, 1)
            WallWithWindow1 = Fusion(WallWithWindow1 - WallWithWindow2).color(253/255, 253/255, 240/255, 1)
            WallWithWindow2 = Fusion(WallWithWindow2 - WallWithWindow3).color(0, 0, 0, 1)
            WallWithWindow3 = translate(-1290, 50, 1520)*scale(-20, 50, 660)*\
                   Cube().color(0, 0, 0, 1)
            WallWithWindow4 = translate(-520, 50, 2180)*scale(-1560, 50, 20)*\
                   Cube().color(0, 0, 0, 1)
            WallWithWindow5 = translate(-520, 60, 1520)*scale(-770, 30, 660)*\
                   Cube().color(0, 0.5, 1, 0.1)
            WallWithWindow6 = translate(-790, 0, 0)*WallWithWindow5
            WallWithWindow7 = translate(-520, 60, 2180)*scale(-1560, 30, 300)*\
                   Cube().color(0, 0.5, 1, 0.1)
            WallWithWindow_list = [WallWithWindow1, WallWithWindow2, WallWithWindow3, WallWithWindow4, WallWithWindow5,
                                   WallWithWindow6, WallWithWindow7]
            WallWithWindow = combine(*WallWithWindow_list)
            WallWithWindow_part2 = translate(0, RoomWidth - 150)*WallWithWindow
            room = combine(floor, roof, column1, column2, wall, WallWithWindow, WallWithWindow_part2, wall_part2, door)
            return room
        L_GuardRoom = 3000
        W_GuardRoom = W_Room
        H_GuardRoom = H_Room
        All_Gates = Gates(W_Aisle, N_Aisle, H_Gate, W_Gate, L_Gate)
        All_Gates = translate(-W_Fence - 50, W_Room/2, 100)*All_Gates
        All_Gates = translate(-L_GuardRoom, 0)*All_Gates
        RoomA = RoomOfAisle(W_Room, H_Room, L_Room, H_Gate, W_Fence)
        RoomA = translate(-L_GuardRoom, 0)*RoomA
        RoomG = RoomOfGuard(W_GuardRoom, H_GuardRoom, L_GuardRoom)
        All_Geometry = [All_Gates, RoomA, RoomG]
        self['闸机房'] = combine(*All_Geometry)


if __name__ == "__main__":
    Final_Geometry = GateRoom()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)