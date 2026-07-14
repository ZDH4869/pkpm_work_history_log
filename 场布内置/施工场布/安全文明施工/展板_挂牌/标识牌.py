import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:
    # 在修机械
    box1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,(data['高度'])/8), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(1,0,0,1) 
    box2 = p3d.Box(p3d.Vec3(0,0,(data['高度'])/8), p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2,data['厚度']/2).color(0,1,1,1) 
    box3 = p3d.Box(p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(0,0,(data['高度'])/2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(225/255,225/255,225/255,1) 
    box11=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 136*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,148*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box12=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 112*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,124*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box13=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 88*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,100*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box14=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 64*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,76*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    B1=p3d.combine(box11,box12,box13,box14)

    text1= p3d.Text("送变电公司",12*(data['底边长']/600),12*(data['底边长']/600)).color(0, 0, 1, 1)
    text1= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text1
    text1= p3d.translation(p3d.Vec3(80*(data['底边长'])/600, -1, 170*(data['高度'])/400))*text1

    text11=p3d.Text("机械名称",10*(data['底边长']/600),10*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text11= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text11
    text11= p3d.translation(p3d.Vec3(35*(data['底边长']/600), -1, 136*(data['高度']/400)))*text11

    text12=p3d.Text("规格能力",10*(data['底边长']/600),10*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text12= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text12
    text12= p3d.translation(p3d.Vec3(35*(data['底边长']/600), -1, 112*(data['高度']/400)))*text12

    text13=p3d.Text("机械编号",10*(data['底边长']/600),10*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text13= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text13
    text13= p3d.translation(p3d.Vec3(35*(data['底边长']/600), -1, 88*(data['高度']/400)))*text13

    text14=p3d.Text("检测时间",10*(data['底边长']/600),10*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text14= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text14
    text14= p3d.translation(p3d.Vec3(35*(data['底边长']/600), -1, 64*(data['高度']/400)))*text14

    text111=p3d.Text("在修机械",27*(data['底边长']/600),27*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text111= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text111
    text111= p3d.translation(p3d.Vec3(70*(data['底边长']/600), -1, 10*(data['高度']/400)))*text111


    T1=p3d.combine(text11,text12,text13,text14)
    F1=p3d.combine(box1,box2,box3,B1,text1,T1,text111)

    2#合格品
    box4 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,50*(data['高度']/400)), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(0,1,0,1) 
    box5 = p3d.Box(p3d.Vec3(0,0,50*(data['高度']/400)), p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(0,1,1,1) 
    box6 = p3d.Box(p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(0,0,(data['高度'])/2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(225/255,225/255,225/255,1) 
    text2= p3d.Text("送变电公司",12*(data['底边长']/600),12*(data['底边长']/600)).color(0, 0, 1, 1)
    text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text2
    text2= p3d.translation(p3d.Vec3(80*(data['底边长'])/600, 0, 170*(data['高度'])/400))*text2

    box22=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 112*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,124*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box23=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 88*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,100*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 

    B2=p3d.combine(box22,box23)

    text21=p3d.Text("材料标识牌",15*(data['底边长']/600),15*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text21= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text21
    text21= p3d.translation(p3d.Vec3((100*data['底边长']/600), -1, 136*(data['高度']/400)))*text21

    text22=p3d.Text("材料名称",12*(data['底边长']/600),12*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text22= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text22
    text22= p3d.translation(p3d.Vec3(35*(data['底边长']/600), -1, 112*(data['高度']/400)))*text22

    text23=p3d.Text("规    格",12*(data['底边长']/600),12*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text23= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text23
    text23= p3d.translation(p3d.Vec3(35*(data['底边长']/600), -1, 88*(data['高度']/400)))*text23

    text222=p3d.Text("合格品",27*(data['底边长']/600),27*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text222= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text222
    text222= p3d.translation(p3d.Vec3(90*(data['底边长']/600), -1, 10*(data['高度']/400)))*text222

    T2=p3d.combine(text21,text22,text23)
    F2=p3d.combine(box5,box6,box4,B2,text2,T2,text222)
    F3 = p3d.translation(p3d.Vec3(data['底边长']/2,0,0)) * F2

    3#完好机械
    box7 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,(data['高度'])/8), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(0,1,0,1) 
    box8 = p3d.Box(p3d.Vec3(0,0,(data['高度'])/8), p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(0,1,1,1) 
    box9 = p3d.Box(p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(0,0,(data['高度']/2)), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(225/255,225/255,225/255,1) 
    box31=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 136*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,148*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box32=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 112*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,124*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box33=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 88*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,100*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box34=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 64*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,76*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    B3=p3d.combine(box31,box32,box33,box34)

    text3= p3d.Text("送变电公司",12*(data['底边长']/600),12*(data['底边长']/600)).color(0, 0, 1, 1)
    text3= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text3
    text3= p3d.translation(p3d.Vec3(80*(data['底边长'])/600, -1, 170*(data['高度'])/400))*text3
    text333=p3d.Text("完好机械",27*(data['底边长']/600),27*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text333= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text333
    text333= p3d.translation(p3d.Vec3(70*(data['底边长']/600), -1, 10*(data['高度'])/400))*text333

    F4=p3d.combine(box7,box8,box9,B3,text3,T1,text333)
    F5 = p3d.translation(p3d.Vec3(0,0,(data['高度']/2))) * F4

    4#待修机械
    box10 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,(data['高度'])/8), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(1,1,0,1) 
    box11= p3d.Box(p3d.Vec3(0,0,(data['高度'])/8), p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(0,1,1,1) 
    box12 = p3d.Box(p3d.Vec3(0,0,2*(data['高度'])/5), p3d.Vec3(0,0,(data['高度'])/2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['底边长']/2, data['厚度']/2, data['底边长']/2, data['厚度']/2).color(225/255,225/255,225/255,1) 
    box41=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 136*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,148*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box42=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 112*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,124*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box43=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 88*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,100*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    box44=p3d.Box(p3d.Vec3((data['底边长']/6), -1, 64*(data['高度']/400)), p3d.Vec3((data['底边长']/6),-1,76*(data['高度'])/400), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), (data['底边长'])/4, 1, (data['底边长'])/4, 1).color(225/255,225/255,225/255,1) 
    B4=p3d.combine(box41,box42,box13,box44)
    text4= p3d.Text("送变电公司",12*(data['底边长']/600),12*(data['底边长']/600)).color(0, 0, 1, 1)
    text4= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text4
    text4= p3d.translation(p3d.Vec3(80*(data['底边长'])/600, -1, 170*(data['高度'])/400))*text4
    text444=p3d.Text("待修机械",27*(data['底边长']/600),27*(data['底边长']/600)).color(225/255,225/255,225/255,1) 
    text444= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text444
    text444= p3d.translation(p3d.Vec3(70*(data['底边长']/600), -1, 10*(data['高度'])/400))*text444

    F6=p3d.combine(box10,box11,box12,B4,text4,T1,text444)
    F7= p3d.translation(p3d.Vec3(data['底边长']/2,0,(data['高度']/2))) * F6
    A=p3d.combine(F1,F3,F5,F7)
    B=data['旋转角度']
    A=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*(B/180))*A
    data['一个指示牌'] = A
  
if __name__ == "__main__":
    data = p3d.P3DData({
        '场布分类':'挂牌资料',
        '构件类型':'其他标识牌',
        '构件名称':'标识牌',
        '底边长': 600,
        '厚度': 10,
        '高度': 400,
        '旋转角度':0
        })

    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('一个指示牌', show=True)
    # 设置可调整属性
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('底边长', obvious=True, group='边长', description='底边长')
    data.setup('厚度', obvious=True, group='边长', description='厚度')
    data.setup('高度', obvious=True, group='边长', description='高度')
    data.setup('旋转角度',obvious=True,group='旋转位置',description='旋转角度')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = test_box
    test_box(data)
    # 发射数据到实例模板库
    p3d.launchData(data)