from pyp3d import *


class JYGFWXT(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件类型'] = Attr('被保护系统-封网保护', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('绝缘杆封网系统', readonly=True, obvious=True, group='构件分类')
        self['承托绳间距'] = Attr(readonly=True,obvious=True, group='封网尺寸')
        self['跨数'] = Attr(5, obvious=True, group='封网尺寸')
        self['整体宽度'] = Attr(18000.0, obvious=True, group='封网尺寸')
        self['整体长度'] = Attr(10000.0, obvious=True, group='封网尺寸')
        self['绝缘杆直径'] = Attr(4.00, obvious=True, group='封网尺寸')
        self['绝缘杆间距'] = Attr(2000.00, obvious=True, group='封网尺寸')
        self['承托绳伸出长度'] = Attr(2000.00, obvious=True, group='封网尺寸')
        self['封网长度'] = Attr(readonly=True, obvious=True, group='封网尺寸')
        self['绝缘杆封网系统'] = Attr(None, show=True)
        self.replace()

    @export   
    def replace(self):

        # Active Parameters
        SpanNum = self['跨数']
        Diameter_JueYuanGan = self['绝缘杆直径']
        Space_JueYuanGan = self['绝缘杆间距']
        Length_ChengTuoSheng = self['承托绳伸出长度']
        Length_Overall = self['整体长度']
        Width_Overall = self['整体宽度']

        # Passive Parameters


        self['承托绳间距'] = Space_ChengTuoSheng = (Width_Overall - 400) / SpanNum
        Width_FengWang = SpanNum * Space_ChengTuoSheng
        self['封网长度'] = Length_FengWang = Length_Overall - Length_ChengTuoSheng
        Length_ChengTuoSheng = Length_Overall - Length_FengWang
        Count_JueYuanGan = int(Length_FengWang/Space_JueYuanGan)+1
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

        # 多跨排布
        MultiChengTuoSheng = Array(SingleChengTuoSheng)
        for point in linspace(Vec3(0, 0, 0), Vec3(0, SpanNum*Space_ChengTuoSheng, 0), SpanNum + 1):
            MultiChengTuoSheng.append(translate(point))

        MultiJueYuanGan = Array(JueYuanGan)
        i = 0
        for point in linspace(Vec3(0, 0, 0), Vec3(0, (SpanNum - 1)*Space_ChengTuoSheng, 0), SpanNum):
            if i % 2 == 0:
                MultiJueYuanGan.append(translate(point))
            else:
                MultiJueYuanGan.append(translate(point + Vec3(Diameter_JueYuanGan, 0, 0)))
            i += 1
        self['绝缘杆封网系统'] = translate(Vec3(0, -(Width_Overall - 400)/2, 0))\
                          *combine(MultiChengTuoSheng, MultiJueYuanGan)


if __name__ == "__main__":
    Final_Geometry = JYGFWXT()
    TwoPointPlace.linearize(Final_Geometry, '整体长度')
    place(Final_Geometry)