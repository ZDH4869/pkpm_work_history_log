import pyp3d as p3d

def test_xdd(data:p3d.P3DData)->None:
    # 上部分
    data['上部分边缘'] = p3d.TorusPipe(p3d.Vec3(0,0,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['半径']-24.7,26.6,2*p3d.pi)
    data['上部分边缘'] = p3d.translation(p3d.Vec3(0,0,4.7)) * data['上部分边缘']
    data['上部分中间1'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-20),data['半径'],data['半径'])
    data['上部分边缘'] = p3d.intersection(data['上部分中间1'],data['上部分边缘'])
    data['上部分中间2'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-20),data['半径']-14.7,data['半径']-14.7)
    data['上部分'] =  p3d.unite(data['上部分中间2'],data['上部分边缘']).color(0.92,0.6,0.08,1)
    # 下部分
    data['下部分边缘'] = p3d.TorusPipe(p3d.Vec3(0,0,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['半径']-11.3,12.2,2*p3d.pi)
    data['下部分边缘'] = p3d.translation(p3d.Vec3(0,0,1.3)) * data['下部分边缘']
    data['下部分中间1'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-10),data['半径'],data['半径'])
    data['下部分边缘'] = p3d.intersection(data['下部分中间1'],data['下部分边缘'])
    data['下部分中间2'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-10),data['半径']-7,data['半径']-7)
    data['下部分下'] =  p3d.unite(data['下部分中间2'],data['下部分边缘'])
    data['下部分上'] =  p3d.rotation(p3d.Vec3(0,1,0),p3d.pi*1) * data['下部分下']
    data['下部分'] = p3d.combine( data['下部分下'],data['下部分上'])
    data['下部分'] = p3d.translation(p3d.Vec3(0,0,-51)) * data['下部分'].color(0.92,0.6,0.08,1)

    # 灯罩
    data['灯罩上'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-6),data['半径'],data['半径'])
    data['灯罩上'] = p3d.translation(p3d.Vec3(0,0,-61)) * data['灯罩上']
    data['灯罩下下'] = p3d.Sphere(p3d.Vec3(0,0,0),84.3/2+data['半径']*data['半径']/168.6) 
    data['灯罩下上'] = p3d.Sphere(p3d.Vec3(0,0,0),85/2+data['半径']*data['半径']/170) 
    data['灯罩边缘'] = p3d.substract(data['灯罩下下'],data['灯罩下上'])
    data['灯罩边缘'] = p3d.translation(p3d.Vec3(0,0,560.8)) * data['灯罩边缘']
    data['灯罩边缘'] = p3d.translation(p3d.Vec3(0,0,-707.8+85/2+data['半径']*data['半径']/170)) * data['灯罩边缘']
    data['灯罩范围'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-100),data['半径'],data['半径'])
    data['灯罩范围'] = p3d.translation(p3d.Vec3(0,0,-61)) * data['灯罩范围']
    data['灯罩'] = p3d.intersection(data['灯罩边缘'],data['灯罩范围']).color(0.66,0.66,0.66,0.8)

    # 光域
    data['光域边缘'] = p3d.TorusPipe(p3d.Vec3(0,0,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['半径'],305,2*p3d.pi)
    data['光域边缘'] = p3d.translation(p3d.Vec3(0,0,-67)) * data['光域边缘']
    data['光域中间1'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-305),data['半径']+305,data['半径']+305)
    data['光域中间1'] = p3d.translation(p3d.Vec3(0,0,-65)) * data['光域中间1']
    data['光域边缘'] = p3d.intersection(data['光域中间1'],data['光域边缘'])
    data['光域中间2'] = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-305),data['半径'],data['半径'])
    data['光域中间2'] = p3d.translation(p3d.Vec3(0,0,-65)) * data['光域中间2']
    data['光域'] =  p3d.unite(data['光域中间2'],data['光域边缘']).color(1,0.88,0.36,0.5)

    data['吸顶灯'] = p3d.combine(data['光域'],data['灯罩'],data['下部分'],data['上部分'])

if __name__ == "__main__":
    data = p3d.P3DData({
        '半径': 335,
    '构件名称':'圆吸顶灯'
        })
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)

   # 输出构件
    data.setup('吸顶灯', show=True)

    # 设置可调整属性
    data.setup('半径', obvious=True, group= '尺寸标注', description= '半径')
    data.setup('构件名称', obvious=True)

    # 设置replace算子
    data['replace'] = test_xdd
    test_xdd(data)

    # 发射数据到实例模板库
    p3d.launchData(data)