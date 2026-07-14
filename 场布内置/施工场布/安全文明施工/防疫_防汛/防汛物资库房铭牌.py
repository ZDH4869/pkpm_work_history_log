import pyp3d as p3d

def billboard(data:p3d.P3DData)->None:
    ratio = 0.01
    silver_l = 600
    silver_d = 400
    d_text_g = 30
    d_text_s = 11
    d_text_b = 30
    d_text_m = 60
    silver_out = p3d.Extrusion(
        (p3d.Vec3(0,0,0),
        p3d.Vec3(silver_l,0,0),
        p3d.Vec3(silver_l,0,silver_d),
        p3d.Vec3(0,0,silver_d),
        p3d.Vec3(0,0,0)),p3d.Vec3(0,10,0)
    ).color(192/255,192/255,192/255,1)
    text_m = p3d.Text("防汛物资库房",d_text_m*ratio*100,d_text_m*ratio*100, "黑体").color(0,0,0,1)
    text_m = p3d.translation(p3d.Vec3(300-d_text_b*1.3*6.5,-1,d_text_m*3))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_m

    board = p3d.combine(silver_out,text_m)
    board = p3d.rotation(p3d.Vec3(0,0,1),data['旋转角度']/180*p3d.pi)*p3d.translation(p3d.Vec3(-silver_l/2,-5,-silver_d/2))*board
    data['防汛物资库房铭牌'] = board
    data['铭牌长'] = silver_l
    data['铭牌宽'] = silver_d
    data['铭牌厚'] = 10
if __name__ == "__main__":
    data = p3d.P3DData({
        '旋转角度': 0 ,
        '场布类型':'防疫',
        '构件类型':'铭牌',
        '构件名称':'防汛物资库房铭牌',

        })
    data.set_view(1,1)
    # 输出构件
    data.setup('防汛物资库房铭牌', show=True)
    # 设置可调整属性
    data.setup('铭牌长', obvious=True, readonly = True, group='外观参数')
    data.setup('铭牌宽', obvious=True, readonly = True, group='外观参数')
    data.setup('铭牌厚', obvious=True, readonly = True, group='外观参数')

    data.setup('场布类型',obvious = True , readonly = True , group = '构件分类')
    data.setup('构件类型',obvious = True , readonly = True , group = '构件分类')
    data.setup('构件名称',obvious=True)

    # 设置replace算子
    data['replace'] = billboard
    billboard(data)

    # 发射数据到实例模板库
    p3d.launchData(data)





