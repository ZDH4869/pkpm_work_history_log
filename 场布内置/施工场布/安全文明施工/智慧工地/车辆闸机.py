from pyp3d import *


class 车辆闸机(Component):
    def __init__(self):
        Component.__init__(self)
        self['机箱长'] = Attr(320, obvious=False, readonly=True, group="机箱参数")
        self['机箱宽'] = Attr(320, obvious=False, readonly=True, group="机箱参数")
        self['机箱高'] = Attr(950, obvious=False, readonly=True, group="机箱参数")
        self['长'] = Attr(2500, obvious=True, readonly=False, group="闸杆参数")
        self['厚'] = Attr(84, obvious=False, readonly=True, group="闸杆参数")
        self['宽'] = Attr(100, obvious=False, readonly=True, group="闸杆参数")
        self['场布类型'] = Attr("智慧工地", obvious=True, readonly=True, group="构件分类")
        self['构建类型'] = Attr("闸机",     obvious=True, readonly=True, group="构件分类")
        self['构建名称'] = Attr("车辆闸机", obvious=True, readonly=False,group="构件分类")

        self['车辆闸机'] = Attr(None, show=True)

        self.replace()
    @export
    def replace(self):
        l_fence = self['长']
        d_fence = self['厚']
        h_fence = self['宽']
        l_box = self['机箱长'] 
        d_box = self['机箱宽']  
        h_box = self['机箱高']  
    # 箱体
        sec_box = Section(
            Vec2(l_box/2*0.9,d_box/2),
            Vec2(-l_box/2*0.9,d_box/2),
            Vec2(-l_box/2,d_box/2*0.9),
            Vec2(-l_box/2,-d_box/2*0.9),
            Vec2(-l_box/2*0.9,-d_box/2),
            Vec2(l_box/2*0.9,-d_box/2),
            Vec2(l_box/2,-d_box/2*0.9),
            Vec2(l_box/2,d_box/2*0.9),
            Vec2(l_box/2*0.9,d_box/2),
        )
        box = Loft(sec_box,translate(0,0,h_box*0.98) * sec_box,translate(0,0,h_box) * scale(0.9) * sec_box).color(255/255,215/255,0/255,1)
     
    # 栏杆
        # 横杆单元色块
        n_block = l_fence//250
        l_block = l_fence/n_block
        sec_block = rotation(Vec3(0,1,0),-0.5*pi) * rotation(-pi*0.5) * Section(
            Vec2(d_fence/2*0.8,h_fence/2),
            Vec2(-d_fence/2*0.8,h_fence/2),
            Vec2(-d_fence/2,h_fence/2*0.8),
            Vec2(-d_fence/2,-h_fence/2*0.8),
            Vec2(-d_fence/2*0.8,-h_fence/2),
            Vec2(d_fence/2*0.8,-h_fence/2),
            Vec2(d_fence/2,-h_fence/2*0.8),
            Vec2(d_fence/2,h_fence/2*0.8),
            Vec2(d_fence/2*0.8,h_fence/2),
        )
        redblock = translate(0,d_fence/2,h_fence/2) *  scale(1,1.1,0.3) * Loft(sec_block,translate(l_block,0,0) * sec_block).color(1,0,0,1) 
        # 横杆
        fence = translate(0,d_fence/2,h_fence/2) * Loft(sec_block,translate(l_fence,0,0) * sec_block).color(1,1,1,1) 
        fencered = combine()
        for i_block in range(n_block):
            if (i_block%2 == 0):
                fencered = combine(fencered,translate(l_block*i_block, 0, 0) * redblock)
        fence = (fence - fencered).color(1,1,1,1) 
        # 横杆支点补全
        fence_supple = translate(0,d_fence/2,h_fence/2) * Loft(sec_block,translate(-d_box/4,0,0) * sec_block).color(1,1,1,1) 
        pivot = combine(
            translate(0,d_fence,h_fence/2) * scale(d_box/15) * Sphere() - fence,
        )
        fence = combine(fence,fencered,fence_supple,pivot)
        # 定位
        fence = translate(0,d_box/2,h_box*0.7) * fence
    # 组装
        gate = combine(fence,box)
        self['车辆闸机'] = gate

if __name__ == "__main__":
    place(车辆闸机())
