from pyp3d import *


class JYGFWXT(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件类型'] = Attr('被保护系统-封网保护', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('绝缘杆封网系统', readonly=True, obvious=True, group='构件分类')
        self['承托绳间距'] = Attr(6000.00, obvious=True, group='封网尺寸')
        self['跨数'] = Attr(3, obvious=True, group='封网尺寸')
        self['整体宽度'] = Attr(18000, obvious=True, group='封网尺寸')
        self['整体长度'] = Attr(10000, obvious=True, group='封网尺寸')
        self['绝缘杆直径'] = Attr(4.00, obvious=True, group='封网尺寸')
        self['绝缘杆间距'] = Attr(2000.00, obvious=True, group='封网尺寸')
        self['承托绳伸出长度'] = Attr(2000.00, obvious=True, group='封网尺寸')
        self['封网长度'] = Attr(readonly=True, obvious=True, group='封网尺寸')
        self['绝缘杆封网系统'] = Attr(None, show=True)
        self.replace()

    @export   
    def replace(self):

        def point_rotate(geometry, center: Vec3, axis: Vec3, angle: float):
            geometry_Temp = translate(Vec3(0, 0, 0) - center)*geometry
            geometry_Temp = rotate(axis, angle)*geometry_Temp
            geometry_New = translate(center)*geometry_Temp
            return geometry_New


              
        # Active Parameters
        Space_ChengTuoSheng = self['承托绳间距']
        SpanNum = self['跨数']
        Diameter_JueYuanGan = self['绝缘杆直径']
        Space_JueYuanGan = self['绝缘杆间距']
        Length_ChengTuoSheng = self['承托绳伸出长度']
        Length_Overall = self['整体长度']
        Width_Overall = self['整体宽度']

        # Passive Parameters
        Width_FengWang = SpanNum * Space_ChengTuoSheng
        Space_ChengTuoSheng = (Width_Overall - 400) / SpanNum
        self['封网长度'] = Length_FengWang = Length_Overall - Length_ChengTuoSheng
        Length_ChengTuoSheng = Length_Overall - Length_FengWang
        Count_JueYuanGan = int(Length_FengWang/Space_JueYuanGan)+1
        RealSpace_JueYuanGan = Length_FengWang/int(Length_FengWang / Space_JueYuanGan)
        Width_JueYuanGan = Space_ChengTuoSheng + 400

        # Geometry
        # 单跨
        # 承托绳
        SecChengTuoSheng = rotate(Vec3(0,1,0),0.5*pi) * Section(scale(1) * Arc(2*pi))
        SingleChengTuoSheng = Loft(SecChengTuoSheng, translate(Length_Overall, 0, 0) * SecChengTuoSheng).color(222/255, 222/255, 222/255, 1)
        
        # 绝缘杆
        SecJueYuanGan = rotate(Vec3(1,0,0),0.5*pi) * Section(scale(Diameter_JueYuanGan/2) * Arc(2*pi))
        SingleJueYuanGan = translate(0, 0, Diameter_JueYuanGan/2+1) * Loft(SecJueYuanGan, translate(0, Width_JueYuanGan, 0) * SecJueYuanGan).color(222/255, 222/255, 222/255, 1)
        JueYuanGan = Array(SingleJueYuanGan)
        for point in linspace(Vec3(Length_ChengTuoSheng/2, -200, 0), Vec3(Length_Overall-Length_ChengTuoSheng/2, -200, 0), Count_JueYuanGan):
            JueYuanGan.append(translate(point))

        # 网格
        SecLeftMesh = rotate(-pi/4)*rotate(Vec3(0, 1, 0), pi/2)*Section(scale(2) * Arc(2*pi))
        LeftPoint = []
        RightPoint = []
        i = 0
        Space_Mesh = 600
        while 1:
            i += 1
            if i*Space_Mesh >= Space_ChengTuoSheng + RealSpace_JueYuanGan:
                break
            if i*Space_Mesh <= Space_ChengTuoSheng:
                LeftPoint.append(Vec3(0, i*Space_Mesh, Diameter_JueYuanGan/2+1))
            else:
                LeftPoint.append(Vec3(-Space_ChengTuoSheng + i*Space_Mesh, Space_ChengTuoSheng, 0))

            if i*Space_Mesh <= RealSpace_JueYuanGan:
                RightPoint.append(Vec3(i*Space_Mesh, 0, 0))
            else:
                RightPoint.append(Vec3(RealSpace_JueYuanGan, -RealSpace_JueYuanGan + i*Space_Mesh, Diameter_JueYuanGan/2+1))

        SingleLeftMesh_List = []
        for i in range(0, len(LeftPoint)):
            SingleLeftMesh_temp = Loft(translate(LeftPoint[i])*SecLeftMesh, translate(RightPoint[i])*SecLeftMesh)
            SingleLeftMesh_List.append(SingleLeftMesh_temp)
        SingleLeftMesh = combine(*SingleLeftMesh_List)

        SecRightMesh = rotate(pi/4)*rotate(Vec3(0, 1, 0), pi/2)*Section(scale(2) * Arc(2*pi))
        LeftPoint = []
        RightPoint = []
        i = 0
        while 1:
            i += 1
            if i*Space_Mesh >= Space_ChengTuoSheng + RealSpace_JueYuanGan:
                break
            if i*Space_Mesh <= RealSpace_JueYuanGan:
                LeftPoint.append(Vec3(RealSpace_JueYuanGan - i*Space_Mesh, 0, 0))
            else:
                LeftPoint.append(Vec3(0, i*Space_Mesh - RealSpace_JueYuanGan, Diameter_JueYuanGan/2 + 1))

            if i*Space_Mesh <= Space_ChengTuoSheng:
                RightPoint.append(Vec3(RealSpace_JueYuanGan, i*Space_Mesh, Diameter_JueYuanGan/2 + 1))
            else:
                RightPoint.append(Vec3(Space_ChengTuoSheng + RealSpace_JueYuanGan - i*Space_Mesh, Space_ChengTuoSheng, 0))

        SingleRightMesh_List = []
        for i in range(0, len(LeftPoint)):
            SingleRightMesh_temp = Loft(translate(LeftPoint[i])*SecRightMesh, translate(RightPoint[i])*SecRightMesh)
            SingleRightMesh_List.append(SingleRightMesh_temp)
        SingleRightMesh = combine(*SingleRightMesh_List)
        SingleMesh = combine(SingleLeftMesh, SingleRightMesh)\
            .color(222/255, 222/255, 222/255, 1)
        Mesh = Array(SingleMesh)
        for point in linspace(Vec3(Length_ChengTuoSheng/2, 0, 0),
                              Vec3(Length_Overall-Length_ChengTuoSheng/2 - RealSpace_JueYuanGan, 0, 0),
                              Count_JueYuanGan - 1):
            Mesh.append(translate(point))

        # 多跨排布
        MultiChengTuoSheng = Array(SingleChengTuoSheng)
        for point in linspace(Vec3(0, 0, 0), Vec3(0, SpanNum*Space_ChengTuoSheng, 0), SpanNum + 1):
            MultiChengTuoSheng.append(translate(point))

        MultiJueYuanGan = Array(JueYuanGan)
        MultiMesh = Array(Mesh)

        i = 0
        for point in linspace(Vec3(0, 0, 0), Vec3(0, (SpanNum - 1)*Space_ChengTuoSheng, 0), int(SpanNum)):
            if i % 2 == 0:
                MultiJueYuanGan.append(translate(point))
                MultiMesh.append(translate(point))
            else:
                MultiJueYuanGan.append(translate(point + Vec3(Diameter_JueYuanGan, 0, 0)))
                MultiMesh.append(translate(point + Vec3(Diameter_JueYuanGan, 0, 0)))
            i += 1
        self['绝缘杆封网系统'] = combine(MultiChengTuoSheng, MultiJueYuanGan, MultiMesh)


if __name__ == "__main__":
    Final_Geometry = JYGFWXT()
    TwoPointPlace.linearize(Final_Geometry, '整体长度')
    place(Final_Geometry)