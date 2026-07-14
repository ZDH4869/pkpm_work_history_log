from pyp3d import *
class 假担(Component):
    def __init__(self):
        Component.__init__(self)
        self['截面长'] = Attr(500.0, obvious=True, readonly = False)
        self['截面宽'] = Attr(500.0, obvious=True, readonly = False)
        self['单节长度'] = Attr(3000.0, obvious=True, readonly = False)
        self['节数'] = Attr(3, obvious=True, readonly = False)
        self['单节斜杆对数'] = Attr(5, obvious=True, readonly = False)
        self['假担'] = Attr(None, show=True)
        self.replace()
    @export
    def replace(self):

        # 描述截面

        AH = self['单节长度']
        AW = self['截面长'] 
        AD = self['截面宽']
        AN = self['节数']
        ANB = self['单节斜杆对数']

        section1 = Section(Vec3(0,0,0),Vec3(20,0,0),Vec3(20,20,0),Vec3(0,20,0))
        section2 = rotate(Vec3(0,1,0),pi/2)*section1
        
        # 扫略
        Loft1 = Loft(section1 , translate(0,0,AH)*section1).color(0.75,0.75,0.75,1)
        Loft1b = translate(AW-20,0,0)*Loft1
        Loft2 = Loft(translate(20,0,AH/ANB/2)*section2 , translate(AW-20,0,AH/ANB-20)*section2).color(0.75,0.75,0.75,1)
        Loft3 = rotate(Vec3(1,0,0),pi)*translate(0,-20,-AH/ANB+40)*Loft2
        Loft2b = Loft(translate(20,0,AH/ANB/2)*section2 , translate(AD-20,0,AH/ANB-20)*section2).color(0.75,0.75,0.75,1)
        Loft3b = rotate(Vec3(1,0,0),pi)*translate(0,-20,-AH/ANB+40)*Loft2b
        Loft4a1 = Loft(section2 , translate(AW,0,0)*section2).color(0.75,0.75,0.75,1)
        Loft4b1 = translate(20,0,0)*rotate(Vec3(0,0,1),pi/2)*Loft(section2 , translate(AD,0,0)*section2).color(0.75,0.75,0.75,1)
        Loft4a2 = translate(0,AD-20,0)*Loft4a1
        Loft4b2 = translate(AW-20,0,0)*Loft4b1
        Bottom = combine(Loft4a1,Loft4b1,Loft4a2,Loft4b2)
        Top = translate(0,0,AH)*Bottom

        pulley2a=combine(Loft2b,Loft3b)
        pulley2b=translate(0,AD,0)*rotate(Vec3(0,0,1),-pi/2)*pulley2a
        pulley=translate(0,0,20)*combine(Loft2,Loft3,pulley2b)
        pulleyArraya = Array(pulley)
        for i in range(ANB):
            pulleyArraya.append(translate(0,0,AH*i/ANB))
        trussA = combine(Loft1,Loft1b,pulleyArraya)        
        trussB = translate(AW,AD,0)*rotate(Vec3(0,0,1),pi)*trussA
        ALL=combine(trussA,trussB,Bottom,Top)
        pulleyArrayb = Array(ALL)
        for i in range(AN):
            pulleyArrayb.append(translate(0,0,AH*i))
        truss = translate(0,0,AW)*rotate(Vec3(0,1,0),pi/2)*pulleyArrayb
        self['假担']=truss
if __name__ == "__main__":
    place(假担())