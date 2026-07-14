import pyp3d as p3d
import math

def cui(data:p3d.P3DData)->None:
    z1=data['圆柱高度']#圆柱高度
    R =data['圆柱半径']#圆柱半径
    c =data['总围栏长']#总围栏长度
    s=data['柱子个数']#柱子个数
    n=data['横幅宽度']#横幅宽度
    f=data['旋转角度']#旋转角度
    
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
    Box1=p3d.Box(p3d.Vec3(0,0,z1-n),p3d.Vec3(0,0,z1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),c,5,c,5).color(1,0,0,0.5)
    Box2 = p3d.translation(p3d.Vec3(0,-5/2,0))*Box1
    cuix = p3d.combine()
    Points = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(c,0,0),s)
    for i in Points:
        cuix.append(p3d.translation(i)*AA)
    AA1=p3d.combine(AA,cuix,Box2)
    AA2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f)*AA1
    AA3 = p3d.translation(p3d.Vec3(0,0,R*3))*AA2
    data['提示遮拦-字'] = AA3
if __name__ == "__main__":
    data=p3d.P3DData({
        '场布分类':'提示遮拦-字',
        '构件类型':'提示遮拦-字',
        '构件名称':'提示遮拦横条',
        '圆柱高度': 2400,
        '圆柱半径': 40,
        '总围栏长': 2000,
        '柱子个数':2,
        '横幅宽度':100,
        '旋转角度':0,
        })
    # data.set_view(1,1)
    data.setup('提示遮拦-字',show = True)
    data.setup('圆柱高度' , obvious = True ,group='圆柱' , description ='高')
    data.setup('圆柱半径',obvious = True,group='圆柱' , description ='半径')
    data.setup('总围栏长',obvious = True,group='总围栏长' , description ='长')
    data.setup('柱子个数',obvious = True,group='圆柱' , description ='个数')
    data.setup('横幅宽度',obvious = True,group='横幅宽度' , description ='横幅宽度')
    data.setup('柱子间距',obvious=False,readonly=True,group='侧板间距',description='柱子间距')
    data.setup('旋转角度',obvious = True,group='旋转', description='旋转角度')
    data.setup('场布分类',obvious=True,readonly=True,group='公共属性',description='场布分类')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = cui
    cui(data)
    p3d.launchData(data)