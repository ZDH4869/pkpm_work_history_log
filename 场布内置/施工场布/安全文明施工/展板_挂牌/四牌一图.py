from pyp3d import *
import pyp3d as p3d
def pai(data: p3d.P3DData) -> None:
    b_t=data['基座高'] #基座高30
    b_l=data['基座边长'] #基座边长100
    z_h=data['总高'] #总高2500
    z_l=data['牌宽'] #牌宽2000
    p_h=data['牌高'] #牌高1200
    R_r=30
    b_w=20
    h_r=20
    wen_1=data['底部文字']#底部文字
    wen_2=data['顶部右侧文字']#顶部右侧文字
    wen_3=data['顶部左侧文字']#顶部左侧文字
    ro=data['旋转角度']
    data['场布分类']='挂牌资料'
    data['构件类型']='办公区"四牌一图"'
    if data['基座高']>100:
        b_t=100
    if data['牌高']!=900:
        if data['牌高']!=1200:
            if data['牌高']!=1500:
                p_h=1200
                z_l=2000
                data['牌高']=1200
                data['牌宽']=2000
            else:
                p_h=1500
                z_l=2400
                data['牌高']=1500
                data['牌宽']=2400
        else:
            p_h=1200
            z_l=2000
            data['牌高']=1200
            data['牌宽']=2000
    else:
        p_h=900
        z_l=1500
        data['牌高']=900
        data['牌宽']=1500
    if data['总高']<data['牌高']+250+data['基座高']:
        z_h=data['牌高']+250+data['基座高']
        data['总高']=data['牌高']+250+data['基座高']

    if (len(data['底部文字'])+6)*56>data['牌宽']:
       wen_1="送变电公司" 
       data['底部文字']="字数超出范围"
    if (len(data['顶部右侧文字'])+2)*112+(len(data['顶部左侧文字'])+2)*84>data['牌宽']:
        wen_2="项目工程概况"
        wen_3="国家电网"
        data['顶部右侧文字']="字数超出范围"
        data['顶部左侧文字']="字数超出范围"
        
    #基座
    box1 = p3d.Box(p3d.Vec3(-b_l/2,-b_l/2,0), p3d.Vec3(-b_l/2,-b_l/2,b_t), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), b_l, b_l, b_l, b_l).color(0.7,0.7,0.7,1)
    #竖杆
    Cone1 = p3d.Cone(p3d.Vec3(0,0,b_t),p3d.Vec3(0,0,z_h),R_r,R_r).color(0.7,0.7,0.7,1)
    Cone2=p3d.combine(box1,Cone1)
    Cone3=p3d.translation(p3d.Vec3(z_l,0,0))*Cone2
    #牌
    box2 = p3d.Box(p3d.Vec3(0,-b_w/2,0), p3d.Vec3(0,b_w/2,0), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), z_l, 100, z_l, 100).color(1,1,1,1)
    box3 = p3d.Box(p3d.Vec3(0,-b_w/2,100), p3d.Vec3(0,b_w/2,100), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), z_l, p_h-300, z_l, p_h-300).color(0.031, 0.384, 0.384, 1)
    box4 = p3d.Box(p3d.Vec3(0,-b_w/2,p_h-200), p3d.Vec3(0,b_w/2,p_h-200), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), z_l, 200, z_l, 200).color(1,1,1,1)
    box5=p3d.translation(p3d.Vec3(0,0,z_h-50-p_h)) *p3d.combine(box2,box3,box4)

    #横杆
    h_1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(z_l,0,0),h_r,h_r).color(0.7,0.7,0.7,1)
    h_2=p3d.translation(p3d.Vec3(0,0,z_h-200-p_h)) *h_1

    #底部文字
    w_1=p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5) *Text(wen_1, 40, 40).color(0.031, 0.384, 0.384, 1)
    w_2=p3d.translation(p3d.Vec3(z_l-(len(wen_1)+2)*56,-b_w/2-0.1,z_h-28-p_h)) *w_1
    #顶部右侧文字
    w_3=p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5) *Text(wen_2, 80, 80).color(0.031, 0.384, 0.384, 1)
    w_4=p3d.translation(p3d.Vec3(z_l-(len(wen_2)+1)*112,-b_w/2-0.1,z_h-206)) *w_3
    #顶部左侧文字
    w_5=p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5) *Text(wen_3, 60, 60).color(0.031, 0.384, 0.384, 1)
    w_6=p3d.translation(p3d.Vec3(2*84,-b_w/2-0.1,z_h-189)) *w_5
    FG=p3d.translation(p3d.Vec3(-z_l/2,0,0))*p3d.combine(Cone2,Cone3,box5,h_2,w_2,w_4,w_6)
    data['四牌一图1'] = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*ro/180) *FG

if __name__=="__main__":
    data=p3d.P3DData({
        '基座高':30,
        '基座边长':100,
        '总高':2500,
        '牌宽':2000,
        '牌高':1200,
        '底部文字':"送变电公司",
        '顶部右侧文字':"项目工程概况",
        '顶部左侧文字':"国家电网",
        '构件名称':"四牌一图",
        '旋转角度':0,
    })
    data.set_view(1,1)
    #输出构件
    data.setup('四牌一图1', show=True)
    # 设置可调整属性
    data.setup('基座高', obvious=True, group='基座', description='——————')
    data.setup('基座边长', obvious=True, group='基座', description='——————')
    data.setup('总高', obvious=True, group='总高', description='——————')
    data.setup('牌高', obvious=True, group='牌(高*宽可选尺寸为900*1500,1200*2000,1500*2400)', description='——————')
    # data.setup('牌宽', obvious=True, group='牌', description='——————')
    data.setup('底部文字', obvious=True, group='文字（请输入中文）', description='——————')
    data.setup('顶部右侧文字', obvious=True, group='文字（请输入中文）', description='——————')
    data.setup('顶部左侧文字', obvious=True, group='文字（请输入中文）', description='——————')
    data.setup('旋转角度', obvious=True, group='旋转', description='——————')
    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称',obvious=True)
    
    # 设置replace算子
    data['replace'] = pai
    pai(data)
    p3d.launchData(data)
    # 发射数据到实例模板库