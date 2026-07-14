import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:
    a=data['高度']
    b=data['半径']
    l=data['场布分类']
    m=data['构件类型']
    Cone1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,20),b+10,b+10).color(1,69/255,0,1)
    Cone2=p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,(a+20)/3),b,b).color(1,69/255,0,1)
    Cone3=p3d.Cone(p3d.Vec3(0,0,(a+20)/3),p3d.Vec3(0,0,(a+80)/3),b+10,b+10).color(1,69/255,0,1)
    Cone4=p3d.Cone(p3d.Vec3(0,0,(a+80)/3),p3d.Vec3(0,0,(a*2+40)/3),b,b).color(1,69/255,0,1)
    Cone5=p3d.Cone(p3d.Vec3(0,0,(a*2+40)/3),p3d.Vec3(0,0,(a*2+100)/3),b+10,b+10).color(1,69/255,0,1)
    Cone6=p3d.Cone(p3d.Vec3(0,0,(a*2+100)/3),p3d.Vec3(0,0,a+20),b,b).color(1,69/255,0,1)
    Cone7=p3d.Cone(p3d.Vec3(0,0,a+20),p3d.Vec3(0,0,a+40),b+10,b+10).color(1,69/255,0,1)
    data['消防桶']=p3d.combine(Cone1,Cone2,Cone3,Cone4,Cone5,Cone6,Cone7)
if __name__ == "__main__":
    data = p3d.P3DData({
        '高度':1050,
        '半径':415,
        '场布分类':'消防水电',
        '构件类型':'消防设备',
        '构件名称':'消防桶',
        })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('消防桶', show=True)
    data.setup('高度', obvious=True, group='消防桶', description='高度')
    data.setup('半径', obvious=True, group='消防桶', description='半径') 
    data.setup('场布分类', obvious=True,readonly=True,group='公共属性', description='场部分类') 
    data.setup('构件类型', obvious=True,readonly=True,group='公共属性', description='构件类型') 
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)