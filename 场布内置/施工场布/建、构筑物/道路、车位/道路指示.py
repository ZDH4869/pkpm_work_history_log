import pyp3d as p3d
from pyp3d import *
def WSL(data:p3d.P3DData)->None:
    L = data['杆长']
    R1 = data['球半径']
    R3 = data['底座下半径']
    R4 = data['底座上半径']
    R5 = data['杆半径']
    H1 = data['底座厚度']
    RAD1 = data['球红色值']
    RAD2 = data['上标示牌红色值']
    RAD3 = data['下标示牌红色值']
    RAD4 = data['杆红色值']
    RAD5 = data['底座红色值']
    G1 = data['球绿色值']
    G2 = data['上标示牌绿色值']
    G3 = data['下标示牌绿色值']
    G4 = data['杆绿色值']
    G5 = data['底座绿色值']
    B1 = data['球蓝色值']
    B2 = data['上标示牌蓝色值']
    B3 = data['下标示牌蓝色值']
    B4 = data['杆蓝色值']
    B5 = data['底座蓝色值']
    D1 = data['球不透明度']
    D2 = data['上标示牌不透明度']
    D3 = data['下标示牌不透明度']
    D4 = data['杆不透明度']
    D5 = data['底座不透明度']
    Rotation = data['水平方向上的旋转角度（角度制）']



    #底座、杆
    A1 = p3d.Cone(p3d.Vec3(250,250,0), p3d.Vec3(250,250,H1), R3,R4).color(RAD5/255,G5/255,B5/255,D5)
    A2 = p3d.Cone(p3d.Vec3(250,250,H1),p3d.Vec3(250,250,H1+L),R5,R5).color(RAD4/255,G4/255,B4/255,D4)
    #牌（上）
    A3 = p3d.Extrusion([p3d.Vec3(150,255,H1+L),p3d.Vec3(150,255,H1+L-100),p3d.Vec3(437.5,255,H1+L-125),p3d.Vec3(500,255,H1+L-62.5),p3d.Vec3(437.5,255,H1+L),p3d.Vec3(200,255,H1+L-62.5)],p3d.Vec3(0,-10,0)).color(RAD2/255,G2/255,B2/255,D2)
    #球
    A4 = p3d.Sphere(p3d.Vec3(250,250,H1+L+R1*2/3),R1).color(RAD1/255,G1/255,B1/255,D1)

    A5 = p3d.combine (A1,A2,A3,A4)
    A5 = p3d.translation(p3d.Vec3(-250,-250,0)) * A5
    #牌（下）
    F1 = p3d.Extrusion((p3d.Vec3(150,255,H1+L-100),p3d.Vec3(150,255,H1+L-225),p3d.Vec3(437.5,255,H1+L-225),p3d.Vec3(500,255,H1+L-162.5),p3d.Vec3(437.5,255,H1+L-100),p3d.Vec3(200,255,H1+L-162.5)),p3d.Vec3(0,-10,0)).color(RAD3/255,G3/255,B3/255,D3)
    F1 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*0.5) * F1
    F1 = p3d.translation(p3d.Vec3(250,-250,0)) * F1

    data['道路指示'] =p3d.combine(A5,F1)
    data['道路指示'] = p3d.rotation(p3d.Vec3(0,0,1),Rotation/180*pi)*data['道路指示']


if __name__ == "__main__":
    data = p3d.P3DData({
        '杆长': 2250,
        '杆半径':20,
        '球半径': 75,
        '底座下半径': 125,
        '底座上半径': 125,
        '底座厚度': 200,
        '球红色值':255,
        '上标示牌红色值':255,
        '下标示牌红色值':51,
        '杆红色值':255,
        '底座红色值':127.5,
        '球绿色值':255,
        '上标示牌绿色值':255,
        '下标示牌绿色值':255,
        '杆绿色值':255,
        '底座绿色值':127.5,
        '球蓝色值':0,
        '上标示牌蓝色值':0,
        '下标示牌蓝色值':127.5,
        '杆蓝色值':255,
        '底座蓝色值':127.5,
        '球不透明度':1,
        '上标示牌不透明度':1,
        '下标示牌不透明度':1,
        '杆不透明度':1,
        '底座不透明度':1,
        '水平方向上的旋转角度（角度制）': 0.00,
        '场布类型':'挂牌资料',
        '构件类型':'标识牌基本类型',
        '构件名称':'道路指示'


        })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('道路指示', show=True)
    data.setup('杆长', obvious=True, group='杆',description='长')
    data.setup('杆半径', obvious=True, group='杆',description='杆的半径')
    data.setup('球半径', obvious=True, group='球',description='球半')
    data.setup('底座上半径', obvious=True, group='底座',description='底座上半')  
    data.setup('底座下半径', obvious=True, group='底座',description='底座下半')  
    data.setup('底座厚度', obvious=True, group='底座',description='底座')
    data.setup('球红色值', obvious=True, readonly=True,group='球体颜色',description='球色')
    data.setup('上标示牌红色值', obvious=True, readonly=True,group='上标示牌颜色',description='上色')
    data.setup('下标示牌红色值', obvious=True, readonly=True,group='下标示牌颜色',description='下色')
    data.setup('杆红色值', obvious=True, readonly=True,group='杆颜色',description='杆色')
    data.setup('底座红色值', obvious=True, readonly=True,group='底座颜色',description='底色')
    data.setup('球绿色值', obvious=True, readonly=True,group='球体颜色',description='球色')
    data.setup('上标示牌绿色值', obvious=True, readonly=True,group='上标示牌颜色',description='上色')
    data.setup('下标示牌绿色值', obvious=True, readonly=True,group='下标示牌颜色',description='下色')
    data.setup('杆绿色值', obvious=True, readonly=True,group='杆颜色',description='杆色')
    data.setup('底座绿色值', obvious=True, readonly=True,group='底座颜色',description='底色')
    data.setup('球蓝色值', obvious=True,  readonly=True,group='球体颜色',description='球色')
    data.setup('上标示牌蓝色值', obvious=True, readonly=True,group='上标示牌颜色',description='上色')
    data.setup('下标示牌蓝色值', obvious=True, readonly=True,group='下标示牌颜色',description='下色')
    data.setup('杆蓝色值', obvious=True, readonly=True,group='杆颜色',description='杆色')
    data.setup('底座蓝色值', obvious=True, readonly=True,group='底座颜色',description='底色')
    data.setup('球不透明度', obvious=True, readonly=True,group='球体颜色',description='球色')
    data.setup('上标示牌不透明度', obvious=True, readonly=True,group='上标示牌颜色',description='上色')
    data.setup('下标示牌不透明度', obvious=True, readonly=True,group='下标示牌颜色',description='下色')
    data.setup('杆不透明度', obvious=True, readonly=True,group='杆颜色',description='杆色')
    data.setup('底座不透明度', obvious=True, readonly=True,group='底座颜色',description='底色')
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    data.setup('水平方向上的旋转角度（角度制）', obvious = True)

    data['replace'] = WSL
    WSL(data)
    p3d.launchData(data)