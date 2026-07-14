from pyp3d import *

class 跨越架验收牌(Component):
    def __init__(self):
        Component.__init__(self)
        self['跨越架验收牌'] = Attr(None, show=True)
        self['场布类型'] = Attr("被保护系统", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("验收牌", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("跨越架验收牌", obvious=True, group="构件分类")

        #跨越架验收牌
        self['长度'] = Attr(600.0, obvious=True,group='跨越架验收牌')
        self['厚度'] = Attr(20.0, obvious=True,group='跨越架验收牌')
        self['高度'] = Attr(400, obvious = True,group='跨越架验收牌')
        self['旋转角度'] = Attr(0,obvious = False)
        self['跨越架验收牌X'] = Attr(0, obvious=False)
        self['跨越架验收牌Y'] = Attr(0, obvious=False)
        self['跨越架验收牌Z'] = Attr(0, obvious=False)

        #文字
        self['验收牌'] = Attr("跨越架验收合格牌", obvious=False)
        self['使用单位-'] = Attr("使用单位：", obvious=False)
        self['使用地点-'] = Attr("使用地点：", obvious=False)
        self['使用时间-'] = Attr("使用时间：", obvious=False)
        self['责任人-'] = Attr("责任人：", obvious=False)
        self['验收人-'] = Attr("验收人：", obvious=False)
        self['验收时间-'] = Attr("验收时间：", obvious=False)

        self['使用单位'] = Attr("  ",  obvious=True,group='文字')
        self['使用地点'] = Attr("  ",  obvious=True,group='文字')
        self['使用时间'] = Attr("  ",  obvious=True,group='文字')
        self['责任人'] = Attr("  ", obvious=True,group='文字')
        self['验收人'] = Attr("  ", obvious=True,group='文字')
        self['验收时间'] = Attr("  ", obvious=True,group='文字')

        self['公司名'] = Attr("北京京电电网维护集团有限公司", obvious=True,group='文字')
        
        self.replace()
    @export
    def replace(self):
        self['高度'] = self['长度']*2/3
        ysp_l = self['长度']
        ysp_t = self['厚度']
        ysp_h = self['高度']
        ysp_x = self['跨越架验收牌X']
        ysp_y = self['跨越架验收牌Y']
        ysp_z = self['跨越架验收牌Z']
        Angle = self['旋转角度']

        text1 = self['验收牌']
        text2 = self['使用单位-']
        text3 = self['使用地点-']
        text4 = self['使用时间-']
        text5 = self['责任人-']
        text6 = self['验收人-']
        text7 = self['验收时间-']
        
        text_1 = self['使用单位']
        text_2 = self['使用地点']
        text_3 = self['使用时间']
        text_4 = self['责任人']
        text_5 = self['验收人']
        text_6 = self['验收时间']

        gsm = self['公司名']

        number=len(gsm)
        print(number)

       

        #验收牌
        跨越架验收牌 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(ysp_l,ysp_t,ysp_h) * Cube().color(225/255,225/255,225/255,1)
        剪切面 = translate(ysp_x,ysp_y,ysp_z) * rotation(math.pi/180 * Angle) * scale(ysp_l,1,ysp_h*3/4) * Cube().color(48/255,128/255,20/255,1)
        跨越架验收牌绿面 = translate(ysp_x,ysp_y,ysp_z+ysp_h/8) * rotation(math.pi/180 * Angle) * scale(ysp_l,1,ysp_h*250/400) * Cube().color(48/255,128/255,20/255,1)
        跨越架验收牌 = (跨越架验收牌-剪切面).color(225/255,225/255,225/255,1)

        #白面
        白面1 = translate(ysp_l*15/48,ysp_y,ysp_h/4) * rotation(math.pi/180 * Angle) * scale(ysp_l*7/40,-1,ysp_h*10/100) * Cube().color(225/255,225/255,225/255,1)
        白面2 = translate(ysp_l*15/48,ysp_y,ysp_h/4+ysp_h*250/400/4) * rotation(math.pi/180 * Angle) * scale(ysp_l*7/40,-1,ysp_h*10/100) * Cube().color(225/255,225/255,225/255,1)
        白面3 = translate(ysp_l*15/48,ysp_y,ysp_h/4+ysp_h*250*2/400/4) * rotation(math.pi/180 * Angle) * scale(ysp_l*7/40,-1,ysp_h*10/100) * Cube().color(225/255,225/255,225/255,1)
        白面4 = translate(ysp_l*73/96,ysp_y,ysp_h/4) * rotation(math.pi/180 * Angle) * scale(ysp_l*7/40,-1,ysp_h*10/100) * Cube().color(225/255,225/255,225/255,1)
        白面5 = translate(ysp_l*73/96,ysp_y,ysp_h/4+ysp_h*250/400/4) * rotation(math.pi/180 * Angle) * scale(ysp_l*7/40,-1,ysp_h*10/100) * Cube().color(225/255,225/255,225/255,1)
        白面6 = translate(ysp_l*73/96,ysp_y,ysp_h/4+ysp_h*250*2/400/4) * rotation(math.pi/180 * Angle) * scale(ysp_l*7/40,-1,ysp_h*10/100) * Cube().color(225/255,225/255,225/255,1)

        白面 = combine(白面1,白面2,白面3,白面4,白面5,白面6)

        #文字
        验收牌= translate(ysp_l/7,-1,ysp_h*82/100)*rotation(Vec3(1,0,0),pi/2)*Text(text1,ysp_l/15,ysp_h/10).color(48/255,128/255,20/255,1)
        使用单位 = translate(ysp_l/16,-1,ysp_h/8+ysp_h*250*3/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text2,ysp_l/30,ysp_h/20).color(225/255,225/255,225/255,1)
        使用地点 = translate(ysp_l/16,-1,ysp_h/8+ysp_h*250*2/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text3,ysp_l/30,ysp_h/20).color(225/255,225/255,225/255,1)
        使用时间 = translate(ysp_l/16,-1,ysp_h/8+ysp_h*250/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text4,ysp_l/30,ysp_h/20).color(225/255,225/255,225/255,1)
        责任人 = translate(ysp_l*11/20,-1,ysp_h/8+ysp_h*250*3/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text5,ysp_l/30,ysp_h/20).color(225/255,225/255,225/255,1)
        验收人 = translate(ysp_l*11/20,-1,ysp_h/8+ysp_h*250*2/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text6,ysp_l/30,ysp_h/20).color(225/255,225/255,225/255,1)
        验收时间 = translate(ysp_l*11/20-ysp_l/30,-1,ysp_h/8+ysp_h*250/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text7,ysp_l/30,ysp_h/20).color(225/255,225/255,225/255,1)
        
        文字固定 = combine(验收牌,使用单位,使用地点,使用时间,责任人,验收人,验收时间)
        
        公司名 = translate(ysp_l-ysp_l/30*number*3/2,-1,ysp_h/25)*rotation(Vec3(1,0,0),pi/2)*Text(gsm,ysp_l/30,ysp_h/20).color(48/255,128/255,20/255,1)
        使用单位2 = translate(ysp_l*15/48,-2,ysp_h*28/100+ysp_h*250*2/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text_1,ysp_l/45,ysp_h/30).color(48/255,128/255,20/255,1)
        使用地点2 = translate(ysp_l*15/48,-2,ysp_h*28/100+ysp_h*250/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text_2,ysp_l/45,ysp_h/30).color(48/255,128/255,20/255,1)
        使用时间2 = translate(ysp_l*15/48,-2,ysp_h*28/100)*rotation(Vec3(1,0,0),pi/2)*Text(text_3,ysp_l/45,ysp_h/30).color(48/255,128/255,20/255,1)
        责任人2 = translate(ysp_l*73/96,-1,ysp_h*28/100+ysp_h*250*2/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text_4,ysp_l/45,ysp_h/30).color(48/255,128/255,20/255,1)
        验收人2 = translate(ysp_l*73/96,-1,ysp_h*28/100+ysp_h*250/400/4)*rotation(Vec3(1,0,0),pi/2)*Text(text_5,ysp_l/45,ysp_h/30).color(48/255,128/255,20/255,1)
        验收时间2 = translate(ysp_l*73/96,-1,ysp_h*28/100)*rotation(Vec3(1,0,0),pi/2)*Text(text_6,ysp_l/45,ysp_h/30).color(48/255,128/255,20/255,1)

        文字可变 = combine(公司名,使用时间2,使用单位2,使用地点2,验收时间2,责任人2,验收人2)
        
        self['跨越架验收牌']=combine(跨越架验收牌,跨越架验收牌绿面,文字固定,文字可变,白面)

if __name__ == "__main__":
    place(跨越架验收牌())        
        