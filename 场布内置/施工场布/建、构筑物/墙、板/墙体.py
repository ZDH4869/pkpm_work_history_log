import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:
    data['墙体'] = \
        p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,data['高']), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['厚度'], data['长'], data['厚度'], data['长']).color(1,1,0,0.5)

if __name__ == "__main__":
    data = p3d.P3DData({
        '厚度': 200,
        '长':  5000,
        '高':  3000,
        '构件名称':'墙体'
        })
    
    # data.view = p3d.rotation(p3d.Vec3(1,1,-1),0)
    # 输出构件
    data.setup('墙体', show=True)
    # 设置可调整属性
    data.setup('长', obvious=True, group='墙体长', description='底面长')
    data.setup('厚度', obvious=True, group='墙体厚', description='底面厚')
    data.setup('高', obvious=True, group='墙体高', description='墙板高度')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = test_box
    test_box(data)
    # 发射数据到实例模板库
    p3d.launchData(data)
