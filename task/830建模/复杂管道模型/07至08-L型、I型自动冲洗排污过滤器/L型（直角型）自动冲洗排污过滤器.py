from pyp3d import *
import math

# '型号':[L, A, B, C, D, 进出水口DN1(mm), 排污口DN2(mm)],
# L表示过滤器整体高度，A、B、C、D为定位尺寸，DN1、DN2分别为进出水口和排污口公称通径
#A、B用来定位进出水口的位置，C、D用来定位排污口的位置
# unit_parameter = {
#     'L-40':  [350, 150, 120, 220, 90, 40, 13],
#     'L-50':  [382, 170, 125, 250, 100, 50, 13],
#     'L-65':  [420, 190, 140, 285, 120, 65, 19],
#     'L-80':  [480, 220, 150, 325, 140, 80, 25],
#     'L-100': [590, 290, 160, 415, 140, 100, 32],
#     'L-125': [660, 320, 200, 460, 200, 125, 38],
#     'L-150': [880, 420, 220, 610, 230, 150, 50],
#     'L-200': [1040, 550, 260, 750, 280, 200, 65],
#     'L-250': [1230, 650, 310, 890, 330, 250, 80],
#     'L-300': [1395, 750, 350, 1030, 380, 300, 100],
#     'L-350': [1680, 900, 420, 1240, 420, 350, 125],
#     'L-400': [1800, 1000, 470, 1340, 470, 400, 150],
#     'L-450': [2080, 1120, 510, 1510, 500, 450, 150],
#     'L-500': [2170, 1250, 550, 1655, 570, 500, 150],
#     'L-600': [2480, 1400, 610, 1900, 610, 600, 200],
#     'L-700': [2820, 1600, 650, 2140, 650, 700, 200],
#     'L-800': [3150, 1745, 760, 2340, 760, 800, 200],
#     'L-900': [3380, 1900, 810, 2560, 810, 900, 200],
#     'L-1000': [3680, 2220, 860, 2780, 860, 1000, 250],
#     'L-1100': [4230, 2490, 960, 3280, 960, 1100, 250],
#     'L-1200': [4500, 2700, 1010, 3540, 1010, 1200, 250],
#     'L-1500': [5500, 3390, 1260, 4380, 1260, 1500, 250]
# }

# marque_list = [
#     'L-40', 'L-50', 'L-65', 'L-80', 'L-100',
#     'L-125', 'L-150', 'L-200', 'L-250', 'L-300',
#     'L-350', 'L-400', 'L-450', 'L-500', 'L-600',
#     'L-700', 'L-800', 'L-900', 'L-1000', 'L-1100',
#     'L-1200', 'L-1500', '自定义'
# ]

# def get_parameter_by_marque(marque):
#     if marque in unit_parameter:
#         return unit_parameter[marque]
#     # 自定义型号返回默认值
#     return [0, 0, 0, 0, 0, 0, 0]

class L型直角式自动冲洗排污过滤器(Component):
    def __init__(self):
        Component.__init__(self)
        self['名称']=Attr('L型直角式自动冲洗排污过滤器',  obvious=True, readonly=True)
        self['型号']=Attr('L-40', obvious=True)
        
        # 定义参数（固定参数值）

        self['设备总长L']=Attr(350, obvious=True, readonly=False)
        self['进出口水平距A']=Attr(150, obvious=True, readonly=False)
        self['进出口垂向距B']=Attr(70, obvious=True, readonly=False)
        self['排污口水平距C']=Attr(220, obvious=True, readonly=False)
        self['排污口垂向距D']=Attr(90, obvious=True, readonly=False)
        self['进出口DN1']=Attr(40, obvious=True, readonly=False)
        self['排污口DN2']=Attr(13, obvious=True, readonly=False)
        self['过滤网规格 (mm)']=Attr(2.0, obvious=True, combo=[1.5, 2.0, 2.5])
        self['最大工作压力 (MPa)']=Attr(1.6, obvious=True, readonly=False)

        # 初始化时更新参数
        # self.update_params()  
        #管口增加驱动点
        self.setDrivenFeaturePoint('point02', SnapMode.Center, '[定位点X]', '[定位点Y]' ,'[定位点Z]')
        self.setDrivenFeaturePoint('point03', SnapMode.Center, '[定位点X]+[进出口水平距A]', '[定位点Y]' ,'[定位点Z]+[进出口垂向距B]')
        self.setDrivenFeaturePoint('point04', SnapMode.Center, '[定位点X]+[排污口水平距C]', '[定位点Y]' ,'[定位点Z]-[排污口垂向距D]')

        self['L型直角式自动冲洗排污过滤器']=Attr(None, show=True)
        self.replace()

    # def update_params(self):
    #     # 获取型号参数
    #     marque = self['型号']
        
    #     # 如果不是自定义型号，根据型号更新参数
    #     if marque != '自定义':
    #         params = get_parameter_by_marque(marque)
            
    #         #根据型号动态计算并更新参数值
    #         self['设备总长L'] = params[0]
    #         self['进出口水平距A'] = params[1]
    #         self['进出口垂向距B'] = params[2]
    #         self['排污口水平距C'] = params[3]
    #         self['排污口垂向距D'] = params[4]
    #         self['进出口DN1'] = params[5]
    #         self['排污口DN2'] = params[6]

                  
    @export
    def replace(self):   
        # 先更新参数（如果用户修改了型号）
        # self.update_params() 
        # 获取所有参数
        A = self['进出口水平距A']  #进出口水平距
        B = self['进出口垂向距B']  #进出口垂向距
        C = self['排污口水平距C']  #排污口水平距
        D = self['排污口垂向距D']  #排污口垂向距
        L = self['设备总长L']  #过滤器总高度
        DN1 = self['进出口DN1']  #进出口公称通径
        DN2 = self['排污口DN2']  #排污口公称通径   
        #进水口
        HR1 = 3*DN1/4  #进水口圆环外半径
        HW1 = B/9  #进水口圆环厚度
        ZR1 = 11*DN1/20  #进水口柱体半径
        ZW1 = int(HW1*3/2)  #进水口柱体高度
        Hr1 = DN1/2  #进水口圆环内半径
        H1 = HW1+ZW1  #进水口总高度
        #出水口
        HR2 = HR1  #出水口圆环外半径
        HW2 = B/9  #出水口圆环厚度
        ZR2 = 11*DN1/20  #出水口柱体半径
        ZW2 = 7*B/9-DN1/4  #出水口柱体高度
        Hr2 = DN1/2  #出水口圆环内半径
        #排污口
        HR3 = 3*DN2/4  #排污口圆环外半径
        HW3 = D/9  #排污口圆环厚度
        ZR3 = 11*DN2/20  #排污口柱体半径
        ZW3 = 55*D/72-DN1/4  #排污口柱体高度
        Hr3 = DN2/2  #排污口圆环内半径
        #主壳体
        Tr = ZR1  #主壳体圆台小圆半径
        TR = Tr+B/9+20  #主壳体圆台大圆半径即柱体半径
        TW = int(L/7)  #主壳体圆台高度
        ZW4 = C+L/10  #主壳体柱体高度
        HR4 = TR+0.15*TR+0.1*DN1  #主壳体连接环半径
        HW4 = HW1  #主壳体连接环厚度
        H2 = TW+ZW4+HW4  #主壳体总高度
        #处理器
        HR5 = HR4  #处理器圆环外半径
        HW5 = HW4  #处理器圆环厚度
        H3 = L-H1-H2  #处理器总高度
        Tb = H3-HW5 #椭球体半径
        Ta = TR #椭球体长度/2

        #阀门
        HR6 = TR/3  #阀门圆盘半径
        HW6 = HW1  #阀门圆盘厚度
        Hr6 = TR/5  #穿壳圆柱体半径
        Hw6 = 2*TR+0.12*TR+20  #穿壳圆柱体高度

        # 创建进水口模型
        self['进水口圆环'] = Cone(Vec3(0, 0, 0), Vec3(HW1, 0, 0), HR1, HR1)
        self['进水口柱体'] = translate(HW1, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW1, 0, 0), ZR1, ZR1)
        self['进水口空腔'] = Cone(Vec3(0, 0, 0), Vec3(HW1+ZW1, 0, 0), Hr1, Hr1)
        part1 = self['进水口圆环'] + self['进水口柱体'] - self['进水口空腔']

        # 创建出水口模型
        self['出水口圆环'] = Cone(Vec3(0, 0, 0), Vec3(0, 0,-HW2), HR2, HR2)
        self['出水口柱体'] = translate(0, 0, -HW2) * Cone(Vec3(0, 0, 0), Vec3(0, 0, -ZW2), ZR2, ZR2)
        self['出水口空腔'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, -(HW2+ZW2)), Hr2, Hr2)
        part2 = self['出水口圆环'] + self['出水口柱体'] - self['出水口空腔']
        part2 = translate(A, 0, B) * part2

        # 创建排污口模型
        self['排污口圆环'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, HW3), HR3, HR3)
        self['排污口柱体'] = translate(0, 0, HW3) * Cone(Vec3(0, 0, 0), Vec3(0, 0, ZW3), ZR3, ZR3)
        self['排污口空腔'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, HW3+ZW3), Hr3, Hr3) 
        part3 = self['排污口圆环'] + self['排污口柱体'] - self['排污口空腔']
        part3 = translate(C, 0, -D) * part3
        
        # 创建主壳体模型
        self['圆台'] = Cone(Vec3(0, 0, 0), Vec3(TW, 0, 0), Tr, TR)
        self['柱体'] = translate(TW, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW4, 0, 0), TR, TR)
        self['主壳体连接环'] = translate(TW+ZW4, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(HW4, 0, 0), HR4, HR4)
        self['主壳体'] = self['圆台'] + self['柱体'] + self['主壳体连接环']
        part4 = translate(H1, 0, 0) * self['主壳体']

        # 创建处理器模型
        self['处理器连接环'] = Cone(Vec3(0, 0, 0), Vec3(HW5, 0, 0), HR5, HR5)
        Line1 = roty(pi/2)*Line(scale(Ta)*Arc(pi*2))
        Section1 = scale(Tb,Ta)*Section(Arc(pi))
        FinalSphere = Sweep(Section1,Line1)
        self['椭球体'] = translate(HW5, 0, 0) * FinalSphere
        part5 = self['处理器连接环'] + self['椭球体']
        part5 = translate(H1+H2, 0, 0) * part5

         # 创建阀门模型
        self['穿壳柱体'] = translate(0, 0, HW6) * Cone(Vec3(0, 0, 0), Vec3(0, 0, Hw6), Hr6, Hr6)
        self['阀门圆盘'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, HW6), HR6, HR6)
        self['阀门'] = self['阀门圆盘'] + self['穿壳柱体']
        part6 = translate(A-HR2-Hr6-0.01*L-5, 0, -HW6-1.06*TR-10) * self['阀门']
        
        # 组合所有部件
        self['L型直角式自动冲洗排污过滤器'] = combine(part1, part2, part3, part4, part5, part6)
        

if __name__ == "__main__":
    FinalGeometry = L型直角式自动冲洗排污过滤器()
    place(FinalGeometry)
