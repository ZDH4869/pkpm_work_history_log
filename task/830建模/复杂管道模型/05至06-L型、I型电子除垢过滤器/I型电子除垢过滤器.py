from pyp3d import *
import math

# '型号':[定位尺寸(mm)：A,B,C,  过滤器高度：L,
# 进出口DN1(mm),排污口DN2(mm),
# 输入功率 (W),处理流量 (T/H)],
# A、B用来定位进出口，C用来定位排污口，L表示过滤器整体高度
# unit_parameter = {
#     'I-40':  [150, 90, 368, 548, 40, 13, 20, 6],
#     'I-50':  [180, 100, 372, 578, 50, 13, 20, 9],
#     'I-65':  [210, 120, 380, 615, 65, 19, 20, 14],
#     'I-80':  [265, 140, 395, 675, 80, 25, 20, 25],
#     'I-100': [340, 180, 413, 728, 100, 32, 40, 40],
#     'I-125': [400, 200, 441, 860, 125, 38, 40, 60],
#     'I-150': [500, 230, 468, 1000, 150, 50, 60, 90],
#     'I-200': [620, 280, 510, 1170, 200, 65, 120, 160],
#     'I-250': [780, 330, 552, 1380, 250, 80, 180, 240],
#     'I-300': [920, 380, 585, 1580, 300, 100, 300, 350],
#     'I-350': [1140, 450, 744, 1880, 350, 125, 360, 480],
#     'I-400': [1300, 480, 818, 2100, 400, 150, 420, 620],
#     'I-450': [1340, 500, 848, 2160, 450, 150, 420, 800],
#     'I-500': [1470, 580, 928, 2332, 500, 150, 500, 980],
#     'I-600': [1750, 610, 1016, 2740, 600, 200, 500, 1200],
#     'I-700': [2140, 660, 1088, 3150, 700, 200, 500, 1500],
#     'I-800': [2340, 760, 1168, 3340, 800, 200, 500, 1800],
#     'I-900': [2550, 810, 1248, 3600, 900, 200, 500, 2000],
#     'I-1000':[2780, 860, 1328, 3880, 1000, 250, 500, 2600]
# }

# marque_list = [
#     'I-40', 'I-50', 'I-65', 'I-80', 'I-100',
#     'I-125', 'I-150', 'I-200', 'I-250', 'I-300',
#     'I-350', 'I-400', 'I-450', 'I-500', 'I-600',
#     'I-700', 'I-800', 'I-900', 'I-1000', '自定义']

# def get_parameter_by_marque(marque):
#     if marque in unit_parameter:
#         return unit_parameter[marque]
#     # 自定义型号返回默认值
#     return [0, 0, 0, 0, 0, 0, 0, 0]

class I型电子除垢过滤器(Component):
    def __init__(self):
        Component.__init__(self)
        self['名称']=Attr('I型电子除垢过滤器',  obvious=True, readonly=True)
        self['型号']=Attr('I-40', obvious=True)
        
        # 定义参数（固定参数值）

        self['排污口水平距A']=Attr(150, obvious=True, readonly=False)
        self['排污口垂向距B']=Attr(90, obvious=True, readonly=False)
        self['处理器垂向距C']=Attr(368, obvious=True, readonly=False)
        self['设备总长L']=Attr(548, obvious=True, readonly=False)
        self['进出口DN1']=Attr(40, obvious=True, readonly=False)
        self['排污口DN2']=Attr(13, obvious=True, readonly=False)
        self['输入功率 (W)']=Attr(20, obvious=True, readonly=False)
        self['处理流量 (T/H)']=Attr(6, obvious=True, readonly=False)

        # 初始化时更新参数
        # self.update_params()  
        #管口增加驱动点
        self.setDrivenFeaturePoint('point01', SnapMode.Center, '[定位点X]', '[定位点Y]' ,'[定位点Z]')
        self.setDrivenFeaturePoint('point02', SnapMode.Center, '[定位点X]-[排污口水平距A]', '[定位点Y]' ,'[定位点Z]+[排污口垂向距B]')
        self.setDrivenFeaturePoint('point03', SnapMode.Center, '[定位点X]-[设备总长L]', '[定位点Y]' ,'[定位点Z]')

        self['I型电子除垢过滤器']=Attr(None, show=True)
        self.replace()

    # def update_params(self):
    #     # 获取型号参数
    #     marque = self['型号']
        
    #     # 如果不是自定义型号，根据型号更新参数
    #     if marque != '自定义':
    #         params = get_parameter_by_marque(marque)
            
    #         #根据型号动态计算并更新参数值
    #         self['排污口水平距A'] = params[0]
    #         self['排污口垂向距B'] = params[1]
    #         self['处理器垂向距C'] = params[2]
    #         self['设备总长L'] = params[3]
    #         self['进出口DN1'] = params[4]
    #         self['排污口DN2'] = params[5]
    #         self['输入功率 (W)'] = params[6]
    #         self['处理流量 (T/H)'] = params[7]
                  
    @export
    def replace(self):   
        # 先更新参数（如果用户修改了型号）
        # self.update_params() 
        # 获取所有参数
        A = self['排污口水平距A']  #排污口水平距
        B = self['排污口垂向距B']  #排污口垂向距
        C = self['处理器垂向距C']  #处理器垂向距
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
        HW2 = HW1  #出水口圆环厚度
        ZR2 = ZR1  #出水口柱体半径
        ZW2 = ZW1  #出水口柱体高度
        Hr2 = DN1/2  #出水口圆环内半径
        H2 = HW2+ZW2  #出水口总高度

        #排污口
        HR3 = 3*DN2/4  #排污口圆环外半径
        HW3 = DN2/6  #排污口圆环厚度
        ZR3 = 11*DN2/20  #排污口柱体半径
        ZW3 = 39*B/54-DN1/4  #排污口柱体高度B-B/9-B/6-20-DN1/4
        Hr3 = DN2/2  #排污口圆环内半径
        #主壳体
        Tr = ZR1  #主壳体圆台小圆半径
        TR = Tr+B/6+20  #主壳体圆台大圆半径即柱体半径
        TW = int(L/8)  #主壳体圆台高度
        ZW4 = L-H1-H2-2*TW  #主壳体柱体高度
        
        #处理器
        ZR52 = TR  #处理器上部柱体半径
        ZW52 = TR+(C-TR-2*HW1)/3  #处理器上部柱体高度
        ZR51 = ZR52+0.1*ZR52  #处理器下部柱体半径
        ZW51 = C-ZW52-2*HW1  #处理器下部柱体高度
        HR51 = ZR51+0.1*ZR51+20  #处理器下部连接法兰圆环半径
        HW51 = HW1  #处理器下部连接法兰圆环厚度
        HR52 = HR51  #处理器上部连接法兰圆环半径
        HW52 = HW1  #处理器上部连接法兰圆环厚度
        
        #把手
        HR6 = TR/3  #把手圆盘半径
        HW6 = HW1  #把手圆盘厚度
        Hr6 = TR/5  #穿壳圆柱体半径
        Hw6 = 2*TR+0.1*TR+20  #穿壳圆柱体高度
        l = L/8  #把手长度
        w = TR/6  #把手宽度
        h = B/15  #把手高度

        # 创建进水口模型
        self['进水口圆环'] = Cone(Vec3(0, 0, 0), Vec3(-HW1, 0, 0), HR1, HR1)
        self['进水口柱体'] = translate(-HW1, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(-ZW1, 0, 0), ZR1, ZR1)
        self['进水口空腔'] = Cone(Vec3(0, 0, 0), Vec3(-(HW1+ZW1), 0, 0), Hr1, Hr1)
        part1 = self['进水口圆环'] + self['进水口柱体'] - self['进水口空腔']

        # 创建出水口模型
        self['出水口圆环'] = Cone(Vec3(0, 0, 0), Vec3(HW2, 0,0), HR2, HR2)
        self['出水口柱体'] = translate(HW2, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW2, 0, 0), ZR2, ZR2)
        self['出水口空腔'] = Cone(Vec3(0, 0, 0), Vec3(HW2+ZW2, 0, 0), Hr2, Hr2)
        part2 = self['出水口圆环'] + self['出水口柱体'] - self['出水口空腔']
        part2 = translate(-L, 0, 0) * part2

        # 创建排污口模型
        self['排污口圆环'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, -HW3), HR3, HR3)
        self['排污口柱体'] = translate(0, 0, -HW3) *Cone(Vec3(0, 0, 0), Vec3(0, 0, -ZW3), ZR3, ZR3)
        self['排污口空腔'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, -(HW3+ZW3)), Hr3, Hr3) 
        part3 = self['排污口圆环'] + self['排污口柱体'] - self['排污口空腔']
        part3 = translate(-A, 0, B) * part3
        
        # 创建主壳体模型
        self['圆台1'] = Cone(Vec3(0, 0, 0), Vec3(-TW, 0, 0), Tr, TR)
        self['柱体'] = translate(-TW, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(-ZW4, 0, 0), TR, TR)
        self['圆台2'] = translate(-(TW+ZW4), 0, 0) * Cone(Vec3(0, 0, 0), Vec3(-TW, 0, 0), TR, Tr)
        self['主壳体'] = self['圆台1'] + self['柱体'] + self['圆台2']
        part4 = translate(-(HW1+ZW1), 0, 0) * self['主壳体']

        # 创建处理器模型
        self['处理器下柱体'] =  Cone(Vec3(0, 0, 0), Vec3(0, 0, ZW51), ZR51, ZR51)
        self['处理器连接下环'] = translate(0, 0, ZW51) * Cone(Vec3(0, 0, 0), Vec3(0, 0, HW51), HR51, HR51)
        self['处理器连接上环'] = translate(0, 0, ZW51+HW51) * Cone(Vec3(0, 0, 0), Vec3(0, 0, HW52), HR52, HR52)
        self['处理器上柱体'] = translate(0, 0, ZW51+HW51+HW52) * Cone(Vec3(0, 0, 0), Vec3(0, 0, ZW52), ZR52, ZR52) 
        part51 = self['处理器连接下环']+ self['处理器下柱体']
        part52 = self['处理器连接上环']+ self['处理器上柱体']
        part5 = translate(-H1-TW-3*ZW4/4, 0, -C) * combine(part51, part52)

        # 创建把手模型
        self['穿壳柱体'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, Hw6), Hr6, Hr6)
        self['把手圆盘'] = translate(0, 0, Hw6) * Cone(Vec3(0, 0, 0), Vec3(0, 0, HW6), HR6, HR6)
        self['把手握处'] = translate(-l, -w/2, Hw6+HW6) * scale(l, w, h) * Cube()
        self['把手'] = self['把手圆盘'] + self['穿壳柱体'] + self['把手握处']
        part6 = translate(-(H1+TW+ZW4/6), 0, -1.05*TR) * self['把手']
        
        # 组合所有部件
        # marque = self['型号']
        # if marque in ['I-40', 'I-50', 'I-65', 'I-80', 'I-100', 'I-125']:
        #     self['I型电子除垢过滤器'] = combine(part1, part2, part3, part4, part5)
        # else:
        self['I型电子除垢过滤器'] = combine(part1, part2, part3, part4, part5, part6)
        

if __name__ == "__main__":
    FinalGeometry = I型电子除垢过滤器()
    place(FinalGeometry)
