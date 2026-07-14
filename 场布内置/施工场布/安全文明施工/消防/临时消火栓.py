from pyp3d import *

class 临时消火栓(Component):
    def __init__(self):
        Component.__init__(self)
        self['临时消火栓'] = Attr(None, show=True)
        self['场布类型'] = Attr("临水", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("消防", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("室外临时消防栓", obvious=True, group="构件分类")
        
    #下引管
        self['高度'] = Attr(1000, obvious=True, group="下引管")
        self['管径'] = Attr(150, obvious=True, group="下引管")
        self['出口管径'] = Attr(65, obvious=False, group="下引管")


    #水带箱体
        self['水带箱长'] = Attr(650.0, obvious=True,readonly=True,group='水带箱')
        self['水带箱宽'] = Attr(240.0, obvious=True,readonly=True,group='水带箱')
        self['水带箱高'] = Attr(800, obvious = True,readonly=True,group='水带箱')
        self['旋转角度'] = Attr(0,obvious = False)
        self['水带箱X'] = Attr(0, obvious=False)
        self['水带箱Y'] = Attr(0, obvious=False)
        self['水带箱Z'] = Attr(0, obvious=False)

    #水带箱门
        self['水带箱门长'] = Attr(450.0, obvious=False)
        self['水带箱门宽'] = Attr(10.0, obvious=False)
        self['水带箱门高'] = Attr(600, obvious = False)
        self['水带箱门X'] = Attr(100.0, obvious=False)
        self['水带箱门Y'] = Attr(-10.0, obvious=False)
        self['水带箱门Z'] = Attr(100.0, obvious=False)

    #文字“消火栓”
        self['显示文字'] = Attr("消火栓", obvious=False)

    #阀门
        self['阀门底座管径'] = Attr(250.0, obvious=False)
        self['阀门球直径'] = Attr(220,obvious=False)

        self.replace()

    @export
    def replace(self):

        xyg_l = self['高度']
        xyg_r = self['管径']
        fmq_r = self['阀门球直径']
        
#下引管

    #阀门

    #阀门底座
        fmdz = translation(0,0,0) * rotate(Vec3(1,0,0), 2*pi) * Section(Vec2(xyg_r*2/3,0), Vec2(xyg_r/3,1.732*xyg_r/3), Vec2(-xyg_r/3,1.732*xyg_r/3),Vec2(-xyg_r*2/3,0),Vec2(-xyg_r/3,-1.732*xyg_r/3),Vec2(xyg_r/3,-1.732*xyg_r/3),Vec2(xyg_r*2/3,0))       
        fmdz_final=Line(Vec3(0,0,0),Vec3(0,0,50))
        阀门底座 = Sweep(fmdz,fmdz_final)
        阀门底座 = translate(Vec3(0,0,xyg_l+50))*阀门底座

    #阀门球
        阀门球 = scale(xyg_r*2/5) * Sphere().color(1,0,0,1)
        阀门球 = translate(Vec3(0,0,xyg_l+20+fmq_r/4))*阀门球

    #把手底座
        bsdz = Section(scale(xyg_r/2)*Arc(pi*2))
        bsdz_final = translate(0,0,30)*bsdz
        把手底座1 = Loft(bsdz,bsdz_final).color(1,0,0,1)
        把手底座1 = translate(Vec3(0,0,xyg_l+50+xyg_r*2/5))*把手底座1

        bsdz2 = Section(scale(xyg_r/4)*Arc(pi*2))
        bsdz2_final = translate(0,0,30)*bsdz2
        把手底座2 = Loft(bsdz2,bsdz2_final).color(1,0,0,1)
        把手底座2 = translate(Vec3(0,0,xyg_l+50+xyg_r*2/5+30))*把手底座2

        bsdz3 = Section(scale(xyg_r/8)*Arc(pi*2))
        bsdz3_final = translate(0,0,30)*bsdz3
        把手底座3 = Loft(bsdz3,bsdz3_final).color(1,0,0,1)
        把手底座3 = translate(Vec3(0,0,xyg_l+50+xyg_r*2/5+30+30))*把手底座3

        bsdz4 = Section(scale(xyg_r/12)*Arc(pi*2))
        bsdz4_final = translate(0,0,30)*bsdz4
        把手底座4 = Loft(bsdz4,bsdz4_final).color(0,0,0,1)
        把手底座4 = translate(Vec3(0,0,xyg_l+50+xyg_r*2/5+30+30+30))*把手底座4

        把手底座 = combine(把手底座1,把手底座2,把手底座3,把手底座4)
    #把手
        bswq = Section(scale(xyg_r/3)*Arc(pi*2))
        bswq_final = translate(0,0,10)*bswq
        把手外圈 = Loft(bswq,bswq_final).color(0,0,0,1)
        bsnq = Section(scale(xyg_r/4)*Arc(pi*2))
        bsnq_final = translate(0,0,10)*bsnq
        把手内圈 = Loft(bsnq,bsnq_final).color(0,0,0,1)
        把手圈 = (把手外圈-把手内圈).color(0,0,0,1)

        把手圈 = translate(Vec3(0,0,xyg_l+50+xyg_r*2/5+30+30+30+30))*把手圈

        bs1 = Section(scale(5)*Arc(pi*2))
        bs1_final = translate(0,0,xyg_r*7/24)*bs1
        把手1 = Loft(bs1,bs1_final).color(0,0,0,1)
        把手1 = rotate(Vec3(0,1,0),0.5*pi)*把手1
        把手1 = translate(Vec3(0,0,xyg_l+50+xyg_r*2/5+30+30+30+30))*把手1

        bs2 = Section(scale(5)*Arc(pi*2))
        bs2_final = translate(0,0,xyg_r*7/24)*bs2
        把手2 = Loft(bs2,bs2_final).color(0,0,0,1)
        把手2 = rotate(Vec3(1,0,0),0.5*pi)*把手2
        把手2 = translate(Vec3(0,0,xyg_l+50+xyg_r*2/5+30+30+30+30))*把手2

        把手3 = translate(Vec3(-xyg_r*7/24,0,0))*把手1
        把手4 = translate(Vec3(0,xyg_r*7/24,0))*把手2

        把手 = combine(把手圈,把手1,把手2,把手3,把手4)

    #阀门
        fmck1 = Section(scale(fmq_r/2-50)*Arc(pi*2))
        fmck1_final = translate(0,0,xyg_r/3)*fmck1
        阀门出口1 = Loft(fmck1,fmck1_final).color(1,0,0,1)
        阀门出口1 = rotate(Vec3(1,0,0),0.5*pi)*阀门出口1
        阀门出口1 = translate(Vec3(0,-fmq_r/6,xyg_l+20+fmq_r/4))*阀门出口1

        fmck2 = Section(scale(fmq_r/2-50)*Arc(pi*2))
        fmck2_final = translate(0,0,xyg_r/3)*fmck1
        阀门出口2 = Loft(fmck2,fmck2_final).color(192/255,192/255,192/255,1)
        阀门出口2 = rotate(Vec3(1,0,0),0.5*pi)*阀门出口2
        阀门出口2 = translate(Vec3(0,-fmq_r/6-xyg_r/3,xyg_l+20+fmq_r/4))*阀门出口2

        fmck外圈 = Section(scale(fmq_r/2-20)*Arc(pi*2))
        fmck外圈_final = translate(0,0,xyg_r/3)*fmck外圈
        阀门出口外圈 = Loft(fmck外圈,fmck外圈_final).color(192/255,192/255,192/255,1)
        fmck外圈减 = Section(scale(fmq_r/2-50)*Arc(pi*2))
        fmck外圈减_final = translate(0,0,xyg_r/3)*fmck外圈减
        阀门出口外圈减 = Loft(fmck外圈减,fmck外圈减_final).color(192/255,192/255,192/255,1)
        fmck外圈 = (阀门出口外圈 - 阀门出口外圈减).color(192/255,192/255,192/255,1)
        阀门出口3 = rotate(Vec3(1,0,0),0.5*pi)*fmck外圈
        阀门出口3 = translate(Vec3(0,-fmq_r/6-xyg_r/3-xyg_r/3,xyg_l+20+fmq_r/4))*阀门出口3

        fmck内圈 = Section(scale(fmq_r/2-80)*Arc(pi*2))
        fmck内圈_final = translate(0,0,xyg_r/3)*fmck内圈
        阀门出口内圈 = Loft(fmck内圈,fmck内圈_final).color(192/255,192/255,192/255,1)
        fmck内圈减 = Section(scale(fmq_r/2-90)*Arc(pi*2))
        fmck内圈减_final = translate(0,0,xyg_r/3)*fmck内圈减
        阀门出口内圈减 = Loft(fmck内圈减,fmck内圈减_final).color(192/255,192/255,192/255,1)
        fmck内圈 = (阀门出口内圈 - 阀门出口内圈减).color(192/255,192/255,192/255,1)
        阀门出口4 = rotate(Vec3(1,0,0),0.5*pi)*fmck内圈
        阀门出口4 = translate(Vec3(0,-fmq_r/6-xyg_r/3-xyg_r/3,xyg_l+20+fmq_r/4))*阀门出口4

        阀门出口 = combine(阀门出口1,阀门出口2,阀门出口3,阀门出口4)


        阀门 = combine(阀门底座,阀门球,把手底座,把手,阀门出口)
        
    #下引管柱
        sectionOut =  Section(scale(xyg_r/2) * Arc(pi*2))
        sectionOut_final = translate(0, 0, xyg_l)*sectionOut
        下引管柱 =  Loft(sectionOut, sectionOut_final).color(192/255,192/255,192/255,1)

        下引管 = combine(下引管柱,阀门)


#水带箱

        #水带箱体
        sdx_l = self['水带箱长']
        sdx_w = self['水带箱宽']
        sdx_h = self['水带箱高']
        sdx_x = self['水带箱X']
        sdx_y = self['水带箱Y']
        sdx_z = self['水带箱Z']

        #水带箱门
        sdxm_l = self['水带箱门长']
        sdxm_w = self['水带箱门宽']
        sdxm_h = self['水带箱门高']
        sdxm_x = self['水带箱门X']
        sdxm_y = self['水带箱门Y']
        sdxm_z = self['水带箱门Z']
        Angle = self['旋转角度']

        #文字“消火栓”
        text = self['显示文字']


        水带箱体 = translate(sdx_x,sdx_y,sdx_z) * rotation(math.pi/180 * Angle) * scale(sdx_l,sdx_w,sdx_h) * Cube()
        水带箱门 = translate(sdxm_x,sdxm_y,sdxm_z) * rotation(math.pi/180 * Angle) * scale(sdxm_l,sdxm_w,sdxm_h) * Cube()
        水带箱=(水带箱体+水带箱门).color(1,0,0,1)
        text1= translate(100,-11,500)*rotation(Vec3(1,0,0),pi/2)*Text(text,100,100).color(225/255,225/255,225/255,1)
        
        水带箱=combine(水带箱,text1)
        水带箱=translate(Vec3(-325,-xyg_r/2-100-240,0))*水带箱


        self['临时消火栓']=combine(水带箱,下引管)



if __name__ == "__main__":
    place(临时消火栓())            
