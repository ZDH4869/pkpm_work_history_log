import pyp3d as p3d
from pyp3d import *
def WSL(data:p3d.P3DData)->None:
    CD = data['矩形标语布长度']
    KD = data['矩形标语布宽度']
    HD = data['矩形标语布厚度']

    R = data['矩形标语布红色值']
    G = data['矩形标语布绿色值']
    B = data['矩形标语布蓝色值']
    T = data['矩形标语布不透明度']

    R1 = data['字体红色值']
    G1 = data['字体绿色值']
    B1 = data['字体蓝色值']
    T1 = data['字体不透明度']
    TEXT = data['标语内容']

    Rotation = data['水平方向上的旋转角度（角度制）']

    #布
    A = p3d.Box(p3d.Vec3(-CD/2,-HD/2,-KD/2), p3d.Vec3(-CD/2,-HD/2,KD/2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),CD,HD,CD,HD).color(R/255,G/255,B/255,T)
    #字
    text = p3d.Text(TEXT,CD/20,KD*3/5).color(R1/255,G1/255,B1/255,T1)
    
    text = p3d.rotation(p3d.Vec3(1,0,0), pi/2)*text
    A1 = text = p3d.translation(p3d.Vec3(-1800*(CD/5000),-1,-150*(KD/500)))*text
    
    AA= p3d.combine (A,A1)
    data['矩形标语布'] = p3d.rotation(p3d.Vec3(1,0,0),Rotation/180*pi)*AA

if __name__ == "__main__":
    data = p3d.P3DData({
        '矩形标语布长度':5000,
        '矩形标语布宽度':500,
        '矩形标语布厚度':1,
        '矩形标语布红色值':255,
        '矩形标语布绿色值':0,
        '矩形标语布蓝色值':0,
        '矩形标语布不透明度':1,
        '水平方向上的旋转角度（角度制）':0.00,
        '字体红色值':255,
        '字体绿色值':255,
        '字体蓝色值':0,
        '字体不透明度':1,
        '标语内容':"生命为贵，安全第一",
        '场布类型':'挂牌资料',
        '构件类型':'标识牌基本类型',
        '构件名称':'矩形标语布',
        '最大字数':10
        })


    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)

    data.setup('矩形标语布', show=True)
    data.setup('矩形标语布长度', obvious=True, group='标语布尺寸',description='标语布')
    data.setup('矩形标语布宽度', obvious=True, group='标语布尺寸',description='标语布')
    #data.setup('矩形标语布厚度', obvious=True, group='标语布尺寸',description='标语布')
    data.setup('矩形标语布红色值', obvious=True, group='标语布颜色',description='标语布')
    data.setup('矩形标语布绿色值', obvious=True, group='标语布颜色',description='标语布')
    data.setup('矩形标语布蓝色值', obvious=True, group='标语布颜色',description='标语布')
    data.setup('矩形标语布不透明度', obvious=True, group='标语布颜色',description='标语布')
    data.setup('字体红色值', obvious=True, group='文本',description='标语布')
    data.setup('字体绿色值', obvious=True, group='文本',description='标语布')
    data.setup('字体蓝色值', obvious=True, group='文本',description='标语布')
    data.setup('字体不透明度', obvious=True, group='文本',description='标语布')
    data.setup('水平方向上的旋转角度（角度制）', obvious=True, group='角度',description='标语布')
    data.setup('最大字数',obvious=True,readonly=True,group='文本',description='标语布')

    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')



    #字
    data.setup('标语内容',obvious=True, group='文本',description='字')
    data.setup('构件名称',obvious=True)

    data['replace'] = WSL
    WSL(data)
    p3d.launchData(data)

