from pyp3d import *

class 地锚验收牌(Component):
    def __init__(self):
        Component.__init__(self)
        self['地锚验收牌'] = Attr(None, show=True)
        self['场布类型'] = Attr("被保护系统", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("验收牌", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("地锚验收牌", obvious=True, group="构件分类")

        #地锚验收牌
        self['长度'] = Attr(600.0, obvious=True,group='地锚验收牌')
        self['厚度'] = Attr(20.0, obvious=True,group='地锚验收牌')
        self['高度'] = Attr(400, obvious = True,group='地锚验收牌')
        self['旋转角度'] = Attr(0,obvious = False)
        self['地锚验收牌X'] = Attr(0, obvious=False)
        self['地锚验收牌Y'] = Attr(0, obvious=False)
        self['地锚验收牌Z'] = Attr(0, obvious=False)

        #文字
        self['验收牌-'] = Attr("地锚、拉线验收牌", obvious=False)
        self['地锚规格-'] = Attr("地锚规格", obvious=False)
        self['拉线规格/角度-'] = Attr("拉线规格/角度", obvious=False)
        self['班组长-'] = Attr("班组长", obvious=False)
        self['班组安全员-'] = Attr("班组安全员", obvious=False)
        self['验收结论-'] = Attr("验收结论", obvious=False)
        self['地锚埋深-'] = Attr("地锚埋深", obvious=False)
        self['绳卡规格/数量-'] = Attr("绳卡规格/数量", obvious=False)
        self['班组技术员-'] = Attr("班组技术员", obvious=False)
        self['监理工程师-'] = Attr("监理工程师", obvious=False)
        self['验收时间-'] = Attr("验收时间", obvious=False)

        self['地锚规格'] = Attr("  ",  obvious=True,group='文字')
        self['拉线规格/角度'] = Attr("  ",  obvious=True,group='文字')
        self['班组长'] = Attr("  ",  obvious=True,group='文字')
        self['班组安全员'] = Attr("  ", obvious=True,group='文字')
        self['验收结论'] = Attr("  ", obvious=True,group='文字')
        self['地锚埋深'] = Attr("  ", obvious=True,group='文字')
        self['绳卡规格/数量'] = Attr("  ", obvious=True,group='文字')
        self['班组技术员'] = Attr("  ", obvious=True,group='文字')
        self['监理工程师'] = Attr("  ", obvious=True,group='文字')
        self['验收时间'] = Attr("  ", obvious=True,group='文字')
        self['公司名'] = Attr("北京京电电网维护集团有限公司", obvious=True,group='文字')



        self.replace()
    @export
    def replace(self):
        self['高度'] = self['长度']*2/3
        ysp_l = self['长度']
        ysp_t = self['厚度']
        ysp_h = self['高度']
        ysp_x = self['地锚验收牌X']
        ysp_y = self['地锚验收牌Y']
        ysp_z = self['地锚验收牌Z']
        Angle = self['旋转角度']
        text1 = self['验收牌-']
        text2 = self['地锚规格-']
        text3 = self['拉线规格/角度-']
        text4 = self['班组长-']
        text5 = self['班组安全员-']
        text6 = self['验收结论-']
        text7 = self['地锚埋深-']
        text8 = self['绳卡规格/数量-']
        text9 = self['班组技术员-']
        text10 = self['监理工程师-']
        text11 = self['验收时间-']

        text_1 = self['地锚规格']
        text_2 = self['拉线规格/角度']
        text_3 = self['班组长']
        text_4 = self['班组安全员']
        text_5 = self['验收结论']
        text_6 = self['地锚埋深']
        text_7 = self['绳卡规格/数量']
        text_8 = self['班组技术员']
        text_9 = self['监理工程师']
        text_10 = self['验收时间']
        gsm = self['公司名']
        number=len(gsm)
        # print(number)

        #验收牌
        地锚验收牌 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(ysp_l,ysp_t,ysp_h) * Cube().color(225/255,225/255,225/255,1)
        剪切面 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(ysp_l,1,ysp_h*3/4) * Cube().color(48/255,128/255,20/255,1)
        地锚验收牌绿面 = translate(ysp_x,ysp_y,ysp_z+ysp_h/8) * rotation(math.pi/180 * Angle) * scale(ysp_l,1,ysp_h*250/400) * Cube().color(48/255,128/255,20/255,1)
        地锚验收牌 = (地锚验收牌-剪切面).color(225/255,225/255,225/255,1)

        白线横 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(ysp_l,2,2) * Cube().color(225/255,225/255,225/255,1)
        白线横1 = translate(Vec3(0,-2,ysp_h*50/400+ysp_h*250/400/5))*白线横
        白线横2 = translate(Vec3(0,-2,ysp_h*50/400+ysp_h*250*2/400/5))*白线横
        白线横3 = translate(Vec3(0,-2,ysp_h*50/400+ysp_h*250*3/400/5))*白线横
        白线横4 = translate(Vec3(0,-2,ysp_h*50/400+ysp_h*250*4/400/5))*白线横
        

        白线竖 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(2,2,ysp_h*250/400) * Cube().color(225/255,225/255,225/255,1)
        白线竖 = translate(Vec3(0,0,ysp_h*50/400))*白线竖
        白线竖1 = translate(Vec3(ysp_l/4,-2,0))*白线竖
        白线竖2 = translate(Vec3(ysp_l/4*2,-2,0))*白线竖
        白线竖3 = translate(Vec3(ysp_l/4*3,-2,0))*白线竖

        #白块 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(2,2,2) * Cube().color(225/255,225/255,225/255,1)
        #白块 = translate(Vec3(ysp_l/4,0,ysp_h*50/400+ysp_h*250/400/5))*白块

        白线 = combine(白线横1,白线横2,白线横3,白线横4,白线竖1,白线竖2,白线竖3)
        
        白面 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(ysp_l*9/40,-1,ysp_h*10/100) * Cube().color(225/255,225/255,225/255,1)
        白面1 = translate(Vec3(ysp_l/4+ysp_l/80+1,0,ysp_h*50/400+(ysp_h*250/400/5-ysp_h*10/100)/2))*白面
        白面2 = translate(Vec3(ysp_l/4+ysp_l/80+1,0,ysp_h*50/400+(ysp_h*250/400/5-ysp_h*10/100)/2+ysp_h*250/400/5+1))*白面
        白面3 = translate(Vec3(ysp_l/4+ysp_l/80+1,0,ysp_h*50/400+(ysp_h*250/400/5-ysp_h*10/100)/2+ysp_h*250/400/5+1+ysp_h*250/400/5))*白面
        白面4 = translate(Vec3(ysp_l/4+ysp_l/80+1,0,ysp_h*50/400+(ysp_h*250/400/5-ysp_h*10/100)/2+ysp_h*250/400/5+1+ysp_h*250/400/5+ysp_h*250/400/5))*白面
        白面5 = translate(Vec3(ysp_l/4+ysp_l/80+1,0,ysp_h*50/400+(ysp_h*250/400/5-ysp_h*10/100)/2+ysp_h*250/400/5+ysp_h*250/400/5+ysp_h*250/400/5+ysp_h*250/400/5+1))*白面
        
        白面a = combine(白面1,白面2,白面3,白面4,白面5)
        白面b = translate(Vec3(ysp_l/4+ysp_l/4,0,0))*白面a
        
        #文字
        验收牌= translate(ysp_l/7,-1,ysp_h*82/100)*rotation(Vec3(1,0,0),pi/2)*Text(text1,ysp_l/15,ysp_h/10).color(48/255,128/255,20/255,1)
        地锚规格 = translate(ysp_l/30,-1,8+ysp_h*50/400+((ysp_h*250/400-8)*4/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text2,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)
        拉线规格角度 = translate(ysp_l/60,-1,6+ysp_h*50/400+((ysp_h*250/400-8)*3/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text3,ysp_l/40,ysp_h/20).color(255/255,215/255,0,1)
        班组长 = translate(ysp_l/19,-1,4+ysp_h*50/400+((ysp_h*250/400-8)*2/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text4,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)
        班组安全员 = translate(ysp_l/70,-1,2+ysp_h*50/400+((ysp_h*250/400-8)/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text5,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)
        验收结论 = translate(ysp_l/30,-1,ysp_h*50/400+((ysp_h*250/400-8)/5-ysp_h/20)/2)*rotation(Vec3(1,0,0),pi/2)*Text(text6,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)
        地锚埋深 = translate(ysp_l/30+ysp_l/2,-1,8+ysp_h*50/400+((ysp_h*250/400-8)*4/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text7,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)
        绳卡规格数量 = translate(ysp_l/60+ysp_l/2,-1,6+ysp_h*50/400+((ysp_h*250/400-8)*3/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text8,ysp_l/40,ysp_h/20).color(255/255,215/255,0,1)
        班组技术员 = translate(ysp_l/70+ysp_l/2,-1,4+ysp_h*50/400+((ysp_h*250/400-8)*2/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text9,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)
        监理工程师 = translate(ysp_l/70+ysp_l/2,-1,2+ysp_h*50/400+((ysp_h*250/400-8)/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text10,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)
        验收时间 = translate(ysp_l/30+ysp_l/2,-1,ysp_h*50/400+((ysp_h*250/400-8)/5-ysp_h/20)/2)*rotation(Vec3(1,0,0),pi/2)*Text(text11,ysp_l/30,ysp_h/20).color(255/255,215/255,0,1)

        文字固定 = combine(验收牌,地锚规格,拉线规格角度,班组长,班组安全员,验收结论,地锚埋深,绳卡规格数量,班组技术员,监理工程师,验收时间)
        

        地锚规格2 = translate(ysp_l/30+ysp_l/4,-2,8+ysp_h*50/400+((ysp_h*250/400-8)*4/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_1,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        拉线规格角度2 = translate(ysp_l/30+ysp_l/4,-2,6+ysp_h*50/400+((ysp_h*250/400-8)*3/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_2,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        班组长2 = translate(ysp_l/30+ysp_l/4,-2,4+ysp_h*50/400+((ysp_h*250/400-8)*2/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_3,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        班组安全员2 = translate(ysp_l/30+ysp_l/4,-2,2+ysp_h*50/400+((ysp_h*250/400-8)/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_4,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        验收结论2 = translate(ysp_l/30+ysp_l/4,-2,ysp_h*50/400+((ysp_h*250/400-8)/5-ysp_h/20)/2)*rotation(Vec3(1,0,0),pi/2)*Text(text_5,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        地锚埋深2 = translate(ysp_l/30+ysp_l/2+ysp_l/4,-2,8+ysp_h*50/400+((ysp_h*250/400-8)*4/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_6,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        绳卡规格数量2 = translate(ysp_l/30+ysp_l/2+ysp_l/4,-2,6+ysp_h*50/400+((ysp_h*250/400-8)*3/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_7,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        班组技术员2 = translate(ysp_l/30+ysp_l/2+ysp_l/4,-2,4+ysp_h*50/400+((ysp_h*250/400-8)*2/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_8,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        监理工程师2 = translate(ysp_l/30+ysp_l/2+ysp_l/4,-2,2+ysp_h*50/400+((ysp_h*250/400-8)/5+((ysp_h*250/400-8)/5-ysp_h/20)/2))*rotation(Vec3(1,0,0),pi/2)*Text(text_9,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        验收时间2 = translate(ysp_l/30+ysp_l/2+ysp_l/4,-2,ysp_h*50/400+((ysp_h*250/400-8)/5-ysp_h/20)/2)*rotation(Vec3(1,0,0),pi/2)*Text(text_10,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)

        公司名 = translate(ysp_l-ysp_l/30*number*3/2,-1,ysp_h/25)*rotation(Vec3(1,0,0),pi/2)*Text(gsm,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)

        文字可变 = combine(地锚规格2,监理工程师2,验收时间2,拉线规格角度2,班组技术员2,绳卡规格数量2,班组长2,班组安全员2,验收结论2,地锚埋深2,公司名)



        self['地锚验收牌']=combine(地锚验收牌,地锚验收牌绿面,白线,白面a,白面b,文字固定,文字可变)
        

if __name__ == "__main__":
    place(地锚验收牌())