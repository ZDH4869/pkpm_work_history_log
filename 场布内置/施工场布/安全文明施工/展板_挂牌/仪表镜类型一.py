import pyp3d as p3d
from pyp3d import *
def wsl(data):
    Rotation = data['水平方向上的旋转角度（角度制）']

    #两侧柱
    Z1 = p3d.Cone(p3d.Vec3(1190,0,0),p3d.Vec3(1190,0,1860),40,40).color(0.82,0.82,0.82,1)
    Z2 = p3d.Cone(p3d.Vec3(-1190,0,0),p3d.Vec3(-1190,0,1860),40,40).color(0.82,0.82,0.82,1)
    #柱顶球
    BALL1 = p3d.Sphere(p3d.Vec3(1190,0,1900),50).color(0.82,0.82,0.82,1)
    BALL2 = p3d.Sphere(p3d.Vec3(-1190,0,1900),50).color(0.82,0.82,0.82,1)
    #展示牌、镜子（顺序由外及里）
    K1 = p3d.Box(p3d.Vec3(-1150,-10,700),p3d.Vec3(-1150,-10,1500),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),2300,20,2300,20).color(0.82,0.82,0.82,1)
    K2 = p3d.Box(p3d.Vec3(-1130,-10,720),p3d.Vec3(-1130,-10,1480),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),2260,20,2260,20).color(0.82,0.82,0.82,1)
    K = p3d.substract(K1,K2).color(0.82,0.82,0.82,1)
    P1 = p3d.Box(p3d.Vec3(-1130,-5,720),p3d.Vec3(-1130,-5,1480),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),2260,10,2260,10).color(0.1,0.1,0.5,1)
    P2 = p3d.Box(p3d.Vec3(430,-10,880),p3d.Vec3(430,-10,1280),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),300,10,300,10).color(0.1,0.1,0.5,1)
    P = p3d.substract(P1,P2).color(0.2,0.2,0.5,1)
    J = p3d.Box(p3d.Vec3(430,-2.5,880),p3d.Vec3(430,-2.5,1280),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),300,5,300,5).color(0.47,0.53,0.6,0.6)
    #装饰
    ZS1 = p3d.Box(p3d.Vec3(-1150,-10,1500),p3d.Vec3(-1150,-10,1750),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),2300,20,2300,20).color(0.82,0.82,0.82,1)
    ZS2 = p3d.Box(p3d.Vec3(-1130,-10,1500),p3d.Vec3(-1130,-10,1730),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),2260,20,2260,20).color(0.82,0.82,0.82,1)
    ZS3 = p3d.substract(ZS1,ZS2).color(0.82,0.82,0.82,1)
    ZS4 = p3d.Box(p3d.Vec3(-1130,-5,1500),p3d.Vec3(-1130,-5,1730),p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),2260,10,2260,10).color(0.3,0.3,0.4,1)
    ZS = p3d.combine(ZS3,ZS4)
    #字
    text = p3d.Text("仪 表 镜",100,100).color(0.1,0.1,1,1)
    text = p3d.rotation(p3d.Vec3(1,0,0), pi/2)*text
    ZI = text = p3d.translation(p3d.Vec3(-500,-6,1300))*text


    data['仪表镜-类型一'] = p3d.combine(Z1,Z2,BALL1,BALL2,K,P,J,ZS,ZI)
    data['仪表镜-类型一'] = p3d.rotation(p3d.Vec3(0,0,1),Rotation/180*pi)*data['仪表镜-类型一']

if __name__ == "__main__":
    data = P3DData({
        '水平方向上的旋转角度（角度制）': 0.00,
        '场布类型':'构筑物',
        '构件类型':'仪表镜',
        '构件名称':'仪表镜类型一'
    })
    data.set_view(-0.125*pi,-0.125*pi)
    data.setup('水平方向上的旋转角度（角度制）', obvious = True)
    data.setup('仪表镜-类型一', show = True)
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    data['replace'] = wsl
    wsl(data)
    p3d.launchData(data)
