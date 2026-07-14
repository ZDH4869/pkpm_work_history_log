from math import ceil
from pyp3d import *
#1.0模型参考现场实际工作搭设建模，发现不利于快速使用模型。
#2.1修改模型搭设模式为直接输入长宽高，以方便快速使模型并与现场实际数据相同。
#2.2修改了跨越架在个别参数下，边框无小横杆的问题。
#2.3增加了封顶杆，让模型更贴近现场实际形状。
#2.4增加了模型比例和旋转角度，以帮助在深化应用时可以更快速的布置场景。
#2.5增加了杉篙使用数量的计算，帮助跨越架搭设施工对材料的掌控。优化了模型参数表达方式。


def kyjds(data):
    # 跨越架参数
    #X轴为横向Y轴为纵向Z轴为高度    
    data['模型比例']
    XZJD=data['旋转角度(度)']
    R=data['杉篙半径(mm)']*data['模型比例']
    H=data['杉篙长度(mm)']*data['模型比例']
    HJ=data['搭接长度(mm)']*data['模型比例']
    KYJ_L=data['跨越架长度(mm)']*data['模型比例']
    KYJ_H=data['跨越架高度(mm)']*data['模型比例']  
    KYJ_W=data['跨越架宽度(mm)']*data['模型比例']
    LG_ZDS=data['立杆最大间距(mm)']*data['模型比例']
    DHG_ZDS=data['大横杆最大间距(mm)']*data['模型比例']
    KYJFD_H=data['封顶杆高度']=DHG_ZDS*2
    KYJZT_H=data['跨越架主体高度']=KYJ_H-KYJFD_H  
    LG_HXS=data['立杆横向间距']=KYJ_W/ceil(KYJ_W/LG_ZDS)
    LG_ZXS=data['立杆纵向间距']=KYJ_L/ceil(KYJ_L/LG_ZDS)
    DHG_S=data['大横杆间距']=KYJZT_H/ceil(KYJZT_H/DHG_ZDS)
    XHGSP_S=data['小横杆水平间距']=LG_ZXS*2
    XHGCZ_S=data['小横杆垂直间距']=DHG_S*2
    LGH_N=data['立杆横向排数']=ceil(KYJ_W/LG_ZDS)+1
    LGZ_N=data['立杆纵向排数']=ceil(KYJ_L/LG_ZDS)+1
    DHGG_N=data['大横杆高度排数']=ceil(KYJZT_H/DHG_ZDS)+1
    XHGSP_N=data['小横杆纵向排数（水平）']=ceil(KYJ_L/XHGSP_S)
    XHGCZ_N=data['小横杆高度排数（垂直）']=ceil(KYJZT_H/XHGCZ_S)
    data['杉篙数量']=((ceil(KYJ_H/(H-HJ)))*LGH_N*LGZ_N)+((ceil(KYJ_L/(H-HJ)))*DHGG_N*LGZ_N)+((ceil(KYJ_W/(H-HJ)))*(XHGSP_N+1)*(XHGCZ_N+1))
    #备用数据，留着以后优化跨越架使用
    # LGG_N=data['立杆高度排数']
    # DHGH_N=data['大横杆横向排数']
    # DHGZ_N=data['大横杆纵向排数']
    # XHGH_N=data['小横杆横向排数']
    
    
    
    # 设立原点杆
    原点立杆 = Cone(Vec3(0,0,0),Vec3(0,0,KYJZT_H),R).color(192/255, 192/255, 192/255, 1)
    原点大横杆 = Cone(Vec3(0,0,0),Vec3(0,KYJ_L,0),R).color(192/255, 192/255, 192/255, 1)
    原点小横杆 = Cone(Vec3(0,0,0),Vec3(KYJ_W,0,0),R).color(192/255, 192/255, 192/255, 1)
    对角小横杆 = Cone(Vec3(0,KYJ_L,KYJZT_H),Vec3(KYJ_W,KYJ_L,KYJZT_H),R).color(192/255, 192/255, 192/255, 1)
    封顶杆立杆 = Cone(Vec3(0,0,KYJZT_H),Vec3(0,0,KYJ_H),R).color(192/255, 192/255, 192/255, 1)
    封顶杆小横杆 = Cone(Vec3(0,0,KYJZT_H+(KYJFD_H/2)),Vec3(LG_HXS,0,KYJZT_H+(KYJFD_H/2)),R).color(192/255, 192/255, 192/255, 1)
    封顶杆小立杆 = Cone(Vec3(LG_HXS*2,0,KYJZT_H),Vec3(LG_HXS*2,0,KYJZT_H+(KYJFD_H/2)),R).color(192/255, 192/255, 192/255, 1)
    封顶杆斜杆 = Cone(Vec3(LG_HXS*3,0,KYJZT_H),Vec3(LG_HXS,0,KYJ_H),R).color(192/255, 192/255, 192/255, 1)
    


    #跨越架主体
    data['立杆排布'] = []
    立杆横向排布_s = linspace(Vec3(0,0,0),Vec3(KYJ_W,0,0),LGH_N)
    立杆纵向排布_s = linspace(Vec3(0,0,0),Vec3(0,KYJ_L,0),LGZ_N)    
    for 立杆横向排布 in 立杆横向排布_s:
        for 立杆纵向排布 in 立杆纵向排布_s:            
            data['立杆排布'].append(translation(立杆横向排布+立杆纵向排布)*原点立杆)
    data['大横杆排布'] = []
    大横杆横向排布_s = linspace(Vec3(0,0,0),Vec3(KYJ_W,0,0),LGH_N)    
    大横杆高度排布_s = linspace(Vec3(0,0,0),Vec3(0,0,KYJZT_H),DHGG_N)
    for 大横杆横向排布 in 大横杆横向排布_s:
        for 大横杆高度排布 in 大横杆高度排布_s:
            data['大横杆排布'].append(translation(大横杆横向排布+大横杆高度排布)*原点大横杆)
    data['小横杆排布'] = []    
    小横杆纵向排布_s = linspace(Vec3(0,0,0),Vec3(0,(XHGSP_N-1)*XHGSP_S,0),XHGSP_N)
    小横杆高度排布_s = linspace(Vec3(0,0,0),Vec3(0,0,(XHGCZ_N-1)*XHGCZ_S),XHGCZ_N)
    for 小横杆纵向排布 in 小横杆纵向排布_s:
        for 小横杆高度排布 in 小横杆高度排布_s:
            data['小横杆排布'].append(translation(小横杆纵向排布+小横杆高度排布)*原点小横杆)


    #封边小横杆
    data['封边小横杆纵向排布'] = []    
    封边小横杆纵向排布_s = linspace(Vec3(0,0,KYJZT_H),Vec3(0,(XHGSP_N-1)*XHGSP_S,KYJZT_H),XHGSP_N)
    for 封边小横杆纵向排布 in 封边小横杆纵向排布_s:
        data['封边小横杆纵向排布'].append(translation(封边小横杆纵向排布)*原点小横杆) 
    data['封边小横杆高度排布'] = [] 
    封边小横杆高度排布_s = linspace(Vec3(0,KYJ_L,0),Vec3(0,KYJ_L,(XHGCZ_N-1)*XHGCZ_S),XHGCZ_N)
    for 封边小横杆高度排布 in 封边小横杆高度排布_s:
        data['封边小横杆高度排布'].append(translation(封边小横杆高度排布)*原点小横杆)
    data['对角小横杆'] = 对角小横杆
    
    
    #封顶架
    data['封顶杆立杆排布'] = []
    封顶杆立杆横向排布_s = linspace(Vec3(0,0,0),Vec3(LG_HXS,0,0),2)
    封顶杆立杆纵向排布_s = linspace(Vec3(0,0,0),Vec3(0,KYJ_L,0),LGZ_N)    
    for 封顶杆立杆横向排布 in 封顶杆立杆横向排布_s:
        for 封顶杆立杆纵向排布 in 封顶杆立杆纵向排布_s:            
            data['封顶杆立杆排布'].append(translation(封顶杆立杆横向排布+封顶杆立杆纵向排布)*封顶杆立杆)

    data['封顶杆小立杆排布'] = []
    封顶杆小立杆纵向排布_s = linspace(Vec3(0,0,0),Vec3(0,KYJ_L,0),LGZ_N)    
    for 封顶杆小立杆纵向排布 in 封顶杆小立杆纵向排布_s:            
        data['封顶杆小立杆排布'].append(translation(封顶杆小立杆纵向排布)*封顶杆小立杆)

    data['封顶杆小横杆排布'] = []
    封顶杆小横杆横向排布_s = linspace(Vec3(0,0,0),Vec3(LG_HXS,0,0),2)
    封顶杆小横杆纵向排布_s = linspace(Vec3(0,0,0),Vec3(0,KYJ_L,0),LGZ_N)    
    for 封顶杆小横杆横向排布 in 封顶杆小横杆横向排布_s:
        for 封顶杆小横杆纵向排布 in 封顶杆小横杆纵向排布_s:            
            data['封顶杆小横杆排布'].append(translation(封顶杆小横杆横向排布+封顶杆小横杆纵向排布)*封顶杆小横杆)

    data['封顶杆小横杆排布2'] = []
    封顶杆小横杆纵向排布2_s = linspace(Vec3(0,0,(KYJFD_H/2)),Vec3(0,KYJ_L,(KYJFD_H/2)),LGZ_N)    
    for 封顶杆小横杆纵向排布2 in 封顶杆小横杆纵向排布2_s:            
        data['封顶杆小横杆排布2'].append(translation(封顶杆小横杆纵向排布2)*封顶杆小横杆)

    data['封顶杆斜杆排布'] = []
    封顶杆斜杆纵向排布_s = linspace(Vec3(0,0,0),Vec3(0,(XHGSP_N-1)*XHGSP_S,0),XHGSP_N)    
    for 封顶杆斜杆纵向排布 in 封顶杆斜杆纵向排布_s:            
        data['封顶杆斜杆排布'].append(translation(封顶杆斜杆纵向排布)*封顶杆斜杆)
    data['封顶杆斜杆最后一根'] = Cone(Vec3(LG_HXS*3,KYJ_L,KYJZT_H),Vec3(LG_HXS,KYJ_L,KYJ_H),R).color(192/255, 192/255, 192/255, 1) 

    data['封顶杆大横杆横向排布'] = []       
    封顶杆大横杆横向排布_s = linspace(Vec3(0,0,KYJ_H),Vec3(LG_HXS,0,KYJ_H),2)
    for 封顶杆大横杆横向排布 in 封顶杆大横杆横向排布_s:
        data['封顶杆大横杆横向排布'].append(translation(封顶杆大横杆横向排布)*原点大横杆)
    data['封顶杆大横杆横向排布2'] = []       
    封顶杆大横杆横向排布2_s = linspace(Vec3(0,0,KYJ_H-(KYJFD_H/2)),Vec3(LG_HXS*2,0,KYJ_H-(KYJFD_H/2)),3)
    for 封顶杆大横杆横向排布2 in 封顶杆大横杆横向排布2_s:
        data['封顶杆大横杆横向排布'].append(translation(封顶杆大横杆横向排布2)*原点大横杆)

    data['封顶杆羊角杆1'] = Cone(Vec3(0,LG_ZXS,KYJ_H-(KYJFD_H/2)),Vec3(0,-LG_ZXS,KYJ_H+(KYJFD_H/2)),R).color(192/255, 192/255, 192/255, 1)
    data['封顶杆羊角杆2'] = Cone(Vec3(0,KYJ_L-LG_ZXS,KYJ_H-(KYJFD_H/2)),Vec3(0,KYJ_L+LG_ZXS,KYJ_H+(KYJFD_H/2)),R).color(192/255, 192/255, 192/255, 1) 

    #组合跨越架
    data['跨越架']= combine(data['封顶杆羊角杆2'],data['封顶杆羊角杆1'],\
        data['立杆排布'],data['大横杆排布'],data['小横杆排布'],data['封边小横杆纵向排布'],data['封边小横杆高度排布'],data['对角小横杆'],\
        data['封顶杆立杆排布'],data['封顶杆小立杆排布'],data['封顶杆小横杆排布'],data['封顶杆小横杆排布2'],data['封顶杆斜杆排布'],\
        data['封顶杆斜杆最后一根'],data['封顶杆大横杆横向排布'],data['封顶杆大横杆横向排布2'])

    #控制跨越架旋转    
    data['跨越架'] = rotation(Vec3(0,0,1),pi*XZJD/180) * data['跨越架']



if __name__ == "__main__":
    data = P3DData({
        '模型比例': 1/10,
        '杉篙半径(mm)': 40,
        '搭接长度(mm)': 1500,
        '杉篙长度(mm)': 6000,
        '跨越架长度(mm)': 24000,
        '跨越架宽度(mm)': 6000,
        '跨越架高度(mm)': 18000, 
        '立杆最大间距(mm)': 1500,
        '大横杆最大间距(mm)':1200,
        '旋转角度(度)':0,                
        '构件名称':'盘扣式钢管跨越架'

                
    })
    
    data.set_view(-0.125*pi,-0.125*pi)
    # 输出构件
    data.setup('跨越架',  show=True)
    # 设置属性（是否可见，分组，描述）
    #模型主要参数
    data.setup('构件名称', obvious = True)
    data.setup('模型比例', obvious = True, group='比例', description='模型比例')
    data.setup('旋转角度(度)', obvious = True, group='旋转', description='旋转角度(度)')
    data.setup('杉篙半径(mm)', obvious = True, group='杉篙', description='杉篙半径(mm)')
    data.setup('跨越架长度(mm)', obvious = True, group='跨越架', description='跨越架长度(mm)')
    data.setup('跨越架宽度(mm)', obvious = True, group='跨越架', description='跨越架宽度(mm)')
    data.setup('跨越架高度(mm)', obvious = True, group='跨越架', description='跨越架高度(mm)')    
    data.setup('立杆最大间距(mm)', obvious = True, group='立杆', description='立杆最大间距(mm)')
    data.setup('大横杆最大间距(mm)', obvious = True, group='大横杆', description='大横杆最大间距(mm)')
    #模型统计参数，可以更改，只影响杉篙数量统计，对跨越架模型无影响。
    for i in ('杉篙长度(mm)', '搭接长度(mm)'):
        data.setup(i, obvious = True, group='统计参数值（可以更改，只影响杉篙数量）', description='模型统计参数，可以更改，只影响杉篙数量，对跨越架模型无影响')
    #模型统计参数，无法更改，只作为施工参考数值。
    for i in ('杉篙数量', '立杆横向排数','立杆纵向排数','大横杆高度排数','小横杆纵向排数（水平）','小横杆高度排数（垂直）' ):
        data.setup(i, obvious = True, group='统计值（无法更改，只作为施工参考数值）', description='模型统计参数，无法更改，只作为施工参考数值')
    

    #备用参数，留着以后优化使用。    
    # data.setup('小横杆水平间距', obvious = True, group='小横杆', description='小横杆水平间距')
    # data.setup('小横杆垂直间距', obvious = True, group='小横杆', description='小横杆垂直间距')  
    # data.setup('立杆高度排数', obvious = True, group='立杆', description='立杆高度排数')
    # data.setup('大横杆横向排数', obvious = True, group='大横杆', description='大横杆横向排数')
    # data.setup('大横杆纵向排数', obvious = True, group='大横杆', description='大横杆纵向排数')
    # data.setup('小横杆横向排数', obvious = True, group='小横杆', description='小横杆横向排数')
    
    # 设置replace算子
    data['replace'] = kyjds
    kyjds(data)
    launchData(data)