import pyp3d as p3d
from math import sin
from math import cos
from math import sqrt
def mf(data:p3d.P3DData)->None:
# 灭火器
    red = (0.8,0.1,0.1,1)
    gra = (0.5,0.5,0.5,1)
    zhu = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,465),100,100).color(red)
    bottom = p3d.TorusPipe(p3d.Vec3(0,0,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),95,5,p3d.pi*2)
    zhu = p3d.combine(zhu,bottom).color(red)
    r = 105
    zd = p3d.Sphere(p3d.Vec3(0,0,465-sqrt(r*r-10000)),r)
    s = p3d.Box(p3d.Vec3(-r,-r,0), p3d.Vec3(-r,-r,465),\
         p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),\
              2*r, 2*r, 2*r, 2*r)
    zd = p3d.substract(zd,s).color(red)
    top = 465-sqrt(r*r-10000)+r
    top1 = p3d.Cone(p3d.Vec3(0,0,top-10),p3d.Vec3(0,0,top+12),20,20).color(red)
    top2 = p3d.TorusPipe(p3d.Vec3(0,0,top+8),\
        p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),\
            20,4,p3d.pi*2).color(gra)
    top3 = p3d.Cone(p3d.Vec3(0,0,top+23),p3d.Vec3(0,0,top+12),16,16).color(gra)
    
    
    a = p3d.Cone(p3d.Vec3(3,-13,top+38),p3d.Vec3(3,13,top+38),21,21)
    b = p3d.Cone(p3d.Vec3(-17,-13,top+55),p3d.Vec3(-17,13,top+55),8,8)
    c = p3d.Extrusion([p3d.Vec3(-21,-13,top+62),p3d.Vec3(61,-13,top+104),p3d.Vec3(74,-13,top+109),\
        p3d.Vec3(95,-13,top+112),p3d.Vec3(111,-13,top+110),p3d.Vec3(95,-13,top+105),\
            p3d.Vec3(61,-13,top+93),p3d.Vec3(27,-13,top+74),p3d.Vec3(26,-13,top+68),\
                p3d.Vec3(37,-13,top+50),p3d.Vec3(51,-13,top+49),p3d.Vec3(72,-13,top+44),\
                    p3d.Vec3(88,-13,top+39),p3d.Vec3(108,-13,top+28),p3d.Vec3(125,-13,top+15),\
                        p3d.Vec3(118,-13,top+14),p3d.Vec3(98,-13,top+26),p3d.Vec3(80,-13,top+33),\
                            p3d.Vec3(58,-13,top+38),p3d.Vec3(25,-13,top+38)], p3d.Vec3(0,26,0))
    top4 = p3d.combine(a,b,c).color(gra)
    top5 = p3d.Cone(p3d.Vec3(0,-30,top+37),p3d.Vec3(0,-24,top+37),25,25)
    top5_ = p3d.Cone(p3d.Vec3(0,-30,top+37),p3d.Vec3(0,-27,top+37),20,20)
    top5 = p3d.substract(top5,top5_)
    top5_ = p3d.Cone(p3d.Vec3(0, 40,top+37),p3d.Vec3(0,-24,top+37),10,10)
    top5 = p3d.combine(top5,top5_).color(gra)
    top6 = p3d.Cone(p3d.Vec3(-16,-17,top+56),p3d.Vec3(-16,17,top+56),2,2).color(gra)
    top7 = p3d.Cone(p3d.Vec3(26,-20,top+55),p3d.Vec3(26,0,top+55),1,1).color(gra)
    top7_ = p3d.TorusPipe(p3d.Vec3(26,20,top+55),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),8,1,p3d.pi*2)
    top7 = p3d.combine(top7,top7_).color(gra)
    

    pipe1 = p3d.Cone(p3d.Vec3(0,0,top+62),p3d.Vec3(-49,0,top+62),9,9).color(gra)
    pipe2 = p3d.TorusPipe(p3d.Vec3(-23,0,top+62),p3d.Vec3(0,1,0),p3d.Vec3(0,0,1),8,5,p3d.pi*2)
    pipe3 = p3d.FilletPipe([p3d.Vec3(-49,0,top+62),p3d.Vec3(-80,0,top+62),p3d.Vec3(-125,0,top),\
        p3d.Vec3(-153,0,top-105), p3d.Vec3(-121,0,300),p3d.Vec3(-148,0,200)], \
            (0,50,100,350,300,0), 9)
    pipe3 = p3d.translation(p3d.Vec3(15,0,0))*pipe3
    c_x = 1
    pipe4 = p3d.Cone(p3d.Vec3(15-148-c_x,0,200-4),p3d.Vec3(15-148,0,200),10,10).color(gra)
    pipe5 = p3d.Cone(p3d.Vec3(15-148-c_x*3,0,200-4*3),p3d.Vec3(15-148,0,200),10,9).color(gra)
    pipe6 = p3d.Cone(p3d.Vec3(15-148-c_x*5,0,200-4*5),p3d.Vec3(15-148-c_x*3,0,200-4*3),12,11).color(gra)
    pipe7 = p3d.Cone(p3d.Vec3(15-148-c_x*8,0,200-4*8),p3d.Vec3(15-148-c_x*5,0,200-4*5),10.5,12).color(gra)
    pipe8 = p3d.Cone(p3d.Vec3(15-148-c_x*15,0,200-4*15),p3d.Vec3(15-148-c_x*8,0,200-4*8),12,10.5).color(gra)
    pipe9 = p3d.Cone(p3d.Vec3(15-148-c_x*16,0,200-4*16),p3d.Vec3(15-148-c_x*15,0,200-4*15),13,13).color(gra)
    
    pipe = p3d.translation(p3d.Vec3(0,0,-25))*(p3d.combine(pipe1,pipe2,pipe3,pipe4,pipe5,pipe6,pipe7,pipe8,pipe9).color(gra))
    
    yao = p3d.TorusPipe(p3d.Vec3(0,0,200),p3d.Vec3(-1,0,0),p3d.Vec3(0,1,0),100,6,p3d.pi*2)
    yao_1 = p3d.FilletPipe([p3d.Vec3(-121,0,200),p3d.Vec3(-110,9,200),\
        p3d.Vec3(-100,20,200),], \
            (0,50,0), 3)
    yao_2 = p3d.FilletPipe([p3d.Vec3(-121,0,200),p3d.Vec3(-110,-9,200),\
        p3d.Vec3(-100,-20,200)], \
            (0,3,0), 3)
    yao = p3d.combine(yao,yao_1,yao_2).color(gra)
    top = p3d.combine(top1,top2,top3,top4,top5,top6,top7)
    
    zd = p3d.combine(zd,top,pipe,yao)

    mhq = p3d.combine(zd,zhu)

    
# 柜子
    h = data['箱体高度']
    h_li = data['箱体离地高度']
    b = data['箱体宽度']
    box = p3d.Box(p3d.Vec3(-b/2,-120,0), p3d.Vec3(-b/2,-120,h), \
        p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), \
            b, 240, b, 240)
    box_ = p3d.Box(p3d.Vec3(-b/2+100,-120,100), p3d.Vec3(-b/2+100,-120,h-100), \
        p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), \
            b-200, 220, b-200, 220)
    box = p3d.substract(box,box_)

    box_ = p3d.Box(p3d.Vec3(-b/2+50,-120,50), p3d.Vec3(-b/2+50,-120,h-50), \
        p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), \
            b-100, 20, b-100, 20)
    

    hole = p3d.Box(p3d.Vec3(-b/2+100,-120,100), p3d.Vec3(-b/2+100,-120,h-100), \
        p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), \
            b-200, 20, b-200, 20).color(0.9,0.9,0.9,0.3)
    box_ = p3d.substract(box_,hole)
    box = p3d.substract(box,box_)
    box = p3d.combine(box,box_).color(red)
    box = p3d.combine(box,hole)
# 生成

    mhq = p3d.combine(p3d.translation(p3d.Vec3(-110,0,5))*mhq, p3d.translation(p3d.Vec3(145,0,5))*mhq)
    data['灭火器箱']  = p3d.translation(p3d.Vec3(0,0,h_li))*(p3d.combine(mhq, box))

if __name__ == "__main__":
    data = p3d.P3DData({
        '箱体离地高度': 0,
        '箱体宽度': 650,
        '箱体高度': 900,
        '构件名称':'灭火器箱'
    })

    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('灭火器箱', show=True)
    data.setup('箱体离地高度', obvious=True, group='底面', description='h_li')
    data.setup('箱体宽度', obvious=True, group='底面', description='b')
    data.setup('箱体高度', obvious=True, group='顶面', description='h')
    data.setup('构件名称',obvious=True)
    data['replace'] = mf
    mf(data)
    p3d.launchData(data)