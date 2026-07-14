from pyp3d import *
from math import *

##################################################################桌子
def check_in_construct(data:P3DData)->None:
    # 参数
    l_table = data['桌面长']   # x axis
    b_table = data['桌面宽']   # y axis
    d_table = data['桌面厚']   
    h_table = data['桌子高']   
    # 桌面
    sec_table = Section(
        Vec2(l_table/2,b_table/2),
        Vec2(-l_table/2,b_table/2),
        Vec2(-l_table/2,-b_table/2),
        Vec2(l_table/2,-b_table/2),
        Vec2(l_table/2,b_table/2),
    )
    table = Loft(
        translate(0,0,h_table-d_table) * sec_table,
        translate(0,0,h_table) * sec_table,
    ).color(210/255,105/255,30/255,1)
    # 桌腿
    sec_leg = Section(Arc(2*pi))
    leg = Loft(
        scale(20) * sec_leg,
        translate(0,0,h_table-d_table) * scale(40) * sec_leg,
    ).color(210/255,105/255,30/255,1)
    leg = combine(
        translate(l_table/2*0.8,b_table/2*0.8) * leg,
        translate(-l_table/2*0.8,b_table/2*0.8) * leg,
        translate(-l_table/2*0.8,-b_table/2*0.8) * leg,
        translate(l_table/2*0.8,-b_table/2*0.8) * leg,
    )
    table = combine(table,leg)
    # 文字
    text01 = translate(15,30,2) * Text('消毒区',0.4*100,0.4*100).color(0.9,1,1,1)
    text01_bottom = scale(200,100,1) * Cube().color(0/255,191/255,255/255,1)
    text01 = combine(text01,text01_bottom)
    text02 = translate(15,30,2) * Text('测温区',0.4*100,0.4*100).color(0.9,1,1,1)
    text02_bottom = scale(200,100,1) * Cube().color(0/255,191/255,255/255,1)
    text02 = combine(text02,text02_bottom)
    text03 = translate(15,30,2) * Text('登记区',0.4*100,0.4*100).color(0.9,1,1,1)
    text03_bottom = scale(200,100,1) * Cube().color(0/255,191/255,255/255,1)
    text03 = combine(text03,text03_bottom)
    # 文字定位
    sign = combine(
        translate(-l_table/3,-b_table/2.5,h_table) * translate(-100,0,0) * text01,
        translate(0,-b_table/2.5,h_table) * translate(-100,0,0) * text02,
        translate(l_table/3,-b_table/2.5,h_table) * translate(-100,0,0) * text03,
    )
        ################################################################测温枪
    # 参数
    b_gun = 40      # 枪宽度
    l_gunhead = 102 # 枪头长度——y axis
    h_gunbody = 100 # 握把长度——z axis
    alpha = pi/6    # 屏幕倾斜角度——与竖向夹角
    beta = pi/12    # 屏幕倾斜角度——与竖向夹角
    # 枪头 - 几何中心定位
    sec_gunhead_front = Section(
        translate(-b_gun/2+b_gun*0.1,+b_gun/2-b_gun*0.1,) * scale(b_gun*0.1) * rotation(0.5*pi) * Arc(0.5*pi),
        rotation(0.5*pi) * translate(-b_gun/2+b_gun*0.1,+b_gun/2-b_gun*0.1,) * scale(b_gun*0.1) * rotation(0.5*pi) * Arc(0.5*pi),
        rotation(1*pi) * translate(-b_gun/2+b_gun*0.1,+b_gun/2-b_gun*0.1,) * scale(b_gun*0.1) * rotation(0.5*pi) * Arc(0.5*pi),
        rotation(1.5*pi) * translate(-b_gun/2+b_gun*0.1,+b_gun/2-b_gun*0.1,) * scale(b_gun*0.1) * rotation(0.5*pi) * Arc(0.5*pi),
    )
    sec_gunhead_back = rotation(Vec3(1,0,0),-alpha) * Section(
        translate(-b_gun/2+b_gun*0.1,+(b_gun/2/cos(alpha))-b_gun*0.1,) * scale(b_gun*0.1) * rotation(0.5*pi) * Arc(0.5*pi),
        translate(-b_gun/2+b_gun*0.1,-(b_gun/2/cos(alpha))+b_gun*0.1,) * scale(b_gun*0.1) * rotation(1*pi) * Arc(0.5*pi),
        rotation(1*pi) * translate(-b_gun/2+b_gun*0.1,+(b_gun/2/cos(alpha))-b_gun*0.1,) * scale(b_gun*0.1) * rotation(0.5*pi) * Arc(0.5*pi),
        rotation(1*pi) * translate(-b_gun/2+b_gun*0.1,-(b_gun/2/cos(alpha))+b_gun*0.1,) * scale(b_gun*0.1) * rotation(1*pi) * Arc(0.5*pi),
    )
    gunhead = Loft(
        rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_front,
        translate(0,-l_gunhead,0) * rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_back,
    )
    # 枪头内凹
    sec_gunhead_fronttailor = scale(0.4)*sec_gunhead_front
    gunhead_fronttailor = Loft(
        translate(0,+5,0) * rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_fronttailor,
        translate(0,-5,0) * rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_fronttailor,
    )
    sec_gunhead_backtailor = scale(0.8)*sec_gunhead_back
    gunhead_backtailor = Loft(
        translate(0,+3-l_gunhead,0) * rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_backtailor,
        translate(0,-3-l_gunhead,0) * rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_backtailor,
    )
    gunhead = (gunhead - gunhead_fronttailor - gunhead_backtailor)
    # 屏幕
    screen = Loft(
        translate(0,+3-l_gunhead,0) * rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_backtailor,
        translate(0,-l_gunhead,0) * rotation(Vec3(1,0,0),0.5*pi) * sec_gunhead_backtailor,
    ).color(135/255,206/255,235/255,0.7)
    temperature = translate(-12,-l_gunhead-3,-6) * rotation(Vec3(1,0,0),0.5*pi-alpha) * Text('36.4℃',0.06*100,0.15*100)
    screen = combine(screen,temperature)
    # 握把
    sec_gunbody = sec_gunhead_front
    gunbody = Loft(
        sec_gunbody,
        translate(0,-tan(beta)*h_gunbody,-h_gunbody) * sec_gunbody,
    )
    gunbody = translate(0,-l_gunhead+b_gun/2,-b_gun/2+0.1*b_gun) * gunbody.color(255/255,255/255,240/255,1)
    # 扳机
    r_triger = 30
    sec_triger = Section(
        scale(r_triger) * Arc(-pi/5),
        Vec3(r_triger+15,-sin(pi/5)*r_triger,0),
        Vec3(r_triger+15,0,0),
    )
    triger = Loft(
        sec_triger,
        translate(0,0,-10) * sec_triger,
    )
    triger = translate(-5,+r_triger-l_gunhead+b_gun+8,-b_gun/2) * rotation(-0.5*pi) * rotation(Vec3(1,0,0),0.5*pi) * triger.color(0,0,0,1)
    # 组装
    gun = (gunbody+gunhead).color(255/255,255/255,240/255,1)
    gun = combine(gun,triger,screen)
    # 定位
    gun = translate(b_gun,0,h_table+b_gun/2) * rotation(Vec3(0,1,0),0.5*pi) * gun
    ####################################################################################登记本
    # 参数
    l_note = 300    # 本封皮长 y axis
    b_note = 200    # 本封皮宽 x axis
    h_note = 20     # 本封皮厚 z axis

    # 书皮
    sec_notecover = Section(
        Vec2(0,0),
        Vec2(b_note,0),
        Vec2(b_note,l_note),
        Vec2(0,l_note),
        Vec2(0,0)
    )
    sec_noteridge = Section(
        Vec2(0,0),
        Vec2(h_note,0),
        Vec2(h_note,l_note),
        Vec2(0,l_note),
        Vec2(0,0)
    )
    notecover_part = Loft(
        sec_notecover, translate(0,0,1) * sec_notecover,
    )
    noteridge = rotation(Vec3(0,1,0),-0.5*pi) * Loft(
        sec_noteridge, translate(0,0,1) * sec_noteridge,
    )
    notecover = notecover_part + translate(0,0,h_note-1) * notecover_part + noteridge
    # 书页
    paper = Loft(
        translate(0,0,1) * sec_notecover,
        translate(0,0,h_note-1) * sec_notecover,
    ).color(1,1,1,1)
    # 文字
    title = Text('登记本',0.3*100,0.3*100)
    title = translate((b_note-3*40)/2,l_note/2,h_note+1) * title.color(0.9,1,1,1)
    # 组装
    notebook = combine(notecover,paper,title)
    # 定位
    notebook = translate(l_table/3-b_note/2,-l_note/2,h_table) * rotation(Vec3(0,1,0),0) * notebook

    check_in = combine(notebook,gun,table,sign)
    check_in = translate(l_table/2,b_table/2,0) * check_in
    data['登记台'] = check_in

if __name__ == "__main__":
    data = P3DData({
        '桌面长':2000,
        '桌面宽':800,
        '桌面厚':200,
        '桌子高':1200,

        '场布类型':'防疫',
        '构件类型':'器具',
        '构件名称':'登记台',
    })
    data.set_view(1,1)
    data.setup('登记台',show=True)

    data.setup('桌面长',obvious = True , readonly = False , group = '桌子参数')
    data.setup('桌面宽',obvious = True , readonly = False , group = '桌子参数')
    data.setup('桌面厚',obvious = False , readonly = True , group = '桌子参数')
    data.setup('桌子高',obvious = True , readonly = False , group = '桌子参数')
    data.setup('场布类型',obvious = True , readonly = True , group = '构件分类')
    data.setup('构件类型',obvious = True , readonly = True , group = '构件分类')
    data.setup('构件名称',obvious=True)


    data['replace'] = check_in_construct
    check_in_construct(data)
    launchData(data)
