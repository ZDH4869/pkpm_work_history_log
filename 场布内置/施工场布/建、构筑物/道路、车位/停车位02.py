import math
import pyp3d as p3d
from pyp3d import *
def post2(data:p3d.P3DData)->None:
    dzg=data['底座高度'] # 底座高度  200mm 
    zsk=data['桩身宽度']  # 桩身宽度  200mm   
    dz_sc = 100       # 底座伸出桩身  100mm
    zsc=data['桩身长度'] # 桩身长度  300mm
    zsg=data['桩身高度']   # 桩身高度  1500mm
    dxr = 20           # 充电线半径    20mm
    zjc = 300           # 电线收纳支架长    300mm
    zjk = 100          # 电线收纳支架宽    100mm
    zjh = 10         # 电线收纳支架厚度    10mm
    zj_sc = 50           # 支架与桩身连接体高    50mm
    kzd = 50          # 电线控制点距离
    ck_jd = 100             # 充电线出口距离底座高  100mm
    bsh = 10                # 充电枪把手厚度    10mm
    qk_r = 30               # 充电枪口半径
    qk_c = 100               # 充电枪口长
    xs_jd=data['显示屏距离底座高度'] # 显示屏距离底座高度    900mm
    xsk=data['显示屏宽'] # 显示屏宽      200mm
    xsg=data['显示屏高'] # 显示屏高  150mm
    xsh = 10            # 显示屏厚度    10mm
    dk_k = 100      # 洞口宽度  100mm
    dk_g = 150      # 洞口高度  150mm
    dk_s = 100       # 洞口深度  100mm
    dk_jd=data['洞口距离底座高度']# 洞口距离底座高度  1200mm

    cx_k = 150      # 车线宽
    cw_h = 10       # 车位厚度
    cw_c=data['车位长'] # 车位长    5000mm
    cw_k=data['车位宽'] # 车位宽    2500mm
    dcq_c = 1800            # 挡车器长度    1800mm
    ro=data['旋转角度']
    dcq_jx = 200            # 挡车器边缘距离停车线  200mm

    if data['显示屏宽']>data['桩身长度']:
        xsk=data['桩身长度']
        data['显示屏宽']=data['桩身长度']
    if data['显示屏高']>data['桩身高度']:
        xsg=data['桩身高度']
        data['显示屏高']=data['桩身高度']
    if data['显示屏距离底座高度']>data['桩身高度']-data['显示屏高']:
        xs_jd=data['桩身高度']-data['显示屏高']
        data['显示屏距离底座高度']=data['桩身高度']-data['显示屏高']
    if data['洞口距离底座高度']>data['桩身高度']-150:
        dk_jd=data['桩身高度']-150
        data['洞口距离底座高度']=data['桩身高度']-150
    # 创建底座
    DZ = p3d.Box(Vec3(-dz_sc,-dz_sc,-dzg),Vec3(-dz_sc,-dz_sc,0),
                Vec3(1,0,0),Vec3(0,1,0),2*dz_sc+zsc,2*dz_sc+zsk,2*dz_sc+zsc,2*dz_sc+zsk).color(0.5,0.5,0.5,1)
    ZS = p3d.Box(Vec3(0,0,0),Vec3(0,0,zsg),Vec3(1,0,0),Vec3(0,1,0),zsc,zsk,zsc,zsk).color(0.9,0.9,0.9,1)
    ZJ1 = p3d.Cone(Vec3(zsc,0.5*zsk,0.5*zsg),Vec3(zsc+zj_sc,0.5*zsk,0.5*zsg),0.1*zjk,0.1*zjk).color(0.9,0.9,0.9,1)
    ZJ2 = p3d.Box(Vec3(zsc+zj_sc,0.5*zsk-0.5*zjk,0.5*zsg-0.5*zjc),Vec3(zsc+zj_sc+zjh,0.5*zsk-0.5*zjk,0.5*zsg-0.5*zjc),Vec3(0,1,0),Vec3(0,0,1),zjk,zjc,zjk,zjc).color(0.9,0.9,0.9,1)

    # 创建电枪放置口
    DK = p3d.Box(Vec3(zsc,0.5*zsk-0.5*dk_k,dk_jd),Vec3(zsc-dk_s,0.5*zsk-0.5*dk_k,dk_jd),Vec3(0,1,0),Vec3(0,0,1),dk_k,dk_g,dk_k,dk_g)
    ZS = p3d.substract(ZS,DK)
    DK = DK.color(0.1,0.1,0.1,1)
    # 电线

    '''Curvelotf方法（暂不可用）'''
    # n = 20
    # OutLine1 = []
    # for i in range (n): 
    #     OutLine1.append(Vec3(dxr*math.sin(i*2*p3d.pi/n),dxr*math.cos(i*2*p3d.pi/n),0))
    # KP = [Vec3(zsc,0.5*zsk,ck_jd),Vec3(zsc+2*kzd,0.5*zsk,ck_jd),Vec3(zsc+2*kzd,0.5*zsk+2*kzd,ck_jd),
    #         Vec3(zsc+kzd,0.5*zsk+2*kzd,0.25*zsg+kzd),Vec3(zsc+dxr,0.5*zsk+2*kzd,0.5*zsg+2*kzd),Vec3(zsc+dxr,0.5*zsk-2*kzd,0.5*zsg+2*kzd),
    #         Vec3(zsc+dxr,0.5*zsk-2*kzd,0.35*zsg+2*kzd), Vec3(zsc+kzd,0.5*zsk-2*kzd,0.25*zsg+kzd),Vec3(zsc+2*kzd,0.5*zsk-2*kzd,0.15*zsg+2*kzd),
    #         Vec3(zsc+4*kzd,0.5*zsk-2*kzd,dxr),Vec3(zsc+4*kzd,0.5*zsk,dxr),Vec3(zsc+4*kzd,zsk+kzd,dxr),
    #         Vec3(zsc+4*kzd,zsk+kzd,0.15*dk_jd),Vec3(zsc+4*kzd,zsk+2*kzd,0.35*dk_jd),Vec3(zsc+4*kzd,zsk+2*kzd,0.5*dk_jd),
    #         Vec3(zsc+1*kzd,0.5*zsk,0.75*dk_jd),Vec3(zsc+0.5*kzd,0.5*zsk,dk_jd+0.45*dk_g)]
        
    # CDX = p3d.CurveLoft(OutLine1, KP, 100,5).color(0.1,0.1,0.1,1)
    '''FilletPipe方法'''
    CDX = p3d.FilletPipe(
        [
            Vec3(zsc,0.5*zsk,ck_jd),Vec3(zsc+2*kzd,0.5*zsk,ck_jd),Vec3(zsc+2*kzd,0.5*zsk+2*kzd,ck_jd),
            Vec3(zsc+kzd,0.5*zsk+2*kzd,0.25*zsg+kzd),Vec3(zsc+dxr,0.5*zsk+2*kzd,0.5*zsg+2*kzd),Vec3(zsc+dxr,0.5*zsk-2*kzd,0.5*zsg+2*kzd),
            Vec3(zsc+dxr,0.5*zsk-2*kzd,0.35*zsg+2*kzd), Vec3(zsc+kzd,0.5*zsk-2*kzd,0.25*zsg+kzd),Vec3(zsc+2*kzd,0.5*zsk-2*kzd,0.15*zsg+2*kzd),
            Vec3(zsc+3*kzd,0.5*zsk-2*kzd,0),Vec3(zsc+3*kzd,zsk+kzd,0),
            Vec3(zsc+3*kzd,zsk+kzd,0.15*dk_jd),Vec3(zsc+3*kzd,zsk+0.8*kzd,0.35*dk_jd),Vec3(zsc+2.5*kzd,zsk+0.25*kzd,0.5*dk_jd),
            Vec3(zsc+2*kzd,0.65*zsk,0.75*dk_jd),Vec3(zsc+0.5*kzd,0.5*zsk,dk_jd+0.45*dk_g)
        ],
        [
            0, dxr * 2, dxr * 2, dxr * 10, dxr * 4, dxr * 4, dxr * 20, dxr * 20, dxr * 20, dxr * 6, dxr * 6, dxr * 10, dxr * 10, dxr * 10, dxr * 10,0
        ],
        dxr)
    # 电枪枪口
    DQK = p3d.Cone(Vec3(zsc,0.5*zsk,dk_jd+0.5*dk_g),Vec3(zsc+qk_c,0.5*zsk,dk_jd+0.5*dk_g),qk_r,qk_r).color(0.5,0.5,0.5,1)
    QTK = p3d.Box(Vec3(zsc+qk_c-bsh-20,0,dk_jd-0.666*qk_r+0.5*dk_g),Vec3(zsc+qk_c-bsh,0,dk_jd-0.666*qk_r+0.5*dk_g),Vec3(0,1,0),Vec3(0,0,1),zsk,0.666*2*qk_r,zsk,0.666*2*qk_r)
    DQK1 = p3d.substract(DQK,QTK).color(0.5,0.5,0.5,1)

    # 显示屏
    XSP = p3d.Box(Vec3(0.5*zsc-0.5*xsk,0,xs_jd),Vec3(0.5*zsc-0.5*xsk,xsh,xs_jd),Vec3(1,0,0),Vec3(0,0,1),xsk,xsg,xsk,xsg).color(0,0,0.9,0.5)
    ZS = p3d.substract(ZS,XSP)
    XSP = p3d.translation(Vec3(0,-0.1,0))*XSP
    CDZ = p3d.translation(Vec3(0.5*cw_k-0.5*zsc,cw_c,dzg))*p3d.combine(DZ,ZS,ZJ1,ZJ2,CDX,DK,DQK1,XSP)

    # 车位
    CWN= p3d.Box(Vec3(cx_k,cx_k,0),Vec3(cx_k,cx_k,-cw_h),Vec3(1,0,0),Vec3(0,1,0),cw_k-2*cx_k,cw_c-2*cx_k,cw_k-2*cx_k,cw_c-2*cx_k)
    CWQ = p3d.Box(Vec3(0.25*cw_k,0,0),Vec3(0.25*cw_k,0,-cw_h),Vec3(1,0,0),Vec3(0,1,0),0.5*cw_k,cx_k,0.5*cw_k,cx_k)
    CW1 = p3d.combine(CWN,CWQ)
    # 停车线
    CW= p3d.Box(Vec3(0,0,0),Vec3(0,0,-cw_h),Vec3(1,0,0),Vec3(0,1,0),cw_k,cw_c,cw_k,cw_c)
    CW2 = p3d.substract(CW,CW1).color(1,1,0,1)
    FCW = p3d.combine(CDZ,CW2,CW1)
    # p3d.createGeometry(FCW)
    #挡车器
    T_1 = p3d.FilletPipe([p3d.Vec3(0,0,0),p3d.Vec3(0,0,100),p3d.Vec3(dcq_c/5,0,100)], (0,1,0), 40).color(1,1,0,1)
    T_2 = p3d.Cone(p3d.Vec3(dcq_c/5,0,100),p3d.Vec3(dcq_c/5*2,0,100),40,40).color(0,0,0,1)
    T_3 = p3d.Cone(p3d.Vec3(dcq_c/5*2,0,100),p3d.Vec3(dcq_c/5*3,0,100),40,40).color(1,1,0,1)
    T_4 = p3d.Cone(p3d.Vec3(dcq_c/5*3,0,100),p3d.Vec3(dcq_c/5*4,0,100),40,40).color(0,0,0,1)
    T_5 = p3d.FilletPipe([p3d.Vec3(dcq_c/5*4,0,100),p3d.Vec3(dcq_c,0,100),p3d.Vec3(dcq_c,0,0)], (0,1,0), 40).color(1,1,0,1)
    T=p3d.translation(p3d.Vec3((cw_k-dcq_c)/2,cw_c-dcq_jx-dk_g,0)) *p3d.combine(T_1,T_2,T_3,T_4,T_5)
    Z=p3d.translation(p3d.Vec3(-cw_k/2,-cw_c/2,0)) *p3d.combine(FCW,T)
    FG=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*ro/180) *Z
    # p3d.createGeometry(T)
    data['停车位'] = FG
if __name__=="__main__":
    data=p3d.P3DData({
        '底座高度':200,
        '桩身宽度':200,
        '桩身长度':300,
        '桩身高度':1500,
        '显示屏距离底座高度':900,
        '显示屏宽':200,
        '显示屏高':150,
        '洞口距离底座高度':1200,
        '车位长':5000,
        '车位宽':2500,
        '旋转角度':0,
        '构件名称':'停车位02'
    })
    data.set_view = (-0.125*p3d.pi,-0.125*p3d.pi)
    
    data.set_view = (-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('停车位', show=True)

    # 设置可调整属性
    data.setup('底座高度', obvious=True, group='底座', description='—————')
    data.setup('桩身宽度', obvious=True, group='桩身', description='—————')
    data.setup('桩身长度', obvious=True, group='桩身', description='—————')
    data.setup('桩身高度', obvious=True, group='桩身', description='—————')
    data.setup('显示屏距离底座高度', obvious=True, group='显示屏', description='—————')
    data.setup('显示屏宽', obvious=True, group='显示屏', description='—————')
    data.setup('显示屏高', obvious=True, group='显示屏', description='—————')
    data.setup('洞口距离底座高度', obvious=True, group='洞口', description='—————')
    data.setup('车位长', obvious=True, group='车位', description='—————')
    data.setup('车位宽', obvious=True, group='车位', description='—————')
    data.setup('旋转角度', obvious=True, group='旋转', description='——————')
    data.setup('构件名称', obvious=True) 
    # 设置replace算子
    data['replace'] = post2
    post2(data)
    p3d.launchData(data)
    # 发射数据到实例模板库