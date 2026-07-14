from pyp3d import *
class 防疫消杀棚(Component):
    def __init__(self):
        Component.__init__(self)
        self['长度'] = Attr(4000, obvious=True,group="棚尺寸")
        self['宽度'] = Attr(3000, obvious=True,group="棚尺寸")
        self['高度'] = Attr(2200, obvious = True,group="棚尺寸")
        self['防疫消杀棚'] = Attr(None, show=True)
        self['旋转角度'] = Attr(0,obvious = True,group="旋转")
        self['场布类型'] = Attr('防疫', obvious=True,readonly = True,group="构件分类")
        self['构件类型'] =  Attr('棚具', obvious=True,readonly = True,group="构件分类")
        self['构件名称'] =  Attr('防疫消杀棚', obvious=True,group="构件分类")
        self.replace()
    @export
    def replace(self):
        lenge = self['长度']
        width = self['宽度']
        high = self['高度']
        场布类型 = self['场布类型']
        构件类型 = self['构件类型']
        Angle = self['旋转角度']
        banner_h=400
        if self['长度']<banner_h*5/2 :
            lenge=banner_h*5/2
            self['长度']=banner_h*5/2
        if self['宽度']<600:
           width=600 
           self['宽度']=600
        if self['高度']<1000:
            high=1000
            self['高度']=1000
        col_r=30
        #框架
        section_one=translate(0,0,col_r) *rotation(Vec3(1,0,0),pi/2) * Section(scale(col_r) * Arc(2*pi))
        col_tran_one=Loft(translate(0,-width/2,0) *section_one, translate(0,width/2,0) * section_one)
        col_tran_two=translate(0,0,high-col_r*2) *col_tran_one

        section_two=Section(scale(col_r) * Arc(2*pi))
        col_z_one=Loft(section_two, translate(0,0,high) * section_two)
        col_z_two=translate(0,width/2-col_r,0) *col_z_one
        col_z_three=translate(0,-width/2+col_r,0) *col_z_one
        col_t=combine(col_z_three,col_z_two,col_z_one,col_tran_two,col_tran_one)
        col_left=translate(-lenge/2+col_r,0,0) *col_t
        col_right=translate(lenge/2-col_r,0,0) *col_t

        section_three=translate(0,0,high-col_r) *rotation(Vec3(0,1,0),pi/2) * Section(scale(col_r) * Arc(2*pi))
        col_x_one=Loft(translate(-lenge/2,0,0) *section_three, translate(lenge/2,0,0) * section_three)
        col_x_two=translate(0,width/2-col_r,0) *col_x_one
        col_x_three=translate(0,-width/2+col_r,0) *col_x_one
        frame=combine(col_x_two,col_x_three,col_x_one,col_left,col_right)
        # create_geometry(frame)
        #侧布
        section_four=Section(Vec2(-lenge/2,-width/2),Vec2(-lenge/2-1,-width/2),Vec2(-lenge/2-1,width/2),Vec2(-lenge/2,width/2))
        clo_left=Loft(section_four, translate(0,0,high-banner_h) * section_four).color(1,1,1,1)
        clo_right=translate(lenge+1,0,0) *clo_left
        cloth=combine(clo_right,clo_left).color(1,1,1,1)
        # create_geometry(cloth)
        #横幅
        section_five=translate(0,0,high-banner_h) *Section(Vec2(-lenge/2,-width/2),Vec2(-lenge/2-1,-width/2),Vec2(-lenge/2-1,width/2),Vec2(-lenge/2,width/2))
        banner_left=Loft(section_five, translate(0,0,banner_h+1) * section_five).color(252/255,50/255,50/255,1)
        banner_right=translate(lenge+1,0,0) *banner_left
        section_six=translate(0,0,high-banner_h) *Section(Vec2(-lenge/2,-width/2),Vec2(-lenge/2,-width/2-1),Vec2(lenge/2,-width/2-1),Vec2(lenge/2,-width/2))
        banner_front=Loft(section_six, translate(0,0,banner_h+1) * section_six).color(252/255,50/255,50/255,1)
        banner_after=translate(0,width+1,0) *banner_front
        banner=combine(banner_front,banner_after,banner_right,banner_left).color(252/255,50/255,50/255,1)
        # create_geometry(banner)
        #顶
        section_seven=translate(0,0,high) *Section(Vec2(-lenge/2-1,-width/2-1),Vec2(lenge/2+1,-width/2-1),Vec2(lenge/2+1,width/2+1),Vec2(-lenge/2-1,width/2+1))
        ceiling=Loft(section_seven, translate(0,0,1) * section_seven).color(1,1,1,1)
        # create_geometry(ceiling)
        #消杀棚
        ding_w_x=translate(-banner_h*5/7,-width/2-1-1,high-banner_h+banner_h/3) *rotation(Vec3(1,0,0),pi/2) *Text("消杀棚",banner_h/3,banner_h/3).color(1,1,0,1)
        ding_w_y=rotation(Vec3(0,0,1),pi) *ding_w_x
        ding_w=combine(ding_w_y,ding_w_x)
        # create_geometry(ding_w)

        wzj_f=rotation(math.pi/180 * Angle) *translate(lenge/2,width/2,0) *combine(ding_w,ceiling,banner,cloth,frame)
        self['防疫消杀棚']=wzj_f

if __name__ == "__main__":
    place(防疫消杀棚())