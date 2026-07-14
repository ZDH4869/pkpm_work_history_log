from pyp3d import *


class GeneralEquipment(Component):
    def __init__(self):
        Component.__init__(self)
        self['场布类型'] = Attr("器械", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("设备", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("通用设备", obvious=True, group="构件分类")
        self['设备长'] = Attr(2000.0, obvious=True, group="设备尺寸")
        self['设备宽'] = Attr(1500.0, obvious=True, group="设备尺寸")
        self['设备高'] = Attr(1500.0, obvious=True, group="设备尺寸")
        self['文字内容'] = Attr("通用设备", obvious=True, group="文字")
        self['文字大小'] = Attr(250, obvious=True, group="文字")
        self['文本X向偏移'] = Attr(0.0, obvious=True, group="文字")
        self['文本Y向偏移'] = Attr(0.0, obvious=True, group="文字")
        self['通用设备'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        text_comment = self['文字内容']
        text_Size = self['文字大小']
        text_X = self['文本X向偏移']
        text_Y = self['文本Y向偏移']
        L_Equipment = self['设备长']
        W_Equipment = self['设备宽']
        H_Equipment = self['设备高']

        # passive parameters
        n_text = len(text_comment)

        # limited parameters
        if n_text*text_Size*20/19 > L_Equipment:
            text_Size = L_Equipment*19/20/n_text
            self['文字大小'] = text_Size
        if text_Size > W_Equipment:
            text_Size = W_Equipment
            self['文字大小'] = text_Size
        if abs(text_X) > (L_Equipment - n_text*text_Size*20/19)/2:
            if text_X > 0:
                text_X = (L_Equipment - n_text*text_Size*20/19)/2
                self['文本X向偏移'] = text_X
            elif text_X < 0:
                text_X = -(L_Equipment - n_text*text_Size*20/19)/2
                self['文本X向偏移'] = text_X
        if abs(text_Y) > (W_Equipment - text_Size)/2:
            if text_Y > 0:
                text_Y = (W_Equipment - text_Size)/2
                self['文本Y向偏移'] = text_Y
            elif text_Y < 0:
                text_Y = -(W_Equipment - text_Size)/2
                self['文本Y向偏移'] = text_Y
        if H_Equipment <= 0:
            H_Equipment = 0.1
            self['设备高'] = H_Equipment

        # Geometry
        Equipment = scale(L_Equipment, W_Equipment, H_Equipment)*Cube().color(1, 1, 1, 1)
        text = Text(text_comment, text_Size / 1.50, text_Size / 1.50).color(0, 0, 0, 1)

        text = translation(L_Equipment/2 - n_text*text_Size/2*19/20 + text_X,
                           W_Equipment/2 - text_Size/3 + text_Y,
                           H_Equipment + 1)*text
        self['通用设备'] = combine(Equipment, text)

if __name__ == "__main__":
    Final_Geometry = GeneralEquipment()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)