from pyp3d import *
class 移动摄像头(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['场布类型'] = Attr("智慧工地", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("监控", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("移动摄像头", obvious=True, group="构件分类")
        self['摄像头高度'] = Attr(1400, obvious=True, group="摄像头")
        #self['转角度数'] = Attr(60, obvious=True, group="连接弯头")
        #self['直径'] = Attr(20, obvious=True, group="连接弯头")
        self['移动摄像头'] = Attr(None, show=True)

        
        self.replace()

    @export
    def replace(self):
        H = self['摄像头高度']
        h = 187.5  #摄像头高
        jjh = H-h/2
        jjL = (3**(1/2))*2/3*jjh
        if H>1200:
            jjh = 1200
            jjL = (3**(1/2))*2/3*jjh
        else :
            jjh = H
            jjL = (3**(1/2))*2/3*jjh

    #摄像头
        sectionOut =  Section(scale(75) * Arc(pi*2))
        sectionOut_final = translate(0, 0, 75)*sectionOut
        
        BottomPipe =  Loft(sectionOut, sectionOut_final)

        BottomBox = scale(75,500,150) * Cube()
        BottomBox = translate(Vec3(-37.5,-150,75)) * BottomBox

        MidPipe = translate(0,0,75) * BottomPipe.color(1,1,1,1)

        Mid = Intersect(BottomBox,MidPipe).color(1,1,1,1)
        Topl = rotate(Vec3(0,0,1), 0.5*pi) * Section(Vec2(37.5,0), scale(37.5) * Arc(pi), Vec2(-37.5,0))
        line2=Line(Vec3(0,0,0),Vec3(0,0,170))
        Top = Sweep(Topl,line2)
        Top = rotate(Vec3(0,1,0),0.5*pi) * Top
        Top = rotate(Vec3(0,0,1),0.5*pi) * Top
        Top = translate(Vec3(0,85,150)) * Top
        Mid2 = translate(0,0,75) * Mid
        Top_f = Intersect(Mid2,Top).color(1,1,1,1)

        #MidBall = scale(200) * Sphere()
        #MidBall = translate(Vec3(0,0,120)) * MidBall
        #sxt = Intersect(Mid,MidBall)
        sectionOut =  Section(scale(12.5) * Arc(pi*2))
        # sectionOut_final = translate(0, 0, h/2+150)*sectionOut
        sectionOut_final = translate(0, 0, H-jjh)*sectionOut
        
        BottomPipe2 =  Loft(sectionOut, sectionOut_final)
        BottomPipe2 = translate(Vec3(0,0,-(H-jjh))) * BottomPipe2

        sxt_way = Line(scale(1) * Arc(pi*2))
        sxt_t = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), scale(10) * Arc(pi/2), Vec2(0,0))
        sxt_tt = Sweep(sxt_t,sxt_way)
        sxt_tt = rotate(Vec3(1,0,0),1.5*pi) * sxt_tt
        sxt_tt = translate(Vec3(0,70,130)) * sxt_tt
        # gdsxt = combine(BottomPipe,Mid,Top_f,BottomPipe2,sxt_tt)
        gdsxt = combine(BottomPipe,BottomPipe2)
        gdsxt = translate(Vec3(0,0,H)) * gdsxt
        #
        h = 400  #摄像头高

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
        sxt = rotate(Vec3(1,0,0),pi) * sxt
        sxt = translate(0,0,H) * sxt
        # #
        # 脚架
        sectionOu2t =  Section(scale(12.5) * Arc(pi*2))
        sectionOut_final2 = translate(0, 0, jjL)*sectionOu2t 
        sjj1 = Loft(sectionOu2t,sectionOut_final2)
        sjj1 = rotate(Vec3(1,0,0),pi/6) * sjj1
        sjj1 = translate(Vec3(0,jjL/2+12.5,0)) * sjj1
        sjj2 = rotate(Vec3(0,0,1),pi*4/3) * sjj1
        sjj3 = rotate(Vec3(0,0,1),pi*2/3) * sjj1
        sjj = combine(sjj1,sjj2,sjj3)
        sjj = rotate(Vec3(0,0,1),pi/6) * sjj

        sectionOu3t =  Section(scale(50) * Arc(pi*2))
        sectionOut_final3 = translate(0, 0, 20)*sectionOu3t  
        sjjdp = Loft(sectionOu3t,sectionOut_final3)
        sjjdp = translate(Vec3(0,0,jjh-10)) * sjjdp

        a=combine(gdsxt,sxt,sjj,sjjdp)
        self['移动摄像头'] =(a) 

if __name__ == "__main__":
    Final_Geometry = 移动摄像头()
    #RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)

 