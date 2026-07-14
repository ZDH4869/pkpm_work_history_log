from pyp3d import *


class ExternalScaffolding(Component):
    def __init__(self):
        Component.__init__(self)
        self['场布类型'] = Attr('措施', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('脚手架', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('外脚手架', obvious=True, group='构件分类')
        self['架体高度'] = Attr(15000.0, obvious=True, group='架体')
        self['架体横距'] = Attr(1200.0, obvious=True, group='架体')
        self['与建筑间距'] = Attr(200.0, obvious=True, group='架体')
        self['走道板宽度'] = Attr(obvious=True, readonly=True, group='走道板')
        self['走道板间隔'] = Attr(3000.0, obvious=True, group='走道板')
        self['走道板底部偏移'] = Attr(300.0, obvious=True, group='走道板')
        self['走道板数量'] = Attr(obvious=True, readonly=True, group='走道板')
        self['警示带宽度'] = Attr(400.0, obvious=True, group='警示带')
        self['警示带间隔'] = Attr(6000.0, obvious=True, group='警示带')
        self['警示带数量'] = Attr(obvious=True, readonly=True, group='警示带')
        self['剪刀撑直径'] = Attr(51.0, obvious=True, readonly=True, group='剪刀撑')
        self['剪刀撑间距'] = Attr(6000.0, obvious=True, readonly=True, group='剪刀撑')
        self['钢管直径'] = Attr(48.0, obvious=True, readonly=True, group='钢管')
        self['钢管间距'] = Attr(1500.0, obvious=True, readonly=True, group='钢管')
        self['默认长度'] = Attr(5000.0, obvious=False, group='架体')
        self['ExternalScaffoldingGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        def point_rotate(geometry, center: Vec3, axis: Vec3, angle: float):
            geometry_Temp = translate(Vec3(0, 0, 0) - center)*geometry
            geometry_Temp = rotate(axis, angle)*geometry_Temp
            geometry_New = translate(center)*geometry_Temp
            return geometry_New

        # Active Parameters
        Height_JiaTi = self['架体高度']
        Space_JiaTi = self['架体横距']
        Space_ZouDaoBan = self['走道板间隔']
        DownOffsite_ZouDaoBan = self['走道板底部偏移']
        Space_Building = self['与建筑间距']
        DefaultLength = self['默认长度']
        Diameter_GangGuan = self['钢管直径']
        Space_GangGuan = self['钢管间距']
        Diameter_JianDaoCheng = self['剪刀撑直径']
        Space_JianDaoCheng = self['剪刀撑间距']
        Width_JingShiDai = self['警示带宽度']
        Space_JingShiDai = self['警示带间隔']

        # Passive Parameters
        self['走道板宽度'] = Space_JiaTi
        Count_ZouDaoBan = int(Height_JiaTi/Space_ZouDaoBan)
        self['走道板数量'] = Count_ZouDaoBan
        Count_LiGan = int((DefaultLength - Diameter_GangGuan)/Space_GangGuan) + 1
        Count_HengGan = int((Height_JiaTi - Diameter_GangGuan - DownOffsite_ZouDaoBan)/Space_GangGuan) + 1
        XSpace_JianDaoCheng = Space_JianDaoCheng
        Count_JianDaoCheng = round((DefaultLength - Height_JiaTi*tan(35/180*pi))/XSpace_JianDaoCheng) + 1
        Count_JingShiDai = int((Height_JiaTi - Width_JingShiDai)/Space_JingShiDai) + 1
        self['警示带数量'] = Count_JingShiDai

        # Geometry
        # 走道板
        Height_Board = 20
        SingleZouDaoBan = translate(0, Space_Building, DownOffsite_ZouDaoBan - Height_Board)*\
                          scale(DefaultLength, Space_JiaTi, Height_Board)*Cube().color(242/255, 215/255, 177/255, 1)
        ZouDaoBan = Array(SingleZouDaoBan)
        for point in linspace(Vec3(0, 0, 0), Vec3(0, 0, (Count_ZouDaoBan - 1)*Space_ZouDaoBan), Count_ZouDaoBan):
            ZouDaoBan.append(translate(point))

        # 立杆
        SingleLiGan_SecDown = Section(translate(Diameter_GangGuan/2, Space_JiaTi + Space_Building+Diameter_GangGuan*1.5)
                                      *scale(Diameter_GangGuan/2)*Arc(pi*2))
        SingleLiGan_SecUp = translate(0, 0, Height_JiaTi)*SingleLiGan_SecDown
        SingleLiGan = Loft(SingleLiGan_SecDown, SingleLiGan_SecUp).color(141/255, 109/255, 84/255, 1)
        LiGan = Array(SingleLiGan)
        for point in linspace(Vec3(0, 0, 0), Vec3((Count_LiGan - 1)*Space_GangGuan, 0, 0), Count_LiGan):
            LiGan.append(translate(point))

        # 横杆
        SingleHengGan_SecDown = translate(
            Diameter_GangGuan/2, Space_JiaTi + Space_Building+Diameter_GangGuan/2,DownOffsite_ZouDaoBan
            )*rotate(Vec3(0, 1, 0), pi/2
            )*Section(scale(Diameter_GangGuan/2) * Arc(pi*2))
        SingleHengGan_SecUp = translate(DefaultLength, 0)*SingleHengGan_SecDown
        SingleHengGan = Loft(SingleHengGan_SecDown, SingleHengGan_SecUp).color(141/255, 109/255, 84/255, 1)
        HengGan = Array(SingleHengGan)
        for point in linspace(Vec3(0, 0, 0), Vec3(0, 0, (Count_HengGan - 1)*Space_GangGuan), Count_HengGan):
            HengGan.append(translate(point))

        # 剪刀撑
        # 中间剪刀撑
        Single_JianDaoCheng_Length = Height_JiaTi/cos(35/180*pi)
        Single_JianDaoCheng_SingleCount = int((Single_JianDaoCheng_Length - 500)/500)
        Single_JianDaoCheng_SingleLength = Single_JianDaoCheng_Length/Single_JianDaoCheng_SingleCount
        Single_JianDaoCheng_Sec = Section(scale(Diameter_JianDaoCheng/2)*Arc(pi*2))
        Single_JianDaoCheng_Single = Loft(Single_JianDaoCheng_Sec, translate(0, 0, Single_JianDaoCheng_SingleLength)
                                          *Single_JianDaoCheng_Sec)
        Single_JianDaoCheng_List = []
        i = 0
        for point in linspace(Vec3(0, 0, 0),
                              Vec3(0, 0, Single_JianDaoCheng_Length - Single_JianDaoCheng_SingleLength),
                              Single_JianDaoCheng_SingleCount):
            if i % 2 == 0:
                Single_JianDaoCheng_List.append(translate(point)*Single_JianDaoCheng_Single.color(1, 1, 1, 1))
            else:
                Single_JianDaoCheng_List.append(translate(point)*Single_JianDaoCheng_Single.color(1, 0, 0, 1))
            i += 1
        Single_JianDaoCheng = combine(*Single_JianDaoCheng_List)
        Single_JianDaoCheng_Positive = rotate(Vec3(0, 1, 0), 35/180*pi)*Single_JianDaoCheng
        JianDaoCheng_Positive = Array(Single_JianDaoCheng_Positive)
        for point in linspace(Vec3(0, 0, 0), Vec3(DefaultLength - Height_JiaTi*tan(35/180*pi), 0, 0),
                              Count_JianDaoCheng):
            JianDaoCheng_Positive.append(translate(point))
        # 两侧剪刀撑
        i = 1
        Court_JianDaoCheng_List = []
        while 1:
            if Count_JianDaoCheng - 1 <= 0:
                H_temp = i*Space_JianDaoCheng*math.tan(55/180*pi)
            else:
                H_temp = i*((DefaultLength - Height_JiaTi*tan(35/180*pi))/(Count_JianDaoCheng - 1))*math.tan(55/180*pi)
            if Height_JiaTi - H_temp <= 0:
                break
            SingleLength = (Height_JiaTi - H_temp)/cos(35/180*pi)
            SingleSingleCount = int((SingleLength - 500)/500)
            SingleSingleLength = SingleLength/SingleSingleCount
            SingleSingleGeo = Loft(Single_JianDaoCheng_Sec, translate(0, 0, SingleSingleLength)
                                   *Single_JianDaoCheng_Sec)
            k = 0
            SingleGeoList = []
            for point in linspace(Vec3(0, 0, 0),
                                  Vec3(0, 0, SingleLength - SingleSingleLength), SingleSingleCount):
                if k%2 == 0:
                    SingleGeoList.append(translate(point)*SingleSingleGeo.color(1, 1, 1, 1))
                else:
                    SingleGeoList.append(translate(point)*SingleSingleGeo.color(1, 0, 0, 1))
                k += 1
            SingleGeo = combine(*SingleGeoList)
            SingleGeo = rotate(Vec3(0, 1, 0), 35/180*pi)*SingleGeo
            SingleGeo = translate(0, 0, H_temp)*SingleGeo
            Court_JianDaoCheng_List.append(SingleGeo)
            i += 1
        Court_JianDaoCheng = combine(*Court_JianDaoCheng_List)
        Court_JianDaoCheng_Part2 = point_rotate(Court_JianDaoCheng, Vec3(DefaultLength/2, 0, Height_JiaTi/2),
                                                Vec3(0, 1, 0), pi)
        JianDaoCheng_Positive = combine(JianDaoCheng_Positive, Court_JianDaoCheng, Court_JianDaoCheng_Part2)
        JianDaoCheng_Negative = point_rotate(JianDaoCheng_Positive, Vec3(DefaultLength/2, Diameter_JianDaoCheng/2, 0),
                                                Vec3(0, 0, 1), pi)
        JianDaoCheng = translate(0, Space_Building + Space_JiaTi + Diameter_JianDaoCheng/2 + 2*Diameter_GangGuan, 0)\
                       *combine(JianDaoCheng_Positive, JianDaoCheng_Negative)

        # 警示带
        CountSingleSingle_JingShiDai = int(DefaultLength/200)
        WidthSingleSingle_JingShiDai = DefaultLength/CountSingleSingle_JingShiDai
        First_JingShiDai_Sec = to_section(Vec3(0, 0, 0), Vec3(0, 0, Width_JingShiDai),
                                       Vec3(WidthSingleSingle_JingShiDai, 0, Width_JingShiDai))
        First_JingShiDai = Loft(First_JingShiDai_Sec, translate(0, 1, 0)*First_JingShiDai_Sec).color(1, 0, 0, 1)
        SingleSingle_JingShiDai_Sec = to_section(Vec3(0, 0, 0), Vec3(WidthSingleSingle_JingShiDai, 0, 0),
                                              Vec3(2*WidthSingleSingle_JingShiDai, 0, Width_JingShiDai),
                                              Vec3(WidthSingleSingle_JingShiDai, 0, Width_JingShiDai))
        SingleSingle_JingShiDai = Loft(SingleSingle_JingShiDai_Sec, translate(0, 1)*SingleSingle_JingShiDai_Sec)
        i = 0
        Single_JingShiDai_List = []
        for point in linspace(Vec3(0, 0, 0), Vec3(DefaultLength - WidthSingleSingle_JingShiDai, 0, 0),
                              CountSingleSingle_JingShiDai):
            if abs(point.x - DefaultLength + WidthSingleSingle_JingShiDai) <= 0.00001:
                break
            if i % 2 == 0:
                Single_JingShiDai_List.append(translate(point)*SingleSingle_JingShiDai.color(1, 1, 1, 1))
            else:
                Single_JingShiDai_List.append(translate(point)*SingleSingle_JingShiDai.color(1, 0, 0, 1))
            i += 1
        Single_JingShiDai_Middle = combine(*Single_JingShiDai_List)
        End_JingShiDai_Sec = to_section(Vec3(DefaultLength - WidthSingleSingle_JingShiDai, 0, 0),
                                     Vec3(DefaultLength, 0, 0), Vec3(DefaultLength, 0, Width_JingShiDai))
        if i % 2 == 0:
            End_JingShiDai = Loft(End_JingShiDai_Sec, translate(0, 1, 0)*End_JingShiDai_Sec).color(1, 1, 1, 1)
        else:
            End_JingShiDai = Loft(End_JingShiDai_Sec, translate(0, 1, 0)*End_JingShiDai_Sec).color(1, 0, 0, 1)

        Single_JingShiDai = translate(0, Space_Building + Space_JiaTi)\
                            *combine(First_JingShiDai, Single_JingShiDai_Middle, End_JingShiDai)
        JingShiDai = Array(Single_JingShiDai)
        for point in linspace(Vec3(0, 0, 0), Vec3(0, 0, (Count_JingShiDai - 1)*Space_JingShiDai), Count_JingShiDai):
            JingShiDai.append(translate(point))

        # 安全网
        AnQuanWang = translate(0, Space_Building + Space_JiaTi - 0.5)\
                     *scale(DefaultLength, 1, Height_JiaTi)*Cube().color(42/255, 158/255, 121/255, 0.3)
        self['ExternalScaffoldingGeo'] = combine(ZouDaoBan, LiGan, HengGan, JianDaoCheng, AnQuanWang, JingShiDai)


if __name__ == "__main__":
    Final_Geometry = ExternalScaffolding()
    TwoPointPlace.linearize(Final_Geometry, '默认长度')
    place(Final_Geometry)
