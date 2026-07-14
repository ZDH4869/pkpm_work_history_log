from pyp3d import *
class 除尘直管(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['场布类型'] = Attr("临水", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("防尘", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("除尘直管", obvious=True, group="构件分类")
        self['长度'] = Attr(200, obvious=True, group="直管")
        self['管径'] = Attr(15, obvious=True, group="直管")
        self['壁厚'] = Attr(3, obvious=True, group="直管")
        self['除尘直管'] = Attr(None, show=True)
        
        self.replace()

    @export
    def replace(self):

        L=self['长度']
        W=self['壁厚']
        D=self['管径']
        if W >= D/2:
            W=D/2-1
    #底部直管
        sectionOut =  Section(scale(D/2) * Arc(pi*2))
        sectionOut_final = translate(0, 0, L)*sectionOut
        
        BottomPipe =  Loft(sectionOut, sectionOut_final).color(61/255,150/255,190/255,1)

        sectionOut2 =  Section(scale(D/2-W) * Arc(pi*2))
        sectionOut_final2 = translate(0, 0, L)*sectionOut2
        
        BottomPipe2 =  Loft(sectionOut2, sectionOut_final2).color(61/255,150/255,190/255,1)

        self['除尘直管']=BottomPipe - BottomPipe2

if __name__ == "__main__":
    Final_Geometry = 除尘直管()
    #RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)