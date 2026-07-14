import pyp3d as p3d
import math
def profild_sheet(data:p3d.P3DData)->None:
    b1 = data['波峰宽度b1']
    b2 = data['波谷宽度b2']
    b3 = data['波距b3']
    t = data['板厚t']
    h = data['波高h']
    b = data['板宽b']
    H = data['混凝土厚度H']
    baseshroud = p3d.Vec3(0,0,0), p3d.Vec3(0,0,-H-h), p3d.Vec3(0.5*b2,0,-H-h), p3d.Vec3(0.5*b3-0.5*b1,0,-H), p3d.Vec3(0.5*b3+0.5*b1,0,-H), p3d.Vec3(b3-0.5*b2,0,-H-h), p3d.Vec3(b3,0,-H-h),\
            p3d.Vec3(b3,0,0)
    # 定义基本的混凝土块的单元拉伸外框线
    baseslab = p3d.Extrusion(baseshroud,p3d.Vec3(0,data['板长度'],0)).color(1,0.4,0.4,1)
    # 将上面的外框线拉成一个基本单元块
    cube = p3d.Box(p3d.Vec3(0,0,-H-h), p3d.Vec3(0,0,0), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),\
                   b%b3,data['板长度'],b%b3,data['板长度'])
    concreteslab1 = p3d.translation(p3d.Vec3(b3*int(b/b3),0,0))*p3d.intersection(cube,baseslab)
    # 考虑到输入的b不一定是b3的整数倍，对于余数部分需要取出对应宽度的板。上述函数即拿出所需板块并放置在正确位置
    final = baseslab
    for i in range(1,int(b/b3)):
        temp2 = p3d.translation(p3d.Vec3(b3*i,0,0))*baseslab
        final = p3d.unite(final,temp2.color(0.4,0.5,0,0.2))
    # 利用for循环使得基本单元块组合成一块完整的板
    concreteslab2 = final
    # 这部分是板的主要部分，需要并上剩余宽度成为完整板
    if b%b3 == 0:
        data['混凝土压型钢板'] = concreteslab2
    else:
        data['混凝土压型钢板'] = p3d.unite(concreteslab1,concreteslab2).color(0.4,0.5,0,0.9)
    
    
    onereinforce = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,data['板长度'],0),data['钢筋直径']/2,data['钢筋直径']/2).color(1,0,0,1)
    locations = p3d.linspace(p3d.Vec3(data['钢筋直径']/2+data['混凝土保护层厚度c'],0,-data['钢筋直径']/2-data['混凝土保护层厚度c']),p3d.Vec3(b-data['钢筋直径']/2-data['混凝土保护层厚度c'],0,-data['钢筋直径']/2-data['混凝土保护层厚度c']),int(b/data['钢筋间距'])+2)
    data['板顶部钢筋'] = []
    for location in locations:
        data['板顶部钢筋'].append(p3d.translation(location)*onereinforce)
    # 创建了钢筋，并使其偏安全分布在混凝土上层

if __name__ == "__main__":
    data = p3d.P3DData({
        '波峰宽度b1': 112,
        '波谷宽度b2': 88,
        '波距b3': 230,
        '板厚t': 2.3,
        '波高h': 75,
        '板宽b': 760,
        '混凝土厚度H': 60,
        '混凝土保护层厚度c': 30,
        '板长度': 5000,
        '钢筋直径': 20,
        '钢筋间距': 150,
        '构件名称':'压型钢板'
        })
    
    # data.view = p3d.rotation(p3d.Vec3(0,0,1),0)
    data.setup('混凝土压型钢板', show=True)
    data.setup('板顶部钢筋', show=True)

    data.setup('波峰宽度b1',obvious=True, group='压型钢板参数', description='波峰宽度b1')
    data.setup('波谷宽度b2',obvious=True, group='压型钢板参数', description='波谷宽度b2')
    data.setup('波距b3',obvious=True, group='压型钢板参数', description='波距b3')
    data.setup('板厚t',obvious=True, group='压型钢板参数', description='板厚t')
    data.setup('波高h',obvious=True, group='压型钢板参数', description='波高h')
    data.setup('板宽b',obvious=True, group='压型钢板参数', description='板宽b')
    data.setup('混凝土厚度H',obvious=True, group='混凝土参数', description='混凝土厚度H')
    data.setup('混凝土保护层厚度c',obvious=True, group='混凝土参数', description='混凝土保护层厚度c')
    data.setup('板长度',obvious=True, group='压型钢板参数', description='板长度')
    data.setup('钢筋直径',obvious=True, group='板顶部钢筋参数', description='钢筋直径')
    data.setup('钢筋间距',obvious=True, group='板顶部钢筋参数', description='钢筋间距')
    data.setup('构件名称',obvious=True)

    data['replace'] = profild_sheet
    profild_sheet(data)
    p3d.launchData(data)