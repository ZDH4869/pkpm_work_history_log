from pyp3d import *
class 固定摄像头(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['场布类型'] = Attr("智慧工地", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("监控", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("固定摄像头", obvious=True, group="构件分类")
        self['摄像头高度'] = Attr(2300, obvious=True, group="摄像头")
        #self['转角度数'] = Attr(60, obvious=True, group="连接弯头")
        #self['直径'] = Attr(20, obvious=True, group="连接弯头")
        self['固定摄像头'] = Attr(None, show=True)

        
        self.replace()

    @export
    def replace(self):
        H = self['摄像头高度']
        h = 400  #摄像头高

        lg_bottom = rotate(Vec3(0,0,1), 0.5*pi) * to_section(Vec3(0,0,0),Vec3(100,0,0),Vec3(75,0,H+h/2),Vec3(0,0,H+h/2))
        lg_way = Line(scale(1) * Arc(pi*2))
        lg = Sweep(lg_bottom,lg_way).color(225/255,225/255,225/255,1)

        #sxt_top = scale(100) * Sphere()
        sxt_top = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), scale(100) * Arc(pi/2), Vec2(0,0))
        sxt_way = Line(scale(1) * Arc(pi*2))
        sxt_topp = Sweep(sxt_top,sxt_way).color(225/255,225/255,225/255,1)
        sectionOut =  Section(scale(100) * Arc(pi*2))
        sectionOut_final = translate(0, 0, -40)*sectionOut
        
        BottomPipe =  Loft(sectionOut, sectionOut_final)

        top = (sxt_topp + BottomPipe).color(225/255,225/255,225/255,1)
        
        sxt_mid = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), scale(90) * Arc(pi/2), Vec2(0,0))
        sxt_midd = Sweep(sxt_mid,sxt_way).color(225/255,225/255,225/255,1)
        sxt_midd_r = rotate(Vec3(1,0,0), pi) * sxt_midd
        sxt_middl = combine(sxt_midd,sxt_midd_r)
        brbox = translate(-500,-500,-50) * scale(1000,1000,-500) * Cube()
        sxt_middf = (sxt_middl - brbox).color(225/255,225/255,225/255,1)
        sxt_middf = rotate(Vec3(1,0,0), pi/12) * sxt_middf
        
        sxt_bot = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), scale(70) * Arc(pi/2), Vec2(0,0))
        sxt_bott = Sweep(sxt_bot,sxt_way).color(225/255,225/255,225/255,1)
        sxt_bott_r = rotate(Vec3(1,0,0), pi) * sxt_bott
        sxt_bottl = combine(sxt_bott,sxt_bott_r)
        brbox1 = translate(-500,-500,-30) * scale(1000,1000,-500) * Cube()
        sxt_bottf = (sxt_bottl - brbox1).color(225/255,225/255,225/255,1)
        sxt_bottf = rotate(Vec3(1,0,0), pi/4) * sxt_bottf
        sxt_bottf = translate(0,15,-60) * sxt_bottf
        
        sxt_t = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), scale(10) * Arc(pi/2), Vec2(0,0))
        sxt_tt = Sweep(sxt_t,sxt_way).color(0,0,0,1)
        sxt_tt_r = rotate(Vec3(1,0,0), pi) * sxt_tt
        sxt_tt_r = rotate(Vec3(1,0,0), pi/4) * sxt_tt_r
        sxt_tt_r = translate(0,33,-78) * sxt_tt_r
        sxt1 = combine(sxt_middf,sxt_bottf,sxt_tt_r)
        sxt1 = translate(0,0,-40) * sxt1
        sxt=combine(top,sxt1)
        sxt = translate(0,250,H) * sxt

        sxt_g1 = rotate(Vec3(0,0,1), 0.5*pi) * Section(Vec2(10,-250), scale(10) * Arc(pi), Vec2(-10,-250))
        line2=Line(Vec3(0,0,0),Vec3(0,0,10))
        SXT_G = Sweep(sxt_g1,line2).color(225/255,225/255,225/255,1)
        SXT_G = translate(-250,0,H+110) * SXT_G
        SXT_G = rotate(Vec3(0,0,1), 1.5*pi) * SXT_G
        gdsxt = combine(sxt,lg,SXT_G)
        gdsxt = rotate(Vec3(0,0,1),1.5*pi) * gdsxt
        self['固定摄像头'] =(gdsxt) 

if __name__ == "__main__":
    Final_Geometry = 固定摄像头()
    #RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)
