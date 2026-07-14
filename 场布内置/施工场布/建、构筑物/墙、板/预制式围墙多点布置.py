from math import sqrt
import pyp3d as p3d
def Safety_fence1(data:p3d.P3DData)->None:
        L1 = data['立柱长度']
        n = data['围墙个数']
        B1 = data['立柱宽度']
        H1 = data['立柱高度']
        H2 = data['其他层柱帽高度']
        H5 = data['上层柱帽高度']
        B2 = data['第一层柱帽宽度']
        B3 = data['围墙宽度']
        H3 = data['围墙高度']
        B4 = data['围墙下部宽度']
        H4 = data['围墙下部高度']
        Elo = data['总长度']
        l_p = data['段首柱子是否显示']
        r_p = data['段尾柱子是否显示']
        l_loop = data['立柱间距']

        KeyPoint = data['关键点']
        n_loop_ = 0

        data['预制式围墙0'] = p3d.combine()

        for ix in range(len(KeyPoint)-1):   
                v12_norm = p3d.norm(KeyPoint[ix]-KeyPoint[ix+1])
                Elo =v12_norm     #长度
                if H3 < H1:           
                        H1 = H1
                        H3 = H3
                else:
                        H3 = H3
                        H1 = H3 + 200

                #立柱
                box1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H1-H2*2-H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 50, B1, 50, B1).color(1,1,1,1) 
                box2 = p3d.Box(p3d.Vec3(50,0,0), p3d.Vec3(50,0,H1-H2*2-H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L1-100, B1, L1-100, B1).color(0,0,1,1) 
                box3 = p3d.Box(p3d.Vec3(L1-50,0,0), p3d.Vec3(L1-50,0,H1-H2*2-H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 50, B1, 50, B1).color(1,1,1,1) 
                box4 = p3d.Box(p3d.Vec3(-30,-(B2-B1)/2,H1-H2*2-H5), p3d.Vec3(-30,-(B2-B1)/2,H1-H2-H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L1+60, B2, L1+60, B2).color(1,1,1,1) 
                box5 = p3d.Box(p3d.Vec3(-60,-(B2-B1)/2-30,H1-H2-H5), p3d.Vec3(-60,-(B2-B1)/2-30,H1-H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L1+120, B2+60, L1+120, B2+60).color(1,1,1,1) 
                box6 = p3d.Box(p3d.Vec3(-90,-(B2-B1)/2-60,H1-H5), p3d.Vec3(-90,-(B2-B1)/2-60,H1), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L1+180, B2+120, L1+180, B2+120).color(1,1,1,1) 
                lz0 = p3d.combine(box1,box2,box3,box4,box5,box6)
                # 段首柱
                lz = p3d.translation(p3d.Vec3(-L1/2,-B1/2,0)) * lz0
                # 段尾柱
                box12 = p3d.translation(p3d.Vec3(l_loop,0,0)) * lz
                # p3d.create_geometry(box12)
                #墙下
                box7 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1, B4, l_loop-L1, B4).color(1,1,1,1)
                box8 = p3d.translation(p3d.Vec3(L1/2,(B1-B4)/2,0)) * box7
                #墙
                box9 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H3-200-H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1, B3,l_loop-L1, B3).color(1,1,1,1)
                box10 = p3d.translation(p3d.Vec3(L1/2,(B1-B3)/2,H4)) * box9
                #墙上
                box11 = p3d.Box(p3d.Vec3(L1/2,(B1-(B3+100))/2,H3-200), p3d.Vec3(L1/2,(B1-(B3+100))/2,H3-150), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1,B3+100, l_loop-L1, B3+100).color(1,1,1,1)
                # Ellipse1 = p3d.Ellipse(p3d.Vec3(0,-100,0), p3d.Vec3(0,100,0), p3d.Vec3(0,0,100), 0, p3d.pi/4)
                # LineString1 = p3d.LineString([p3d.Vec3(0,-100+100/sqrt(2),100/sqrt(2)),p3d.Vec3(0,-100+100/sqrt(2)+B3+100,100/sqrt(2))])
                # Ellipse2 = p3d.Ellipse(p3d.Vec3(0,B3+100+100,0), p3d.Vec3(0,-100,0), p3d.Vec3(0,0,100), p3d.pi/4, -p3d.pi/4)
                # LineString2 = p3d.LineString([p3d.Vec3(0,B3+100,0),p3d.Vec3(0,0,0)])
                # OuterContour = p3d.ContourLine([Ellipse1,LineString1,Ellipse2,LineString2])
                # extrusionPlus1 = p3d.ExtrusionPlus([OuterContour],p3d.Vec3(l_loop-L1,0,0)).color(1,1,1,1)
                # a2 = p3d.translation(p3d.Vec3(L1/2,(B1-(B3+100))/2,H3-150)) * extrusionPlus1
                WallTopBox = p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,-50,100/sqrt(2)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),l_loop-L1,B3+100, l_loop-L1, B3+200 )
                a2 = p3d.translation(p3d.Vec3(L1/2,(B1-(B3+100))/2,H3-150)) * WallTopBox
                
                wall0 = p3d.combine(box8,box10,box11,a2)
                wall =  p3d.translation(p3d.Vec3(0,-B1/2,0)) * wall0


                # 栏-墙单元循环
                loop = p3d.combine(box12,wall)
                loop_int = p3d.Array(loop)
                n_loop = int(Elo/l_loop)
                for point in range(1,n_loop):
                        loop_int.append(p3d.translation(point*l_loop,0,0))
                # ##################################################################
                # 段首补充
                #墙下
                box7_head = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1/2, B4, l_loop-L1/2, B4).color(1,1,1,1)
                box8_head = p3d.translation(p3d.Vec3(0,(B1-B4)/2,0)) * box7_head
                #墙
                box9_head = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H3-200-H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1/2, B3,l_loop-L1/2, B3).color(1,1,1,1)
                box10_head = p3d.translation(p3d.Vec3(0,(B1-B3)/2,H4)) * box9_head
                #墙上
                box11_head = p3d.Box(p3d.Vec3(0,(B1-(B3+100))/2,H3-200), p3d.Vec3(0,(B1-(B3+100))/2,H3-150), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1/2,B3+100, l_loop-L1/2, B3+100).color(1,1,1,1)

                # extrusionPlus1_head = p3d.ExtrusionPlus([OuterContour],p3d.Vec3(l_loop-L1/2,0,0)).color(1,1,1,1)
                # a2_head = p3d.translation(p3d.Vec3(0,(B1-(B3+100))/2,H3-150)) * extrusionPlus1_head
                WallTopBox = p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,-50,100/sqrt(2)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),l_loop-L1/2,B3+100, l_loop-L1/2, B3+200 )
                a2_head = p3d.translation(p3d.Vec3(0,(B1-(B3+100))/2,H3-150)) * WallTopBox
                wall_head = p3d.translation(p3d.Vec3(0,-B1/2,0)) * p3d.combine(box8_head,box10_head,box11_head,a2_head)
                wall_head = p3d.combine(wall_head,box12)
                # 段尾补充
                l_tail = Elo-n_loop*l_loop-L1/2
                wall_tail = p3d.combine()
                if l_tail>0:
                        #墙下
                        box7_tail = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_tail, B4, l_tail, B4).color(1,1,1,1)
                        box8_tail = p3d.translation(p3d.Vec3(0,(B1-B4)/2,0)) * box7_tail
                        #墙
                        box9_tail = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H3-200-H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_tail, B3,l_tail, B3).color(1,1,1,1)
                        box10_tail = p3d.translation(p3d.Vec3(0,(B1-B3)/2,H4)) * box9_tail
                        #墙上
                        box11_tail = p3d.Box(p3d.Vec3(0,(B1-(B3+100))/2,H3-200), p3d.Vec3(0,(B1-(B3+100))/2,H3-150), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_tail,B3+100, l_tail, B3+100).color(1,1,1,1)

                        # extrusionPlus1_tail = p3d.ExtrusionPlus([OuterContour],p3d.Vec3(l_tail,0,0)).color(1,1,1,1)
                        # a2_tail = p3d.translation(p3d.Vec3(0,(B1-(B3+100))/2,H3-150)) * extrusionPlus1_tail
                        WallTopBox = p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,-50,100/sqrt(2)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),l_tail,B3+100, l_tail, B3+200 )
                        a2_tail = p3d.translation(p3d.Vec3(0,(B1-(B3+100))/2,H3-150)) * WallTopBox
                        wall_tail = p3d.translation(p3d.Vec3(n_loop*l_loop+L1/2,-B1/2,0)) * p3d.combine(box8_tail,box10_tail,box11_tail,a2_tail)
                        if ix != len(KeyPoint)-2:
                                wall_tail = p3d.combine(wall_tail,p3d.translate(Elo,0,0)*lz)
                        n_loop = n_loop+1
                # 段首判断
                if l_p == '是' and ix == 0:
                        wall_head = p3d.combine(wall_head,lz)
                if r_p == '是' and ix == len(KeyPoint)-2:
                        wall_tail = p3d.combine(wall_tail,p3d.translation(p3d.Vec3(Elo,0,0)) * lz)

                fence_final = p3d.combine(wall_head,wall_tail,loop_int)
                data['预制式围墙0'].append(p3d.translation(KeyPoint[ix]) * p3d.rotation_to(KeyPoint[ix+1]-KeyPoint[ix]) * fence_final)
                n_loop_ = n_loop_ + n_loop   # 计数

                data['围墙长度'] = Elo/n
                data['围墙下部长度'] = data['围墙长度']
                data['围墙个数'] = n_loop_
                data['第一层柱帽长度'] = L1+120
                data['第二层柱帽长度'] = L1+240
                data['第三层柱帽长度'] = L1+360
                data['第二层柱帽宽度'] = B2+120
                data['第三层柱帽宽度'] = B2+240
                data['围墙红色值'] = 255
                data['围墙绿色值'] = 255
                data['围墙蓝色值'] = 255
                data['围墙颜色透明度'] = 1
                data['柱帽红色值'] = 255
                data['柱帽绿色值'] = 255
                data['柱帽蓝色值'] = 255
                data['柱帽颜色透明度'] = 1
                data['立柱红色值'] = 0
                data['立柱绿色值'] = 0
                data['立柱蓝色值'] = 255
                data['立柱颜色透明度'] = 1
                data['场布分类'] = '建/构筑物'
                data['构件类型'] = '建筑墙'
            
if __name__ == "__main__":
    data = p3d.P3DData({
        '立柱长度':410,
        '立柱宽度':600,
        '围墙个数':6,
        '立柱高度':2800,
        '立柱间距' : 1950,

        '其他层柱帽高度':50,
        '上层柱帽高度':100,
        '第一层柱帽宽度':600,
        '围墙高度':2500,
        '总长度': 6000,
        '围墙宽度':200,
        '围墙下部高度':350,
        '围墙下部宽度':300,
        '段首柱子是否显示':'是',
        '段尾柱子是否显示':'是',
        '构件名称':'预制式围墙多点布置',
        '关键点':[p3d.Vec3(0,0,0),p3d.Vec3(10000,500,0),p3d.Vec3(15000,30000,0),p3d.Vec3(0,0,0)],
        })
    data.set_view(1,1)
    data.setup('预制式围墙0', show=True)
    
    data.setup('场布分类',obvious=True,readonly = True, group='类型参数')
    data.setup('构件类型',obvious=True,readonly = True, group='类型参数')
    data.setup('立柱高度',obvious=True, group='立柱参数')
    data.setup('立柱宽度',obvious=True, group='立柱参数')
    data.setup('立柱长度',obvious=True, group='立柱参数')
    data.setup('段首柱子是否显示', obvious=True, group='立柱参数', description='[是]或[否]')
    data.setup('段尾柱子是否显示', obvious=True, group='立柱参数', description='[是]或[否]')
    data.setup('第一层柱帽宽度',obvious=True, group='柱帽参数')
    data.setup('其他层柱帽高度',obvious=True, group='柱帽参数')
    data.setup('上层柱帽高度',obvious=True, group='柱帽参数')
    data.setup('第一层柱帽长度',obvious=True,readonly = True, group='柱帽参数')
    data.setup('第二层柱帽长度',obvious=True,readonly = True, group='柱帽参数')
    data.setup('第三层柱帽长度',obvious=True,readonly = True, group='柱帽参数')
    data.setup('第二层柱帽宽度',obvious=True,readonly = True, group='柱帽参数')
    data.setup('第三层柱帽宽度',obvious=True,readonly = True, group='柱帽参数')
    data.setup('围墙个数',obvious=True, group='围墙参数')
    data.setup('围墙宽度',obvious=True, group='围墙参数')
    data.setup('围墙高度',obvious=True, group='围墙参数')
    data.setup('围墙长度',obvious=True,readonly = True, group='围墙参数')
    data.setup('立柱间距',obvious=True, group='围墙参数')

    data.setup('围墙下部宽度',obvious=True, group='围墙下部参数')
    data.setup('围墙下部高度',obvious=True, group='围墙下部参数')
    data.setup('围墙下部长度',obvious=True,readonly = True, group='围墙下部参数')

    data.setup('总长度', obvious=True,group='几何尺寸')

    data.setup('围墙红色值',obvious=True,readonly = True, group='围墙颜色')
    data.setup('围墙绿色值',obvious=True,readonly = True, group='围墙颜色')
    data.setup('围墙蓝色值',obvious=True,readonly = True, group='围墙颜色')
    data.setup('围墙颜色透明度',obvious=True,readonly = True, group='围墙颜色')
    data.setup('柱帽红色值',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('柱帽蓝色值',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('柱帽绿色值',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('柱帽颜色透明度',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('立柱红色值',obvious=True,readonly = True, group='立柱颜色')
    data.setup('立柱绿色值',obvious=True,readonly = True, group='立柱颜色')
    data.setup('立柱蓝色值',obvious=True,readonly = True, group='立柱颜色')
    data.setup('立柱颜色透明度',obvious=True,readonly = True, group='立柱颜色')

    data.setup('构件名称',obvious=True)
    
    data['replace'] = Safety_fence1
    Safety_fence1(data)
    p3d.MultiPointPlace.MultiPointFunction(data, '关键点')
    p3d.launchData(data)