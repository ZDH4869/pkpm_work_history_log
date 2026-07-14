import pyp3d as p3d
import math
def GLW(data:p3d.P3DData)->None:
    z1=data['圆柱高度']#圆柱高度
    R =data['圆柱半径']#圆柱半径
    # c =data['总围栏长']#总围栏长度
    # s=data['柱子个数']#柱子个数
    a=data['网半径']#网半径
    w=data['间隔宽度']#两柱之间间距
    Elo = data['总长度']
    n= int(Elo/w)
    data['总长度'] = n*w
    f1=data['旋转角度']
    
#固定圆柱
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,z1/6),R,R).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,z1/6),p3d.Vec3(0,0,z1*2/6),R,R).color(1,0,0,1) 
    Cone3 = p3d.Cone(p3d.Vec3(0,0,z1*2/6),p3d.Vec3(0,0,z1*3/6),R,R).color(1,1,1,1)
    Cone4 = p3d.Cone(p3d.Vec3(0,0,z1*3/6),p3d.Vec3(0,0,z1*4/6),R,R).color(1,0,0,1)
    Cone5 = p3d.Cone(p3d.Vec3(0,0,z1*4/6),p3d.Vec3(0,0,z1*5/6),R,R).color(1,1,1,1)
    Cone6 = p3d.Cone(p3d.Vec3(0,0,z1*5/6),p3d.Vec3(0,0,z1),R,R).color(1,0,0,1)
    AA = p3d.combine(Cone1,Cone2,Cone3,Cone4,Cone5,Cone6)

# 第二根圆柱
    midsg1 = p3d.translation(p3d.Vec3(w+R,0,0)) * AA
# 十字网柱
    # 网横柱
    ConeA = p3d.Cone(p3d.Vec3(0,0,z1*1.1/6),p3d.Vec3(w,0,z1*1.1/6),R,R).color(1,0,0,1)
    ConeB = p3d.Cone(p3d.Vec3(0,0,z1*3.5/6),p3d.Vec3(w,0,z1*3.5/6),R,R).color(1,0,0,1)
    ConeC = p3d.Cone(p3d.Vec3(0,0,z1*5.9/6),p3d.Vec3(w,0,z1*5.9/6),R,R).color(1,0,0,1)
    # 网立柱
    ConeD = p3d.Cone(p3d.Vec3(w/2,0,z1/6),p3d.Vec3(w/2,0,z1),R,R).color(1,0,0,1)
    WZ=p3d.combine(ConeA,ConeB,ConeC,ConeD)

# 网   
    # 竖线
    ConeA = p3d.Cone(p3d.Vec3(0,0,z1*1.2/6),p3d.Vec3(0,0,z1*5.8/6),a,a).color(1,0,0,1)
    HW = p3d.Array(ConeA)
    for i in  p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(w,0,0),32):
        HW.append(p3d.translation(i))
    # 横线
    ConeB = p3d.Cone(p3d.Vec3(0,0,z1*1.2/6),p3d.Vec3(w,0,z1*1.2/6),a,a).color(1,0,0,1)
    SW = p3d.Array(ConeB)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,0,z1*4.6/6),18):
        SW.append(p3d.translation(i))
    AA1=p3d.combine(HW,SW)
# 网+第二根圆柱+十字网柱
    SS=p3d.combine(midsg1,AA1,WZ)
    unit = p3d.Array(SS)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(int(Elo/w-1)*(w),0,0),(int(n))):
        unit.append(p3d.translation(i))

# 第一根柱子+(十字网柱+网+第二根圆柱)再旋转
    XZ1=p3d.combine(AA,unit)
    XZ2= p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f1) *XZ1
    data['所有']=XZ2
if __name__ == "__main__":
    data=p3d.P3DData({
        '圆柱高度': 1200,
        '圆柱半径': 20,
        # '总围栏长': 2000,
        # '柱子个数':2,
        '间隔宽度':2000,
        '总长度': 5000,
        '网半径':3,
        '旋转角度':0,
        '场布分类':'辅助设施',
        '构件类型':'区域维护类',
        '构件名称':'安全隔离网样式二两点布置',
        })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('隔离网样式二',show = True)
    data.setup('所有', show=True)
    data.setup('圆柱高度' , obvious = True ,group='圆柱' , description ='高')
    data.setup('圆柱半径',obvious = True,group='圆柱' , description ='半径')
    data.setup('网半径',obvious = True,group='网' , description ='半径')
    data.setup('总长度',obvious = True,group='总长度' , description ='长')
    # data.setup('柱子个数',obvious = True,group='柱子个数' , description ='个数')
    data.setup('间隔宽度',obvious=True,readonly=True,group='间距',description='间隔宽度')
    data.setup( '旋转角度', obvious=True, group='旋转',description= '旋转角度')
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('构件名称',obvious=True)

    data['replace'] = GLW
    p3d.TwoPointPlace.linearize(data, '总长度')
    # GLW(data)
    p3d.launchData(data)