import pyp3d as p3d
#预制围墙

def replace_operator(data:p3d.P3DData)->None:
    ch = data['预制柱地面高(不包含超过墙身部分）'] # column height
    cl = data['柱截面长'] # column length
    cw = data['柱截面宽'] # column width
    wt = data['墙厚'] # wall thickness
    wd = data['墙嵌入深度'] # wall depth
    xwl = data['x方向预制墙板长'] # wall length
    ywl = data['y方向预制墙板长'] # wall length
    n = data['墙身分割块数'] # 预制墙板分割块数
    a = data['预制围墙切角尺寸'] # 预制围墙切角
    d = data['预制柱埋深'] # 预制柱埋入底下深度
    h = data['柱顶与墙身高差'] # 柱顶（未包括柱帽）与墙身高差（未包括压顶）
    wy = data['墙身压顶宽度'] # 墙身压顶宽度
    ty = data['墙身压顶厚度'] # 墙身压顶厚度
    qdqr = data['墙顶嵌入压顶尺寸（不能大于压顶厚度）'] # 强顶嵌入压顶尺寸
    zl = data['柱压顶长'] #柱子压顶长
    zw = data['柱压顶宽'] #柱子压顶宽
    tz = data['柱压顶厚'] #柱子压顶厚

    # 预制柱
    data['prefabricatedcolumn'] = p3d.Extrusion(
        [
        p3d.Vec3(0,0,0),
        p3d.Vec3(cl,0,0),
        p3d.Vec3(cl,cw/2-wt/2,0),
        p3d.Vec3(cl-wd,cw/2-wt/2,0),
        p3d.Vec3(cl-wd,cw/2+wt/2,0),
        p3d.Vec3(cl,cw/2+wt/2,0),
        p3d.Vec3(cl,cw,0),
        p3d.Vec3(cl/2+wt/2,cw,0),
        p3d.Vec3(cl/2+wt/2,cw-wd,0),
        p3d.Vec3(cl/2-wt/2,cw-wd,0),
        p3d.Vec3(cl/2-wt/2,cw,0),
        p3d.Vec3(0,cw,0),
        ],
        p3d.Vec3(0,0,ch+h)
        ).color(125/255,125/255,125/255,0.9)

    # 预制柱压顶
    data['prefabricatedzhuyading'] = p3d.Extrusion(
        [
        p3d.Vec3(-zl/2+cl/2,cw/2-zw/2,ch+h),
        p3d.Vec3(cl/2+zl/2,cw/2-zw/2,ch+h),
        p3d.Vec3(cl/2+zl/2,cw/2+zw/2,ch+h),
        p3d.Vec3(-zl/2+cl/2,cw/2+zw/2,ch+h),
        ],
        p3d.Vec3(0,0,tz)
        ).color(125/255,125/255,125/255,0.9)

    # 预制柱埋深部分
    data['baseprefabricatedcolumn']=p3d.Extrusion(
        [
        p3d.Vec3(0,0,0),
        p3d.Vec3(cl,0,0),
        p3d.Vec3(cl,cw/2-wt/2,0),
        p3d.Vec3(cl-wd,cw/2-wt/2,0),
        p3d.Vec3(cl-wd,cw/2+wt/2,0),
        p3d.Vec3(cl,cw/2+wt/2,0),
        p3d.Vec3(cl,cw,0),
        p3d.Vec3(cl/2+wt/2,cw,0),
        p3d.Vec3(cl/2+wt/2,cw-wd,0),
        p3d.Vec3(cl/2-wt/2,cw-wd,0),
        p3d.Vec3(cl/2-wt/2,cw,0),
        p3d.Vec3(0,cw,0),
        ],
        p3d.Vec3(0,0,-d)
        ).color(125/255,125/255,125/255,0.9)

    # 预制墙板x方向
    data['prefabricatedwallx'] = p3d.Extrusion(
        [
        p3d.Vec3(cl-wd,cw/2+wt/2-a,0),
        p3d.Vec3(cl-wd,cw/2-wt/2+a,0),
        p3d.Vec3(cl-wd,cw/2-wt/2,a),
        p3d.Vec3(cl-wd,cw/2-wt/2,(ch)/n-a),
        p3d.Vec3(cl-wd,cw/2-wt/2+a,(ch)/n),
        p3d.Vec3(cl-wd,cw/2+wt/2-a,(ch)/n),
        p3d.Vec3(cl-wd,cw/2+wt/2,(ch)/n-a),
        p3d.Vec3(cl-wd,cw/2+wt/2,a),
        ],
        p3d.Vec3(xwl,0,0)
        ).color(1,0,0,0.9)

    # 预制压顶x方向
    data['prefabricatedyadingx'] = p3d.Extrusion(
        [
        p3d.Vec3(cl,cw/2-wt/2,ch-qdqr),
        p3d.Vec3(cl,cw/2-wt/2,ch),
        p3d.Vec3(cl,cw/2+wt/2,ch),
        p3d.Vec3(cl,cw/2+wt/2,ch-qdqr),
        p3d.Vec3(cl,cw/2+wy/2-30,ch-qdqr),
        p3d.Vec3(cl,cw/2+wy/2-30,ch-qdqr+10),
        p3d.Vec3(cl,cw/2+wy/2-20,ch-qdqr+10),
        p3d.Vec3(cl,cw/2+wy/2-20,ch-qdqr),
        p3d.Vec3(cl,cw/2+wy/2,ch-qdqr),
        p3d.Vec3(cl,cw/2+wy/2,ch+ty-qdqr),
        p3d.Vec3(cl,cw/2-wy/2,ch+ty-qdqr),
        p3d.Vec3(cl,cw/2-wy/2,ch-qdqr),
        p3d.Vec3(cl,cw/2-wy/2+20,ch-qdqr),
        p3d.Vec3(cl,cw/2-wy/2+20,ch-qdqr+10),
        p3d.Vec3(cl,cw/2-wy/2+30,ch-qdqr+10),
        p3d.Vec3(cl,cw/2-wy/2+30,ch-qdqr),
        ],
        p3d.Vec3(xwl-wd-wd,0,0)
        ).color(125/255,125/255,125/255,0.9)

      # 预制墙板y方向
    data['prefabricatedwally'] = p3d.Extrusion(
        [
        p3d.Vec3(cl/2-wt/2+a,cw-wd,0),
        p3d.Vec3(cl/2+wt/2-a,cw-wd,0),
        p3d.Vec3(cl/2+wt/2,cw-wd,a),
        p3d.Vec3(cl/2+wt/2,cw-wd,(ch)/n-a),
        p3d.Vec3(cl/2+wt/2-a,cw-wd,(ch)/n),
        p3d.Vec3(cl/2-wt/2+a,cw-wd,(ch)/n),
        p3d.Vec3(cl/2-wt/2,cw-wd,(ch)/n-a),
        p3d.Vec3(cl/2-wt/2,cw-wd,a),
        ],
        p3d.Vec3(0,ywl,0)
        ).color(1,0,0,0.9)

    # 预制压顶y方向
    data['prefabricatedyadingy'] = p3d.Extrusion(
        [
        p3d.Vec3(cl/2-wt/2,cw,ch-qdqr),
        p3d.Vec3(cl/2-wt/2,cw,ch),
        p3d.Vec3(cl/2+wt/2,cw,ch),
        p3d.Vec3(cl/2+wt/2,cw,ch-qdqr),
        p3d.Vec3(cl/2+wy/2-30,cw,ch-qdqr),
        p3d.Vec3(cl/2+wy/2-30,cw,ch-qdqr+10),
        p3d.Vec3(cl/2+wy/2-20,cw,ch-qdqr+10),
        p3d.Vec3(cl/2+wy/2-20,cw,ch-qdqr),
        p3d.Vec3(cl/2+wy/2,cw,ch-qdqr),
        p3d.Vec3(cl/2+wy/2,cw,ch+ty-qdqr),
        p3d.Vec3(cl/2-wy/2,cw,ch+ty-qdqr),
        p3d.Vec3(cl/2-wy/2,cw,ch-qdqr),
        p3d.Vec3(cl/2-wy/2+20,cw,ch-qdqr),
        p3d.Vec3(cl/2-wy/2+20,cw,ch-qdqr+10),
        p3d.Vec3(cl/2-wy/2+30,cw,ch-qdqr+10),
        p3d.Vec3(cl/2-wy/2+30,cw,ch-qdqr),
        ],
        p3d.Vec3(0,ywl-wd-wd,0)
        ).color(125/255,125/255,125/255,0.9)

    # 结合x&y方向墙
    Walls = p3d.combine(data['prefabricatedwallx'], data['prefabricatedwally'])

     # 分割柱为n等份并复制wall墙板
    Points1 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,0,(n-1)/n*ch),n)
    ReWalls = []
    for point in Points1:
        ReWalls.append(p3d.translation(point) * Walls)

     # 输出构件
    data.setup('prefabricatedcolumn', show=True)
    data['ReWalls'] = ReWalls
    data.setup('ReWalls', show=True)
    data.setup('baseprefabricatedcolumn',show=True)
    data.setup('prefabricatedyadingx', show=True)
    data.setup('prefabricatedyadingy', show=True)
    data.setup('prefabricatedzhuyading', show=True)

if __name__ == "__main__":
    data = p3d.P3DData({
    '预制柱地面高(不包含超过墙身部分）': 4000,
    '柱截面长':300, # 柱底x方向长
    '柱截面宽': 300, # 柱底y方向宽
    '墙厚': 80, # 预制围墙厚
    '墙嵌入深度': 80, # 预制围墙嵌入预制柱内尺寸
    '墙身分割块数': 7, #设置围墙竖向分割块数
    'x方向预制墙板长': 3000, #设置预制围墙板长度
    'y方向预制墙板长': 3000, #设置预制围墙板长度
    '预制围墙切角尺寸': 15, # 设置预制围墙切角尺寸
    '预制柱埋深': 500, #预制柱埋入地下深度
    '柱顶与墙身高差': 300, #柱顶（未包括柱帽）与墙身高差（未包括压顶）
    '墙身压顶宽度': 180, #墙身压顶宽度
    '墙身压顶厚度': 60, #墙身压顶厚度
    '墙顶嵌入压顶尺寸（不能大于压顶厚度）':10, #墙顶嵌入压顶尺寸
    '柱压顶长':400, #柱压顶长
    '柱压顶宽':400, #柱压顶宽'
    '柱压顶厚':100, #柱压顶厚'
    '构件名称':'预制围墙角柱带边墙'
    })
    

    

    # 设置视角旋转角度
    # data.view = p3d.rotation(p3d.Vec3(1,1,1),-p3d.pi/4)

    # 设置属性（是否可见，分组，描述）
    data.setup('预制柱地面高(不包含超过墙身部分）', obvious=True, group='预制柱参数')
    data.setup('柱截面长', obvious=True, group='预制柱参数')
    data.setup('柱截面宽', obvious=True, group='预制柱参数')
    data.setup('预制柱埋深', obvious=True, group='预制柱参数')
    data.setup('墙厚', obvious=True, group='墙体参数')
    data.setup('墙嵌入深度', obvious=True, group='墙体参数')
    data.setup('墙身分割块数', obvious=True, group='墙体参数')
    data.setup('x方向预制墙板长', obvious=True, group='墙体参数')
    data.setup('y方向预制墙板长', obvious=True, group='墙体参数')
    data.setup('预制围墙切角尺寸', obvious=True, group='墙体参数')
    data.setup('柱顶与墙身高差', obvious=True, group='其他')
    data.setup('墙身压顶宽度', obvious=True, group='墙身压顶')
    data.setup('墙身压顶厚度', obvious=True, group='墙身压顶')
    data.setup('墙顶嵌入压顶尺寸（不能大于压顶厚度）', obvious=True, group='墙身压顶')
    data.setup('柱压顶长', obvious=True, group='柱压顶')
    data.setup('柱压顶宽', obvious=True, group='柱压顶')
    data.setup('柱压顶厚', obvious=True, group='柱压顶')

    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = replace_operator
    replace_operator(data)

    # 发射数据到实例模板库
    p3d.launchData(data)



