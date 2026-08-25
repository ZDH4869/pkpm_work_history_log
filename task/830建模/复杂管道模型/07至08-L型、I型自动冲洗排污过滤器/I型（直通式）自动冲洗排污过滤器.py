from pyp3d import *
import math

# I型直通式自动冲洗排污过滤器参数表
# '型号':[L, A, B, D, 进出水口DN1(mm), 排污口DN2(mm)]
#A、D定位排污口，B定位阀门垂向位置，L设备总长，DN1、DN2进出口公称通径
# unit_parameter = {
#     'I-40':  [248, 150, 70, 90, 40, 13],
#     'I-50':  [278, 180, 80, 100, 50, 13],
#     'I-65':  [315, 210, 86, 120, 65, 19],
#     'I-80':  [375, 265, 110, 140, 80, 25],
#     'I-100': [428, 340, 128, 140, 100, 32],
#     'I-125': [560, 400, 162, 200, 125, 38],
#     'I-150': [700, 500, 189, 230, 150, 50],
#     'I-200': [870, 620, 220, 280, 200, 65],
#     'I-250': [1080, 780, 255, 330, 250, 80],
#     'I-300': [1280, 920, 290, 380, 300, 100],
#     'I-350': [1580, 1140, 330, 420, 350, 125],
#     'I-400': [1860, 1300, 377, 470, 400, 150],
#     'I-450': [1800, 1340, 420, 500, 450, 150],
#     'I-500': [2030, 1470, 462, 570, 500, 150],
#     'I-600': [2440, 1750, 537, 610, 600, 200],
#     'I-700': [2850, 2140, 607, 650, 700, 200],
#     'I-800': [3040, 2340, 685, 760, 800, 200],
#     'I-900': [3300, 2550, 785, 810, 900, 200],
#     'I-1000': [3580, 2780, 860, 860, 1000, 250],
#     'I-1100': [4130, 3280, 915, 960, 1100, 250],
#     'I-1200': [4400, 3540, 965, 1010, 1200, 250],
#     'I-1500': [5400, 4380, 1220, 1260, 1500, 250]
# }

# marque_list = [
#     'I-40', 'I-50', 'I-65', 'I-80', 'I-100',
#     'I-125', 'I-150', 'I-200', 'I-250', 'I-300',
#     'I-350', 'I-400', 'I-450', 'I-500', 'I-600',
#     'I-700', 'I-800', 'I-900', 'I-1000', 'I-1100',
#     'I-1200', 'I-1500', '自定义'
# ]

# def get_parameter_by_marque(marque):
#     """根据型号获取参数列表"""
#     if marque in unit_parameter:
#         return unit_parameter[marque]
#     # 自定义型号返回默认值
#     return [0, 0, 0, 0, 0, 0]

class I型直通式自动冲洗排污过滤器(Component):
    def __init__(self):
        Component.__init__(self)
        self['名称']=Attr('I型直通式自动冲洗排污过滤器',  obvious=True, readonly=True)
        self['型号']=Attr('I-40', obvious=True)
        
        # 定义参数（固定参数值）

        self['设备总长L']=Attr(248, obvious=True, readonly=False)
        self['排污口水平距A']=Attr(150, obvious=True, readonly=False)
        self['阀门垂向距B']=Attr(70, obvious=True, readonly=False)
        self['排污口垂向距D']=Attr(90, obvious=True, readonly=False)
        self['进出口DN1']=Attr(40, obvious=True, readonly=False)
        self['排污口DN2']=Attr(13, obvious=True, readonly=False)
        self['过滤网规格 (mm)']=Attr(2.0, obvious=True, combo=[1.5, 2.0, 2.5])
        self['最大工作压力 (MPa)']=Attr(1.6, obvious=True, readonly=False)

        # 初始化时更新参数
        # self.update_params()  
        #管口增加驱动点
        self.setDrivenFeaturePoint('point01', SnapMode.Center, '[定位点X]', '[定位点Y]' ,'[定位点Z]')
        self.setDrivenFeaturePoint('point02', SnapMode.Center, '[定位点X]+[设备总长L]', '[定位点Y]' ,'[定位点Z]')
        self.setDrivenFeaturePoint('point03', SnapMode.Center, '[定位点X]+[排污口水平距A]', '[定位点Y]' ,'[定位点Z]-[排污口垂向距D]')

        self['I型直通式自动冲洗排污过滤器']=Attr(None, show=True)
        self.replace()

    # def update_params(self):
    #     # 获取型号参数
    #     marque = self['型号']
        
    #     # 如果不是自定义型号，根据型号更新参数
    #     if marque != '自定义':
    #         params = get_parameter_by_marque(marque)
            
    #         #根据型号动态计算并更新参数值
    #         self['设备总长L'] = params[0]
    #         self['排污口水平距A'] = params[1]
    #         self['阀门垂向距B'] = params[2]
    #         self['排污口垂向距D'] = params[3]    
    #         self['进出口DN1'] = params[4]
    #         self['排污口DN2'] = params[5]
           
                  
    @export
    def replace(self):   
        # 先更新参数（如果用户修改了型号）
        # self.update_params() 
        # 获取所有参数
        A = self['排污口水平距A']  #排污口水平距
        B = self['阀门垂向距B']  #阀门垂向距
        D = self['排污口垂向距D']  #排污口垂向距
        L = self['设备总长L']  #过滤器总高度
        DN1 = self['进出口DN1']  #进出口公称通径
        DN2 = self['排污口DN2']  #排污口公称通径   
        #进水口
        #进水口圆环半径=0.5*B，进水口圆环厚度=H，进水口柱体半径=B/3,柱体厚度=H_p
        HR1 = 3*DN1/4  #进水口圆环外半径
        HW1 = B/9  #进水口圆环厚度
        ZR1 = 11*DN1/20  #进水口柱体半径
        ZW1 = int(HW1*3/2)  #进水口柱体高度
        Hr1 = DN1/2  #进水口圆环内半径
        H1 = HW1+ZW1  #进水口总高度
        #出水口
        HR2 = HR1  #出水口圆环外半径
        HW2 = HW1  #出水口圆环厚度
        ZR2 = 11*DN1/20  #出水口柱体半径
        ZW2 = ZW1  #出水口柱体高度
        Hr2 = DN1/2  #出水口圆环内半径
        H2 = HW2+ZW2  #出水口总高度
        #排污口
        HR3 = 3*DN2/4  #排污口圆环外半径
        HW3 = HW1  #排污口圆环厚度
        ZR3 = 11*DN2/20  #排污口柱体半径
        ZW3 = 55*D/72-DN1/4  #排污口柱体高度
        Hr3 = DN2/2  #排污口圆环内半径
        #主壳体
        Tr = ZR1  #主壳体圆台小圆半径
        TR = Tr+B/9+20  #主壳体圆台大圆半径即柱体半径
        TW = 7*L/72  #主壳体圆台高度
        ZW4 = L-H1-H2-2*TW  #主壳体柱体高度

        #阀门
        HR5 = TR/3  #阀门圆盘半径
        HW5 = HW1  #阀门圆盘厚度
        Hr5 = TR/6  #穿壳圆柱体半径
        Hw5 = B+TR  #穿壳圆柱体高度

        # 创建进水口模型
        self['进水口圆环'] = Cone(Vec3(0, 0, 0), Vec3(HW1, 0, 0), HR1, HR1)
        self['进水口柱体'] = translate(HW1, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW1, 0, 0), ZR1, ZR1)
        self['进水口空腔'] = Cone(Vec3(0, 0, 0), Vec3(HW1+ZW1, 0, 0), Hr1, Hr1)
        part1 = self['进水口圆环'] + self['进水口柱体'] - self['进水口空腔']

         # 创建出水口模型
        self['出水口圆环'] = Cone(Vec3(0, 0, 0), Vec3(-HW2, 0,0), HR2, HR2)
        self['出水口柱体'] = translate(-HW2, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(-ZW2, 0, 0), ZR2, ZR2)
        self['出水口空腔'] = Cone(Vec3(0, 0, 0), Vec3(-(HW2+ZW2), 0, 0), Hr2, Hr2)
        part2 = self['出水口圆环'] + self['出水口柱体'] - self['出水口空腔']
        part2 = translate(L, 0, 0) * part2

        # 创建排污口模型
        self['排污口圆环'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, HW3), HR3, HR3)
        self['排污口柱体'] = translate(0, 0, HW3) * Cone(Vec3(0, 0, 0), Vec3(0, 0, ZW3), ZR3, ZR3)
        self['排污口空腔'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, HW3+ZW3), Hr3, Hr3) 
        part3 = self['排污口圆环'] + self['排污口柱体'] - self['排污口空腔']
        part3 = translate(A, 0, -D) * part3
        
        # 创建主壳体模型
        self['圆台1'] = Cone(Vec3(0, 0, 0), Vec3(TW, 0, 0), Tr, TR)
        self['柱体'] = translate(TW, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW4, 0, 0), TR, TR)
        self['圆台2'] = translate(TW+ZW4, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(TW, 0, 0), TR, Tr)
        self['主壳体'] = self['圆台1'] + self['柱体'] + self['圆台2']
        part4 = translate(H1, 0, 0) * self['主壳体']

         # 创建阀门模型
        self['穿壳柱体'] = translate(0, 0, -HW5) * Cone(Vec3(0, 0, 0), Vec3(0, 0, -Hw5), Hr5, Hr5)
        self['阀门圆盘'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, -HW5), HR5, HR5)
        self['阀门'] = self['阀门圆盘'] + self['穿壳柱体']
        part5 = translate(A-2*ZW4/3+20, 0, B) * self['阀门']

        
        # 组合所有部件
        self['I型直通式自动冲洗排污过滤器'] = combine(part1, part2, part3, part4, part5)
        

if __name__ == "__main__":
    FinalGeometry = I型直通式自动冲洗排污过滤器()
    place(FinalGeometry)
