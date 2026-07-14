import pyp3d as p3d
def cx(data:p3d.P3DData)->None:
    # 广告牌
    H1= data['广告板长']#广告板长度及两柱子间距离
    H2= data['广告板宽']#广告板宽度
    H3= data['柱高']#柱子高柱及顶棚高度
    H4= data['柱半径']#柱子半径
    H5= data['广告板厚']#广告板厚度
    if H5<300:
        ConH5 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,H3+40),H4,H4).color(0,1,1,1)
        Cone2 = p3d.Cone(p3d.Vec3(H1+H4+H4,0,0),p3d.Vec3(H1+H4+H4,0,H3+40),H4,H4).color(0,1,1,1)
        Box1 = p3d.Box(p3d.Vec3(H4,0,H3-H2),p3d.Vec3(H4,0,H3-200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),H1,H5,H1,H5).color(0.5,0.5,0.5,1)
        Box2 = p3d.RotationalSweep([p3d.Vec3(-200,H5+140,H3-200),p3d.Vec3(-200,H5+150,H3-200),p3d.Vec3(H1+200+H4+H4,H5+150,H3-200),p3d.Vec3(H1+200+H4+H4,H5+140,H3-200)]\
            ,p3d.Vec3(0,0,H3-200),p3d.Vec3(1,0,0),1*p3d.pi).color(0.8,0.8,0.8,1)
        Box3 = p3d.translation(p3d.Vec3(0,0,-(H5+140-245))) * Box2
        BoxA = p3d.Box(p3d.Vec3(H4,0,H3-H2),p3d.Vec3(H4,0,H3-200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),H1,-H5,H1,-H5).color(0.5,0.5,0.5,1)
        BoxB = p3d.Box(p3d.Vec3(H4+100,0,H3-H2+100),p3d.Vec3(H4+100,0,H3-100-200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),H1-200,-H5,H1-200,-H5).color(0.5,0.5,0.5,1)
        BB=p3d.substract(BoxA,BoxB).color(0.5,0.5,0.5,1)
        # BB1 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * BB
        # BB2 = p3d.translation(p3d.Vec3(H4*2+H1,25,0)) * BB1
        data['宣传架-有顶棚']= p3d.combine(ConH5,Cone2,Box1,BB,Box3)
        # p3d.createGeometry(data['A'])
    else:
        H5=300
        ConH5 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,H3+40),H4,H4).color(0,1,1,1)
        Cone2 = p3d.Cone(p3d.Vec3(H1+H4+H4,0,0),p3d.Vec3(H1+H4+H4,0,H3+40),H4,H4).color(0,1,1,1)
        Box1 = p3d.Box(p3d.Vec3(H4,0,H3-H2),p3d.Vec3(H4,0,H3-200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),H1,H5,H1,H5).color(0.5,0.5,0.5,1)
        Box2 = p3d.RotationalSweep([p3d.Vec3(-200,H5+140,H3-200),p3d.Vec3(-200,H5+150,H3-200),p3d.Vec3(H1+200+H4+H4,H5+150,H3-200),p3d.Vec3(H1+200+H4+H4,H5+140,H3-200)]\
            ,p3d.Vec3(0,0,H3-200),p3d.Vec3(1,0,0),1*p3d.pi).color(0.8,0.8,0.8,1)
        Box3 = p3d.translation(p3d.Vec3(0,0,-(H5+140-245))) * Box2
        BoxA = p3d.Box(p3d.Vec3(H4,0,H3-H2),p3d.Vec3(H4,0,H3-200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),H1,-H5,H1,-H5).color(0.5,0.5,0.5,1)
        BoxB = p3d.Box(p3d.Vec3(H4+100,0,H3-H2+100),p3d.Vec3(H4+100,0,H3-100-200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),H1-200,-H5,H1-200,-H5).color(0.5,0.5,0.5,1)
        BB=p3d.substract(BoxA,BoxB).color(0.5,0.5,0.5,1)
        # BB1 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * BB
        # BB2 = p3d.translation(p3d.Vec3(H4*2+H1,25,0)) * BB1
        data['宣传架-有顶棚']= p3d.combine(ConH5,Cone2,Box1,BB,Box3)
        # p3d.createGeometry(data['A'])
if __name__ == "__main__":
    data=p3d.P3DData({
        '场布分类':'挂牌资料',
        '构件类型':'其他标识牌',
        '构件名称':'宣传架有顶棚',
        '广告板长':1800,
        '广告板宽': 1200,
        '柱高': 2340,
        '柱半径': 50,
        '广告板厚': 60,
        })
    data.setup('宣传架-有顶棚',show = True)
    data.setup('广告板长' , obvious = True ,group='广告板参数' , description ='广告板长')
    data.setup('广告板宽',obvious = True,group='广告板参数' , description ='广告板宽')
    data.setup('柱高',obvious = True,group='柱子参数' , description ='柱高')
    data.setup('柱半径',obvious = True,group='柱子参数' , description ='柱半径')
    data.setup('广告板厚',obvious = True,group='广告板参数', description='广告板厚')
    data.setup('场布分类',obvious=True,readonly=True,group='公共属性',description='场布分类')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)
    

    data['replace'] = cx
    cx(data)
    p3d.launchData(data)