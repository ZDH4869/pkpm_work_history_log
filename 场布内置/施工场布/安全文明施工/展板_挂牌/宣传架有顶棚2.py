import pyp3d as p3d
def zsp(data:p3d.P3DData)->None:
    A1= data['展示板长']
    A2= data['展示板宽']
    C1= data['柱高']
    C2= data['柱半径']
    D1= 100
    D2= 200
    k=data['旋转角度']
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,C1),C2,C2).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(A1+C2+C2,0,0),p3d.Vec3(A1+C2+C2,0,C1),C2,C2).color(1,1,1,1)
    Box1 = p3d.Box(p3d.Vec3(C2,-25,C1-A2),p3d.Vec3(C2,-25,C1-D2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),A1,60,A1,60).color(1,1,1,1)
    # Box1 =p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*Box1
    Box2 = p3d.RotationalSweep([p3d.Vec3(-200,240,C1-D2),p3d.Vec3(-200,250,C1-D2),p3d.Vec3(A1+D2+C2+C2,250,C1-D2),p3d.Vec3(A1+D2+C2+C2,240,C1-D2)],p3d.Vec3(2100,0,C1-D2),p3d.Vec3(1,0,0),1*p3d.pi).color(135/255,206/255,235/255,1)
    # Box2 =p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*Box2
    BoxA = p3d.Box(p3d.Vec3(C2,20,C1-A2),p3d.Vec3(C2,20,C1-D2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),A1,60,A1,60).color(0.5,0.5,0.5,1)
    BoxB = p3d.Box(p3d.Vec3(C2+D1,20,C1-A2+D1),p3d.Vec3(C2+D1,20,C1-D1-D2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),A1-D2,60,A1-D2,60).color(0.5,0.5,0.5,1)
    BB=p3d.substract(BoxA,BoxB).color(192/255,192/255,192/255,1)
    DisplayBoard= p3d.combine(Cone1,Cone2,Box1,Box2,BB)
    DisplayBoard=p3d.translation(p3d.Vec3(-(A1/2+C2),0,0))*DisplayBoard
    # DisplayBoard=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*DisplayBoard
    DisplayBoard=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*DisplayBoard
    DisplayBoard=p3d.translation(p3d.Vec3(A1/2+C2,0,0))*DisplayBoard
    # p3d.createGeometry(data['A'])
    Texture = p3d.translation(p3d.Vec3(A1/2+C2,0,0))*p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*p3d.translation(p3d.Vec3(-(A1/2+C2),0,0))*p3d.Box(p3d.Vec3(C2+D1,-40,C1-A2+D1),p3d.Vec3(C2+D1,-40,C1-D1-D2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),A1-D2,5,A1-D2,5).color(1,0,0,1)
    data['贴图']=Texture
    data['展示板']=p3d.combine(DisplayBoard,Texture)
    # data['展示板']= Box1
if __name__ == "__main__":
    data=p3d.P3DData({
        '展示板长': 1800,
        '展示板宽': 1200,
        '柱高': 2340,
        '柱半径': 50,
        '旋转角度':0,
        '场布类型':'构筑物',
        '构件类型':'展示牌',
        '构件名称':'宣传架有顶棚2',
        })
    # data.set_view(1,1)
    data.setup('展示板',show = True)
    # data.setup('贴图',show = True)

    data.setup('展示板长' , obvious = True ,group='长' , description ='板长')
    data.setup('展示板宽',obvious = True,group='宽' , description ='板宽')
    data.setup('柱高',obvious = True,group='高' , description ='柱高')
    data.setup('柱半径',obvious = True,group='半径' , description ='柱半径')
    data.setup('旋转角度',obvious=True,group='旋转角度',description='旋转角度')
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    data['replace'] = zsp
    zsp(data)
    p3d.launchData(data)


