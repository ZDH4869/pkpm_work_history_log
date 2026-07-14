import pyp3d as p3d

def billboard(data:p3d.P3DData)->None:
    silver_l = 600
    silver_d = 400
    d_text_g = data['公司名-字体大小']
    d_text_s = data['公司英文名-字体大小']
    d_text_b = data['工程名-字体大小']
    d_text_m = data['部门名-字体大小']
    silver_out = p3d.Extrusion(
        (p3d.Vec3(0,0,0),
        p3d.Vec3(silver_l,0,0),
        p3d.Vec3(silver_l,0,silver_d),
        p3d.Vec3(0,0,silver_d),
        p3d.Vec3(0,0,0)),p3d.Vec3(0,10,0)
    ).color(192/255,192/255,192/255,1)
    
    text_g = p3d.Text(data['公司名'],d_text_g*1,d_text_g*1, "黑体").color(0/255,139/255,139/255,1)
    text_g = p3d.translation(p3d.Vec3(data['公司名-缩进'],-1,silver_d-d_text_g*3))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_g
    text_s = p3d.Text(data['公司英文名'],d_text_s*1,d_text_s*1, "黑体").color(0,0,0,1)
    text_s = p3d.translation(p3d.Vec3(data['公司英文名-缩进'],-1,silver_d-d_text_g*3-2*d_text_s))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_s
    text_b = p3d.Text(data['工程名'],d_text_b*1,d_text_b*1, "黑体").color(0,0,0,1)
    text_b = p3d.translation(p3d.Vec3(data['工程名-缩进'],-1,silver_d-d_text_b*6))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_b
    text_m = p3d.Text(data['部门名'],d_text_m*1,d_text_m*1, "黑体").color(0,0,0,1)
    text_m = p3d.translation(p3d.Vec3(data['部门名-缩进'],-1,d_text_m*1.5))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5)*text_m
    board = p3d.combine(silver_out,text_g,text_s,text_b,text_m)
    board = p3d.rotation(p3d.Vec3(0,0,1),data['旋转角度']/180*p3d.pi)*p3d.translation(p3d.Vec3(-silver_l/2,-5,-silver_d/2))*board
    data['无字铭牌A'] = board
    data['铭牌长'] = silver_l
    data['铭牌宽'] = silver_d
    data['铭牌厚'] = 10
if __name__ == "__main__":
    data = p3d.P3DData({
        '旋转角度': 0 ,
        '场布分类': '挂牌资料' ,
        '构件类型': '办公区铭牌' ,
        '构件名称': '办公区铭牌无字通用' ,
        '公司名-字体大小': 30,
        '公司英文名-字体大小': 11 ,
        '工程名-字体大小': 30 ,
        '部门名-字体大小': 60 ,
        '公司名-缩进':30,
        '公司英文名-缩进':30,
        '工程名-缩进':30,
        '部门名-缩进':30,
        '公司名': '',
        '公司英文名': '',
        '工程名': '',
        '部门名': '',

        })
    # data.view = p3d.rotation(p3d.Vec3(1,1,-1),0)
    # 输出构件
    data.setup('无字铭牌A', show=True)
    # 设置可调整属性
    data.setup('旋转角度', obvious=True, group='布置参数')
    data.setup('铭牌长', obvious=True, group='外观参数')
    data.setup('铭牌宽', obvious=True, group='外观参数')
    data.setup('铭牌厚', obvious=True, group='外观参数')
    data.setup('场布分类', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件类型', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('公司名', obvious=True,  group='名称参数')
    data.setup('公司英文名', obvious=True,  group='名称参数')
    data.setup('工程名', obvious=True,  group='名称参数')
    data.setup('部门名', obvious=True, group='名称参数')
    data.setup('公司名-缩进', obvious=True, group='名称参数')
    data.setup('公司名-字体大小', obvious=True, group='名称参数')
    data.setup('公司英文名-字体大小', obvious=True, group='名称参数')
    data.setup('公司英文名-缩进', obvious=True, group='名称参数')
    data.setup('工程名-缩进', obvious=True, group='名称参数')
    data.setup('部门名-缩进', obvious=True, group='名称参数')
    data.setup('工程名-字体大小', obvious=True, group='名称参数')
    data.setup('部门名-字体大小', obvious=True, group='名称参数')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = billboard
    billboard(data)
    # 发射数据到实例模板库
    p3d.launchData(data)





