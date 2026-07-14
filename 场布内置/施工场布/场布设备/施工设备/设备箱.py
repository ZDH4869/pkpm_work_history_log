from pyp3d import *


class EquipmentBox(Component):
    def __init__(self):
        Component.__init__(self)
        self['场布类型'] = Attr("材料堆场", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("器具", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("设备箱", obvious=True, group="构件分类")
        self['箱体长'] = Attr(3000.0, obvious=True, group="箱体")
        self['箱体宽'] = Attr(2000.0, obvious=True, group="箱体")
        self['箱体高'] = Attr(2300.0, obvious=True, group="箱体")
        self['枕木长度'] = Attr(obvious=True, readonly=True, group="底座")
        self['枕木宽度'] = Attr(100.0, obvious=True, group="底座")
        self['枕木高度'] = Attr(100.0, obvious=True, group="底座")
        self['枕木间距'] = Attr(obvious=True, readonly=True, group="底座")
        self['枕木数量'] = Attr(4, obvious=True, group="底座")
        self['设备箱'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        # active parameters
        L_Box = self['箱体长']
        W_Box = self['箱体宽']
        H_Box = self['箱体高']
        W_Sleeper = self['枕木宽度']
        H_Sleeper = self['枕木高度']
        n_Sleeper = self['枕木数量']
        # passive parameters
        L_Sleeper = W_Box
        self['枕木长度'] = L_Sleeper
        S_Sleeper = L_Box/(n_Sleeper - 1)
        self['枕木间距'] = S_Sleeper
        RealS_Sleeper = (L_Box - n_Sleeper*W_Sleeper)/(n_Sleeper - 1)
        # limited parameters

        # geometry
        Equipment_Box = translation(15, 15, 15)*scale(L_Box - 30, W_Box - 30, H_Box - 30)\
                        *Cube().color(199/255,183/255,169/255,1)
        ReinforcementStrip = scale(L_Box, W_Box, H_Box)*Cube()
        ReinforcementStrip = Fusion(ReinforcementStrip - Equipment_Box)
        ReinforcementStrip_Sub1 = translation(W_Sleeper, W_Sleeper, 0)*\
                                  scale(L_Box - 2*W_Sleeper, W_Box - 2*W_Sleeper, H_Box)*Cube()
        ReinforcementStrip = Fusion(ReinforcementStrip - ReinforcementStrip_Sub1)
        ReinforcementStrip_Sub2_Single = translation(W_Sleeper, 0, W_Sleeper)*\
                                         scale(RealS_Sleeper, 15, H_Box - 2*W_Sleeper)*Cube()
        ReinforcementStrip_Sub2 = ReinforcementStrip_Sub2_Single
        for x in linspace(0, L_Box - 2*W_Sleeper - RealS_Sleeper, n_Sleeper - 1):
            if x == 0:
                continue
            ReinforcementStrip_temp = translation(x, 0, 0)*ReinforcementStrip_Sub2_Single
            ReinforcementStrip_Sub2 = combine(ReinforcementStrip_Sub2, ReinforcementStrip_temp)
        ReinforcementStrip_Sub3 = translation(0, W_Box - 15, 0)*ReinforcementStrip_Sub2
        ReinforcementStrip = Fusion(ReinforcementStrip - ReinforcementStrip_Sub2).color(1, 1, 0, 1)
        ReinforcementStrip = Fusion(ReinforcementStrip - ReinforcementStrip_Sub3).color(1, 1, 0, 1)
        ReinforcementStrip_Add1_Single = translation(W_Sleeper + RealS_Sleeper, 0, H_Box-15)*\
                                         scale(W_Sleeper, W_Box, 15)*Cube().color(1, 1, 0, 1)
        ReinforcementStrip_Add1 = ReinforcementStrip_Add1_Single
        for x in linspace(0, L_Box - 2*(2*W_Sleeper + RealS_Sleeper) + W_Sleeper, n_Sleeper - 2):
            if x == 0:
                continue
            ReinforcementStrip_temp = translation(x, 0, 0)*ReinforcementStrip_Add1_Single
            ReinforcementStrip_Add1 = combine(ReinforcementStrip_Add1, ReinforcementStrip_temp)
        ReinforcementStrip = Fusion(ReinforcementStrip + ReinforcementStrip_Add1).color(1, 1, 0, 1)

        ny_SleeperSub = int(W_Box/RealS_Sleeper)
        y_RealS_Sleeper = (W_Box - (ny_SleeperSub + 1)*W_Sleeper)/ny_SleeperSub
        ReinforcementStrip_Sub4_Single = translation(0, W_Sleeper, W_Sleeper)*\
                                         scale(15, y_RealS_Sleeper, H_Box - 2*W_Sleeper)*Cube()
        ReinforcementStrip_Sub4 = ReinforcementStrip_Sub4_Single
        for y in linspace(0, W_Box - 2*W_Sleeper - y_RealS_Sleeper, ny_SleeperSub):
            if y == 0:
                continue
            ReinforcementStrip_temp = translation(0, y, 0)*ReinforcementStrip_Sub4_Single
            ReinforcementStrip_Sub4 = combine(ReinforcementStrip_Sub4, ReinforcementStrip_temp)
        ReinforcementStrip_Sub5 = translation(L_Box - 15, 0, 0)*ReinforcementStrip_Sub4
        ReinforcementStrip = Fusion(ReinforcementStrip - ReinforcementStrip_Sub4)
        ReinforcementStrip = Fusion(ReinforcementStrip - ReinforcementStrip_Sub5).color(216/255,152/255,81/255, 1)
        Equipment_Box_UP = combine(Equipment_Box, ReinforcementStrip)
        Equipment_Box_UP = translation(0, 0, H_Sleeper)*Equipment_Box_UP

        Equipment_Box_Down_Single = scale(W_Sleeper, W_Box, H_Sleeper)*Cube().color(216/255,152/255,81/255, 1)
        Equipment_Box_Down = Equipment_Box_Down_Single
        for x in linspace(0, L_Box - W_Sleeper, n_Sleeper):
            if x == 0:
                continue
            Equipment_Box_Down_temp = translation(x, 0, 0)*Equipment_Box_Down_Single
            Equipment_Box_Down = combine(Equipment_Box_Down, Equipment_Box_Down_temp)

        self['设备箱'] = combine(Equipment_Box_UP, Equipment_Box_Down)


if __name__ == "__main__":
    Final_Geometry = EquipmentBox()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)