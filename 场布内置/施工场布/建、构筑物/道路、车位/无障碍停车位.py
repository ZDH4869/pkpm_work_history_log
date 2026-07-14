import pyp3d as p3d
from pyp3d import *
def tingchewei(data:p3d.P3DData)->None:
    #建立无障碍停车位

    l=data['停车位长度']
    w=data['停车位宽度']
    w1=data['无障碍宽度']
    x=data['线宽度']
    rota=data['旋转角度']
    n=data['个数']
    data['场布分类']='道路交通'
    data['构件类型']='停车位'
    #建立
    #横线
    line1=p3d.Box(p3d.Vec3(0,0,1), p3d.Vec3(0,0,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), w, x, w, x).color(1,1,1,1)
    line2=translation(0,l-x,0)*line1
    #竖线
    line3=p3d.Box(p3d.Vec3(0,0,1), p3d.Vec3(0,0,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), x, l, x, l).color(1,1,1,1)
    line4=translation(w-x,0,0)*line3
    b=p3d.Box(p3d.Vec3(-1,0,0), p3d.Vec3(0,0,3), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 0.5*w, 800, 0.5*w, 800).color(1,1,1,1)
    b=translation(0.25*w,l-400,0)*b
    line2=substract(line2,b)
    line5=translation(-w1+x,0,0)*line3
    line6=translation(-w1+x,0,0)*line1
    line7=p3d.Box(p3d.Vec3(0,0,1), p3d.Vec3(0,0,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), w1, x, w1, x).color(1,1,1,1)
    line7=translation(-w1+x,l-x,0)*line7
    line=unite(line1,line2,line3,line4,line5,line6,line7)
    line=translation(w1-x,0,0)*line
    # p3d.createGeometry(line)

    box1=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), w-2*x, l-2*x, w-2*x, l-2*x).color(164/255,150/255,146/255,1)
    box1=translation(x,x,0)*box1
    box2=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),0.5*w, x, 0.5*w, x).color(164/255,150/255,146/255,1)
    box2=translation(0.25*w,l-x,0)*box2
    box=unite(box1,box2).color(164/255,150/255,146/255,1)
    box=translation(w1-x,0,0)*box
    # p3d.createGeometry(box)

    #建立无障碍内部线
    box2=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), w1-2*x, l-2*x, w1-2*x, l-2*x).color(164/255,150/255,146/255,1)
    box2=translation(x,x,0)*box2
    # p3d.createGeometry(box2)
    box=unite(box,box2).color(164/255,150/255,146/255,1)

    #建立斜线
    line7=p3d.Box(p3d.Vec3(0,0,1), p3d.Vec3(0,0,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), w1*1.8, x, w1*1.8, x).color(1,1,1,1)
    line7=rotation(p3d.Vec3(0,0,1),p3d.pi/4)*line7
    points1 = p3d.linspace(p3d.Vec3(0,-0.5*l,0),p3d.Vec3(0,l,0),int(1.5*l/700))
    linezu = p3d.combine() 
    for point in points1:
        linezu.append(p3d.translation(point) * line7)
    linezu=translation(x,0,0)*linezu
    # p3d.createGeometry(linezu)
    jianti1=p3d.Box(p3d.Vec3(0,0,1), p3d.Vec3(0,0,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 2*w1, l+l, 2*w1, l+l).color(1,1,1,1)
    jianti1=translation(w1,0,0)*jianti1
    jianti2=translation(-w1,l,0)*jianti1
    jianti3=translation(-w1,-2*l,0)*jianti1
    linezu=substract(linezu,jianti1)
    linezu=substract(linezu,jianti2)
    linezu=substract(linezu,jianti3)
    linezu=unite(linezu,line)

    linezuhe=p3d.combine()
    if n<1:
        n=1
        data['个数']=1
        for i in range(int(n)):
            linezuhe=unite(translation((w+w1-x-x)*i,0,0)*linezu,linezuhe)
    else:
        for i in range(int(n)):
            linezuhe=unite(translation((w+w1-x-x)*i,0,0)*linezu,linezuhe)
    boxz=p3d.combine()
    if n<1:
        n=1
        data['个数']=1
        for i in range(int(n)):
            boxz=combine(translation((w+w1-x-x)*i,0,0)*box,boxz)   
    else:
        for i in range(int(n)):
            boxz=combine(translation((w+w1-x-x)*i,0,0)*box,boxz)     
    che=combine(linezuhe,boxz)
    # che=translation(-(w*int(n)+w1*int(n)+x)/2,-l/2,0)*che
    che=rotation(p3d.Vec3(0,0,1),p3d.pi*rota/180)*che
    data['无障碍停车位']=che

if __name__ == "__main__":
    data = p3d.P3DData({
        '停车位长度': 5300,  
        '停车位宽度': 2500,
        '无障碍宽度':1200,
        '线宽度':100,
        '旋转角度':0,    
        '个数':1, 
        '构件名称':'无障碍停车位'
        })
    
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('无障碍停车位', show=True)
    # 设置可调整属性
    data.setup('停车位长度', obvious=True,)
    data.setup('停车位宽度', obvious=True,)
    data.setup('无障碍宽度', obvious=True,) 
    data.setup('线宽度', obvious=True,)  
    data.setup('旋转角度', obvious=True)
    data.setup('个数', obvious=True)
    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称', obvious=True)   
    # 设置replace算子
    data['replace'] = tingchewei
    tingchewei(data)
    # 发射数据到实例模板库
    p3d.launchData(data)

