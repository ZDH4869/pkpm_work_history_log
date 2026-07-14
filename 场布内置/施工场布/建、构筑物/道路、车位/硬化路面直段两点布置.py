import pyp3d as p3d
from pyp3d import *

def wsl(data):
    B = data['路面宽度(mm)']
    H = data['路面厚度(mm)']
    Dis = data['偏轴距离(mm)']
    Rot = data['轴转角(度)']
    Elo = data['路面长度(mm)']
    Rotation = data['水平方向上的旋转角度（角度制）']

    # 截面 
    data['硬化路面类型一'] = RuledSweep([Vec3(B/2,0,H/2), Vec3(-B/2,0,H/2), Vec3(-B/2,0,-H/2),Vec3(B/2,0,-H/2)],
    [Vec3(B/2,Elo,H/2),Vec3(-B/2,Elo,H/2),Vec3(-B/2,Elo,-H/2),Vec3(B/2,Elo,-H/2)]).color(0.5,0.5,0.5,1)

    data['硬化路面类型一'] = rotation(Vec3(0,1,0),Rot/180*pi) * data['硬化路面类型一'].color(0.5,0.5,0.5,1) # 旋转
    data['硬化路面类型一'] = translation(Vec3(-Dis,0,0)) * data['硬化路面类型一'].color(0.5,0.5,0.5,1) # 偏移
    data['硬化路面类型一'] = rotation(Vec3(0,0,1),-pi/2) * data['硬化路面类型一'].color(0.5,0.5,0.5,1) 
    data['硬化路面类型一'] = p3d.rotation(p3d.Vec3(0,0,1),Rotation/180*pi)*data['硬化路面类型一']


if __name__ == "__main__":
    data = P3DData({
        '路面宽度(mm)':3500,
        '路面厚度(mm)':200,
        '偏轴距离(mm)':0,
        '轴转角(度)':0,
        '路面长度(mm)':3500,
        '水平方向上的旋转角度（角度制）': 0.00,
        '场布类型':'道路交通',
        '构件类型':'硬化路面',
        '构件名称':'硬化路面直段两点布置'

    })
    # data.set_view(-0.125*pi,-0.125*pi)
    data.setup('路面宽度(mm)', obvious = True)
    data.setup('路面厚度(mm)', obvious = True)
    #data.setup('偏轴距离(mm)', obvious = True)
    #data.setup('轴转角(度)', obvious = True)
    data.setup('路面长度(mm)', obvious = True)
    data.setup('硬化路面类型一', show = True)
    data.setup('水平方向上的旋转角度（角度制）', obvious = True)
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    data['replace'] = wsl
    p3d.TwoPointPlace.linearize(data,'路面长度(mm)')
    # wsl(data)
    launchData(data)