import pyp3d as p3d
import math

def dengta(data:p3d.P3DData)->None:
    TLW = data['桁架最顶面长宽']
    BLW = data['桁架最底面长宽']
    UH = data['每单元节高度']
    UN = data['单元节个数']
    LLW = data['灯台长宽']
    LH = data['灯台高度']
    DLW = data['底座长宽']
    DH = data['底座高度']
    L2L = data['灯具长']
    L2W = data['灯具宽']
    L2H = data['灯具高']
    RC1 = data['桁架及灯台红色值']
    GC1 = data['桁架及灯台绿色值']    
    BC1 = data['桁架及灯台蓝色值']
    RC2 = data['底座红色值']
    GC2 = data['底座绿色值']    
    BC2 = data['底座蓝色值']    
    UAH = UH*UN
    RR = data['整体朝向角度°'] 

    #使桁架顶底长宽不超过灯台和底座，且最底面长宽不能超过最顶面长宽
#     if TLW > BLW:
#          TLW = BLW
#     if BLW > DLW:
#          BLW = DLW
#     if TLW > LLW:
#          TLW = LLW
    if data['灯具宽']>200:
         L2W =200
         data['灯具宽']=L2W

    if data['灯具长']>600:
         L2L =600
         data['灯具长']=L2L
    if data['灯台长宽']>2000:
         LLW =2000
         data['灯台长宽']=2000
    if data['灯台长宽']<1200:
         LLW =1200
         data['灯台长宽']=1200
 
    #桁架
    truss = p3d.combine()
    Points = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3((BLW-TLW)/2,(BLW-TLW)/2,UAH),UN+1)
    Pointsb = p3d.linspace(p3d.Vec3(BLW,0,0),p3d.Vec3((BLW-TLW)/2+TLW,(BLW-TLW)/2,UAH),UN+1)
    Points1 = Points[0:UN]
    Points2 = Points[1:UN+1]
    Pointsb1 = Pointsb[0:UN]
    Pointsb2 = Pointsb[1:UN+1]
    #桁架参数化
    for i in range(UN):
         Cone1=p3d.Cone(Points1[i],Points2[i],10,10).color(RC1/255,GC1/255,BC1/255,1)
         Cone2=p3d.Cone(Points2[i],Pointsb2[i],10,10).color(RC1/255,GC1/255,BC1/255,1)
         Cone3=p3d.Cone(Points2[i],Pointsb1[i],10,10).color(RC1/255,GC1/255,BC1/255,1)
         Cone4=p3d.Cone(Points1[i],Pointsb2[i],10,10).color(RC1/255,GC1/255,BC1/255,1)
         Cones = p3d.combine(Cone1,Cone2,Cone3,Cone4)
         Cones2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*90/180) * Cones
         Cones2=p3d.translation(p3d.Vec3(BLW,0,0)) * Cones2
         Cones3=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*180/180) * Cones
         Cones3=p3d.translation(p3d.Vec3(BLW,BLW,0)) * Cones3
         Cones4=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*270/180) * Cones
         Cones4=p3d.translation(p3d.Vec3(0,BLW,0)) * Cones4
         ConesT=p3d.combine(Cones,Cones2,Cones3,Cones4)
         truss.append(ConesT)
    #灯台及栏杆
    head = p3d.Extrusion((p3d.Vec3(-LLW/2,-LLW/2,UAH+10),p3d.Vec3(LLW/2,-LLW/2,UAH+10),p3d.Vec3(LLW/2,LLW/2,UAH+10),p3d.Vec3(-LLW/2,LLW/2,UAH+10)),p3d.Vec3(0,0,2)).color(RC1/255,GC1/255,BC1/255,1)
    head = p3d.translation(p3d.Vec3(BLW/2,BLW/2,0)) * head
    headhandle1 = p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(10,0,0),p3d.Vec3(10,0,LH-10),p3d.Vec3(LLW-10,0,LH-10),p3d.Vec3(LLW-10,0,LH),p3d.Vec3(0,0,LH)),p3d.Vec3(0,10,0)).color(RC1/255,GC1/255,BC1/255,1)
    headhandle2 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*90/180) * headhandle1
    headhandle2 = p3d.translation(p3d.Vec3(LLW,0,0)) * headhandle2
    headhandle3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*180/180) * headhandle1
    headhandle3 = p3d.translation(p3d.Vec3(LLW,LLW,0)) * headhandle3
    headhandle4 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*270/180) * headhandle1
    headhandle4 = p3d.translation(p3d.Vec3(0,LLW,0)) * headhandle4
    headhandles = p3d.combine(headhandle1,headhandle2,headhandle3,headhandle4)
    headhandles = p3d.translation(p3d.Vec3(BLW/2-LLW/2,BLW/2-LLW/2,UAH+10)) * headhandles
    #底座
    box1 = p3d.Extrusion((p3d.Vec3(-DLW/2,-DLW/2,-DH),p3d.Vec3(DLW/2,-DLW/2,-DH),p3d.Vec3(DLW/2,DLW/2,-DH),p3d.Vec3(-DLW/2,DLW/2,-DH)),p3d.Vec3(0,0,DH)).color(RC2/255,GC2/255,BC2/255,1)
    box1 = p3d.translation(p3d.Vec3(BLW/2,BLW/2,0)) * box1
    #灯具
    light1 = p3d.Extrusion([p3d.Vec3(-L2L/2,-L2W/2,-L2H),p3d.Vec3(-L2L/2,-L2W/2,-L2H+6.25),p3d.Vec3(-L2L/2,(L2W/2)-6.25,-L2H+6.25),p3d.Vec3(-L2L/2,(L2W/2)-6.25,-(L2H/4)),p3d.Vec3(-L2L/2,0,-6.25),p3d.Vec3(-L2L/2,-L2W/2,-6.25),p3d.Vec3(-L2L/2,-L2W/2,0),p3d.Vec3(-L2L/2,0,0),p3d.Vec3(-L2L/2,L2W/2,-50),p3d.Vec3(-L2L/2,L2W/2,-L2H)],p3d.Vec3(L2L,0,0)).color(76.5/255,76.5/255,76.5/255,1)
    light2 = p3d.Extrusion([p3d.Vec3(-L2L/2,-L2W/2,-L2H+6.25),p3d.Vec3(-L2L/2,-L2W/2,-6.25),p3d.Vec3(-L2L/2,0,-6.25),p3d.Vec3(-L2L/2,0,-6.25),p3d.Vec3(-L2L/2,(L2W/2)-6.25,-(L2H/4)),p3d.Vec3(-L2L/2,(L2W/2)-6.25,-L2H+6.25)],p3d.Vec3(6.25,0,0)).color(76.5/255,76.5/255,76.5/255,1)
    light3 = p3d.translation(p3d.Vec3(L2L-6.25,0,0)) * light2
    light4 = p3d.Box(p3d.Vec3(-L2L/2+6.25,-L2W/2,-L2H+6.25), p3d.Vec3(-L2L/2+6.25,-L2W/2,-6.25), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),L2L-12.5,6.25,L2L-12.5,6.25).color(255/255,255/255,255/255,0.7)
    lightA = p3d.combine(light1,light2,light3,light4)
    lightA2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*90/180) * lightA
    lightA2=p3d.translation(p3d.Vec3(LLW/2-200,LLW/2,0)) * lightA2
    lightA3=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*180/180) * lightA
    lightA3=p3d.translation(p3d.Vec3(0,LLW-200,0)) * lightA3
    lightA4=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*270/180) * lightA
    lightA4=p3d.translation(p3d.Vec3(-LLW/2+200,LLW/2,0)) * lightA4
    lightA =p3d.translation(p3d.Vec3(0,200,0)) * lightA
    lights = p3d.combine(lightA,lightA2,lightA3,lightA4)
    lights = p3d.translation(p3d.Vec3(BLW/2,-LLW/2+BLW/2,UAH+L2H+20)) * lights
    dengta1 = p3d.combine(truss,headhandles,head,box1,lights)
    data['灯塔'] = dengta1
    data['灯塔'] = p3d.translation(p3d.Vec3(-BLW/2,-BLW/2,DH))*data['灯塔']
    data['灯塔'] = p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*RR/180)*data['灯塔']
if __name__ == "__main__":
    data = p3d.P3DData({
        '桁架最顶面长宽':500,
        '桁架最底面长宽':1000,
        '每单元节高度':1000,
        '单元节个数':15,
        '灯台长宽':1200,
        '灯台高度':300,
        '底座长宽':2000,
        '底座高度':50,
        '灯具长':500,
        '灯具宽':150,
        '灯具高':400,
        '桁架及灯台红色值':196,
        '桁架及灯台绿色值':196,
        '桁架及灯台蓝色值':196,
        '底座红色值':222,
        '底座绿色值':222,
        '底座蓝色值':222,
        '场布分类':'构筑物',
        '构件类型':'照明设施',
        '整体朝向角度°':0,
        '构件名称':'锥形固定式照明灯塔'
    })
#     data.set_view(1,1)
    data.setup('桁架最顶面长宽', obvious = True, group='桁架')
    data.setup('桁架最底面长宽', obvious = True, group='桁架')
    data.setup('每单元节高度', obvious = True, group='桁架')
    data.setup('单元节个数', obvious = True, group='桁架')
    data.setup('灯台长宽', obvious = True, group='灯台')
    data.setup('灯台高度', obvious = True, group='灯台')
    data.setup('底座长宽', obvious = True, group='底座')
    data.setup('底座高度', obvious = True, group='底座')
    data.setup('灯具长', obvious=True, group='灯具')
    data.setup('灯具宽', obvious=True, group='灯具')
    data.setup('灯具高', obvious=True, group='灯具')
    data.setup('桁架及灯台红色值', obvious = True, group='桁架')
    data.setup('桁架及灯台绿色值', obvious = True, group='桁架')
    data.setup('桁架及灯台蓝色值', obvious = True, group='桁架')
    data.setup('底座红色值', obvious = True, group='底座')
    data.setup('底座绿色值', obvious = True, group='底座')
    data.setup('底座蓝色值', obvious = True, group='底座')
    data.setup('整体朝向角度°', obvious = True, group='整体')
    data.setup('场布分类', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件类型', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件名称',obvious=True)
    data.setup('灯塔', show = True)
    data['replace'] = dengta
    dengta(data)
    p3d.launchData(data)