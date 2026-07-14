import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:

    a=data['长度']
    b=data['宽度']
    c=data['墙体高度']
    d=data['屋顶高度']
    e=data['底部厚度']
    f=data['告示牌长度']
    g=data['告示牌宽度']
    h=data['门高度']
    i=data['门宽度']
    j=data['门厚度']
    k=data['旋转角度']
    l=data['场布分类']
    m=data['构件类型']
#底座
    box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,100),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b,a,b,a).color(135/255,206/255,235/255,1)
#房板
    box2=p3d.Box(p3d.Vec3(0,0,100),p3d.Vec3(0,0,100+c),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b,a,b,a).color(128/255,138/255,135/255,1)
#屋顶
    box3=p3d.Box(p3d.Vec3(0,0,100+c),p3d.Vec3(0,0,100+c+d),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b,a,b,a).color(135/255,206/255,235/255,1)
#门   
    box4=p3d.Box(p3d.Vec3(b-60,a/2-600,100),p3d.Vec3(b-60,a/2-600,2400),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),60,1200,60,1200).color(0,0,0,1)
    box5=p3d.Box(p3d.Vec3(b-60,a/2-600,100),p3d.Vec3(b-60,a/2-600,2400),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),60,1200,60,1200).color(30/255,144/255,1,1)
#告示牌    
    box6=p3d.Box(p3d.Vec3(b,a*51/80,c/2),p3d.Vec3(b,a*51/80,c/2+1200),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),2,(a+c)/8,2,(a+c)/8).color(1,1,1,1)
#文字
    text = p3d.Text("消防泵房", 500, 500).color(224/255,224/255,224/255,1)
    text =p3d.translation(p3d.Vec3(a/3, 100+c+d/4, b+1))*text
    text = p3d.rotation(p3d.Vec3(0, 0, 1), p3d.pi*0.5)*text
    text = p3d.rotation(p3d.Vec3(0, 1, 0), p3d.pi*0.5)*text
#整体
    AAA=p3d.substract(box2,box4).color(128/255,138/255,135/255,1)
    F1=p3d.combine(box1,box3,AAA,box5,box6,text)
    F1=p3d.translation(p3d.Vec3(-b/2,-a/2,0))*F1
    F2 = p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*270)* F1
    F2 = p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)* F2
    data['消防泵房']=p3d.combine(F2)

if __name__ == "__main__":
    data = p3d.P3DData({
        '长度':8000,
        '宽度':6000,
        '墙体高度':4000,
        '屋顶高度':1000,
        '底部厚度':100,
        '告示牌长度':1500,
        '告示牌宽度':1200,
        '门高度':2300,
        '门宽度':1200,
        '门厚度':60,
        '旋转角度':0,
        '场布分类':'消防水电',
        '构件类型':'消防泵房',
        '构件名称':'消防泵房'
        })
    
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('消防泵房', show=True)
    data.setup('长度', obvious=True, group='泵房', description='长度')
    data.setup('宽度', obvious=True, group='泵房', description='宽度')
    data.setup('墙体高度', obvious=True, group='泵房', description='墙体高度')
    data.setup('屋顶高度', obvious=True, group='泵房', description='屋顶高度') 
    data.setup('底部厚度', obvious=True,readonly=True,group='泵房', description='底部厚度') 
    data.setup('告示牌长度', obvious=True,readonly=True,group='告示牌', description='告示牌长度') 
    data.setup('告示牌宽度', obvious=True,readonly=True,group='告示牌', description='告示牌宽度') 
    data.setup('门高度', obvious=True,readonly=True,group='门', description='门高度') 
    data.setup('门宽度', obvious=True,readonly=True,group='门', description='门宽度') 
    data.setup('门厚度', obvious=True,readonly=True,group='门', description='门厚度') 
    data.setup('旋转角度', obvious=True,group='旋转角度', description='旋转角度') 
    data.setup('场布分类', obvious=True,readonly=True,group='公共属性', description='场部分类') 
    data.setup('构件类型', obvious=True,readonly=True,group='公共属性', description='构件类型') 
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)