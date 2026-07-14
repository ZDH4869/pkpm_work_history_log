import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:
    a=data['消防栓长度']
    b=data['消防栓宽度']
    c=data['消防栓厚度']
    d=data['上门长']
    e=data['上门宽']
    f=data['下门长']
    g=data['下门宽']
    h=data['门距底部距离']
    i=data['门框宽']
    j=data['告示牌长']
    k=data['告示牌宽']
    l=data['告示牌高']
    m=data['旋转角度']
    aaaa=data['场布分类']
    bbbb=data['构件类型']
#消防栓
    box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,1200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),300,700,300,700).color(1,69/255,0,1)
    box2=p3d.Box(p3d.Vec3(280,100,200),p3d.Vec3(280,100,1100),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,500,20,500).color(1,1,1,1)
    aaa=p3d.substract(box1,box2).color(1,69/255,0,1)
    box3=p3d.Box(p3d.Vec3(280,100,200),p3d.Vec3(280,100,1100),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,500,20,500).color(192/255,192/255,192/255,1)
    box4=p3d.Box(p3d.Vec3(280,150,600),p3d.Vec3(280,150,1050),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,400,20,400).color(192/255,192/255,192/255,1)
    box5=p3d.Box(p3d.Vec3(280,150,250),p3d.Vec3(280,150,550),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,400,20,400).color(192/255,192/255,192/255,1)
    box6=p3d.Box(p3d.Vec3(280,150,600),p3d.Vec3(280,150,1100),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,400,20,400).color(1,1,1,0.4)
    box7=p3d.Box(p3d.Vec3(280,150,250),p3d.Vec3(280,150,550),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,400,20,400).color(1,1,1,0.4)
#告示牌
    box8=p3d.Box(p3d.Vec3(0,-100,1200),p3d.Vec3(0,-100,1440),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),300,900,300,900).color(227/255,23/255,13/255,1)
    box9=p3d.Box(p3d.Vec3(0,-100,1200),p3d.Vec3(0,-100,1440),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),200,800,200,800).color(227/255,23/255,13/255,1)
    # createGeometry(box8)
    box9=p3d.translation(50,50,0)*box9
    # createGeometry(box9)
    box8=p3d.substract(box8,box9).color(227/255,23/255,13/255,1)
    # createGeometry(box8)
    a=p3d.substract(box3,box4)
    b=p3d.substract(a,box5).color(192/255,192/255,192/255,1)            #门框
    text = p3d.Text("消防栓", 50, 50).color(1, 0, 0, 1)
    text = p3d.rotation(p3d.Vec3(0, 0, 1), p3d.pi*0.5)*text
    text = p3d.rotation(p3d.Vec3(0, 1, 0), p3d.pi*0.5)*text
    text = p3d.translation(p3d.Vec3(301, 250, 900))*text
    F1=p3d.combine(aaa,b,box6,box7,box8,text)
    F1=p3d.translation(p3d.Vec3(-150,-350,0))*F1
    F3 = p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*270) * F1
    
    F4 = p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*m) * F3
    data['消防栓']=p3d.combine(F4)
    data['消防栓']=F4
if __name__ == "__main__":
    data = p3d.P3DData({
            '消防栓长度':1200,
            '消防栓宽度':700,
            '消防栓厚度':300,
            '上门长':500,
            '上门宽':400,
            '下门长':300,
            '下门宽':400,
            '门距底部距离':200,
            '门框宽':1200,
            '告示牌长':60,
            '告示牌宽':240,
            '告示牌高':240,
            '告示牌厚度':50,
            '旋转角度':0,
            '场布分类':'消防水电',
            '构件类型':'消防设备',
            '构件名称':'消防栓',
            })
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('消防栓', show=True)
    data.setup('消防栓长度', obvious=True, readonly=True,group='消防栓', description='消防栓长度')
    data.setup('消防栓宽度', obvious=True, readonly=True,group='消防栓', description='消防栓宽度')
    data.setup('消防栓厚度', obvious=True, readonly=True,group='消防栓', description='消防栓厚度')
    data.setup('上门长', obvious=True,readonly=True, group='门', description='上门长') 
    data.setup('上门宽', obvious=True,readonly=True,group='门', description='上门宽') 
    data.setup('下门长', obvious=True,readonly=True,group='门', description='下门长') 
    data.setup('下门宽', obvious=True,readonly=True,group='门', description='下门宽') 
    data.setup('门距底部距离', obvious=True,readonly=True,group='门', description='门距底部距离') 
    data.setup('门框宽', obvious=True,readonly=True,group='门', description='门框宽') 
    data.setup('告示牌长', obvious=True,readonly=True,group='告示牌', description='告示牌长') 
    data.setup('告示牌宽', obvious=True,readonly=True,group='告示牌', description='告示牌宽') 
    data.setup('告示牌高', obvious=True,readonly=True,group='告示牌', description='告示牌高') 
    data.setup('告示牌厚度', obvious=True,readonly=True,group='告示牌', description='告示牌厚度') 
    data.setup('旋转角度', obvious=True,group='旋转角度', description='旋转角度') 
    data.setup('场布分类', obvious=True,readonly=True,group='公共属性', description='场部分类') 
    data.setup('构件类型', obvious=True,readonly=True,group='公共属性', description='构件类型') 
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)