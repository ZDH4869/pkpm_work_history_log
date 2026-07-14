# from math import comb
from pyp3d import *
import pyp3d as p3d
def machine(data: p3d.P3DData) -> None:
    b_h=data['基座高'] #基座高50
    b_r=data['基座半径']  #基座半径40
    c_l=data['箱体长'] #箱体长900
    c_h=data['箱体高'] #箱体高850
    c_w=data['箱体宽']#箱体宽800
    s_r=data['锯片半径'] #锯片半径200
    ro=data['旋转角度']
    data['场布分类']='材料堆场'
    data['构件类型']='土建'
    sd_w=10 #锯口宽
    n = 10

    if data['箱体长']<400:
        c_l=400
        data['箱体长']=400
    if data['箱体宽']<400:
        c_w=400
        data['箱体宽']=400
    # if data['箱体高']<data['锯片半径']*5/2:
    #     c_h=data['锯片半径']*5/2
    #     data['箱体高']=data['锯片半径']*5/2
    if data['锯片半径']>data['箱体高']*2/5:
        s_r=data['箱体高']*2/5
        data['锯片半径']=data['箱体高']*2/5
    if data['基座半径']>data['箱体长']/4:
        b_r=data['箱体长']/4
        data['基座半径']=data['箱体长']/4
    if data['基座半径']>data['箱体宽']/4:
        b_r=data['箱体宽']/4
        data['基座半径']=data['箱体宽']/4
    if data['锯片半径']>(data['箱体长']-100)/3:
        s_r=(data['箱体长']-100)/3
        data['锯片半径']=(data['箱体长']-100)/3  
    cl_r1 = 0.1*s_r
    cl_r2 = 0.5*cl_r1
    LP = p3d.Cone(Vec3(0,0,0),Vec3(0,0,-1),s_r,s_r).color(0.9333,0.9333,0.9333,1) 
    #基座
    base_1 = p3d.Cone(p3d.Vec3(b_r,b_r,-b_h),p3d.Vec3(b_r,b_r,0),b_r,b_r)
    base_2=p3d.translation(p3d.Vec3(c_l-2*b_r,0,0)) * base_1
    base_3=F2 = p3d.translation(p3d.Vec3(0,c_w-2*b_r,0)) * base_1
    base_4=F2 = p3d.translation(p3d.Vec3(0,c_w-2*b_r,0)) * base_2
    base_f=combine(base_1,base_2,base_4,base_3).color(0,0,0,1)
    # p3d.createGeometry(base_f)
    #箱体
    case_1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,c_h), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_l, c_w, c_l, c_w)
    box_1=p3d.Box(p3d.Vec3(50,0,50), p3d.Vec3(50,0,c_h*2/5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_l-100, c_w, c_l-100, c_w)
    case_2=p3d.substract(case_1,box_1)
    box_2=p3d.Box(p3d.Vec3(c_l/2-50,0,c_h*3/5), p3d.Vec3(c_l/2-50,0,c_h), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_l/2, c_w/2, c_l/2, c_w/2) 
    case_3=p3d.substract(case_2,box_2).color(0.62,0.639,0.62,1)
    # p3d.createGeometry(case_3)
    #锯片仓
    jc_1=p3d.Extrusion(
            (p3d.Vec3(0,0,0),p3d.Vec3(0,0,c_h*2/5-50),p3d.Vec3(0,-50,c_h*2/5),p3d.Vec3(0,5,c_h*2/5),p3d.Vec3(0,5,0)),p3d.Vec3(c_l/2,0,0)
            ).color(0.62,0.639,0.62,1)
    jc_2 = p3d.translation(p3d.Vec3(c_l/2-50,0,c_h*3/5)) * jc_1
    # p3d.createGeometry(jc_2)
    #工作平台
    work_1=p3d.Box(p3d.Vec3(-50,-50,0), p3d.Vec3(-50,-50,50), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_l+100, c_w+100, c_l+100, c_w+100).color(0.9333,0.9333,0.9333,1)
    box_3=p3d.translation(p3d.Vec3(c_l-50,50,0)) *p3d.Box(p3d.Vec3(0,50-sd_w/2,0), p3d.Vec3(0,50-sd_w/2,50), p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0), 2*s_r+50, sd_w, 2*s_r+50, sd_w).color(0.9333,0.9333,0.9333,1)

    work_2=p3d.substract(work_1,box_3).color(0.9333,0.9333,0.9333,1)
    box_4=p3d.translation(p3d.Vec3(0,c_w/2,30))*p3d.Box(p3d.Vec3(-50,-15,0), p3d.Vec3(-50,-15,20), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_l+100, 30, c_l+100,30).color(0.9333,0.9333,0.9333,1)
    work_3=p3d.substract(work_2,box_4).color(0.9333,0.9333,0.9333,1)
    work_4= p3d.translation(p3d.Vec3(0,0,c_h)) * work_3
    # p3d.createGeometry(work_4)

    #锯片
    # 读取外圆弧
    list_point = []
    for i in range (1,n+1):
        t = math.pi*(i/n)/2                        # t 为取样点角度，i代表个数
        list_point.append(Vec3(s_r*math.cos(math.asin(cl_r1/s_r))+cl_r1*math.cos(t),cl_r1*math.sin(t),0))
    list_point.append(Vec3(s_r*math.cos(math.asin(cl_r1/s_r)),cl_r1,0))
    list_point.append(Vec3(s_r*math.cos(math.asin(cl_r1/s_r)),0,0))
    
    for i in range(1,n):
        t = math.pi-math.pi*i/n                        # t 为取样点角度，i代表个数
        list_point.append(Vec3(s_r*math.cos(math.asin(cl_r1/s_r))+cl_r2+cl_r2*math.cos(t),cl_r2*math.sin(t),0))

    F = p3d.Extrusion(list_point,p3d.Vec3(0,0,-1)).color(0.9333,0.9333,0.9333,1)

    # 旋转角度控制
    n = int(2*p3d.pi/math.asin(cl_r1/s_r))
    FF = p3d.combine()
    for i in range(n):
        FF.append(p3d.rotation(p3d.Vec3(0,0,1),2*p3d.pi*i/n) * F)
    F_1 =p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5) * p3d.combine(F,FF,LP)
    F_2=p3d.translation(p3d.Vec3(0,16.5,-s_r/2)) * F_1


    #防护罩
    out = Ellipse(Vec3(0,0,0), Vec3(s_r+27,0,0), Vec3(0,0,52), 0, pi)
    outContour = p3d.ContourLine([out])
    extrusionPlus1 = p3d.ExtrusionPlus([outContour],p3d.Vec3(0, 34 ,0)).color(1,1,1,0.3)
    inner = Ellipse(Vec3(0,0,0), Vec3(s_r+25,0,0), Vec3(0,0,50), 0, pi)
    InnerContour = p3d.ContourLine([inner])
    extrusionPlus2 = p3d.ExtrusionPlus([InnerContour],p3d.Vec3(0, 30 ,0)).color(1,1,1,0.3)
    z_1= p3d.translation(p3d.Vec3(0,2,0)) *extrusionPlus2

    z_2=p3d.substract(extrusionPlus1,z_1).color(1,1,1,0.3)
    box_5=p3d.Box(p3d.Vec3(-s_r-100,0,-100), p3d.Vec3(-s_r-100,50,-100), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), (s_r+100)*2, 100, (s_r+100)*2, 100)
    z_3=p3d.substract(z_2,box_5).color(1,1,1,0.3)
    z_4=p3d.translation(p3d.Vec3(0,0,s_r/2)) *z_3

    Cone1 = p3d.Cone(p3d.Vec3(s_r+25,0,0),p3d.Vec3(s_r+25,0,s_r/2),1,1).color(1,1,1,0.3)
    zz_1=p3d.translation(p3d.Vec3(1,1,0)) *Cone1
    zz_2=p3d.translation(p3d.Vec3(0,32,0)) *zz_1
    z_f=p3d.translation(p3d.Vec3(c_l-s_r-75,83,c_h+50)) *p3d.combine(z_4,zz_2,zz_1,F_2)
    # createGeometry(z_f)

    #推尺
    r_1=p3d.Box(p3d.Vec3(0,-c_w/4,0), p3d.Vec3(0,-c_w/4,50), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 50, c_w/2, 50, c_w/2).color(0.9333,0.9333,0.9333,1)
    r_2=p3d.Box(p3d.Vec3(0,-c_w/4,10), p3d.Vec3(0,-c_w/4,40), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 20, c_w/2, 20, c_w/2)
    r_3=p3d.substract(r_1,r_2).color(0.9333,0.9333,0.9333,1)
    cone2=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,2),c_w/4,c_w/4).color(1,0,0,0.3)
    box_6=p3d.Box(p3d.Vec3(0,-c_w/4,0), p3d.Vec3(0,-c_w/4,2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_w/4, c_w/2, c_w/4, c_w/2)
    cp_1=p3d.substract(cone2,box_6)
    cone3=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,2),c_w/4-40,c_w/4-40).color(1,0,0,0.3)
    cp_2=p3d.substract(cp_1,cone3).color(0.9333,0.9333,0.9333,1)
    cone4=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,2),c_w/4-60,c_w/4-60).color(1,0,0,0.3)
    cp_3=p3d.substract(cone4,box_6).color(0.9333,0.9333,0.9333,1)
    box_7=p3d.Box(p3d.Vec3(-1,-c_w/4,0), p3d.Vec3(-1,-c_w/4,50), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 1, c_w/2, 1, c_w/2).color(0.9333,0.9333,0.9333,1)
    cp_4=p3d.combine(cp_2,cp_3,box_7,r_3)


    #螺栓
    luo_1=p3d.Cone(p3d.Vec3(0,0,-20),p3d.Vec3(0,0,20),10,10)
    luo_2=p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,30),10,20)
    luo_3=p3d.unite(luo_1,luo_2).color(0,0,0,1)
    luo_4=p3d.translation(p3d.Vec3(-c_w/4+50,0,0)) *luo_3

    luo_5=p3d.translation(p3d.Vec3(0,0,25)) *p3d.rotation(p3d.Vec3(0,1,0),-pi*0.5) * luo_3
    luo_6=p3d.translation(p3d.Vec3(0,c_w/12,0)) *luo_5
    luo_7=p3d.translation(p3d.Vec3(0,-c_w/12,0)) *luo_5
    luo_f=p3d.combine(luo_6,luo_7,luo_4)

    tuichi=p3d.translation(p3d.Vec3(c_w/4-50,c_w/2,c_h+50)) *p3d.combine(cp_4,luo_f)
    # createGeometry(tuichi)
    FG=p3d.translation(p3d.Vec3(-c_l/2,-c_w/2,0)) *p3d.combine(base_f,case_3,jc_2,work_4,z_f,tuichi)
    data['木模板加工器械1'] = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*ro/180) *FG

if __name__=="__main__":
    data=p3d.P3DData({
        '基座高':50,
        '基座半径':40,
        '箱体长':900,
        '箱体高':850,
        '箱体宽':800,
        '锯片半径':200,
        '旋转角度':0,
        '构件名称':'木模板加工器械'
    })
    data.set_view = (-0.125*p3d.pi,-0.125*p3d.pi)
    #输出构件
    data.setup('木模板加工器械1', show=True)
    # 设置可调整属性
    data.setup('基座高', obvious=True, group='基座', description='——————')
    data.setup('基座半径', obvious=True, group='基座', description='——————')
    data.setup('箱体长', obvious=True, group='箱体', description='——————')
    data.setup('箱体宽', obvious=True, group='箱体', description='——————')
    data.setup('箱体高', obvious=True, group='箱体', description='——————')
    data.setup('锯片半径', obvious=True, group='锯片', description='——————')
    data.setup('旋转角度', obvious=True, group='旋转', description='——————')
    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称',obvious=True)

    # 设置replace算子
    data['replace'] = machine
    machine(data)
    p3d.launchData(data)
    # 发射数据到实例模板库