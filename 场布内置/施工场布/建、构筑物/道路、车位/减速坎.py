import pyp3d as p3d
def WSL(data:p3d.P3DData)->None:
    Rotation = data['水平方向上的旋转角度（角度制）']

    A = p3d.Extrusion([p3d.Vec3(-1750,-175,0),p3d.Vec3(-1750,175,0),p3d.Vec3(-1750,75,40),p3d.Vec3(-1750,-75,40)],p3d.Vec3(350,0,0)).color(1,1,0,1)
    A1 = p3d.Extrusion([p3d.Vec3(-1400,-175,0),p3d.Vec3(-1400,175,0),p3d.Vec3(-1400,75,40),p3d.Vec3(-1400,-75,40)],p3d.Vec3(350,0,0)).color(0,0,0,1)

    A2 = p3d.combine(A,A1)
    A3 = p3d.combine()
    Number = 5
    for i in range(Number):
        A3.append(p3d.translation(p3d.Vec3(700*i,0,0))*A2)

    data['减速坎'] = A3
    data['减速坎'] = p3d.rotation(p3d.Vec3(0,0,1),Rotation/180*p3d.pi)*data['减速坎']



if __name__ == "__main__":
    data = p3d.P3DData({
        '减速坎宽度':350,
        '减速坎长度':3500,
        '减速坎厚度':40,
        '水平方向上的旋转角度（角度制）': 0.00,
        '场布类型':'挂牌资料',
        '构件类型':'其他标识牌',
        '构件名称':'减速坎'
        })

    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('减速坎', show=True)

    data.setup('水平方向上的旋转角度（角度制）', obvious=True, group='位置',description='角度')
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    data['replace'] = WSL
    WSL(data)
    p3d.launchData(data)
