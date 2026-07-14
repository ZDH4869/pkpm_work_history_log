import pyp3d as p3d
import math
from pyp3d import *
def GLW(data:p3d.P3DData)->None:
    z1=data['圆柱高度']#圆柱高度
    R =data['圆柱半径']#圆柱半径
    # c =data['总围栏长']#总围栏长度
    # s=data['柱子个数']#柱子个数
    a=data['网半径']#网半径
    w=data['间隔宽度']#两柱之间间距
    f1=data['旋转角度']
    
#固定圆柱
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,z1/7),R,R).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,z1/7),p3d.Vec3(0,0,z1*2/7),R,R).color(1,0,0,1)
    Cone3 = p3d.Cone(p3d.Vec3(0,0,z1*2/7),p3d.Vec3(0,0,z1*3/7),R,R).color(1,1,1,1)
    Cone4 = p3d.Cone(p3d.Vec3(0,0,z1*3/7),p3d.Vec3(0,0,z1*4/7),R,R).color(1,0,0,1)
    Cone5 = p3d.Cone(p3d.Vec3(0,0,z1*4/7),p3d.Vec3(0,0,z1*5/7),R,R).color(1,1,1,1)
    Cone6 = p3d.Cone(p3d.Vec3(0,0,z1*5/7),p3d.Vec3(0,0,z1*6/7),R,R).color(1,0,0,1)
    Cone7 = p3d.Cone(p3d.Vec3(0,0,z1*6/7),p3d.Vec3(0,0,z1),R,R).color(1,1,1,1)
    Cone8 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-R*1.5),R*3,R*3).color(1,1,1,1)
    Cone9 = p3d.Cone(p3d.Vec3(0,0,-R*1.5),p3d.Vec3(0,0,-R*3),R*4,R*4).color(1,1,1,1)
    AA = p3d.combine(Cone1,Cone2,Cone3,Cone4,Cone5,Cone6,Cone7,Cone8,Cone9)

# 第二根圆柱

    midsg1 = p3d.translation(p3d.Vec3(w+40,0,0)) * AA
# 网   
    # 竖线   
    ConeA = p3d.Cone(p3d.Vec3(0,0,z1*2.2/7),p3d.Vec3(0,0,z1*6.2/7),a,a).color(1,1,1,1)
    HW = p3d.Array(ConeA)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(w,0,0),42):
        HW.append(translation(i))
    # 横线
    ConeB = p3d.Cone(p3d.Vec3(0,0,z1*2.2/7),p3d.Vec3(w,0,z1*2.2/7),a,a).color(1,1,1,1)
    SW = p3d.Array(ConeB)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,0,z1*4/7),18):
        SW.append(translation(i))
    AA1=p3d.combine(HW,SW)
# 网+第二根圆柱
    SS=p3d.combine(midsg1,AA1)
# 第一根柱子+(网+第二根圆柱)
    XZ1=p3d.combine(AA,SS)
    XZ2= p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f1) *XZ1
    data['所有']=p3d.combine(XZ2)
if __name__ == "__main__":
    data=p3d.P3DData({
        '圆柱高度': 1500,
        '圆柱半径': 40,
        # '总围栏长': 2000,
        # '柱子个数':2,
        '间隔宽度':2400,
        '网半径':2,
        '旋转角度':0,
        '场布分类':'辅助设施',
        '构件类型':'区域维护类',
        '构件名称':'安全隔离网样式一单点布置',
        })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('隔离网样式一附加',show = True)
    data.setup('所有', show=True)
    data.setup('圆柱高度' , obvious = True ,group='圆柱' , description ='高')
    data.setup('圆柱半径',obvious = True,group='圆柱' , description ='半径')
    data.setup('网半径',obvious = True,group='网' , description ='半径')
    # data.setup('柱子个数',obvious = True,group='柱子个数' , description ='个数')
    data.setup('间隔宽度',obvious=True,readonly=True,group='间距',description='间隔宽度')
    data.setup( '旋转角度', obvious=True, group='旋转',description= '旋转角度')
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = GLW
    GLW(data)
    p3d.launchData(data)
    