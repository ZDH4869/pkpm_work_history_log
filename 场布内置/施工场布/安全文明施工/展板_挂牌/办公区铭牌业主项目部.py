import pyp3d as p3d

def billboard(data:p3d.P3DData)->None:
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
    text_g = p3d.Text("国家电网公司",d_text_g*1,d_text_g*1, "黑体").color(0/255,139/255,139/255,1)
    text_g = p3d.translation(p3d.Vec3(300-d_text_g*1.3*3,-1,silver_d-d_text_g*3))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_g
    text_s = p3d.Text("STATE GRID CORPORATION OF CHINA",d_text_s*1,d_text_s*1, "黑体").color(0,0,0,1)
    text_s = p3d.translation(p3d.Vec3(300-d_text_s*1.3*7.8,-1,silver_d-d_text_g*3-2*d_text_s))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_s
    text_b = p3d.Text("北京XX500kV变电站工程",d_text_b*1,d_text_b*1, "黑体").color(0,0,0,1)
    text_b = p3d.translation(p3d.Vec3(300-d_text_b*1.3*5.7,-1,silver_d-d_text_b*6))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_b
    text_m = p3d.Text("业主项目部",d_text_m*1,d_text_m*1, "黑体").color(0,0,0,1)
    text_m = p3d.translation(p3d.Vec3(300-d_text_b*1.3*5.5,-1,d_text_m*1.5))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_m

    board = p3d.combine(silver_out,text_g,text_s,text_b,text_m)
    board = p3d.rotation(p3d.Vec3(0,0,1),data['旋转角度']/180*p3d.pi)*p3d.translation(p3d.Vec3(-silver_l/2,-5,-silver_d/2))*board
    data['业主项目部A'] = board
    data['铭牌长'] = silver_l
    data['铭牌宽'] = silver_d
    data['铭牌厚'] = 10
if __name__ == "__main__":
    data = p3d.P3DData({
        '旋转角度': 0 ,
        '场布分类': '挂牌资料' ,
        '构件类型': '办公区铭牌' ,
        '构件名称': '办公区铭牌业主项目部' ,
        })
    data.set_view = (-0.125*p3d.pi, 0.125*p3d.pi)
    # 输出构件
    data.setup('业主项目部A', show=True)
    # 设置可调整属性
    data.setup('旋转角度', obvious=True, group='布置参数')
    data.setup('铭牌长', obvious=True, group='外观参数')
    data.setup('铭牌宽', obvious=True, group='外观参数')
    data.setup('铭牌厚', obvious=True, group='外观参数')
    data.setup('场布分类', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件类型', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件名称',obvious=True)

    # 设置replace算子
    data['replace'] = billboard
    billboard(data)
    # 发射数据到实例模板库
    p3d.launchData(data)





