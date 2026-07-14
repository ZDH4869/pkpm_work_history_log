import pyp3d as p3d
from pyp3d import *
def xiyandian(data:p3d.P3DData)->None:
    rota=data['旋转角度']
    l=  data['开间']
    m=  data['进深']
    h_w=data['墙高度']
    j=  data['单位墙板长度']  
    r_t=data[ '屋顶厚度']   
    r_c=data['屋檐外伸长度']       
    r_lc=data['山墙外伸长度']
    k_k = 30       # 窗框宽度
    k_h = 30+30    # 窗框厚度
    d_k = 30       # 门框宽度
    d_h = 30+30    # 门框厚度
    c_g= data['窗户高度']
    c_k= data['窗户宽度']
    c_h= data[ '窗台高度']
    c_q= data['窗户距离墙距离']
    di= data['地板厚度']        
    di_c= data['地板正面外延长度']         
    di_lc=data['地板侧面外延长度']
    m_g= data['门高度']
    m_k= data['门宽度']
    m_h=di    #门距地面高度，与底板厚度有关，关联参数
    m_q= data['门距离墙距离']
    e_l=data['通风洞边长']
    e_h=data['通风洞距地板高度']
    e_q=data['洞距离远离门一侧墙距离']
    e_r=3*e_l/8   #关联
    b_l=400    #吸烟牌长度
    b_w=200    #吸烟牌宽度
    b_h=data['吸烟牌距地板高度']
    b_q=data['吸烟牌距门距离']
    step_w=m_k     #台阶宽度 与门宽相同（与门联动）
    tw=175         #踢面高度
    rw=di/2        #踏面宽度 （与底板厚度联动）  
    thickness=5    #风扇厚度
    data['场布分类']='建/构筑物'
    data['构件类型']='其他临建'

    #创建工棚  
    x1=p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(l,0,0),p3d.Vec3(l,0,h_w),p3d.Vec3(0,0,h_w)),p3d.Vec3(0,m,0)).color(1,1,1,1)
    x2=p3d.Extrusion((p3d.Vec3(100,100,0),p3d.Vec3(l-100,100,0),p3d.Vec3(l-100,100,h_w),p3d.Vec3(100,100,h_w)),p3d.Vec3(0,m-200,0)).color(1,1,1,1)   #墙厚100
    bb=p3d.substract(x1,x2) .color(0.95,0.95,0.95,1)
    # p3d.createGeometry(bb)


    #创建窗户洞和门洞，进行布尔减法，创建带窗洞和门洞的临时工棚
    cd=p3d.Box(p3d.Vec3(0,-150,0), p3d.Vec3(0,150,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  c_g, c_k, c_g, c_k).color(1,1,0,1) 
    cd=p3d.translation(c_q,0,c_h)*cd         
    bb=p3d.substract(bb,cd).color(1,1,1,1)

    md = p3d.Box(p3d.Vec3(0,-150,0), p3d.Vec3(0,150,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  m_g, m_k, m_g, m_k).color(1,1,0,1) 
    md=p3d.translation(l-m_q-m_k,0,0)*md  
    bb =p3d.substract(bb,md).color(1,1,1,1)
    # p3d.createGeometry(bb)


    #创建窗户
    #创建窗户玻璃
    b = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  c_g, c_k/2, c_g, c_k/2).color(1,1,1,0)   #10 玻璃厚度
    b=p3d.translation(k_k,k_h,k_k)*b  
    # p3d.createGeometry(b)  
    b1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  c_g, c_k/2, c_g, c_k/2).color(1,1,1,0) 
    b1=p3d.translation(k_k+c_k/2,k_h-10,k_k)*b1
    # p3d.createGeometry(b1)

    #创建窗框
    c_k_w=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,k_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), c_g+2*k_k, c_k+2*k_k, c_g+2*k_k, c_k+2*k_k).color(1,1,0,1) 
    c_k_n=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,k_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), c_g, c_k, c_g, c_k).color(1,1,0,1) 
    c_k_n=p3d.translation(k_k,0,k_k)*c_k_n
    ck =p3d.substract(c_k_w,c_k_n).color(1,1,1,1)
    # p3d.createGeometry(ck) 

    #窗户组合
    c=p3d.combine(b,b1,ck)
    c=p3d.translation(c_q-k_k,-k_h,c_h-k_k)*c  
    # p3d.createGeometry(c) 


    #创建门
    #创建门框
    m_wk=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,d_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), m_g, m_k, m_g, m_k).color(1,1,0,1) 
    m_nk=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,d_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), m_g-2*d_k, m_k-2*d_k, m_g-2*d_k, m_k-2*d_k).color(1,1,0,1) 
    m_nk=p3d.translation(d_k,0,d_k)*m_nk
    mk =p3d.substract(m_wk,m_nk).color(1,1,1,1)
    # p3d.createGeometry(mk) 

    #创建门板
    mb=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,20,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), m_g-2*d_k, m_k-2*d_k, m_g-2*d_k, m_k-2*d_k).color(1,1,0,1)   #20 门厚度
    mb=p3d.translation(d_k,d_h/2-10,d_k)*mb
    #创建有门洞的门板
    m_d=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,300,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300, 500,  300, 500).color(1,1,0,1) 
    m_d=translation(m_k/2-250,0,m_g-600)*m_d
    mb=p3d.substract(mb,m_d).color(1,1,1,1)
    # p3d.createGeometry(m) 

    #继续创建门玻璃
    m_b=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300, 500,  300, 500).color(1,1,1,0)                       #10 门玻璃厚度
    m_b=translation(m_k/2-250,d_h/2-5,m_g-600)*m_b
    # p3d.createGeometry(m_b) 

    #创建门玻璃框
    m_b_wk=p3d.Box(p3d.Vec3(0-10,0,0-10), p3d.Vec3(0-10,10,0-10), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300+20, 500+20,  300+20, 500+20).color(1,1,1,1)                      
    m_b_nk=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300, 500,  300, 500).color(1,1,1,1)              #10 门玻璃框厚度               
    m_b_k=p3d.substract(m_b_wk,m_b_nk).color(1,1,1,1)
    m_b_k=translation(m_k/2-250,d_h/2-5-10,m_g-600)*m_b_k
    # p3d.createGeometry(m_b_k)

    #门组合
    m1=p3d.combine(mk,mb,m_b,m_b_k)
    m1=p3d.translation(l-m_q-m_k,-d_h,0)*m1 
    # p3d.createGeometry(m1)


    #建立线
    zhu1=p3d.Extrusion((p3d.Vec3(0,0,0), p3d.Vec3(21,0,0), p3d.Vec3(14,-10,0), p3d.Vec3(7,-10,0)),p3d.Vec3(0,0,h_w))
    points1 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3((int(l/j))*j,0,0),int(l/j))
    xiaozhu1 = p3d.combine() 
    for point in points1:
        xiaozhu1.append(p3d.translation(point) * zhu1)
    xiaozhu1=p3d.substract(xiaozhu1,cd)
    xiaozhu1=p3d.substract(xiaozhu1,md)
    # p3d.createGeometry(xiaozhu1)

    #x正向，靠近门的一侧
    zhu2=p3d.rotation(p3d.Vec3(0,0,1),-p3d.pi/2)*zhu1
    zhu2=p3d.translation(0,21,0)*zhu2
    points2 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,(int(m/j))*j,0),int(m/j))
    xiaozhu2 = p3d.combine() 
    for point in points2:
        xiaozhu2.append(p3d.translation(point) * zhu2)
    # p3d.createGeometry(xiaozhu2)

    #房后
    zhu3=p3d.rotation(p3d.Vec3(0,0,-1),p3d.pi)*zhu1
    zhu3=p3d.translation(21,0,0)*zhu3
    points3 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3((int(l/j))*j,0,0),int(l/j))
    xiaozhu3 = p3d.combine() 
    for point in points3:
        xiaozhu3.append(p3d.translation(point) * zhu3)
    xiaozhu3=p3d.translation(0,m,0)*xiaozhu3
    # p3d.createGeometry(xiaozhu3)

    zhu4=p3d.rotation(p3d.Vec3(0,0,-1),-p3d.pi/2)*zhu1
    zhu4=p3d.translation(l,0,0)*zhu4
    points4 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,(int(m/j))*j,0),int(m/j))
    xiaozhu4 = p3d.combine() 
    for point in points4:
        xiaozhu4.append(p3d.translation(point) * zhu4)
    # p3d.createGeometry(xiaozhu4)

    #建立洞口
    ex=p3d.Extrusion((p3d.Vec3(0,0,0), p3d.Vec3(0,e_l,0), p3d.Vec3(0,e_l,e_l), p3d.Vec3(0,0,e_l),\
        p3d.Vec3(0,0,e_l)),p3d.Vec3(2000,0,0))
    ex1=translation(l-300,m-e_r-e_q,e_h)*ex
    bb=p3d.substract(bb,ex1).color(1,1,1,1)
    # p3d.createGeometry(bb)
    xiaozhu4=p3d.substract(xiaozhu4,ex1).color(1,1,1,1)
    # p3d.createGeometry(xiaozhu4)

    #创建风扇洞
    ex2=p3d.Extrusion((p3d.Vec3(0,0,0), p3d.Vec3(0,e_l,0), p3d.Vec3(0,e_l,e_l), p3d.Vec3(0,0,e_l),\
        p3d.Vec3(0,0,e_l)),p3d.Vec3(50,0,0))    #50 厚度
    fans= p3d.Cone(p3d.Vec3(0,e_l/2,e_l/2),p3d.Vec3(50,e_l/2,e_l/2),e_r,e_r).color(1,1,1,1)        # 厚度 50
    ex2=substract(ex2,fans)

    #创建风扇
    #定义外接圆半径
    list_n=[[0 for i in range(2)] for j in range(50)]
    for i in range (1,50+1):
        t = math.pi*i/50                        # t 为取样点角度，i代表个数
        # print (round(e_r * math.cos(2 * math.pi * i / n),2),round(e_r * math.sin(2 * math.pi * i / n),2))
        list_n[i-1][0]=int(round(e_r * math.sin(3*t)*math.cos(t),2))          # round取小数点后两位
        list_n[i-1][1]=int(round(e_r * math.sin(3*t)*math.sin(t),2))          # x = math.sin(3*t)*math.cos(t)  y = math.sin(3*t)*math.sin(t)为图形函数   
        i += 1
    # print(list_n)
    list_nn = [0 for i in range(50)]
    tuple_n = ()
    for j in range (50):
        list_nn[j] = (list_n[j][0],list_n[j][1],0)
        tuple_n += (p3d.Vec3(list_nn[j]),)
    # print(tuple_n)
    F = p3d.Extrusion((tuple_n),p3d.Vec3(0,0,thickness)).color(1,1,1,1)
    F1 = p3d.rotation(Vec3(0,1,0),0.5*p3d.pi)*F
    F2 = p3d.rotation(Vec3(1,0,0),p3d.pi*2/3)*F1
    F3 = p3d.rotation(Vec3(1,0,0),p3d.pi*2/3)*F2
    F4=p3d.combine(F1,F2,F3)
    F4=translation(50-thickness,e_l/2,e_l/2)*F4     #50-thickness  
    # createGeometry(F4)

    fans=combine(ex2,F4)
    # createGeometry(fans)
    fans=translation(l-50,m-e_r-e_q,e_h)*fans     #50 厚度
    # p3d.createGeometry(fans)

    #建立吸烟牌

    box1=p3d.Extrusion((p3d.Vec3(0,0,0), p3d.Vec3(b_l,0,0), p3d.Vec3(b_l,0,b_w), p3d.Vec3(0,0,b_w),\
        ),p3d.Vec3(0,3,0)) .color(1,1,1,1)
    box2=p3d.Extrusion((p3d.Vec3(0,0,0), p3d.Vec3(b_l,0,0), p3d.Vec3(b_l,0,b_w/8), p3d.Vec3(0,0,b_w/8),\
        ),p3d.Vec3(0,-1,0)) .color(34/255,21/255,106/255,1)   
    box3=p3d.Extrusion((p3d.Vec3(0,0,b_w-b_w/8), p3d.Vec3(b_l,0,b_w-b_w/8), p3d.Vec3(b_l,0,b_w), p3d.Vec3(0,0,b_w),\
        ),p3d.Vec3(0,-1,0)) .color(38/255,152/255,83/255,1)
    box4=combine(box1,box2,box3)
    # createGeometry(box4)
    text = Text("吸烟室", 80, 80, "微软雅黑").color(1, 0, 0, 1)
    text = p3d.rotation(Vec3(1, 0, 0), pi/2)*text
    text = translation(Vec3(40, -1, 60))*text
    # createGeometry(text)
    brand=combine(box4,text)
    brand=translation(Vec3(0, -10-3, 0))*brand                      #   10 装配厚度，3 板子厚度
    brand=translation(l-m_q-m_k-b_q-b_l,0,b_h)*brand            
    

    #建立屋顶，同时地上部分组合
    roof=p3d.Extrusion((p3d.Vec3(0-r_lc,0-r_c,0),p3d.Vec3(l+r_lc,0-r_c,0), p3d.Vec3(l+r_lc,m+r_c,0), p3d.Vec3(0-r_lc,m+r_c,0)),p3d.Vec3(0,0,r_t)).color(0/255,133/255,232/255,1)
    roof=p3d.translation(0,0,h_w)*roof
    wz=p3d.combine(bb,c,m1,xiaozhu1,xiaozhu3,xiaozhu4,xiaozhu2,roof,fans,brand)
    wz=p3d.translation(0,0,di)* wz

    #建立地板
    wzd=p3d.Extrusion([p3d.Vec3(0-di_lc,0-di_c,0),p3d.Vec3(l+di_lc,0-di_c,0), p3d.Vec3(l+di_lc,m+di_c,0), p3d.Vec3(0-di_lc,m+di_c,0)],p3d.Vec3(0,0,di)).color(0/255,133/255,232/255,1)
    #建立台阶
    step_w=m_k      #与门宽相同（与门联动）
    tw=250         #踢面宽度
    rw=di/2        #踏面宽度 （与底板厚度联动）
    step=p3d.Extrusion((p3d.Vec3(0,0,0), p3d.Vec3(0,-2*tw,0), p3d.Vec3(0,-tw*2,rw), p3d.Vec3(0,-tw,rw),\
        p3d.Vec3(0,-tw,2*rw),p3d.Vec3(0,0,2*rw)),p3d.Vec3(step_w,0,0))
    step=p3d.translation(l-m_q-m_k,-di_c,0)*step
    # p3d.createGeometry(step)

    wz=combine(wz,wzd,step)
    wz=rotation(p3d.Vec3(0,0,1),p3d.pi*rota/180)*wz
    # p3d.createGeometry(wz)
    data['吸烟点']=wz
    data['风扇半径（随洞口边长而定）']=e_r
    data['门距离地面高度（随地板变化）']=m_h
    data['台阶宽度（关联，与门宽相同）']=step_w

if __name__ == "__main__":
    data = p3d.P3DData({
        '旋转角度':0,
        '墙高度': 2500,
        '开间': 4000,  
        '进深': 3000,
        '单位墙板长度':200,

        '屋顶厚度':100,
        '屋檐外伸长度':200,
        '山墙外伸长度':100,

        '门高度': 2000,
        '门宽度': 900,
        '门距离地面高度':100,   
        '门距离墙距离':400,
        '门框宽度':30,
        '门框厚度':60,

        '窗户宽度': 1000,
        '窗户高度': 1000,
        '窗台高度':900,
        '窗户距离墙距离':400,
        '窗框宽度':30,
        '窗框厚度':60,

        '地板厚度':100,
        '地板正面外延长度':100,
        '地板侧面外延长度':100,

        '通风洞边长':400,
        '通风洞距地板高度':1700,
        '洞距离远离门一侧墙距离':1000,
        '风扇半径':150,

        '吸烟牌长度':400,
        '吸烟牌宽度':200,
        '吸烟牌距地板高度':1600,
        '吸烟牌距门距离':300,
        '台阶宽度':900,
        '踏面宽度':175,
        '台阶个数':2,
        '构件名称':'吸烟点'
        })
    
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('吸烟点', show=True)
    # 设置可调整属性
    data.setup('旋转角度', obvious=True,group='场地参数')
    data.setup('开间', obvious=True, group='场地参数' )
    data.setup('进深', obvious=True, group='场地参数' )
    data.setup('墙高度', obvious=True, group='场地参数' )
    data.setup('单位墙板长度', obvious=True, group='场地参数' )
    data.setup('屋顶厚度', obvious=True, group='屋顶参数' )
    data.setup('屋檐外伸长度', obvious=True, group='屋顶参数' )
    data.setup('山墙外伸长度', obvious=True, group='屋顶参数' )
    data.setup('门高度', obvious=True, group='门参数' )
    data.setup('门宽度', obvious=True, group='门参数' )  
    data.setup('门距离地面高度', obvious=True,readonly=True, group='门参数' ) 
    data.setup('门距离墙距离', obvious=True, group='门参数' )  
    data.setup('门框宽度', obvious=True,readonly=True,group='门参数' )
    data.setup('门框厚度', obvious=True,readonly=True,group='门参数' )
    data.setup('窗户高度', obvious=True, group='窗户参数' )
    data.setup('窗户宽度', obvious=True, group='窗户参数' )
    data.setup('窗台高度', obvious=True, group='窗户参数' )
    data.setup('窗户距离墙距离', obvious=True, group='窗户参数' )    
    data.setup('窗框宽度', obvious=True,readonly=True,group='窗户参数' )
    data.setup('窗框厚度', obvious=True,readonly=True,group='窗户参数' )
    data.setup('地板厚度', obvious=True, group='地板参数' )   
    data.setup('地板正面外延长度', obvious=True, group='地板参数' )
    data.setup('地板侧面外延长度', obvious=True, group='地板参数' )
    data.setup('吸烟牌长度', obvious=True,readonly=True,group='吸烟牌参数' )
    data.setup('吸烟牌宽度', obvious=True,readonly=True, group='吸烟牌参数' )
    data.setup('吸烟牌距地板高度', obvious=True, group='吸烟牌参数' )
    data.setup('吸烟牌距门距离', obvious=True, group='吸烟牌参数' )
    data.setup('通风洞边长', obvious=True, group='通风处参数' )  
    data.setup('通风洞距地板高度', obvious=True, group='通风处参数' )   
    data.setup('洞距离远离门一侧墙距离', obvious=True, group='通风处参数' )   
    data.setup('风扇半径', obvious=True,readonly=True, group='通风处参数' )  
    data.setup('台阶宽度', obvious=True,readonly=True, group='台阶参数' )
    data.setup('踏面宽度', obvious=True,readonly=True, group='台阶参数' )   
    data.setup('台阶个数', obvious=True,readonly=True, group='台阶参数' )
    data.setup('场布分类', obvious=True,readonly=True, group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True, group = '类型参数')
    data.setup('构件名称', obvious=True)    
    # 设置replace算子
    data['replace'] = xiyandian
    xiyandian(data)
    # 发射数据到实例模板库
    p3d.launchData(data)    
