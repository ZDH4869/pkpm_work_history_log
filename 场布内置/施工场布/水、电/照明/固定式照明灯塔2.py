import pyp3d as p3d
def lighthouse(data:p3d.P3DData)->None:
        b_l=data['底板长'] 
        b_w=data['底板宽']
        b_t=data['底板厚']
        rob_1_h=data['竖杆1高']
        R_1=data['竖杆1半径']
        rob_2_h=data['竖杆2高']
        R_2=data['竖杆2半径']  
        rob_3_h=data['竖杆3高']
        R_3=data['竖杆3半径']
        rob_4_h=data['横杆杆长']
        R_4=data['横杆半径']
        lampshade_1_h=data['灯罩1高']
        lampshade_1_r=data['灯罩1半径']
        lampshade_2_h=data['灯罩2高']
        lampshade_2_r=data['灯罩2半径']
        S_R=data['灯泡半径']
        ro=data['旋转角度']
        data['场布分类']='消防水电'
        data['构件类型']='电气设备'

        b_w=data['底板宽']
        b_l=data['底板长']
        if data['竖杆1半径']>data['底板长']/2:
                R_1=b_l/2
                data['竖杆1半径']=data['底板长']/2
        if data['竖杆2半径']>data['竖杆1半径']:
                R_2=R_1
                data['竖杆2半径']=data['竖杆1半径']
        if data['竖杆3半径']>data['竖杆2半径']:
                R_3=R_2
                data['竖杆3半径']=data['竖杆2半径']
        if data['横杆半径']>data['竖杆3半径']:
                R_4=R_3
                data['横杆半径']=data['竖杆3半径']
        if data['灯罩1半径']>data['灯罩2半径']:
                lampshade_1_h=lampshade_2_h
                data['灯罩1半径']=data['灯罩2半径']
        if data['灯泡半径']>data['灯罩2半径']:
                S_R=lampshade_2_h
                data['灯泡半径']=data['灯罩2半径']
        if data['灯罩2半径']>data['横杆杆长']/2:
                lampshade_2_r=rob_4_h/2
                data['灯罩2半径']=data['横杆杆长']/2
        if data['灯罩1高']>data['竖杆3高']/2:
                lampshade_1_h=rob_3_h/2
                data['灯罩1高']=data['竖杆3高']/2
        if data['灯罩2高']>data['竖杆3高']/2:
                lampshade_2_h=rob_3_h/2
                data['灯罩2高']=data['竖杆3高']/2
        #底座
        bottom=p3d.Box(p3d.Vec3(-b_l/2,-b_w/2,0), p3d.Vec3(-b_l/2,-b_w/2,b_t), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), b_l, b_w, b_l, b_w).color(0.7,0.7,0.7,1)

        #灯杆
        #灯杆1
        rob_1=p3d.Cone(p3d.Vec3(0,0,b_t),p3d.Vec3(0,0,b_t+rob_1_h),R_1,R_1).color(1,1,1,1)
        
        #灯杆2
        rob_2=p3d.Cone(p3d.Vec3(0,0,b_t+rob_1_h),p3d.Vec3(0,0,b_t+rob_1_h+rob_2_h),R_2,R_2).color(1,1,1,1)
        
        #灯杆3
        rob_3=p3d.Cone(p3d.Vec3(0,0,b_t+rob_1_h+rob_2_h),p3d.Vec3(0,0,b_t+rob_1_h+rob_2_h+rob_3_h),R_3,R_3).color(1,1,1,1)
        # p3d.createGeometry(rob_3)

        #三角支撑
        post1=p3d.Extrusion(
                (p3d.Vec3(R_1,-10,b_t),p3d.Vec3(R_1+(b_l/2-R_1)*3/4,-10,b_t),p3d.Vec3(R_1,-10,b_t+(b_l/2-R_1)*3/4)),p3d.Vec3(0,20,0)
                ).color(0.7,0.7,0.7,1)
        post2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*0.5) * p3d.Extrusion(
                (p3d.Vec3(R_1,-10,b_t),p3d.Vec3(R_1+(b_w/2-R_1)*3/4,-10,b_t),p3d.Vec3(R_1,-10,b_t+(b_w/2-R_1)*3/4)),p3d.Vec3(0,20,0)
                ).color(0.7,0.7,0.7,1)
        # post2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*0.5) * post1
        post3=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * post1
        post4=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * post2
        post=p3d.Combine(post1,post2,post3,post4)

        #横杆
        Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,rob_4_h),R_4,R_4).color(1,1,1,1)
        F1 = p3d.rotation(p3d.Vec3(0,1,0),p3d.pi*-0.5) * Cone1

        #灯
        Cone2 = p3d.Cone(p3d.Vec3(-rob_4_h*2/3,-R_4/2,0),p3d.Vec3(-rob_4_h*2/3,-R_4/2-lampshade_1_h,0),lampshade_1_r,lampshade_1_r).color(1,1,1,1)
        Cone3 = p3d.Cone(p3d.Vec3(-rob_4_h*2/3,-R_4/2-lampshade_1_h,0),p3d.Vec3(-rob_4_h*2/3,-R_4/2-lampshade_1_h-lampshade_2_h,0),lampshade_2_r,lampshade_2_r).color(1,1,1,1)
        Sphere1 = p3d.Sphere(p3d.Vec3(-rob_4_h*2/3,-R_4/2-lampshade_1_h-lampshade_2_h,0),S_R).color(1,1,1,1)
        light1=p3d.Combine(Sphere1,Cone3).color(1,1,1,1)
        light2=p3d.Combine(light1,F1,Cone2).color(1,1,1,1)
        light3=p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5) * light2
        light4=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*1) * light3
        light=p3d.translation(p3d.Vec3(0,0,b_t+rob_1_h+rob_2_h+rob_3_h-100)) *(p3d.Combine(light3,light4))

        #灯与杆3布尔并
        l_r3=p3d.Combine(light,rob_3)
        FG=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*ro/180) *p3d.Combine(bottom,rob_1,rob_2,post, l_r3) 
        data['灯塔'] = FG

if __name__=="__main__":
        data=p3d.P3DData({
                '底板长':500,
                '底板宽':500,
                '底板厚':50,
                '竖杆1高':3000,
                '竖杆1半径':50,
                '竖杆2高':2000,
                '竖杆2半径':40,
                '竖杆3高':1000,
                '竖杆3半径':30,
                '横杆杆长':600,
                '横杆半径':20,
                '灯罩1高':40,
                '灯罩1半径':50,
                '灯罩2高':100,
                '灯罩2半径':100,
                '灯泡半径':50,
                '旋转角度':0,
                '构件名称':'固定式照明灯塔2'
        })
        # data.set_view(1,1)
        # 输出构件
        data.setup('灯塔', show=True)
        # 设置可调整属性
        data.setup('底板长', obvious=True, group='底板', description='——————')
        data.setup('底板宽', obvious=True, group='底板', description='——————')
        data.setup('底板厚', obvious=True, group='底板', description='——————')
        data.setup('竖杆1高', obvious=True, group='竖杆1', description='——————')
        data.setup('竖杆1半径', obvious=True, group='竖杆1', description='——————')
        data.setup('竖杆2高', obvious=True, group='竖杆2', description='——————')
        data.setup('竖杆2半径', obvious=True, group='竖杆2', description='——————')
        data.setup('竖杆3高', obvious=True, group='竖杆3', description='——————')
        data.setup('竖杆3半径', obvious=True, group='竖杆3', description='——————')
        data.setup('横杆杆长', obvious=True, group='横杆', description='——————')
        data.setup('横杆半径', obvious=True, group='横杆', description='——————')
        data.setup('灯罩1高', obvious=True, group='灯罩1', description='——————')
        data.setup('灯罩1半径', obvious=True, group='灯罩1', description='——————')
        data.setup('灯罩2高', obvious=True, group='灯罩2', description='——————')
        data.setup('灯罩2半径', obvious=True, group='灯罩2', description='——————')
        data.setup('灯泡半径', obvious=True, group='灯泡', description='——————')
        data.setup('旋转角度', obvious=True, group='旋转', description='——————')
        data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
        data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
        data.setup('构件名称', obvious=True) 
        # 设置replace算子
        data['replace'] = lighthouse
        lighthouse(data)
        # 发射数据到实例模板库
        p3d.launchData(data)