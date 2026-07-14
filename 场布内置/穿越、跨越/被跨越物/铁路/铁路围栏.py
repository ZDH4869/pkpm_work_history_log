from pyp3d import *
#
class 放样体(Component):
 def __init__(self):
    Component.__init__(self)
    self['构件类型'] = Attr('被跨越物', obvious = True, group='构件分类',readonly = True)
    self['应用场景'] = Attr('铁路', obvious = True, group='构件分类',readonly = True)
    self['构件名称'] = Attr('铁路围栏', obvious = True, group='构件分类')
    self['围栏上端是否显示'] = Attr('是', obvious=True, group='构件分类')
#围栏尺寸
    self['围栏长度'] = Attr(1500, obvious=False, group='围栏尺寸')
    self['围栏高度'] = Attr(1500, obvious=True, group='围栏尺寸')
    self['单段围栏宽度'] = Attr(3000, obvious=True, group='围栏尺寸')
    self['边框角钢边长'] = Attr(40, obvious = True, group='围栏尺寸')
#立柱尺寸
    self['立柱长'] = Attr(60, obvious=True, group='立柱尺寸')
    self['立柱宽'] = Attr(60, obvious = True, group='立柱尺寸')
#基础尺寸
    self['基础长'] = Attr(300, obvious = True, group='基础尺寸')
    self['基础宽'] = Attr(180, obvious = True, group='基础尺寸')
    self['基础厚'] = Attr(0, obvious = True, group='基础尺寸')

    self['放样体'] = Attr(None, show=True)
    self.replace()
 @export
 def replace(self):
    L = self['围栏长度']
    H = self['围栏高度']
    W = self['单段围栏宽度']
    D = self['边框角钢边长']
    a1 = self['立柱长']
    b1 = self['立柱宽']
    a2 = self['基础长']
    b2 = self['基础宽']
    h2 = self['基础厚']
    k  = self['围栏上端是否显示']
#立柱
    Col1= scale(a1,b1,H) * Cube()
    self['立柱高'] = Attr(H, obvious=True, group='立柱尺寸',readonly = True)
#立柱文本
    Text1= translation(a1/4,-a1/2,H*4/5)*rotate(Vec3(1,0,0), pi/2)*Text('禁',a1/4,a1)
    Text2= translation(a1/4,-a1/2,H*3/5)*rotate(Vec3(1,0,0), pi/2)*Text('止',a1/4,a1)
    Text3= translation(a1/4,-a1/2,H*2/5)*rotate(Vec3(1,0,0), pi/2)*Text('入',a1/4,a1)
    Text4= translation(a1/4,-a1/2,H*1/5)*rotate(Vec3(1,0,0), pi/2)*Text('内',a1/4,a1)
    Text5= Combine(Text1,Text2,Text3,Text4)
    Col= Combine(Text5,Col1)
#基础
    Base= translation(-(a2-a1)/2,-b2/2,0)*scale(a2,b2,-h2) * Cube()

#栏杆边框
    Cube1= translation(a1+40,D/4,D)*scale(W,D,H-D) * Cube()
    Cube2= translation(a1+40+D,D/4,2*D)*scale(W-D*2,D,H-D-2*D) * Cube()
    Cube3= Cube1-Cube2
    Cube4= translation(a1+40+(W-D)/2,D/4,2*D)*scale(D,D,H-D-2*D) * Cube()
    Cube_frame=(Cube3+Cube4).color(0,0.4,0,1)
#连接
    Cube5= translation(a1,0,H/4)*scale(30,10,30) * Cube().color(0.8,0.8,0.8,1)
    Cube6= translation(a1+10,10,H/4)*scale(30,10,30) * Cube().color(0.8,0.8,0.8,1)
    Section1= rotate(Vec3(1,0,0), pi/2)*Section(scale(5) * Arc(2*pi))
    Loft1= translation(a1+20,0,H/4+15)*Loft(Section1, translate(0,20,0) * Section1).color(0.8,0.8,0.8,1)
    Cube_c1= Combine(Loft1,Cube5,Cube6)
    Cube_c2= translation(0,0,H/4)*Cube_c1
    Cube_c3= translation(0,0,H/4)*Cube_c2
    Cube_con1= Combine(Cube_c1,Cube_c2,Cube_c3)
    Cube_con2= translation(W+D,0,H)*rotate(Vec3(a1+40,1,0), pi)*Cube_con1
    Cube_con= translation(0,a1/2,0)*Combine(Cube_con1,Cube_con2)
    if h2== 0:
        CUBE_1 = Combine(Cube_con,Cube_frame,Col)
    else:
        CUBE_1 = Combine(Cube_con,Cube_frame,Col,Base)
#铁丝网
    Section2= rotate(Vec3(0,1,0), pi/2)*Section(scale(5) * Arc(2*pi))
    Loft1= translation(a1+40+D,D/2,D+170)*Loft(Section2, translate(W-2*D,0,0) * Section2).color(0,0.4,0,1)

    Section3= Section(scale(5) * Arc(2*pi))
    Loft2= translation(a1+100+D,D/2,2*D)*Loft(Section3, translate(0,0,H-2*D) * Section3).color(0,0.4,0,1)

    #上端横向铁丝
    wet_up1= translation(0,0,H-2*D-100)*Loft1
    wet_up2= translation(0,-20,80)*wet_up1
    wet_up3= translation(0,-70,120)*wet_up2
    wet_up=Combine(wet_up1,wet_up2,wet_up3)
    #上端竖向铁丝
    Loft3= rotate(Vec3(1,0,0), pi/6)*Loft(Section3, translate(0,0,210) * Section3).color(0,0.4,0,1)
    wet_A=translation(a1+100+D,D/2,H+70)*Loft3
    Loft4= translation(a1+100+D,D/2,H)*Loft(Section3, translate(0,0,70) * Section3).color(0,0.4,0,1)
    wet_C=Combine(Loft4,wet_A)

    LeftUP_Array = Array(wet_C)
    n2=int((W-2*D)/60)
    for i in linspace(Vec3(0,0,0),Vec3(W-2*D-60,0,0),n2):
     LeftUP_Array.append(translate(i))
    WET3= LeftUP_Array

    #横向铁丝 
    Up_Array = Array(Loft1)
    n1=int((H-D-2*D)/120)
    for i in linspace(Vec3(0,0,0),Vec3(0,0,H-170-2*D),n1):
      Up_Array.append(translate(i))
    WET1= Up_Array
    #竖向铁丝
    Left_Array = Array(Loft2)
    n2=int((W-2*D)/60)
    for i in linspace(Vec3(0,0,0),Vec3(W-2*D-60,0,0),n2):
     Left_Array.append(translate(i))
    WET2= Left_Array

#围栏上端

    SectionA= Section(Vec2(0,0), Vec2(0,60), Vec2(-120,268), Vec2(-155,248), Vec2(-40,60), Vec2(-40,0))
    LoftA= rotate(Vec3(0,1,0), pi/2)*Loft(SectionA, translate(0,0,40) * SectionA)
    LoftB= rotate(Vec3(1,0,0), pi/2)*LoftA.color(0,0.4,0,1)
    Cube_up1=translation((a1-D)/2,D+(a1-D)/2,H)*LoftB
    Cube_up2=translation(a1/2+D/2+40,0,0)*Cube_up1
    Cube_up3=translation(W-D,0,0)*Cube_up2
    Cube_c4= translation((a1+D)/2,0,H+150)*rotate(Vec3(-1,0,0), pi*5/6)*scale((a1+D)/2,20,20) * Cube().color(0,0.4,0,1)
    Cube_c5= translation(W+40+(a1-D)/2,0,0)*Cube_c4.color(0,0.4,0,1)
    Cube_all=Combine(Cube_up1,Cube_up2,Cube_up3,Cube_c4,Cube_c5)

#组合与可变性
    Geo_up=Combine(wet_up,WET3,wet_C,Cube_all)
    Geo_low=Combine(CUBE_1,WET1,WET2)
    if k=="否":
        geo = Combine(Geo_low)
    else:
        geo = Combine(Geo_up,Geo_low)

#最终の阵列
    ALL_Array = Array(geo)
    n3=int(L/(W+a1+80))
    for i in linspace(Vec3(0,0,0),Vec3((n3-1)*(W+a1+80),0,0),n3):
      ALL_Array.append(translate(i))
#结尾补柱
    if h2== 0:
        col_1 = Combine(Col,Cube_up1)
    else:
        col_1 = Combine(Col,Cube_up1,Base)
    col_2= translation(n3*(W+a1+80),0,0)*col_1
    Fin_geo= Combine(col_2,ALL_Array)
    self['放样体'] =Fin_geo

if __name__ == "__main__":
    FinalGeometry = 放样体()
    TwoPointPlace.linearize(FinalGeometry,'围栏长度')
    place(FinalGeometry)
    

     