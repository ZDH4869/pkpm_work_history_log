import pyp3d as p3d
from pyp3d import*
def WSL(data:p3d.P3DData)->None:

    K = data['路面宽度(mm)']
    H = data['路面厚度(mm)']
    R = data['转弯角度(角度制)']
    R1 = data['转弯半径(沿道路内侧)']
    Rotation = data['水平方向上的旋转角度（角度制）']

    #旋转扫描
    A = p3d.RotationalSweep([p3d.Vec3(-K/2,0,-H/2),p3d.Vec3(K/2,0,-H/2),p3d.Vec3(K/2,0,H/2),p3d.Vec3(-K/2,0,H/2)],p3d.Vec3((K/2)+R1,0,0),p3d.Vec3(0,0,1),R/180*pi).color(0.5,0.5,0.5,1)
    data['硬化路面类型二'] = p3d.rotation(p3d.Vec3(0,0,1),Rotation/180*pi)*A


if __name__ == "__main__":
    data = P3DData({
        '路面宽度(mm)':3500,
        '路面厚度(mm)':200,
        '转弯角度(角度制)':90,
        '转弯半径(沿道路内侧)':3500,
        '水平方向上的旋转角度（角度制）': 0.00,
        '场布类型':'道路交通',
        '构件类型':'硬化路面',
        '构件名称':'硬化路面转弯'

    })

    # data.set_view(-0.125*pi,-0.125*pi)
    data.setup('路面宽度(mm)', obvious = True)
    data.setup('路面厚度(mm)', obvious = True)
    data.setup('转弯角度(角度制)', obvious = True)
    data.setup('转弯半径(沿道路内侧)', obvious = True)
    data.setup('水平方向上的旋转角度（角度制）', obvious = True)
    data.setup('硬化路面类型二', show = True)
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)


    data['replace'] = WSL
    WSL(data)
    p3d.launchData(data)

