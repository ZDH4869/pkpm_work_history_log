import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:
    a=data['爬梯长度']
    b=data['爬梯宽度']
    c=data['爬梯数量']
    d=data['爬梯间距']
    e=data['爬梯半径']
    f=data['挂钩踏板半径']
    g=data['挂钩高度']
    h=data['挂钩宽度']
    i=data['挂钩斜杆长度']
    j=data['旋转角度']
    l=data['场布分类']
    m=data['构件类型']
    #左竖杆
    Cone1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,a),e,e).color(128/255,138/255,135/255,1)
    #右竖杆
    Cone2=p3d.Cone(p3d.Vec3(0,b+e*2,0),p3d.Vec3(0,b+e*2,a),e,e).color(128/255,138/255,135/255,1)
    #踏板
    Cone3=p3d.Cone(p3d.Vec3(0,0,d),p3d.Vec3(0,b+e*2,d),f,f).color(128/255,138/255,135/255,1)
    #挂钩
    a1=p3d.FilletPipe((p3d.Vec3(0,0,a),p3d.Vec3(0,0,a+g),p3d.Vec3(-h,0,a+g),p3d.Vec3(-h-200,0,a+g-250)),(0,20,20,0),f).color(128/255,138/255,135/255,1)
    a2=p3d.FilletPipe((p3d.Vec3(0,b+e*2,a),p3d.Vec3(0,b+e*2,a+g),p3d.Vec3(-h,b+e*2,a+g),p3d.Vec3(-h-200,b+e*2,a+g-250)),(0,20,20,0),f).color(128/255,138/255,135/255,1)
    #线性排布
    points1=p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,0,a-d),int(a/d)-1)
    A=p3d.combine()
    for point in points1:
        A.append(p3d.translation(point)*Cone3)
    B=p3d.combine(Cone1,Cone2,A,a1,a2)
    F1 = p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*j)*B
    data['爬梯数量']=int(a/d)-1
    data['下线爬梯']=p3d.combine(F1)
if __name__ == "__main__":
    data = p3d.P3DData({
        '爬梯长度':5600,
        '爬梯宽度':400,
        '爬梯间距':400,
        '爬梯半径':12,
        '挂钩踏板半径':9,
        '挂钩高度':400,
        '挂钩宽度':170,
        '挂钩斜杆长度':320,
        '旋转角度':270,
        '爬梯数量':14,
        '场布分类':'施工器械',
        '构件类型':'爬梯',
        '构件名称':'下线爬梯'
        })
    # data.set_view(1,1)
    data.setup('下线爬梯', show=True)
    data.setup('爬梯长度', obvious=True, group='爬梯', description='爬梯长度')
    data.setup('爬梯宽度', obvious=True, group='爬梯', description='爬梯宽度')
    data.setup('爬梯间距', obvious=True, group='爬梯', description='爬梯间距')
    data.setup('爬梯数量', obvious=True,readonly=True, group='爬梯', description='爬梯数量') 
    data.setup('爬梯半径', obvious=True,group='圆钢', description='爬梯半径') 
    data.setup('挂钩踏板半径', obvious=True,group='圆钢', description='挂钩踏板半径') 
    data.setup('挂钩高度', obvious=True,readonly=True,group='挂钩', description='挂钩高度') 
    data.setup('挂钩宽度', obvious=True,readonly=True,group='挂钩', description='挂钩宽度') 
    data.setup('挂钩斜杆长度', obvious=True,readonly=True,group='挂钩', description='挂钩斜杆长度') 
    data.setup('旋转角度', obvious=True,group='旋转角度', description='旋转角度') 
    data.setup('场布分类', obvious=True,readonly=True,group='公共属性', description='场部分类') 
    data.setup('构件类型', obvious=True,readonly=True,group='公共属性', description='构件类型') 
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)



