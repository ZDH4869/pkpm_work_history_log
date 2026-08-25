from pyp3d import *
import math

# '型号':[定位尺寸(mm)：A,B,C,  过滤器高度：L,
# 进出口DN1(mm),排污口DN2(mm),
# 输入功率 (W),处理流量 (T/H)],
# A、B用来定位进出口，C用来定位排污口，L表示过滤器整体高度
# unit_parameter = {
#     'L-40':[150,120,220,600,40,13,  20,6],
#     'L-50':[170,125,250,630,50,13,  20,9],
#     'L-65':[190,140,285,660,65,19,  20,14],
#     'L-80':[220,150,325,720,80,25,  20,25],
#     'L-100':[290,160,415,830,100,32,  40,40],
#     'L-125':[320,200,460,890,125,38,  40,60],
#     'L-150':[420,220,610,1120,150,50,  60,90],
#     'L-200':[550,260,750,1260,200,65,  120,160],
#     'L-250':[650,310,890,1450,250,80,  180,240],
#     'L-300':[750,350,1030,1600,300,100,  300,350],
#     'L-350':[900,420,1240,1880,350,125,  360,480],
#     'L-400':[1000,470,1340,1960,400,150,  420,620],
#     'L-450':[1120,510,1510,2240,450,150,  500,800],
#     'L-500':[1250,550,1655,2350,500,150,  500,980],
#     'L-600':[1400,610,1900,2620,600,200,  500,1200],
#     'L-700':[1600,650,2140,2960,700,200,  500,1500],
#     'L-800':[1745,760,2340,3290,800,200,  500,1800],
#     'L-900':[1900,810,2560,3520,900,200,  500,2000],
#     'L-1000':[2220,860,2780,3820,1000,250,  500,2600]}


# marque_list = [
#     'L-40','L-50','L-65','L-80','L-100','L-125','L-150','L-200','L-250',
#     'L-300','L-350','L-400','L-450','L-500','L-600','L-700','L-800','L-900','L-1000','自定义']

# def get_parameter_by_marque(marque):
#     if marque in unit_parameter:
#         return unit_parameter[marque]
#     # 自定义型号返回默认值
#     return [0, 0, 0, 0, 0, 0, 0, 0]

class L型电子除垢过滤器(Component):
    def __init__(self):
        Component.__init__(self)
        self['名称']=Attr('L型电子除垢过滤器',  obvious=True, readonly=True)
        self['型号']=Attr('L-40', obvious=True)
        
        # 定义参数（固定参数值）

        self['进出口水平距A']=Attr(150, obvious=True, readonly=False)
        self['进出口垂向距B']=Attr(120, obvious=True, readonly=False)
        self['污水口水平距C']=Attr(220, obvious=True, readonly=False)
        self['设备总长L']=Attr(600, obvious=True, readonly=False)
        self['进出口DN1']=Attr(40, obvious=True, readonly=False)
        self['排污口DN2']=Attr(13, obvious=True, readonly=False)
        self['输入功率 (W)']=Attr(20, obvious=True, readonly=False)
        self['处理流量 (T/H)']=Attr(6, obvious=True, readonly=False)

        # 初始化时更新参数
        # self.update_params()  
        #管口增加驱动点
        self.setDrivenFeaturePoint('point02', SnapMode.Center, '[定位点X]', '[定位点Y]' ,'[定位点Z]')
        self.setDrivenFeaturePoint('point03', SnapMode.Center, '[定位点X]+[进出口水平距A]', '[定位点Y]' ,'[定位点Z]+[进出口垂向距B]')
        self.setDrivenFeaturePoint('point04', SnapMode.Center, '[定位点X]+[污水口水平距C]', '[定位点Y]' ,'[定位点Z]-4*[进出口垂向距B]/9-11*[进出口DN1]/20-20')

        self['L型电子除垢过滤器']=Attr(None, show=True)
        self.replace()

    # def update_params(self):
    #     # 获取型号参数
    #     marque = self['型号']
        
    #     # 如果不是自定义型号，根据型号更新参数
    #     if marque != '自定义':
    #         params = get_parameter_by_marque(marque)
            
    #         #根据型号动态计算并更新参数值
    #         self['进出口水平距A'] = params[0]
    #         self['进出口垂向距B'] = params[1]
    #         self['污水口水平距C'] = params[2]
    #         self['设备总长L'] = params[3]
    #         self['进出口DN1'] = params[4]
    #         self['排污口DN2'] = params[5]
    #         self['输入功率 (W)'] = params[6]
    #         self['处理流量 (T/H)'] = params[7]
                  
    @export
    def replace(self):   
        # 获取所有参数
        A = self['进出口水平距A']  #进出口水平距
        B = self['进出口垂向距B']  #进出口垂向距
        C = self['污水口水平距C']  #污水口水平距
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
        HW2 = B/9  #出水口圆环厚度
        ZR2 = 11*DN1/20  #出水口柱体半径
        ZW2 = 55*B/72-DN1/4  #出水口柱体高度
        Hr2 = DN1/2  #出水口圆环内半径
        #排污口
        HR3 = 3*DN2/4  #排污口圆环外半径
        HW3 = HW1  #排污口圆环厚度
        ZR3 = 11*DN2/20  #排污口柱体半径
        ZW3 = B/4  #排污口柱体高度
        Hr3 = DN2/2  #排污口圆环内半径
        #主壳体
        Tr = ZR1  #主壳体圆台小圆半径
        TR = Tr+B/8+20  #主壳体圆台大圆半径即柱体半径
        TW = int(L/8)  #主壳体圆台高度
        ZW4 = int(3*L/5)  #主壳体柱体高度
        HR4 = TR+0.15*TR+0.1*DN1  #主壳体连接环半径
        HW4 = HW1  #主壳体连接环厚度
        H2 = TW+ZW4+HW4  #主壳体总高度
        #处理器
        HR5 = HR4  #处理器圆环外半径
        HW5 = HW4  #处理器圆环厚度
        H3 = L-H1-H2  #处理器总高度
        ZR51 = int(3*TR/4)  #处理器柱体1半径
        ZW51 = int(2*H3/7)  #处理器柱体1高度
        ZR52 = int(5*TR/6)  #处理器柱体2半径
        ZW52 = H3-HW5-ZW51  #处理器柱体2高度

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
        self['排污口圆环'] = translate(0, 0, -ZW3) * Cone(Vec3(0, 0, 0), Vec3(0, 0, -HW3), HR3, HR3)
        self['排污口柱体'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, -ZW3), ZR3, ZR3)
        self['排污口空腔'] = Cone(Vec3(0, 0, 0), Vec3(0, 0, -(HW3+ZW3)), Hr3, Hr3) 
        part3 = self['排污口圆环'] + self['排污口柱体'] - self['排污口空腔']
        part3 = translate(C, 0, -TR+ZW3/6) * part3
        
        # 创建主壳体模型
        self['圆台'] = Cone(Vec3(0, 0, 0), Vec3(TW, 0, 0), Tr, TR)
        self['柱体'] = translate(TW, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW4, 0, 0), TR, TR)
        self['主壳体连接环'] = translate(TW+ZW4, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(HW4, 0, 0), HR4, HR4)
        self['主壳体'] = self['圆台'] + self['柱体'] + self['主壳体连接环']
        part4 = translate(HW1+ZW1, 0, 0) * self['主壳体']

        # 创建处理器模型
        self['处理器连接环'] = Cone(Vec3(0, 0, 0), Vec3(HW5, 0, 0), HR5, HR5)
        self['处理器柱体1'] = translate(HW5, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW51, 0, 0), ZR51, ZR51)
        self['处理器柱体2'] = translate(HW5+ZW51, 0, 0) * Cone(Vec3(0, 0, 0), Vec3(ZW52, 0, 0), ZR52, ZR52) 
        part5 = self['处理器连接环'] + self['处理器柱体1'] + self['处理器柱体2']
        part5 = translate(H1+H2, 0, 0) * part5
        
        # 组合所有部件
        self['L型电子除垢过滤器'] = combine(part1, part2, part3, part4, part5)
        

if __name__ == "__main__":
    FinalGeometry = L型电子除垢过滤器()
    place(FinalGeometry)
