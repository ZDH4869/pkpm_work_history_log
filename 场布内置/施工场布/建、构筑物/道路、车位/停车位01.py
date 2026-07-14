import pyp3d as p3d
from pyp3d import *
def tingchewei(data:p3d.P3DData)->None:
    #建立停车位
    l=data['停车位长度']
    w=data['停车位宽度']
    x=data['线宽度']
    rota=data['旋转角度']
    n=data['个数']
    data['场布分类']='道路交通'
    data['构件类型']='停车位'

    #建立
    line1=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), w, x, w, x).color(1,1,1,1)
    line2=translation(0,l-x,0)*line1
    line3=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), x, l, x, l).color(1,1,1,1)
    line4=translation(w-x,0,0)*line3
    b=p3d.Box(p3d.Vec3(-1,0,0), p3d.Vec3(0,0,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 0.5*w, 800, 0.5*w, 800).color(1,1,1,1)
    b=translation(0.25*w,l-400,0)*b
    line2=substract(line2,b)
    line=unite(line1,line2,line3,line4)
    # p3d.createGeometry(line)

    box1=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), w-2*x, l-2*x, w-2*x, l-2*x).color(164/255,150/255,146/255,1)
    box1=translation(x,x,0)*box1
    box2=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),0.5*w, x, 0.5*w, x).color(164/255,150/255,146/255,1)
    box2=translation(0.25*w,l-x,0)*box2
    box=unite(box1,box2).color(164/255,150/255,146/255,1)
    linez=p3d.combine()
    if n<1:
        n=1
        data['个数']=1
        for i in range(int(n)):
            linez=unite(translation((w-x)*i,0,0)*line,linez)
    else:
        for i in range(int(n)):
            linez=unite(translation((w-x)*i,0,0)*line,linez)

    boxz=p3d.combine()
    if n<1:
        n=1
        data['个数']=1
        for i in range(int(n)):
            boxz=combine(translation((w-x)*i,0,0)*box,boxz)  
    else:
        for i in range(int(n)):
            boxz=combine(translation((w-x)*i,0,0)*box,boxz)  

    che=combine(linez,boxz)
    # che=translation(-(int(n)*w+(int(n)-1)*x)/2,-l/2,0)*che
    che=rotation(p3d.Vec3(0,0,1),p3d.pi*rota/180)*che
    data['停车位']=che
if __name__ == "__main__":
    data = p3d.P3DData({
        '停车位长度': 5300,  
        '停车位宽度': 2500,
        '线宽度':100,
        '旋转角度':0, 
        '个数':1,
        '构件名称':'停车位01'
        })
    
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('停车位', show=True)
    # 设置可调整属性
    data.setup('停车位长度', obvious=True,)
    data.setup('停车位宽度', obvious=True,)
    data.setup('线宽度', obvious=True,)  
    data.setup('旋转角度', obvious=True)
    data.setup('个数', obvious=True)
    data.setup('场布分类', obvious=True,group = '类型参数')
    data.setup('构件类型', obvious=True,group = '类型参数')
    data.setup('构件名称', obvious=True) 
    # 设置replace算子
    data['replace'] = tingchewei
    tingchewei(data)
    # 发射数据到实例模板库
    p3d.launchData(data)






