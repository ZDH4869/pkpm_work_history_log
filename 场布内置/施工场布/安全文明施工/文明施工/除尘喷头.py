from pyp3d import *
class 除尘喷头(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['场布类型'] = Attr("临水", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("防尘", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("除尘喷头", obvious=True, group="构件分类")
        self['直径'] = Attr(20, obvious=True, readonly=True, group="喷头")
        self['高度'] = Attr(50, obvious=True, readonly=True, group="喷头")
        self['长度'] = Attr(200, obvious=True, group="直管")
        self['管径'] = Attr(15, obvious=True, readonly=True, group="直管")
        self['除尘喷头'] = Attr(None, show=True)
        
        self.replace()

    @export
    def replace(self):

        L=self['长度']
    #底部直管
        sectionOut =  Section(scale(7.5) * Arc(pi*2))
        sectionOut_final = translate(0, 0, L)*sectionOut
        
        BottomPipe =  Loft(sectionOut, sectionOut_final).color(61/255,150/255,190/255,1)
    
    #八角形连接1   
        sectionOut2 = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(6.44,0), Vec2(15.56,0), Vec2(22,6.44),Vec2(22,15.56),Vec2(15.56,22),Vec2(6.44,22),Vec2(0,15.56),Vec2(0,6.44),Vec2(6.44,0))       
        #line2=Line(Vec3(0,0,0),Vec3(0,10,0))
        sweep2 = Loft(sectionOut2,translation(0,10,0)*sectionOut2)
        sweep2=rotate(Vec3(-1,0,0),0.5*pi) * sweep2
      
        bjlj1=translate(0,0,L-200)*translate(Vec3(-11,-11,200))*sweep2
   
    #弯管    
        sectionOut3 = translation(20,0,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(7.5,7.5) * Arc(math.pi*2))
        line3 = Line(scale(500) * Arc(math.pi/3))
        sweep3 = Sweep(sectionOut3,line3)
        sweep3=rotate(Vec3(1,0,0),0.5*pi) * sweep3
        sweep3=rotate(Vec3(0,0,1),0.5*pi) * sweep3
      
        wg=translate(Vec3(0,-20,210))*sweep3
   
    #八角形连接2    
        sectionOut4 = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(6.44,0), Vec2(15.56,0), Vec2(22,6.44),Vec2(22,15.56),Vec2(15.56,22),Vec2(6.44,22),Vec2(0,15.56),Vec2(0,6.44),Vec2(6.44,0))       
        #line4=Line(Vec3(0,0,0),Vec3(0,10,0))
        sweep4 = Loft(sectionOut4,translation(0,10,0)*sectionOut4)
      
        bjlj2=translate(Vec3(-11,0,-11))*sweep4
   
    #连接直管
        sectionOut5 =translation(0,-10,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(7.5,7.5) * Arc(math.pi*2))      
        line5 = Line(Vec3(0,0,0),Vec3(0,20,0))
      
        ljzg = Loft(sectionOut5,translation(0,20,0)*sectionOut5)

    #套管1
        sectionOut6 =translation(0,-25,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(10,10) * Arc(math.pi*2))      
        line6= Line(Vec3(0,0,0),Vec3(0,15,0))
      
        tg1 = Loft(sectionOut6,translation(0,15,0)*sectionOut6)
   
    #套管2
        sectionOut7 =translation(0,-45,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(12.5,12.5) * Arc(math.pi*2))      
        line7= Line(Vec3(0,0,0),Vec3(0,20,0))
     
        tg2 = Sweep(sectionOut7,line7)
   
    #除尘喷头螺栓
        sectionOut8 =translation(0,-51,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(10,10) * Arc(math.pi*2))      
        line8= Line(Vec3(0,0,0),Vec3(0,6,0))
        sweep8 = Loft(sectionOut8,translation(0,6,0)*sectionOut8)
        sectionOut9 =translation(0,-52,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11,11) * Arc(math.pi*2))      
        line9= Line(Vec3(0,0,0),Vec3(0,1,0))
        sweep9 = Loft(sectionOut9,translation(0,1,0)*sectionOut9)
        sectionOut10 =translation(0,-53,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11.2,11.2) * Arc(math.pi*2))      
        line10= Line(Vec3(0,0,0),Vec3(0,1,0))
        sweep10 = Loft(sectionOut10,translation(0,1,0)*sectionOut10)
        sectionOut11 =translation(0,-54,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11,11) * Arc(math.pi*2))      
        line11= Line(Vec3(0,0,0),Vec3(0,1,0))
        sweep11 = Loft(sectionOut11,translation(0,1,0)*sectionOut11)
        sectionOut12 =translation(0,-55,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11,11) * Arc(math.pi*2))      
        line12= Line(Vec3(0,0,0),Vec3(0,1,0))
        sweep12 = Loft(sectionOut12,translation(0,1,0)*sectionOut12)
        sectionOut14 =translation(0,-56,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11,11) * Arc(math.pi*2))      
        line14= Line(Vec3(0,0,0),Vec3(0,1,0))
        sweep14 =Loft(sectionOut14,translation(0,1,0)*sectionOut14)
        sectionOut13 =translation(0,-57,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11.2,11.2) * Arc(math.pi*2))      
        line13= Line(Vec3(0,0,0),Vec3(0,1,0))
        sweep13 = Loft(sectionOut13,translation(0,1,0)*sectionOut13)
        sectionOut15 =translation(0,-58.5,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11.2,11.2) * Arc(math.pi*2))      
        line15= Line(Vec3(0,0,0),Vec3(0,1,0))
        sweep15 =Loft(sectionOut15,translation(0,1.5,0)*sectionOut15)
        sectionOut16 =translation(0,-60,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(11.2,11.2) * Arc(math.pi*2))      
        line16= Line(Vec3(0,0,0),Vec3(0,1.5,0))
        sweep16 = Loft(sectionOut16,translation(0,1.5,0)*sectionOut16)
      
        ls=combine(sweep8,sweep9,sweep10,sweep11,sweep12,sweep13,sweep14,sweep15,sweep16)
   
    #六角垫片
        sectionOut17 = translation(-(12*1.1),-64,-(11.5)) * rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(6*1.1,0), Vec2(18*1.1,0), Vec2(24*1.1,6*1.1*1.732),Vec2(18*1.1,6*1.1*1.732*2),Vec2(6*1.1,6*1.1*1.732*2),Vec2(0,6*1.1*1.732),Vec2(6*1.1,0))       
        line17=Line(Vec3(0,0,0),Vec3(0,4,0))

        ljdp = Loft(sectionOut17,translation(0,4,0)*sectionOut17)

    #六角
        sectionOut18 = translation(-5.192*2,-75,-5.195*1.732) * rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(5.195,0), Vec2(5.195*3,0), Vec2(5.195*4,5.195*1.732),Vec2(5.195*3,5.195*1.732*2),Vec2(5.195,5.195*1.732*2),Vec2(0,5.195*1.732),Vec2(5.195,0))       
        line18=Line(Vec3(0,0,0),Vec3(0,11,0))
        sweep18 = Loft(sectionOut18,translation(0,11,0)*sectionOut18)
   
        lj=rotate(Vec3(0,1,0),pi/6)*sweep18

    #圆形垫片
        sectionOut19 =translation(0,-76,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(8,8) * Arc(math.pi*2))      
        line19= Line(Vec3(0,0,0),Vec3(0,1,0))

        ydp = Loft(sectionOut19,translation(0,1,0)*sectionOut19)

    #喷头
        sectionOut20 =translation(0,-84.5,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(9,9) * Arc(math.pi*2))      
        line20= Line(Vec3(0,0,0),Vec3(0,8.5,0))

        pt1 = Loft(sectionOut20,translation(0,8.5,0)*sectionOut20)
   
    #喷嘴
        sectionOut21=rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), Vec2(4.5,0), Vec2(9,8),Vec2(0,8),Vec2(0,0))
        line21 = Line(scale(500) * Arc(pi*2))
        sweep21 = Sweep(sectionOut21,line21)
        sweep21=rotate(Vec3(-1,0,0),0.5*pi) * sweep21
   
        pz=translate(Vec3(0,-92.5,0))*sweep21
  
        pt=combine(bjlj2,ljzg,tg1,tg2,ls,ljdp,lj,ydp,pt1,pz)
        pt=rotate(Vec3(-1,0,0),0.5*pi) * pt
        pt=rotate(Vec3(1,0,0),pi/3) * pt
        pt=translate(Vec3(0,-9.5,228))*pt    
        b=combine(wg,pt)
        b=translate(0,0,L-210)*b
        a=combine(BottomPipe,b,bjlj1)

        if L==0:
            self['除尘喷头'] = (b)
        if L>0:
            self['除尘喷头'] = (a)  

            
if __name__ == "__main__":
    Final_Geometry = 除尘喷头()
    #RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)