from pyp3d import *


class MaterialStacking(Component):
    def __init__(self):
        Component.__init__(self)
        self['场布类型'] = Attr("材料堆场", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("棚架", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("材料堆放架", obvious=True, group="构件分类")
        self['立柱长'] = Attr(100.0, obvious=True, readonly=True, group="立柱")
        self['立柱宽'] = Attr(100.0, obvious=True, readonly=True, group="立柱")
        self['立柱高'] = Attr(1200.0, obvious=True, group="立柱")
        self['立柱横向间距'] = Attr(1500.0, obvious=True, group="立柱")
        self['立柱纵向间距'] = Attr(1000.0, obvious=True, group="立柱")
        self['横向立柱数量'] = Attr(5, obvious=True, group="立柱")
        self['纵向立柱数量'] = Attr(6, obvious=True, group="立柱")
        self['材料堆放架'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        # active parameters
        L_Column = self['立柱长']
        W_Column = self['立柱宽']
        H_Column = self['立柱高']
        SOX_Column = self['立柱横向间距']
        SOY_Column = self['立柱纵向间距']
        NOX_Column = self['横向立柱数量']
        NOY_Column = self['纵向立柱数量']
        W_Beam = 40
        H_Beam = 200
        # limited parameters
        if SOX_Column < 200.0:
            SOX_Column = 200.0
            self['立柱横向间距'] = SOX_Column

        if SOY_Column < 200.0:
            SOY_Column = 200.0
            self['立柱纵向间距'] = SOY_Column

        if H_Column < 200.0:
            H_Column = 200.0
            self['立柱高'] = H_Column

        # passive parameters
        LOX_Beam = SOX_Column*(NOX_Column - 1)
        LOY_Beam = SOY_Column*(NOY_Column - 1)
        R_Material = (SOX_Column - 800)/2
        H_MaterialCenter = H_Beam + R_Material*cos(pi/6)

        # Geometry

        # 立柱部分
        Columns_Part_List = []
        i = 0
        while i - 3:
            Columns_List = []
            if i == 1:
                Column_Single = translate(-L_Column/2, -W_Column/2)*scale(L_Column, W_Column, H_Column/3)*\
                                Cube().color(26/255, 26/255, 24/255, 1)
            else:
                Column_Single = translate(-L_Column/2, -W_Column/2)*scale(L_Column, W_Column, H_Column/3)*\
                                Cube().color(228/255, 155/255, 57/255, 1)
            for X_point in linspace(0, LOX_Beam, NOX_Column):
                for Y_point in linspace(0, LOY_Beam, NOY_Column):
                    Columns_List.append(translate(X_point, Y_point)*Column_Single)
            if i == 1:
                Columns_List = translate(0, 0, i*H_Column/3)*Columns_List
                Columns_Part_List.append(combine(*Columns_List))
            else:
                Columns_List = translate(0, 0, i*H_Column/3)*Columns_List
                Columns_Part_List.append(combine(*Columns_List))
            i += 1
        Columns = combine(*Columns_Part_List)

        # 连接梁部分
        # X部分
        XOBeam_Single = translate(0, -W_Beam/2)*scale(LOX_Beam, W_Beam, H_Beam)*\
                        Cube().color(228/255, 155/255, 57/255, 1)
        XOBeams_List = []
        for Y_point in linspace(0, LOY_Beam, NOY_Column):
            XOBeams_List.append(translate(0, Y_point)*XOBeam_Single)
        XOBeams = combine(*XOBeams_List)
        # Y部分
        YOBeam_Single = translate(-W_Beam/2, 0)*scale(W_Beam, LOY_Beam, H_Beam)*\
                        Cube().color(228/255, 155/255, 57/255, 1)
        YOBeams_List = []
        for X_point in linspace(0, LOX_Beam, NOX_Column):
            YOBeams_List.append(translate(X_point, 0)*YOBeam_Single)
        YOBeams = combine(*YOBeams_List)
        Beams = combine(XOBeams, YOBeams)

        # 材料部分
        MaterialSection_Points = []
        for theta in linspace(0, pi*2, 7):
            x_point = R_Material*cos(theta)
            z_point = R_Material*sin(theta)
            MaterialSection_Points.append(Vec3(x_point, 0, z_point))
        MaterialSection = to_section(*MaterialSection_Points)

        Material_Stack_Single = Loft(translate(SOX_Column/2, -500, H_MaterialCenter)*MaterialSection,
                                     translate(SOX_Column/2, LOY_Beam + 500, H_MaterialCenter)*MaterialSection)\
                                     .color(124/255, 116/255, 98/255, 1)
        Materials_list = []
        for x_material_point in linspace(0, LOX_Beam - SOX_Column, NOX_Column - 1):
            Materials_list.append(translate(x_material_point, 0)*Material_Stack_Single)
        Materials = combine(*Materials_list)

        # 全图形
        if SOX_Column < 900.0:
            All_Geometry = [Columns, Beams]
        else:
            All_Geometry = [Columns, Beams, Materials]
        self['材料堆放架'] = combine(*All_Geometry)


if __name__ == "__main__":
    Final_Geometry = MaterialStacking()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)