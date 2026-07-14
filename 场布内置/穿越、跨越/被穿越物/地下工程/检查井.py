from pyp3d import *
class 检查井(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['应用场景'] = Attr("隧道穿越", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("地下工程", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("检查井", obvious=True,readonly=False, group="构件分类")
        self['井高'] = Attr(1000, obvious=True, group="检查井")
        self['开口外径'] = Attr(700, obvious=True, group="检查井")
        self['开口部分高度'] = Attr(400, obvious=True, group="检查井")
        self['井外径'] = Attr(900, obvious=True, group="检查井")
        self['井厚'] = Attr(100, obvious=True, group="检查井")
        self['检查井'] = Attr(None, show=True)

        self.replace()

    @export
    def replace(self):

        H=self['井高']
        r=self['开口外径']
        h=self['开口部分高度']
        R=self['井外径']
        d=self['井厚']

        #直管外径
        sectionOut =  Section(scale(R/2) * Arc(pi*2))
        sectionOut_low = translate(0, 0, -H)*sectionOut
        sectionOut_mid = translate(0, 0, -h)*sectionOut

        #直管内径
        sectionin =  Section(scale(R/2-d) * Arc(pi*2))
        sectionin_low = translate(0, 0, -H)*sectionin
        sectionin_mid = translate(0, 0, -h)*sectionin

        #开口部分截面
        sectionOut_up =  Section(scale(r/2) * Arc(pi*2))
        sectionin_up =  Section(scale(r/2-d) * Arc(pi*2))

        BottomPipe =  Loft(sectionOut_up, sectionOut_mid, sectionOut_low).color(128/255,128/255,128/255,1)
        BottomPipe2 =  Loft(sectionin_up, sectionin_mid, sectionin_low).color(128/255,128/255,128/255,1)
        #井壁开洞
        sectionOut3 =  translate(0,0,-h-300)*rotation(Vec3(1,0,0,),0.5*pi)*Section(scale(200) * Arc(pi*2))
        sectionOut_final3 = translate(0, R/2, 0)*sectionOut3

        BottomPipe3 =  Loft(sectionOut3, sectionOut_final3)

        self['检查井']=BottomPipe - BottomPipe2 - BottomPipe3

if __name__ == "__main__":
    Final_Geometry = 检查井()
    place(Final_Geometry)    