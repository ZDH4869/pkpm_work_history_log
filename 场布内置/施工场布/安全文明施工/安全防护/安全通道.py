import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:
    box1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,data['通道高度']), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['侧面厚度'], data['通道长度'], data['侧面厚度'], data['通道长度']).color(30/255,166/255,1,1)
    box2 = p3d.Box(p3d.Vec3(data['侧面厚度']+data['通道宽度'],0,0), p3d.Vec3(data['侧面厚度']+data['通道宽度'],0,data['通道高度']), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['侧面厚度'], data['通道长度'], data['侧面厚度'], data['通道长度']).color(30/255,166/255,1,1)
    box3 = p3d.Box(p3d.Vec3(0,0,data['通道高度']), p3d.Vec3(0,0,data['通道高度']+data['顶面厚度']), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 2*data['侧面厚度']+data['通道宽度'], data['通道长度'], 2*data['侧面厚度']+data['通道宽度'], data['通道长度']).color(30/255,166/255,1,1)
    text1= p3d.Text("安全通道",((2*data['侧面厚度'])+data['通道宽度'])/6,2*(data['顶面厚度']/3)).color(225/255,225/255,225/255, 1)
    text1= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text1
    text1= p3d.translation(p3d.Vec3(((2*data['侧面厚度'])+data['通道宽度'])/36, -1,data['通道高度']+(data['顶面厚度']/6)))*text1

   
    B1=p3d.combine(box1,box2,box3,text1)
    
    data['安全通道']=B1
    data['总长度']=data['通道高度']
    data['总宽度']=((2*data['侧面厚度'])+data['通道宽度'])
    data['总高度']=data['通道高度']+data['顶面厚度']
    B=data['旋转角度']
    B1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*B)*B1
    # B1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*90)*B1
    # p3d.createGeometry(B1)
    data['安全通道']=B1
if __name__ == "__main__":
    data = p3d.P3DData({
        '场布分类':'道路交通',
        '构件类型':'安全通道',
        '构件名称':'安全通道',
        '通道长度':5000,
        '侧面厚度':300,
        '顶面厚度':300,
        '通道高度':1500,
        '通道宽度':1000,
        '旋转角度':0
         })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('安全通道', show=True)
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('通道长度', obvious=True, group='通道空间', description='通道长度')
    data.setup('侧面厚度', obvious=True, group='结构面', description='侧面厚度')
    data.setup('顶面厚度', obvious=True, group='结构面', description='顶面厚度')
    data.setup('通道高度', obvious=True, group='通道空间', description='通道高度')
    data.setup('通道宽度', obvious=True, group='通道空间', description='通道宽度')
    data.setup('总长度',obvious=True,readonly=True,group='整体边长',description='总长度')
    data.setup('总宽度',obvious=True,readonly=True,group='整体边长',description='总宽度')
    data.setup('总高度',obvious=True,readonly=True,group='整体边长',description='总高度')
    data.setup('旋转角度',obvious=True,group='旋转位置',description='旋转角度')
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)