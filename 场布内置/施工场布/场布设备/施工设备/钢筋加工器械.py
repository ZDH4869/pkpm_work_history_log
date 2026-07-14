from math import sqrt
import pyp3d as p3d
def reinfotcing(data: p3d.P3DData) -> None:
    x_l=data['箱长']#箱长900
    x_h=data['箱高']#箱高850
    x_w=data['箱宽'] #箱宽800
    l_r=50#轮半径
    l_w=30#轮厚
    a_r=10#轴半径
    b_w=30#顶板厚
    z_r=data['转盘半径']#转盘半径250
    z_l=40#转盘高度
    c_h=60 #卡座高
    c_l=80 #卡座长
    c_w=20 #支座宽
    g_r=20#送料滚半径
    ro=data['旋转角度']
    if data['箱长']<data['转盘半径']*2+c_l*4-60:
        x_l=data['转盘半径']*2+c_l*4-60
        data['箱长']=data['转盘半径']*2+c_l*4-60
    if data['箱宽']>data['箱长']:
       x_w=data['箱长'] 
       data['箱宽']=data['箱长']
    if data['箱宽']<data['转盘半径']*2-100:
        x_w=data['转盘半径']*2-100
        data['箱宽']=data['转盘半径']*2-100
    j_l=(x_w-340)/8 #间距
    #轮
    wheel_r=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,l_w,0),l_r,l_r).color(0.0824,0.125,0.125,1)
    wheel_l=p3d.translation(p3d.Vec3(0,x_w+l_w,0)) *wheel_r
    axis=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,x_w+2*l_w,0),a_r,a_r).color(0.0824,0.125,0.125,1)
    wh_1=p3d.translation(p3d.Vec3(-x_l/2+a_r,-x_w/2-l_w,-x_h/2-a_r)) *p3d.combine(wheel_r,wheel_l,axis)
    wh_2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * wh_1
    wh=p3d.combine(wh_1,wh_2)
    #箱体
    box_1 = p3d.Box(p3d.Vec3(-x_l/2,-x_w/2,-x_h/2), p3d.Vec3(-x_l/2,x_w/2,-x_h/2), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), x_l, x_h, x_l, x_h).color(0.0667,0.102,0.0824,1)
    door_1 = p3d.Box(p3d.Vec3(-x_l/2+50,-x_w/2-0.01,-x_h/2+50), p3d.Vec3(-x_l/2+50,-x_w/2,-x_h/2+50), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), x_l-100, x_h-100, x_l-100, x_h-100).color(0.286,0.71,0.757,1)
    door_2 =p3d.translation(p3d.Vec3(0,x_w+0.01,0)) *door_1 
    door_3= p3d.Box(p3d.Vec3(-x_l/2-0.01,-x_w/2+50,-x_h/2+50), p3d.Vec3(-x_l/2,-x_w/2+50,-x_h/2+50), p3d.Vec3(0,1,0), p3d.Vec3(0,0,1), x_w-100, x_h-100, x_w-100, x_h-100).color(0.286,0.71,0.757,1)
    door_4 =p3d.translation(p3d.Vec3(x_l+0.01,0,0)) *door_3 
    box_f=p3d.combine(box_1,door_2,door_4,door_1,door_3)
   #顶板
    top_b =p3d.translation(p3d.Vec3(0,0,x_h/2)) * p3d.Box(p3d.Vec3(-x_l/2-50,-x_w/2-50,0), p3d.Vec3(-x_l/2-50,-x_w/2-50,b_w), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), x_l+100, x_w+100, x_l+100, x_w+100).color(0.282,0.345,0.435,1)
    #转盘
    turntable_1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,z_l),z_r,z_r).color(0.82,0.84,0.878,1)
    c0ne_1=p3d.Cone(p3d.Vec3(0,0,z_l),p3d.Vec3(0,0,z_l+1),sqrt(2)*z_r/10,sqrt(2)*z_r/10).color(0,0,0,1)
    Cone_2=p3d.translation(p3d.Vec3(sqrt(2)*z_r*2/5.5,0,0)) *c0ne_1
    Cone_3=p3d.translation(p3d.Vec3(-sqrt(2)*z_r*2/5.5,0,0)) *c0ne_1
    Cone_4=p3d.combine(c0ne_1,Cone_2,Cone_3)
    Cone_5=p3d.translation(p3d.Vec3(0,-sqrt(2)*z_r*2/5.5,0)) *Cone_4
    Cone_6=p3d.translation(p3d.Vec3(0,sqrt(2)*z_r*2/5.5,0)) *Cone_4
    Cone_7=p3d.combine(Cone_4,Cone_5,Cone_6)
    Cone_8=p3d.Cone(p3d.Vec3(0,0,-20),p3d.Vec3(0,0,0),sqrt(2)*z_r/10,sqrt(2)*z_r/10).color(0.82,0.84,0.878,1)
    turntable=p3d.translation(p3d.Vec3(0,0,x_h/2+b_w+20)) *p3d.combine(turntable_1,Cone_8,Cone_7)
    #卡座
    cassette_1= p3d.Box(p3d.Vec3(-c_l/2,(-x_w+100)/2,0), p3d.Vec3(-c_l/2,(-x_w+100)/2,c_h), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_l, x_w-100, c_l, x_w-100).color(0.82,0.84,0.878,1)
    ##小洞
    y_1=p3d.Cone(p3d.Vec3(0,0,c_h),p3d.Vec3(0,0,c_h+1),10,10).color(0,0,0.0,1)
    y_2=p3d.translation(p3d.Vec3(20,0,0)) *y_1
    y_3=p3d.translation(p3d.Vec3(-20,0,0)) *y_1
    y_4=p3d.combine(y_2,y_3)
    y_5=p3d.translation(p3d.Vec3(0,(x_w-100)/2-15,0)) *y_4
    y_6=p3d.translation(p3d.Vec3(0,-(x_w-100)/2+15,0)) *y_4
    y_7=p3d.combine(y_4,y_5,y_6) 
    #大洞
    y_8=p3d.Cone(p3d.Vec3(0,0,c_h),p3d.Vec3(0,0,c_h+1),20,20).color(0,0,0,1)
    y_9=p3d.translation(p3d.Vec3(0,j_l+20,0)) *y_8
    y_10=p3d.translation(p3d.Vec3(0,j_l+40,0)) *y_9
    y_11=p3d.translation(p3d.Vec3(0,j_l+40,0)) *y_10
    y_12=p3d.combine(y_11,y_10,y_9)
    y_13=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * y_12
    y_14=p3d.combine(y_12,y_13,y_7,cassette_1)
    y_15=p3d.translation(p3d.Vec3(z_r+c_l/2+20,0,x_h/2+b_w))* y_14
    y_16=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * y_15
    y_f=p3d.combine(y_15,y_16)
     #送料滚
    g_1=p3d.Cone(p3d.Vec3(0,(-x_w+100)/2,c_h-g_r),p3d.Vec3(0,-(-x_w+100)/2,c_h-g_r),g_r,g_r).color(1,0,0,1)
    k_1=p3d.Box(p3d.Vec3(-c_l/2,-c_w/2,0), p3d.Vec3(-c_l/2,-c_w/2,c_h-2*g_r), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), c_l, c_w, c_l, c_w).color(1,1,0,1)
    k_3=p3d.Box(p3d.Vec3(-g_r,-c_w/2,c_h-2*g_r), p3d.Vec3(-g_r,-c_w/2,c_h-g_r), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 2*g_r, c_w, 2*g_r, c_w).color(1,1,0,1)
    k_4=p3d.combine(k_1,k_3)
    k_5=p3d.translation(p3d.Vec3(0,(x_w-100-c_w)/2,0)) *k_4
    k_6=p3d.translation(p3d.Vec3(0,-(x_w-100-c_w)/2,0)) *k_4
    k_7=p3d.unite(g_1,k_5,k_6)
    k_8=p3d.translation(p3d.Vec3((x_l+100)/2-c_l/2,0,x_h/2+b_w)) *k_7
    k_9=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) *k_8
    k_f=p3d.combine(k_8,k_9)
    FG= p3d.translation(p3d.Vec3(0,0,x_h/2)) *p3d.combine(wh,box_f, top_b,turntable,y_f,k_f)
    data['加工器械'] =p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*ro/180) *FG
if __name__ == "__main__":
    data = p3d.P3DData({
        '箱长' :900,
        '箱高' :850,
        '箱宽' :800,
        '转盘半径' :250,
        '旋转角度':0,
        '构件名称':'钢筋加工器械'
    })

    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('加工器械', show=True)
    # 设置可调整属性
    data.setup('箱长', obvious=True, group='箱', description='—————')
    data.setup('箱高', obvious=True, group='箱', description='—————')
    data.setup('箱宽', obvious=True, group='箱', description='—————')
    data.setup('转盘半径', obvious=True, group='转盘', description='—————')
    data.setup('旋转角度', obvious=True, group='旋转', description='——————')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = reinfotcing
    reinfotcing(data)
    p3d.launchData(data)
    # 发射数据到实例模板库