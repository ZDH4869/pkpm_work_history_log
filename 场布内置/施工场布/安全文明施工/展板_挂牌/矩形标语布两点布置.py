import pyp3d as p3d
from pyp3d import *

def biaoshiyu(data:p3d.P3DData)->None:
    w=data['标语宽度']
    text=data['标语文字']
    word_size = 0.5*w
    l=data['标语长度']
    box1=Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l, w, l, w).color(1,0,0,1)
    # createGeometry(box1)

    # word_list = []
    # i = 0 
    # for item in text:
    #     word_list.append(item) 
    #     i += 1
    # word_string = p3d.combine()
    # # for i in range(len(text)):
    #     word_string.append(p3d.translation(p3d.Vec3(word_size*1.3*i,0.25*w, 0))*p3d.Text(text,word_size,word_size,"微软雅黑").color(1,1,0,1)) 
    word_string = p3d.Text(text,word_size,word_size,"微软雅黑").color(1,1,0,1)    
    # word_combine = p3d.combine(word_string)
    word_combine =translation(Vec3(data['文字边距'],0.25*w,3))* word_string
    # word_combine =translation(Vec3(l/2-len(text)*w/2,0.25*w,3))* word_string
    # createGeometry(word_combine)
    biaoyu = combine(box1,word_combine)
    biaoyu = rotation(p3d.Vec3(1,0,0),p3d.pi/2)*biaoyu
    # createGeometry(biaoyu)

    data['矩形标语布']=biaoyu
    data['标语颜色']='红色'
if __name__ == "__main__":
    data = p3d.P3DData({
        '标语长度':5000,
        '标语宽度':500,
        '标语文字':'生命为贵，安全第一',    
        '横幅颜色':'红色',
        '场布分类':'挂牌资料',
        '构件类型':'标识牌基本类型',
        '构件名称':'矩形标语布两点布置',
        '文字边距':1000,
        })
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('矩形标语布', show=True)
    # 设置可调整属性
    data.setup('标语长度', obvious=True,)
    data.setup('标语宽度', obvious=True,)
    data.setup('标语文字', obvious=True,)
    data.setup('横幅颜色', obvious=True,readonly=True,) 
    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = biaoshiyu
    biaoshiyu(data)
    p3d.TwoPointPlace.linearize(data, '标语长度')

    # 发射数据到实例模板库
    p3d.launchData(data)






