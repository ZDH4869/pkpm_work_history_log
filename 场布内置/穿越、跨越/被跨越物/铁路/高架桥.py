from pyp3d import *
# 放样体
class 高架桥(Component):
      def __init__(self):
            Component.__init__(self)
            self['长'] = Attr(30000.0, obvious=True, group='桥参数')
            self['宽'] = Attr(15000, obvious=True, group='桥参数')
            self['高'] = Attr(3000, obvious = True, group='桥参数')
            self['桥墩宽'] = Attr(2500, obvious = True, group='桥参数')
            self['桥墩间距'] = Attr(20000, obvious = True, group='桥参数')
            self['人行道宽'] = Attr(1650, obvious = True, group='桥参数')
            self['挡土墙高'] = Attr(750, obvious = True, group='桥参数')
            self['标高'] = Attr(0, obvious = True, group='桥参数')
            self['铁轨宽度'] = Attr(4000.0, obvious=True, group='铁轨参数')
            self['枕木间距'] = Attr(700, obvious = True, group='铁轨参数')
            self['铁轨间距'] = Attr(1000, obvious = True, group='铁轨参数')

            self['构件类型'] = Attr('被跨越物', obvious = True, group='构件分类',readonly = True)
            self['应用场景'] = Attr('铁路', obvious = True, group='构件分类',readonly = True)
            self['构件名称'] = Attr('铁路围栏', obvious = True, group='构件分类')
            self['围栏上端是否显示'] = Attr('是', obvious=True, group='构件分类')
#围栏尺寸
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
            self['桥'] = Attr(None, show=True)
            self.replace()
      @export
      def replace(self):
            L = self['长']
            b = self['宽']
            h = self['高']
            h0 = self['标高']
            h1 = self['挡土墙高']
            h2 = self['枕木间距']
            b1 = self['桥墩宽']
            b2 = self['桥墩间距']
            b3 = self['人行道宽']
            b4 = self['铁轨宽度']
            b7 = self['铁轨间距']
            H = self['围栏高度']
            W = self['单段围栏宽度']
            D = self['边框角钢边长']
            a1 = self['立柱长']
            b5 = self['立柱宽']
            a2 = self['基础长']
            b6 = self['基础宽']
            H1 = self['基础厚']
            k  = self['围栏上端是否显示']
            
#桥底面
#桥底面截面
            section1 = to_section(Vec3(0,0,0), Vec3(400,0,0),Vec3(1092,0,-400),Vec3(3000,0,-400), Vec3(3400,0,0), Vec3(b-3400,0,0), Vec3(b-3000,0,-400), Vec3(b-1092,0,-400), Vec3(b-400,0,0), Vec3(b,0,0), Vec3(b,0,200), Vec3(0,0,200))
# 桥底面放样
            qiaomian1 = Loft(section1, translate(0,L,0) * section1) .color(1,1,1,1)

#桥墩
   #1
            section2 = to_section(Vec3(800,0,-h), Vec3(800+b1,0,-h),Vec3(800+b1,b1,-h), Vec3(800,b1,-h))
            loft2 = Loft(section2, translate(0,0,h) * section2).color(1,1,1,1)
   #2
            section3 = to_section(Vec3(b-800-b1,0,-h), Vec3(b-800,0,-h),Vec3(b-800,b1,-h), Vec3(b-800-b1,b1,-h))
            loft3 = Loft(section3, translate(0,0,h) * section3).color(1,1,1,1)

            qiaodun1 = combine(loft2,loft3)
#对桥墩阵列
# 转为 Array
            qiaodun = Array(qiaodun1)
# 线性排布
            for i in linspace(Vec3(0,10,0),Vec3(0,L-b2,0),int(L/b2)): 
# 将 Test_Array 依次平移并添加到这十一个点上，并存于 Test_Array 中
                  qiaodun.append(translate(i)) 

# 桥顶面
# 桥顶面截面
            section4 = to_section(Vec3(0,0,0), Vec3(-100,0,0),Vec3(-200,0,200),Vec3(-100,0,600), Vec3(b3+200,0,600), Vec3(b3+200,0,800), Vec3(b-b3-200,0,800), Vec3(b-b3-200,0,600), Vec3(b+100,0,600), Vec3(b+200,0,200), Vec3(b+100,0,0), Vec3(b,0,0), Vec3(b,0,200), Vec3(0,0,200))
            qiaomian2 = Loft(section4, translate(0,L,0) * section4).color(1,1,1,1)

# 挡渣墙
# 截面
            section5 = to_section(Vec3(b3+100,0,600), Vec3(b3+200,0,600),Vec3(b3+200,0,600+h1),Vec3(b3+100,0,600+h1))
# 放样
            dangtuqiang1 = Loft(section5, translate(0,L,0) * section5).color(1,1,1,1)
            dangtuqiang2 = translation(b-2*b3-300,0,0) *dangtuqiang1

# 人行道扶手
 # 扶手1
            section6 = to_section(Vec3(75,51,750), Vec3(225,51,750),Vec3(225,51,800),Vec3(75,51,800))
            fushou1 = Loft(section6, translate(0,L,0) * section6).color(1,1,1,1)
 # 扶手2
            section7 = to_section(Vec3(225,51,1020), Vec3(225,51,1070),Vec3(75,51,1070),Vec3(75,51,1020))
            fushou2 = Loft(section7, translate(0,L,0) * section7).color(1,1,1,1)

 # 扶栏
            section14 = to_section(Vec3(205,0,770), Vec3(205,0,1070),Vec3(95,0,1070),Vec3(95,0,770))
            fulan1 = Loft(section14, translate(0,80,0) * section14).color(1,1,1,1)
      # fulan1阵列
      # 转为 Array
            fulan1_1 = Array(fulan1)
      # 线性排布
            for i in linspace(Vec3(0,280,0),Vec3(0,L-280,0),int(L/280)): 
                  fulan1_1.append(translate(i))

      
 # 柱
            section9 = to_section(Vec3(0,0,600), Vec3(300,0,600),Vec3(300,0,700),Vec3(0,0,700))
            zhu1 = Loft(section9, translate(0,300,0) * section9)

            section10 = to_section(Vec3(250,50,700), Vec3(250,50,1070),Vec3(50,50,1070),Vec3(50,50,700))
            zhu2 = Loft(section10, translate(0,200,0) * section10)

            section11 = to_section(Vec3(300,0,1070), Vec3(300,0,1150),Vec3(0,0,1150),Vec3(0,0,1070))
            zhu3 = Loft(section11, translate(0,300,0) * section11)

            section12 = to_section(Vec3(270,30,1150), Vec3(270,30,1200),Vec3(30,30,1200),Vec3(30,30,1150))
            zhu4 = Loft(section12, translate(0,240,0) * section12)

            self['05'] = combine(zhu1,zhu2)
            self['06'] = combine(self['05'],zhu3)
            zhu5 = combine(self['06'],zhu4).color(1,1,1,1)

      # zhu5阵列
      # 转为 Array
            zhu5_1 = Array(zhu5)
      # 线性排布
            for i in linspace(Vec3(0,0,0),Vec3(0,L-840,0),int(L/1500)): 
                  zhu5_1.append(translate(i))
            zhu5_2 = translate(b-300,0,0)*zhu5_1
# 组合

            self['07'] = combine(fushou1,fushou2)
            self['03'] = combine(self['07'],fulan1_1)
            self['04'] = translate(b-300,0,0)*self['03']





#铁轨
#铁轨底部
# 截面
            section101 = to_section(Vec3(0, 0, 0), Vec3(64,0, 0),Vec3(66,0,2), Vec3(66,0,6.5), Vec3(62,0,10.5),Vec3(24,0,21), Vec3(0,0,27),Vec3(-24,0,21), Vec3(-62,0,10.5), Vec3(-66,0,6.5), Vec3(-66,0,2), Vec3(-64,0,0)).color(1,0,0,1)
            section102 = translate(Vec3(64,0,2))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(2)*Arc(2*pi)).color(1,0,0,1) 
            section103 = translate(Vec3(62,0,6.5))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(4)*Arc(2*pi)).color(1,0,0,1)
            section104 = translate(Vec3(-64,0,2))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(2)*Arc(2*pi)).color(1,0,0,1) 
            section105 = translate(Vec3(-62,0,6.5))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(4)*Arc(2*pi)).color(1,0,0,1)
# #底部放样
            loft101 = Loft(section101, translate(0,L,0) * section101) 
            loft102 = Loft(section102, translate(0,L,0) * section102) 
            loft103 = Loft(section103, translate(0,L,0) * section103)
            loft104 = Loft(section104, translate(0,L,0) * section104) 
            loft105 = Loft(section105, translate(0,L,0) * section105)


            lofta = loft101 + loft102 + loft103 + loft104 + loft105

# 铁轨中部
# 截面
            section106 = to_section(Vec3(0,0,27),Vec3(24,0,21),Vec3(9,0,36.7),Vec3(9.7,0,105.2),Vec3(15.4,0,113.8),Vec3(-15.4,0,113.8),Vec3(-9.7,0,105.2),Vec3(-9,0,36.7),Vec3(-24,0,21),Vec3(0,0,27)).color(1,0,0,1)
            section107 = translate(Vec3(28,0,36))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(20)*Arc(2*pi)).color(1,0,0,1)
            section108 = translate(Vec3(-28,0,36))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(20)*Arc(2*pi)).color(1,0,0,1)

# 中部放样
            loft106 = Loft(section106, translate(0,L,0) * section106)   
            loft107 = Loft(section107, translate(0,L,0) * section107)
            loft108 = Loft(section108, translate(0,L,0) * section108)

            loftb = loft106 - loft107 - loft108
# 铁轨上部
# 截面      
            section109 = to_section(Vec3(0,0,110),Vec3(35,0,118.7),Vec3(35,0,138.7),Vec3(23,0,152),Vec3(-23,0,152),Vec3(-35,0,138.7),Vec3(-35,0,118.7),Vec3(0,0,110)).color(1,0,0,1)
            section110 = translate(Vec3(22,0,138))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(13,14)*Arc(2*pi)).color(1,0,0,1)
            section111 = translate(Vec3(-22,0,138))*rotation(Vec3(1,0,0),pi*0.5)*Section(scale(13,14)*Arc(2*pi)).color(1,0,0,1)
# 底部放样
            loft109 = Loft(section109, translate(0,L,0) * section109)
            loft110 = Loft(section110, translate(0,L,0) * section110)
            loft111 = Loft(section111, translate(0,L,0) * section111)

            loftc = loft109 + loft110 +loft111
      # 上中下组合
            loftd = lofta + loftb + loftc
      # 生成左右铁轨
            lofte = translate(0.5*b4-66,0,584) * loftd.color(0,0,0,1)
            loftf = translate(-0.5*b4+66,0,584) * loftd.color(0,0,0,1)





# 枕木
      # 截面
            section112 = to_section(Vec3(0,0,0),Vec3(0,600,0),Vec3(0,570,584),Vec3(0,30,584)).color(1,0,0,1) 
      # 截面放样
            loft112 = Loft(translate(-0.5*b4-500,0,0) * section112,translate(0.5*b4+500,0,0) * section112).color(0.41,0.41,0.41,1)
      # 线性排布
            zhenmu = Array(loft112)   
            for i in linspace(Vec3(0,0,0),Vec3(0,int(L/(h2 + 600))*(h2 + 600),0),int(L/(h2 + 600))):
                  zhenmu.append(translate(i))

# 组合
            zuhe = Combine(zhenmu,lofte,loftf) 
            tiegui = translate(b4/2+b3+800,0,500)*zuhe
      # 铁轨阵列
      # 转为 Array
            tiegui_1 = Array(tiegui)
      # 线性排布
            for i in linspace(Vec3(0,0,0),Vec3(b-b3*2-1450-b4,0,0),int((b-b3*2-1450)/(b4+b7))): 
                  tiegui_1.append(translate(i))



# 铁路栏杆
#立柱
            Col1= scale(a1,b5,H) * Cube()
            self['立柱高'] = Attr(H, obvious=True, group='立柱尺寸',readonly = True)
#立柱文本
            Text1= translation(a1/4,-a1/2,H*4/5)*rotate(Vec3(1,0,0), pi/2)*Text('禁',a1/4,a1)
            Text2= translation(a1/4,-a1/2,H*3/5)*rotate(Vec3(1,0,0), pi/2)*Text('止',a1/4,a1)
            Text3= translation(a1/4,-a1/2,H*2/5)*rotate(Vec3(1,0,0), pi/2)*Text('入',a1/4,a1)
            Text4= translation(a1/4,-a1/2,H*1/5)*rotate(Vec3(1,0,0), pi/2)*Text('内',a1/4,a1)
            Text5= Combine(Text1,Text2,Text3,Text4)
            Col= Combine(Text5,Col1)
#基础
            Base= translation(-(a2-a1)/2,-b6/2,0)*scale(a2,b6,-H1) * Cube()

#栏杆边框
            Cube1= translation(a1+40,D/4,D)*scale(W,D,H-D) * Cube()
            Cube2= translation(a1+40+D,D/4,2*D)*scale(W-D*2,D,H-D-2*D) * Cube()
            Cube3= Cube1-Cube2
            Cube4= translation(a1+40+(W-D)/2,D/4,2*D)*scale(D,D,H-D-2*D) * Cube()
            Cube_frame=(Cube3+Cube4).color(0,0.4,0,1)
#连接
            Cube5= translation(a1,0,H/4)*scale(30,10,30) * Cube().color(0.8,0.8,0.8,1)
            Cube6= translation(a1+10,10,H/4)*scale(30,10,30) * Cube().color(0.8,0.8,0.8,1)
            Section201= rotate(Vec3(1,0,0), pi/2)*Section(scale(5) * Arc(2*pi))
            Loft201= translation(a1+20,0,H/4+15)*Loft(Section201, translate(0,20,0) * Section201).color(0.8,0.8,0.8,1)
            Cube_c1= Combine(Loft201,Cube5,Cube6)
            Cube_c2= translation(0,0,H/4)*Cube_c1
            Cube_c3= translation(0,0,H/4)*Cube_c2
            Cube_con1= Combine(Cube_c1,Cube_c2,Cube_c3)
            Cube_con2= translation(W+D,0,H)*rotate(Vec3(a1+40,1,0), pi)*Cube_con1
            Cube_con= translation(0,a1/2,0)*Combine(Cube_con1,Cube_con2)
            if H1== 0:
                  CUBE_1 = Combine(Cube_con,Cube_frame,Col)
            else:
                  CUBE_1 = Combine(Cube_con,Cube_frame,Col,Base)
#铁丝网
            Section202= rotate(Vec3(0,1,0), pi/2)*Section(scale(5) * Arc(2*pi))
            Loft201= translation(a1+40+D,D/2,D+170)*Loft(Section202, translate(W-2*D,0,0) * Section202).color(0,0.4,0,1)

            Section203= Section(scale(5) * Arc(2*pi))
            Loft202= translation(a1+100+D,D/2,2*D)*Loft(Section203, translate(0,0,H-2*D) * Section203).color(0,0.4,0,1)

    #上端横向铁丝
            wet_up1= translation(0,0,H-2*D-100)*Loft201
            wet_up2= translation(0,-20,80)*wet_up1
            wet_up3= translation(0,-70,120)*wet_up2
            wet_up=Combine(wet_up1,wet_up2,wet_up3)
    #上端竖向铁丝
            Loft203= rotate(Vec3(1,0,0), pi/6)*Loft(Section203, translate(0,0,210) * Section203).color(0,0.4,0,1)
            wet_A=translation(a1+100+D,D/2,H+70)*Loft203
            Loft204= translation(a1+100+D,D/2,H)*Loft(Section203, translate(0,0,70) * Section203).color(0,0.4,0,1)
            wet_C=Combine(Loft204,wet_A)

            LeftUP_Array = Array(wet_C)
            n2=int((W-2*D)/60)
            for i in linspace(Vec3(0,0,0),Vec3(W-2*D-60,0,0),n2):
                  LeftUP_Array.append(translate(i))
            WET3= LeftUP_Array

    #横向铁丝 
            Up_Array = Array(Loft201)
            n1=int((H-D-2*D)/120)
            for i in linspace(Vec3(0,0,0),Vec3(0,0,H-170-2*D),n1):
                  Up_Array.append(translate(i))
            WET1= Up_Array
    #竖向铁丝
            Left_Array = Array(Loft202)
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
            n3=int((L)/(W+a1+80))
            for i in linspace(Vec3(0,0,0),Vec3((n3-1)*(W+a1+80),0,0),n3):
                  ALL_Array.append(translate(i))
            Fin_geo= ALL_Array
            self['放样体'] = Fin_geo
            langan1 = rotation(Vec3(0,0,1),.5*pi) * self['放样体']
            langan2 = translate(0,0,600)*langan1


            self['1'] = combine(qiaomian1,qiaodun)
            self['2'] = combine(self['1'],self['04'])
            self['3'] = combine(self['2'],tiegui_1)
            self['4'] = combine(self['3'],qiaomian2)
            self['5'] = combine(self['4'],dangtuqiang1)
            self['6'] = combine(self['5'],zhu5_2)
            self['7'] = combine(self['6'],dangtuqiang2)
            self['8'] = combine(self['7'],langan2)

            self['桥'] = translate(-b/2,0,h+h0)*self['8']


if __name__ == "__main__":

 FinalGeometry = rotation(Vec3(0,0,1),1.5*pi) * 高架桥()
 # 第二行 实现两点布置
 TwoPointPlace.linearize(FinalGeometry,'长')
 place(FinalGeometry)



#  place(高架桥())



