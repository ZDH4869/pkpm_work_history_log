import pyp3d as p3d
from pyp3d import *
import math
def WSL(data:p3d.P3DData)->None:
    H = data['灯具高度（最小值1403）']

    C = data['灯具长']
    K = data['灯具宽']
    G = data['灯具高']
    C1 = data['灯具底座长']
    K1 = data['灯具底座宽']
    G1 = data['灯具底座厚度']

    R = data['伸缩杆内管半径']
    L1 = data['伸缩杆外管长度']
    R1 = data['伸缩杆外管半径']
    
    L3 = data['三角底座支架长度']
    J = data['三角底座支架与地面的夹角']

    RAD = data['支架红色值']
    GREEN = data['支架绿色值']
    BLUE = data['支架蓝色值']
    T = data['支架不透明度']
    RAD1 = data['灯具外壳红色值']
    GREEN1 = data['灯具外壳绿色值']
    BLUE1 = data['灯具外壳蓝色值']
    T1 = data['灯具外壳不透明度']
    RAD2 = data['灯具红色值']
    GREEN2 = data['灯具绿色值']
    BLUE2 = data['灯具蓝色值']
    T2 = data['灯具不透明度']

    Rotation = data['水平方向上的旋转角度（角度制）']
    if H<1403:
        H = 1403

    #三脚架
    A0 = p3d.Cone(p3d.Vec3(0,0,0), p3d.Vec3(0,0,L3),5,10).color(RAD/255,GREEN/255,BLUE/255,T)
    A1 = p3d.rotation(p3d.Vec3(0,1,0),p3d.pi*J) * A0
    A2 = p3d.translation(p3d.Vec3((-200)*math.sqrt(3),0,0)) * A1
    A3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*(2/3)) * A2
    A4 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*(4/3)) * A2
    A5 = p3d.Cone(p3d.Vec3(0,0,175), p3d.Vec3(0,0,275),15,15).color(RAD/255,GREEN/255,BLUE/255,T)

    A6 = p3d.combine (A2,A3,A4,A5)
    #伸缩杆
    B0 = p3d.Cone(p3d.Vec3(0,0,200), p3d.Vec3(0,0,L1+200),R1,R1).color(RAD/255,GREEN/255,BLUE/255,T)
    B1 = p3d.Cone(p3d.Vec3(0,0,L1+200), p3d.Vec3(0,0,H-203),R,R).color(RAD/255,GREEN/255,BLUE/255,T)
    #灯
    DZ = p3d.Box(p3d.Vec3(-50,-50,H-G-G1), p3d.Vec3(-50,-50,H-G), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),C1,K1,C1,K1).color(RAD/255,GREEN/255,BLUE/255,T)
    D1 = p3d.Extrusion([p3d.Vec3(-C/2,-K/2,H-G),p3d.Vec3(-C/2,-K/2,H-G+6.25),p3d.Vec3(-C/2,(K/2)-6.25,H-G+6.25),p3d.Vec3(-C/2,(K/2)-6.25,H-(G/4)),p3d.Vec3(-C/2,0,H-6.25),p3d.Vec3(-C/2,-K/2,H-6.25),p3d.Vec3(-C/2,-K/2,H),p3d.Vec3(-C/2,0,H),p3d.Vec3(-C/2,K/2,H-50),p3d.Vec3(-C/2,K/2,H-G)],p3d.Vec3(C,0,0)).color(RAD1/255,GREEN1/255,BLUE1/255,T1)
    D2 = p3d.Extrusion([p3d.Vec3(-C/2,-K/2,H-G+6.25),p3d.Vec3(-C/2,-K/2,H-6.25),p3d.Vec3(-C/2,0,H-6.25),p3d.Vec3(-C/2,0,H-6.25),p3d.Vec3(-C/2,(K/2)-6.25,H-(G/4)),p3d.Vec3(-C/2,(K/2)-6.25,H-G+6.25)],p3d.Vec3(6.25,0,0)).color(RAD1/255,GREEN1/255,BLUE1/255,T1)
    D3 = p3d.translation(p3d.Vec3(C-6.25,0,0)) * D2
    D4 = p3d.Box(p3d.Vec3(-C/2+6.25,-K/2,H-G+6.25), p3d.Vec3(-C/2+6.25,-K/2,H-6.25), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),C-12.5,6.25,C-12.5,6.25).color(RAD2/255,GREEN2/255,BLUE2/255,T2)

    A7= p3d.combine (A6,B0,B1,DZ,D1,D2,D3,D4)
    data['移动式灯具-类型一'] = p3d.rotation(p3d.Vec3(0,0,1),Rotation/180*pi)*A7


if __name__ == "__main__":
    data = p3d.P3DData({
        '灯具高度（最小值1403）':2003,
        '灯具长':300,
        '灯具宽':75,
        '灯具高':200,
        '灯具底座长':100,
        '灯具底座宽':100,
        '灯具底座厚度':3,
        '伸缩杆内管半径':10,
        '伸缩杆外管长度':1000,
        '伸缩杆外管半径':12,
        '三角底座支架长度':400,
        '三角底座支架与地面的夹角':1/3,
        '支架红色值':127.5,
        '支架绿色值':127.5,
        '支架蓝色值':127.5,
        '支架不透明度':1,
        '灯具外壳红色值':76.5,
        '灯具外壳绿色值':76.5,
        '灯具外壳蓝色值':76.5,
        '灯具外壳不透明度':1,
        '灯具红色值':127.5,
        '灯具绿色值':204,
        '灯具蓝色值':255,
        '灯具不透明度':0.7,
        '水平方向上的旋转角度（角度制）': 0.00,
        '场布类型':'消防水电',
        '构件类型':'电气设备',
        '构件名称':'移动式灯具类型一'


        })

    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('移动式灯具-类型一', show=True)
    data.setup('灯具高度（最小值1403）', obvious=True, group='灯具高度',description='灯具整体')
    data.setup('灯具长', obvious=True, readonly=True,group='灯具',description='灯具外壳')
    data.setup('灯具宽', obvious=True, readonly=True,group='灯具',description='灯具外壳')
    data.setup('灯具高', obvious=True, readonly=True,group='灯具',description='灯具外壳')
    data.setup('灯具底座长', obvious=True, readonly=True,group='灯具',description='灯具外壳')
    data.setup('灯具底座宽', obvious=True, readonly=True,group='灯具',description='灯具外壳')
    data.setup('灯具底座厚度', obvious=True, readonly=True,group='灯具',description='灯具外壳')

    data.setup('伸缩杆内管半径', obvious=True, readonly=True,group='伸缩杆',description='支架')
    data.setup('伸缩杆外管长度', obvious=True, readonly=True,group='伸缩杆',description='支架')
    data.setup('伸缩杆外管半径', obvious=True, readonly=True,group='伸缩杆',description='支架')

    data.setup('三角底座支架长度', obvious=True, readonly=True,group='三角架',description='长度')
    data.setup('三角底座支架与地面的夹角', obvious=True, readonly=True,group='三角架',description='夹角')
    #data.setup('支架红色值', obvious=True, readonly=True,group='三角架',description='颜色')
    #data.setup('支架绿色值', obvious=True, readonly=True,group='三角架',description='颜色')
    #data.setup('支架蓝色值', obvious=True, readonly=True,group='三角架',description='颜色')
    #data.setup('支架不透明度', obvious=True, readonly=True,group='三角架',description='颜色')
    #data.setup('灯具外壳红色值', obvious=True, readonly=True,group='灯具',description='颜色')
    #data.setup('灯具外壳绿色值', obvious=True, readonly=True,group='灯具',description='颜色')
    #data.setup('灯具外壳蓝色值', obvious=True, readonly=True,group='灯具',description='颜色')
    #data.setup('灯具外壳不透明度', obvious=True, readonly=True,group='灯具',description='颜色')
    #data.setup('灯具红色值', obvious=True,readonly=True,group='灯',description='颜色')
    #data.setup('灯具绿色值', obvious=True,readonly=True,group='灯',description='颜色')
    #data.setup('灯具蓝色值', obvious=True,readonly=True,group='灯',description='颜色')
    data.setup('灯具不透明度', obvious=True, group='灯',description='颜色')
    data.setup('水平方向上的旋转角度（角度制）', obvious=True, group='位置',description='角度')
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = WSL
    WSL(data)
    p3d.launchData(data)
    
