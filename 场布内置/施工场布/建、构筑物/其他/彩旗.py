import pyp3d as p3d
from pyp3d import *
def flag(data: p3d.P3DData) -> None:
    wide = data['灯箱宽度']
    height = data['灯箱高度']
    gan_l = data['杆高']
    gan_r = data['杆半径']
    flag_h = 2*data['杆半径']
    string_text = data['文字']
    ro=data['旋转角度']
    word_size = height/((len(string_text)+2)*1.3)
    # word_gap = height*0.752/len(string_text)

    # ==文字限制
    if len(string_text)<2 :
        string_text = "文字超限"
        data['文字'] = string_text
    if word_size>data['灯箱宽度']/1.5:
         word_size=data['灯箱宽度']/1.5
    if data['灯箱高度']>data['杆高']:
        height=data['杆高']
        data['灯箱高度']=data['杆高']
    # 1. 建立灯箱
    GAN = p3d.Cone(Vec3(0,0,0),Vec3(0,0,gan_l),gan_r,gan_r).color(0.7,0.7,0.7,1)
    BO = p3d.Box(Vec3(0,-0.5*flag_h,gan_l-height),Vec3(0,0.5*flag_h,gan_l-height),Vec3(1,0,0),Vec3(0,0,1),wide,height,wide,height).color(0,0.533,0.769,1)
    # 1.2.2 灯箱文字
    # 文字一
    word_combine = p3d.combine()
    word_list = [0 for i in range(len(string_text))]
    i = 0 
    for item in string_text:
        word_list[i] = item
        i += 1
    word_string = p3d.combine()
    for i in range(len(string_text)):
            word_string.append(p3d.translation(p3d.Vec3(0, -word_size*i*1.30, 0))*p3d.Text(word_list[i],word_size,word_size).color(1,1,1,1))     
    word_combine = p3d.combine(word_string).color(1,1,1,1)
    W = p3d.translation(p3d.Vec3(0.5*wide-0.50*word_size,-flag_h/2-1,(len(string_text)-2)*word_size*1.30/2+gan_l-height/2))*p3d.rotation(p3d.Vec3(1, 0, 0), p3d.pi*0.5)*word_combine.color(1,1,1,1)
    data['彩旗'] =p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*ro/180) * p3d.combine(BO,GAN, W)

if __name__ == "__main__":
    data = p3d.P3DData({
        '灯箱宽度' :400,
        '灯箱高度' :1200,
        '杆半径' :20,
        '杆高' :1800,
        '文字':"认真开展安全年活",
        '旋转角度':0,
        '构件名称':'彩旗'
    })
    
    data.set_view = (-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('彩旗', show=True)
    # 设置可调整属性
    data.setup('灯箱宽度', obvious=True, group='灯箱', description='—————')
    data.setup('灯箱高度', obvious=True, group='灯箱', description='—————')
    data.setup('杆高', obvious=True, group='杆', description='—————')
    data.setup('杆半径', obvious=True, group='杆', description='—————')
    data.setup('文字', obvious=True, group='文字', description='—————')
    data.setup('旋转角度', obvious=True, group='旋转', description='——————')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = flag
    flag(data)
    p3d.launchData(data)
    # 发射数据到实例模板库