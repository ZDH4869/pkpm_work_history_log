from pyp3d import *
import math

# '型号':[除湿量 (kg/h),风量 (m3/h),送风方式,机外静压 (Pa),
# 输入功率 (kW),机组噪声 dB (A),宽 (mm),深 (mm),高 (mm),重量 (kg)],
# 风口定位尺寸：A,C,D,E,F,G,H,J,其中仅用到F,G,H来定位水口、电口
unit_parameter = {
    'CLF6':[5.9,1500,'侧风',0,2.43,55,600,600,2000,210,  600,526,2000,600,108,216.5,70,572],
    'CLF8':[7.6,2000,'侧风',0,3.02,55,850,600,2000,230,  850,776,2000,600,108,216.5,70,572],
    'CLF10':[10,2500,'侧风',0,4.01,60,850,600,2000,230,  850,766,2000,600,108,216.5,70,572],
    'CLF16':[15.5,4000,'侧风',0,5.92,62,1300,700,2000,  340,1300,1230,2000,700,98,211,70,672],
    'CLF21':[20.8,5000,'侧风',0,8.5,64,1300,700,2000,  370,1300,1230,2000,700,98,211,70,672],
    'CLF25':[24.3,6500,'侧风',0,9.64,65,1700,700,2120,  585,1700,1576,2210,700,140,212,80,670],
    'CLF32':[30.8,8000,'侧风',0,12.14,65,1700,700,2120,  615,1700,1576,2210,700,140,212,80,670],
    'CLF42':[41.5,10000,'侧风',0,16.2,64,1900,850,2230,  690,1900,1776,2300,850,170,210,80,820]}

marque_list = [
    'CLF6','CLF8','CLF10','CLF16',
    'CLF21','CLF25','CLF32','CLF42','自定义']

def get_parameter_by_marque(marque):
    if marque in unit_parameter:
        return unit_parameter[marque]
    # 自定义型号返回默认值
    return [0.0, 0, '侧风', 0, 0.0, 0, 600, 600, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class 升温型除湿机(Component):
    def __init__(self):
        Component.__init__(self)

        self['型号']=Attr('CLF6', obvious=True, combo=['CLF6','CLF8','CLF10','CLF16',
        'CLF21','CLF25','CLF32','CLF42','自定义'])
        
        # 定义参数（初始值，会在replace方法中根据型号动态更新）
        self['除湿量 (kg/h)']=Attr(0.0, obvious=True, readonly=False)
        self['风量 (m3/h)']=Attr(0, obvious=True, readonly=False)
        self['送风方式']=Attr('', obvious=True, readonly=True)
        self['机外静压 (Pa)']=Attr(0, obvious=True, readonly=False)
        self['输入功率 (kW)']=Attr(0.0, obvious=True, readonly=False)
        self['机组噪声 dB (A)']=Attr(0, obvious=True, readonly=False)
        self['宽']=Attr(0, obvious=True, readonly=False)
        self['深']=Attr(0, obvious=True, readonly=False)
        self['高']=Attr(0, obvious=True, readonly=False)
        self['重量 (kg)']=Attr(0, obvious=True, readonly=False)
        self['冷却水口直径'] = Attr(40, obvious=True, readonly=False)
        self['电口直径'] = Attr(15, obvious=True, readonly=False)
        self['管口水平距'] = Attr(0, obvious=True, readonly=False)       #F
        self['管口1高'] = Attr(0.0, obvious=True, readonly=False)       #G
        self['管口2高'] = Attr(0, obvious=True, readonly=False)         #H
        
        # 文字参数
        self['文字高度'] = Attr(500, obvious=True, readonly=False)
        self['文字厚度'] = Attr(20, obvious=True, readonly=False)

        # 初始化时更新参数
        self.update_params()
        #管口增加驱动点
        self.setDrivenFeaturePoint('point02', SnapMode.EndPoint, '[定位点X]-20', '[定位点Y]+[深]-[管口水平距]' ,'[定位点Z]+[管口1高]')
        self.setDrivenFeaturePoint('point03', SnapMode.EndPoint, '[定位点X]-20', '[定位点Y]+[深]-[管口水平距]' ,'[定位点Z]+[管口1高]+[管口2高]')
        self.setDrivenFeaturePoint('point04', SnapMode.EndPoint, '[定位点X]-20', '[定位点Y]+[深]/2' ,'[定位点Z]+[管口1高]/2')
        
        self['升温型除湿机']=Attr(None, show=True)
        self.replace()

    def update_params(self):
        # 获取型号参数
        marque = self['型号']
        
        # 如果不是自定义型号，根据型号更新参数
        if marque != '自定义':
            params = get_parameter_by_marque(marque)
            
            #根据型号动态计算并更新参数值
            self['除湿量 (kg/h)'] = params[0]
            self['风量 (m3/h)'] = params[1] 
            self['送风方式'] = params[2]
            self['机外静压 (Pa)'] = params[3]
            self['输入功率 (kW)'] = params[4]
            self['机组噪声 dB (A)'] = params[5]
            self['宽'] = params[6]
            self['深'] = params[7]
            self['高'] = params[8]
            self['重量 (kg)'] = params[9]
            self['管口水平距'] = params[14]
            self['管口1高'] = params[15]
            self['管口2高'] = params[16]
        else:
            # 自定义型号时，保持当前参数值不变
            # 确保送风方式始终为侧风
            self['送风方式'] = '侧风'
                
    @export
    def replace(self):   
        # 先更新参数（如果用户修改了型号）
        self.update_params() 
        # 获取所有参数
        W = self['宽']
        S = self['深'] 
        H = self['高']
        F = self['管口水平距'] 
        G = self['管口1高']  
        H_p = self['管口2高'] #与H高参数命名重复，做出区分

        # 水口直径、电口直径
        Water_radius = self['冷却水口直径']/2
        Elec_radius = self['电口直径']/2
        Pip_high = 20

        # 百叶参数
        FGH_Box = W  # 风管宽度
        FGW_Box = H * 0.2  # 风管高度
        BYH_Box = S / 10  # 窗高
        BYW_Box = W  # 窗宽
        BYL_Box = S  # 百叶长度
        BYW_Box = FGH_Box + 54.0
        BYL_Box = FGW_Box + 54.0
        liefThick = 10
        liefHeight = 30

        # 创建除湿机主体模型
        part1 = scale(W, S, H) * Cube()
        
        # 创建侧面送风内部空腔
        line_2 = Line(Vec3(0, 0, 0), Vec3(0, S/10, 0))
        section_2 = Section(Line(Vec3(0, 0, 0), Vec3(0, 0, H*0.2), Vec3(W, 0, H*0.2), Vec3(W, 0, 0)))
        part2 = translate(0, 0, H - H*0.2) * Sweep(section_2, line_2)

        # 创建侧面回风内部空腔
        line_3 = Line(Vec3(0, 0, 0), Vec3(0, S/15, 0))
        section_3 = Section(Line(Vec3(0, 0, 0), Vec3(0, 0, H*0.2), Vec3(W-200, 0, H*0.2), Vec3(W-200, 0, 0)))
        part3 = translate(100, 0, H*0.5 - H*0.2) * Sweep(section_3, line_3)
                
        # 布尔运算 - 确保主体不会被完全减去
        主体 = part1
        if W > 0 and H > 0:
            主体 = 主体 - part2
            主体 = 主体 - part3

        # 冷却水进水孔、出水孔、电口
        Pip_inlet = translate(0, S-F, G) *Cone(Vec3(0, 0, 0), Vec3(-Pip_high, 0, 0), Water_radius, Water_radius)
        Pip_outlet = translate(0, S-F, G+H_p) *Cone(Vec3(0, 0, 0), Vec3(-Pip_high, 0, 0), Water_radius, Water_radius)
        Pip_elec = translate(0, S/2, G/2) *Cone(Vec3(0, 0, 0), Vec3(-Pip_high, 0, 0), Elec_radius, Elec_radius)

        # 送风口百叶模型
        # 风管
        mainCube = translate(-0.5 * FGW_Box, -0.5 * FGH_Box, 0) * scale(FGW_Box, FGH_Box, BYH_Box) * Cube()
        
        # 百叶风管创建挖空布尔体       
        BYW_BoxEmpty = FGH_Box - 50
        BYL_BoxEmpty = FGW_Box - 50
        if BYW_BoxEmpty > 0 and BYL_BoxEmpty > 0:
            emptyCube = translate(-0.5 * BYL_BoxEmpty, -0.5 * BYW_BoxEmpty, 0) * scale(BYL_BoxEmpty, BYW_BoxEmpty, BYH_Box) * Cube()
            mainCube = mainCube - emptyCube
        
        # 逆时针以原点为中心的叶片
        liefx = 0.5 * FGW_Box
        liefy = 0.5 * liefThick
        
        # 去除一个厚度的偏移
        liefOffset = liefHeight - liefThick
        liefHLoction = BYH_Box
        
        # 创建叶片
        sectionlief = translate(0.5 * BYL_BoxEmpty - 30, -0.5 * BYW_BoxEmpty, liefHLoction) * rotate(Vec3(1, 0, 0), 0.5 * math.pi) * Section(
            Vec3(0, 0),
            Vec3(-10, 0),
            Vec3(-10 - liefOffset, -liefOffset),
            Vec3(-10 - liefOffset - 3.6, -liefOffset),
            Vec3(-10 - liefOffset - 3.6, -liefOffset + 5.5),
            Vec3(-10 - liefOffset - 3.6 - liefThick, -liefOffset + 5.5),
            Vec3(-10 - liefOffset - 3.6 - liefThick, -liefOffset - liefThick),
            Vec3(-liefOffset - 8.3, -liefThick - liefOffset),
            Vec3(-8.3, -liefThick),
            Vec3(0, -liefThick)
        )
        
        line = Line(Vec3(0, 0, 0), Vec3(0, BYW_BoxEmpty, 0))
        lief = Sweep(sectionlief, line)
        
        # 风管内侧减去第一个起点距离
        canOffsetLength = BYL_BoxEmpty - 30
        
        # 每一个叶片的厚度 +40的间距
        liefoffset = liefHeight + liefThick + 3.6 + 10 + 23
        num = int(canOffsetLength / liefoffset)

        for i in range(num):
            mainCube = mainCube + translate(-i * liefoffset, 0, 0) * lief
        
        百叶窗矩形面 = translate(FGH_Box/2, BYH_Box, H-H*0.1) * rotate(Vec3(1, 0, 0), 0.5*math.pi) * rotate(Vec3(0, 0, 1), 0.5*math.pi) * mainCube
        
        # 创建三维文字 - XOZ平面
        text_height = self['文字高度']
        text_thickness = self['文字厚度']
        text = Text("升温型除湿机", text_height, "Arial")
        text_3d = translate(-W/2, S/2, H/2) * rotate(Vec3(0, 1, 0), 0.5*math.pi) * extrude(text, text_thickness)
        
        # 组合所有部件
        final_model = 主体
        final_model = final_model + 百叶窗矩形面
        final_model = final_model + text_3d
        
        self['升温型除湿机'] = combine(final_model, Pip_inlet, Pip_outlet, Pip_elec)

if __name__ == "__main__":
    FinalGeometry = 升温型除湿机()
    place(FinalGeometry)
