import pyp3d as p3d
from pyp3d import *
def yinshuidian(data:p3d.P3DData)->None:
    cone1_r=30    #底部柱半径
    cone1_h=400   #底部柱高度
    cone2_r=230   #承托板半径
    cone2_t=50    #承托板厚度
    b_r=200       #水桶半径
    b_h=300       #水桶高度
    rota=data['旋转角度']
    j   =data['饮水机个数']
    s_d =data['顶棚宽度']   
    s_l =data['顶棚长度']
    s_g =s_d/2                    #data['顶棚高度（与宽度有关）']  #随动
    s_h =data['距地板距离']
    s_e =data['侧面外伸长度']

    f_t=data['地板厚度']        
    f_l=data['地板长度']         
    f_w=data['地板宽度']

    c_l =data['椅子长度']
    c_w =data['椅子宽度']
    c_g =math.cos(pi*0.1)*c_w          #data['椅背高度']    随动
    c_h =data['距地板高度']                       
    c_h =data['距地板高度']
    k_r=20        #支架径长
    k_h=200       #距离地面距离
    k_hh=80       #踏板距离地面距离
    c_t=30        #椅子厚度

    sk_l=15       #顶棚龙骨边长

    vb_r=20         #data['竖杆半径（固定）']
    vb_xr=20        #data['斜杆半径（固定）']


    #创建地板
    f = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,f_t), p3d.Vec3(0,1,0), p3d.Vec3(1,0,0),  f_w, f_l, f_w, f_l).color(150/255,130/255,106/255,1) 

    #创建杆
    vb1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,s_h),vb_r,vb_r).color(1,1,1,1)
    vb2=p3d.translation(s_l-2*s_e-sk_l,0,0)*vb1
    vb=combine(vb1,vb2)
    vb=translation(f_l/2-s_l/2+s_e+sk_l/2,f_w-220,f_t)*vb

    vb3=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,0.3*s_h*math.sqrt(2)),vb_xr,vb_xr).color(1,1,1,1)
    vb3=rotation(p3d.Vec3(1,0,0),pi/4)*vb3
    vb3=translation(0,0,0.7*s_h)*vb3
    vb4=p3d.translation(s_l-2*s_e-sk_l,0,0)*vb3
    vb5=combine(vb3,vb4)
    vb5=translation(f_l/2-s_l/2+s_e+sk_l/2,f_w-220,f_t)*vb5

    vb=combine(vb,vb5)
    vbx=rotation(p3d.Vec3(0,0,1),pi)*vb
    vbx=translation(2*(f_l/2-s_l/2+s_e+sk_l/2)+s_l-2*s_e-sk_l,f_w-220+f_w-80-s_d+160,0)*vbx

    #创建椅子
    k1=p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(0,k_r,0),p3d.Vec3(0,k_r,c_h-k_r-c_t),p3d.Vec3(0,0,c_h-k_r-c_t)),p3d.Vec3(k_r,0,0)).color(1,1,1,1)
    k2=p3d.translation(0,c_w-k_r,0)*k1
    k31=p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(0,c_w,0),p3d.Vec3(0,c_w,k_r),p3d.Vec3(0,0,k_r)),p3d.Vec3(k_r,0,0)).color(1,1,1,1)
    k3=p3d.translation(0,0,c_h-c_t-k_r)*k31
    k4=p3d.translation(0,0,k_h-k_r)*k31
    k4=substract(k4,k1)
    k4=substract(k4,k2)

    c1=p3d.combine(k1,k2,k3,k4)
    c2=p3d.translation(c_l-k_r,0,0)*c1

    k51=p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(0,c_w,0),p3d.Vec3(0,c_w,c_t),p3d.Vec3(0,0,c_t)),p3d.Vec3(c_l,0,0)).color(1,1,1,1)
    k5=p3d.translation(0,0,c_h-c_t)*k51
    k6=p3d.rotation(p3d.Vec3(1,0,0),pi*2.4)*k51
    k6=p3d.translation(0,c_w,c_h-c_t)*k6

    k7=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,k_r,0), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1),  c_l-2*k_r, k_r, c_l-2*k_r, k_r)
    k7=p3d.translation(k_r,0,k_hh)*k7     

    #椅子组合
    chair=combine(c1,c2,k5,k6,k7)
    chair=translation(f_l/2-c_l/2,f_w-400-c_w,f_t)*chair


    #建立顶棚
    #建立顶棚皮
    outer1 = Ellipse(Vec3(0,s_d/2,0), Vec3(0,s_d/2+5,0), Vec3(0,0,s_d/2+5),0,pi)
    outer2=LineString([Vec3(0,-5,0), Vec3(0,s_d+5,0)])
    inner1 = Ellipse(Vec3(0,s_d/2,0), Vec3(0,s_d/2,0), Vec3(0,0,s_d/2), 0, pi)
    inner2 = LineString([Vec3(0,0,0), Vec3(0,s_d,0)])
    A1 = ContourLine([outer1,outer2])
    A2 = ContourLine([inner1,inner2])
    shed= ExtrusionPlus([A1,-A2], Vec3(s_l,0,0)).color(1/255,139/255,204/255,1)

    #建立弯曲骨架
    outer3 = Ellipse(Vec3(0,s_d/2,0), Vec3(0,s_d/2,0), Vec3(0,0,s_d/2),0,pi)
    outer4=LineString([Vec3(0,0,0), Vec3(0,s_d,0),])
    inner3 = Ellipse(Vec3(0,s_d/2,0), Vec3(0,s_d/2-sk_l,0), Vec3(0,0,s_d/2-sk_l), 0, pi)
    inner4 = LineString([Vec3(0,sk_l,0), Vec3(0,s_d-sk_l,0),])
    A3 = ContourLine([outer3,outer4])
    A4 = ContourLine([inner3,inner4])
    s= ExtrusionPlus([A3,-A4], Vec3(sk_l,0,0)).color(1,1,1,1)
    s1=translation(s_e,0,0)*s
    s2=translation(s_l-s_e-sk_l,0,0)*s
    #建立纵向骨架
    s3=Extrusion((Vec3(0,0,0),Vec3(0,s_d,0),Vec3(0,s_d,sk_l),Vec3(0,0,sk_l)),Vec3(sk_l,0,0)).color(1,1,1,1)
    s4=translation(s_e,0,0)*s3
    s3=translation(s_l-s_e-sk_l,0,0)*s3

    #建立横向骨架
    sf=Extrusion((Vec3(0,0,0),Vec3(0,sk_l,0),Vec3(0,sk_l,sk_l),Vec3(0,0,sk_l)),Vec3(s_l-2*s_e-2*sk_l,0,0)).color(1,1,1,1)
    s5=rotation(Vec3(1,0,0),pi/3) * sf
    s5=translation(0,2*sk_l,0)*s5
    s5=translation(0,(s_d-2*sk_l)/4,(s_d-2*sk_l)/4*math.sqrt(3))*s5

    s6=rotation(Vec3(-1,0,0),pi/3) * sf
    s6=translation(0,2*sk_l,0)*s6
    s6=translation(0,(s_d-2*sk_l)/4*3,(s_d-2*sk_l)/4*math.sqrt(3))*s6

    s56=combine(s5,s6)
    s56=translation(s_e+sk_l,0,0)*s56

    #组合
    skeleton=combine(s1,s2,s3,s4,s56)
    #顶蓬皮与龙骨组合
    shed=combine(shed,skeleton)
    shed=translation(f_l/2-s_l/2,f_w-80-s_d,s_h+f_t)*shed

    #创建饮水机
    #创建承托部分
    cone1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,cone1_h),cone1_r,cone1_r).color(149/255,128/255,104/255,1)
    cone2=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,cone2_t),cone2_r,cone2_r).color(149/255,128/255,104/255,1)
    cone2=translation(0,0,cone1_h)*cone2
    cone3=combine(cone1,cone2)

    #创建水桶
    b=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,b_h),b_r,b_r).color(1,1,1,1)
    b1=p3d.Cone(p3d.Vec3(0,0,-1000),p3d.Vec3(0,0,b_h),1000,1000).color(1,1,1,1)   #b1为减体
    Sphere1 = p3d.Sphere(p3d.Vec3(0,0,b_h-b_r),math.sqrt(2*b_r*b_r)).color(1,1,1,1)
    top=p3d.substract(Sphere1,b1)
    ha1=p3d.TorusPipe(p3d.Vec3(b_r,0,0.8*b_h),p3d.Vec3(0,0,1),p3d.Vec3(1,0,0),15,5,p3d.pi).color(1,1,1,1)
    ha2=p3d.TorusPipe(p3d.Vec3(-b_r,0,0.8*b_h),p3d.Vec3(0,0,-1),p3d.Vec3(-1,0,0),15,5,p3d.pi).color(1,1,1,1)
    a1 = p3d.FilletPipe((p3d.Vec3(0,-b_r-5,0.95*b_h),p3d.Vec3(0,-b_r-5,b_h),p3d.Vec3(0,-b_r+10,b_h+10)), (0,10,0), 5).color(1,1,1,1)
    qiu = p3d.Sphere(p3d.Vec3(0,0,b_h+math.sqrt(2*b_r*b_r)-b_r),10).color(1,1,1,1)
    b=p3d.combine(top,b,ha1,ha2,a1,qiu)
    b=translation(0,0,cone1_h+cone2_t)*b
    #饮水机组合
    wd=combine(b,cone3)
                                                                                                                                                                                                                                                                                
    points1 = p3d.linspace(p3d.Vec3((f_l-s_l)/2,0,0),p3d.Vec3(f_l-(f_l-s_l)/2,0,0),j)
    wds = p3d.combine() 
    for point in points1:
        wds.append(p3d.translation(point) *wd)
    wds=translation(0,f_w-0.7*s_d-cone2_r-80,f_t)*wds

    if  data['是否显示地板']== '否' or data['是否显示地板']== '隐藏' or data['是否显示地板']== '不显示':
        #组合
        Dp=combine(shed,vb,vbx,chair,wds)
        Dp=translation(0,0,-f_t)*Dp
    else :
        Dp=combine(f,shed,vb,vbx,chair,wds)
        pass
    Dp=rotation(p3d.Vec3(0,0,1),p3d.pi*rota/180)*Dp
    data['饮水点']=Dp
    data['顶棚龙骨边长']= sk_l
    data['顶棚高度']=s_g
    data['椅背高度']=c_g
    data['竖杆半径']=vb_r
    data['斜杆半径']=vb_xr

if __name__ == "__main__":
    data = p3d.P3DData({
        '饮水机个数':6,
        '旋转角度':0,
        '顶棚宽度':2400,
        '顶棚长度':3000,
        '顶棚高度':1200,
        '侧面外伸长度':100,
        '距地板距离':2000,

        '地板厚度':100,
        '地板长度':4000,
        '地板宽度':3000,
        '是否显示地板':'',

        '椅子长度':2000,
        '椅子宽度':400,
        '椅背高度':389.0,  #随动
        '距地板高度':500,

        '竖杆半径':20,
        '斜杆半径':20,
        '顶棚龙骨边长':15,
        '场布分类':'建/构筑物',
        '构件类型':'其他临建',
        '构件名称':'饮水点',
        })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('饮水点', show=True)
    # 设置可调整属性
    data.setup('旋转角度', obvious=True,group='场地参数')
    data.setup('饮水机个数', obvious=True,group='场地参数')
    data.setup('地板长度', obvious=True, group='场地参数' )
    data.setup('地板宽度', obvious=True, group='场地参数' )
    data.setup('是否显示地板', obvious=True, group='场地参数' )
    data.setup('地板厚度', obvious=True, group='场地参数' )
    data.setup('顶棚宽度', obvious=True, group='顶棚参数' )
    data.setup('顶棚长度', obvious=True, group='顶棚参数' )
    data.setup('顶棚高度',readonly=True, obvious=True, group='顶棚参数' )
    data.setup('侧面外伸长度', obvious=True, group='顶棚参数' )
    data.setup('距地板距离', obvious=True, group='顶棚参数' )
    data.setup('顶棚龙骨边长', obvious=True,readonly=True, group='顶棚参数' )
    data.setup('椅子长度', obvious=True, group='椅子参数' )
    data.setup('椅子宽度', obvious=True, group='椅子参数' )
    data.setup('椅背高度', obvious=True,readonly=True, group='椅子参数' )  
    data.setup('距地板高度', obvious=True,readonly=True,group='椅子参数' )
    data.setup('竖杆半径', obvious=True,readonly=True,group='杆参数' )
    data.setup('斜杆半径', obvious=True,readonly=True,group='杆参数' )
    data.setup('场布分类', obvious=True,group = '类型参数')
    data.setup('构件类型', obvious=True,group = '类型参数')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = yinshuidian
    yinshuidian(data)
    # 发射数据到实例模板库
    p3d.launchData(data)

    