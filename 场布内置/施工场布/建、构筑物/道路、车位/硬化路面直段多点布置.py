import pyp3d as p3d
from pyp3d import *

def wsl(data):
    B = data['路面宽度(mm)']
    H = data['路面厚度(mm)']
    Dis = data['偏轴距离(mm)']
    Rot = data['轴转角(度)']
    Rotation = data['水平方向上的旋转角度（角度制）']

    # 截面 
    KeyPoint = data['关键点']
    temp = []
    for i in range(len(KeyPoint)-1): 
        v12_norm = norm(KeyPoint[i]-KeyPoint[i+1])
        G=translation(0,- B/2,0) * Box(Vec3(0,0,-0.5*H),Vec3(0,0,0.5*H),Vec3(1,0,0), Vec3(0,1,0), v12_norm,  B, v12_norm,  B).color(1,1,1,1)
        # G =RuledSweep([Vec3(B/2,0,H/2), Vec3(-B/2,0,H/2), Vec3(-B/2,0,-H/2),Vec3(B/2,0,-H/2)],[Vec3(B/2,v12_norm,H/2),Vec3(-B/2,v12_norm,H/2),Vec3(-B/2,v12_norm,-H/2),Vec3(B/2,v12_norm,-H/2)]).color(0.5,0.5,0.5,1)
        temp.append(translation(KeyPoint[i]) * rotation_to(KeyPoint[i+1]-KeyPoint[i]) * G)
    for i in range(len(KeyPoint)-1):
        if i>0:
            k_1=p3d.Cone(p3d.Vec3(0,0,-0.5*H),p3d.Vec3(0,0,0.5*H),B/2,B/2).color(1,1,1,1)
            temp.append(translation(KeyPoint[i])  * k_1)
    # for i in range(len(data['硬化路面类型一'])):
    #     if i==0:
    #         data['d_1']=data['硬化路面类型一'][i]
    #     if i!=0:
    #         data['d_1']=p3d.unite(data['d_1'],data['硬化路面类型一'][i])
    data['硬化路面类型一'] = p3d.unite(*temp)
    data['硬化路面类型一'] = p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*Rotation)*data['硬化路面类型一']     


if __name__ == "__main__":
    data = P3DData({
        '路面宽度(mm)':3500,
        '路面厚度(mm)':200,
        '偏轴距离(mm)':0,
        '轴转角(度)':0,
        '水平方向上的旋转角度（角度制）': 0.00,
        '场布类型':'道路交通',
        '构件类型':'硬化路面',
        '构件名称':'硬化路面直段多点布置',
        '关键点':[Vec3(0,0,0),Vec3(1000,0,0),Vec3(1000,2000,0)]

    })
    # data.set_view(-0.125*pi,-0.125*pi)
    data.setup('路面宽度(mm)', obvious = True)
    data.setup('路面厚度(mm)', obvious = True)
    #data.setup('偏轴距离(mm)', obvious = True)
    #data.setup('轴转角(度)', obvious = True)
    data.setup('硬化路面类型一', show = True)
    data.setup('水平方向上的旋转角度（角度制）', obvious = True)
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    data['replace'] = wsl
    p3d.MultiPointPlace.MultiPointFunction(data, '关键点')
    wsl(data)
    p3d.launchData(data)