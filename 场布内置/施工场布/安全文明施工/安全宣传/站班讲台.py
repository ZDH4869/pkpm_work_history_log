import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:

    a1=data['长度']#讲台及背景墙长度
    a2=data['讲台宽度']
    a3=data['讲台高度']
    b2=data['背景墙厚度']
    b3=data['背景墙宽度']
    aaa = data['是否显示讲台']
    k=data['旋转角度']

    # 背景墙和讲台
    box1 = p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,a3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a2,a1,a2).color(128/255,42/255,42/255,1)
    box2 = p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,b3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,b2,a1,b2).color(176/255,224/255,230/255,1)
    AAA = p3d.combine(box1,box2)

    # 圆桌
    if aaa == '否':
        AAA=p3d.translation(p3d.Vec3(-a1,-a2,0))*AAA
        AAA= p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*180)* AAA
        AAA= p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)* AAA
        data['讲台'] = AAA

    else :
        data['是否显示讲台'] = '是'
        Cone1=p3d.Cone(p3d.Vec3(2000,2000,0),p3d.Vec3(2000,2000,500),500,500).color(139/255,69/255,19/255,1)
        Cone2=p3d.Cone(p3d.Vec3(2000,2000,1400),p3d.Vec3(2000,2000,1600),500,500).color(139/255,69/255,19/255,1)
        Cone3=p3d.Cone(p3d.Vec3(2000,2000,500),p3d.Vec3(2000,2000,1400),200,400).color(244/255,164/255,96/255,1)
        Cone4=p3d.Cone(p3d.Vec3(2000,2000,1600),p3d.Vec3(2000,2000,1800),50,20).color(94/255,38/255,18/255,1)
        Sphere1 = p3d.Sphere(p3d.Vec3(2000,2000,1800),50).color(41/255,36/255,33/255,1)
        BBB=p3d.combine(Cone1,Cone2,Cone3,Cone4,Sphere1)

    # 整体
        CCC = p3d.combine(AAA,BBB)
        DDD=p3d.translation(p3d.Vec3(-a1,-a2,0))*CCC
        DDD= p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*180)* DDD
        DDD= p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)* DDD
        data['讲台']=DDD


if __name__ == "__main__":
    data = p3d.P3DData({
        '讲台宽度': 3000,
        '长度': 4000,#讲台及背景墙长度
        '讲台高度': 300,
        '背景墙厚度':300,
        '背景墙宽度': 4300,
        '是否显示讲台':'是',
        '旋转角度':0,
        '场布分类':'辅助设施',
        '构件类型':'站班讲台',
        '构件名称':'站班讲台',
         })  
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('讲台', show=True)
    data.setup('讲台宽度', obvious=True, group='讲台', description='讲台宽度')
    data.setup('长度', obvious=True, group='讲台', description='讲台长度')
    data.setup('是否显示讲台', obvious=True, group='讲台', description='讲台长度')
    data.setup('讲台高度', obvious=True, group='讲台', description='讲台高度')
    data.setup('背景墙厚度', obvious=True, group='背景墙', description='背景墙厚度')
    data.setup('背景墙宽度', obvious=True, group='背景墙', description='背景墙宽度') 
    data.setup('旋转角度', obvious=True, group='旋转角度', description='旋转角度') 
    data.setup('场布分类', obvious=True,readonly=True,group='类型参数', description='场部分类') 
    data.setup('构件类型', obvious=True,readonly=True,group='类型参数', description='构件类型') 
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)