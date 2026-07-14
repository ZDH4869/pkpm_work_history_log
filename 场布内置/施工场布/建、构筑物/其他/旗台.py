import pyp3d as p3d
def LKH(data:p3d.P3DData)->None:
    a1= data['底座高度']
    a2 = data['底座长度']
    a3 = data['底座宽度']
    b1=data['杆1高度']
    b2=data['杆1半径']
    c1=data['杆2高度']
    c2=data['杆2半径']
    d1=data['杆3高度']
    d2=data['杆3半径']
    e1=data['旗面宽度']
    e2=data['旗面长度']
    f1=data['旋转角度']
    lflag_interval = data['左旗杆间隔']
    rflag_interval = data['右旗杆间隔']
    
    
    
    if c2*2+150 < lflag_interval < 0.5*a2 and c2*2+150 < rflag_interval < 0.5*a2:   
        lflag_interval = lflag_interval
        rflag_interval = rflag_interval   
    elif c2*2+150 < lflag_interval < 0.5*a2 and rflag_interval >= 0.5*a2:  
        lflag_interval = lflag_interval
        rflag_interval = 0.5*a2-c2
    elif lflag_interval >= 0.5*a2 and c2*2+150 < rflag_interval < 0.5*a2:   
        lflag_interval = 0.5*a2-b2
        rflag_interval = rflag_interval
    elif lflag_interval >= 0.5*a2 and rflag_interval >= 0.5*a2:
        lflag_interval = 0.5*a2-b2
        rflag_interval = 0.5*a2-c2  
    elif c2*2+150 < lflag_interval < 0.5*a2 and rflag_interval < c2*2+150:
        lflag_interval = lflag_interval
        rflag_interval = c2*2 +150       
    elif lflag_interval < c2*2+150 and c2*2+150 < rflag_interval < 0.5*a2:
        lflag_interval = c2*2+150
        rflag_interval = rflag_interval
    elif lflag_interval < c2*2+150 and rflag_interval < c2*2+150:
        lflag_interval = c2*2+150
        rflag_interval = c2*2 +150
    elif lflag_interval < c2*2+150 and rflag_interval >= 0.5*a2:
        lflag_interval = c2*2+150
        rflag_interval = 0.5*a2-c2
    elif lflag_interval >= 0.5*a2 and rflag_interval < c2*2+150:
        lflag_interval = 0.5*a2-b2
        rflag_interval = c2*2+150        
# 旗台
    box1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,a1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), a2, a3, a2,a3).color(94/255,38/255,18/255,1)
    # 旗杆
    Cone1 = p3d.Cone(p3d.Vec3(a2*0.5-lflag_interval,a3*0.5,a1),p3d.Vec3(a2*0.5-lflag_interval,a3*0.5,b1+a1,),b2,b2).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(a2*0.5,a3*0.5,a1),p3d.Vec3(a2*0.5,a3*0.5,c1+a1),c2,c2).color(1,1,1,1)
    Cone3 = p3d.Cone(p3d.Vec3(a2*0.5+rflag_interval,a3*0.5,a1),p3d.Vec3(a2*0.5+rflag_interval,a3*0.5,d1+a1),d2,d2).color(1,1,1,1)
    box2 = p3d.Box(p3d.Vec3(a2*0.5-lflag_interval+b2,a3*0.5,a1+b1-e1-100), p3d.Vec3(a2*0.5-lflag_interval+b2,a3*0.5,b1+a1-100), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), e2, 1, e2,1).color(192/255,192/255,192/255,1)
    box3 = p3d.Box(p3d.Vec3(a2*0.5+c2,a3*0.5,a1+c1-e1-100), p3d.Vec3(a2*0.5+c2,a3*0.5,c1+a1-100), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), e2, 1, e2,1).color(1,0,0,1)
    box4 = p3d.Box(p3d.Vec3(a2*0.5+rflag_interval+d2,a3*0.5,a1+d1-e1-100), p3d.Vec3(a2*0.5+rflag_interval+d2,a3*0.5,d1+a1-100), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), e2, 1, e2,1).color(1,1,0,1)
    # 阻断球
    Sphere1 = p3d.Sphere(p3d.Vec3(a2*0.5-lflag_interval,a3*0.5,a1+b1+b2*1.5),b2*1.5).color(1,1,1,1)
    Sphere2 = p3d.Sphere(p3d.Vec3(a2*0.5,a3*0.5,a1+c1+c2*1.52),c2*1.5).color(1,1,1,1)
    Sphere3 = p3d.Sphere(p3d.Vec3(a2*0.5+rflag_interval,a3*0.5,a1+d1+d2*1.5),d2*1.5).color(1,1,1,1)
        
    # data['间距']=a2*0.25 #a2 = data['底座长度']
    data['一个圆锥台'] = p3d.combine(box1,Cone1, Cone2,Cone3, box2,box3,box4,Sphere1,Sphere2,Sphere3)
    # 整体旋转
    A1=p3d.combine(box1,Cone1, Cone2,Cone3, box2,box3,box4,Sphere1,Sphere2,Sphere3)
    A2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f1) *A1
    data['一个圆锥台'] = A2
if __name__ == "__main__":
    data = p3d.P3DData({
         '底座高度':500,
         '底座长度':8000,
         '底座宽度':1500,
         '杆1高度':11000,
         '杆1半径':100,
         '杆2高度':12000,
         '杆2半径':100,
         '杆3高度':11000,
         '杆3半径':100,
         '旗面宽度':960,
         '旗面长度':1440,
         '阻断球1半径':150,
         '阻断球2半径':150,
         '阻断球3半径':150,
         '旋转角度':0,
         '场布分类':'辅助设施',
         '构件类型':'旗台',
         '构件名称':'旗台',
         '左旗杆间隔':2000,
         '右旗杆间隔':2000,
         

    })
    data.setup('一个圆锥台', show=True)
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('底座高度', obvious=True, group='底座',description='底座高度')
    data.setup('底座长度', obvious=True, group='底座',description='底座长度')
    data.setup('底座宽度', obvious=True, group='底座',description='底座宽度')
    data.setup('杆1高度', obvious=True, group='旗杆',description='杆1高度')
    data.setup('杆1半径', obvious=True, group='旗杆',description='杆1半径')
    data.setup('杆2高度', obvious=True, group='旗杆',description='杆2高度')
    data.setup('杆2半径', obvious=True, group='旗杆',description='杆2半径')
    data.setup('杆3高度', obvious=True, group='旗杆',description='杆3高度')
    data.setup('杆3半径', obvious=True, group='旗杆',description= '杆3半径')
    data.setup( '旗面宽度', obvious=True, group='旗面',description= '旗面宽度')
    data.setup( '旗面长度', obvious=True, group='旗面',description= '旗面长度')
    data.setup( '旋转角度', obvious=True, group='旋转',description= '旋转角度')
    data.setup( '左旗杆间隔', obvious=True, group='间距')
    data.setup( '右旗杆间隔', obvious=True, group='间距')
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = LKH
    LKH(data)
    p3d.launchData(data)