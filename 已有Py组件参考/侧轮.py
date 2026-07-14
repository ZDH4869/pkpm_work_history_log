from pyp3d import *

class 侧轮(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['L'] = Attr(240.0, obvious=True)
        self['H2'] = Attr(30.0, obvious=True)
        self['L1'] = Attr(40.0, obvious=True)
        self['L2'] = Attr(160.0, obvious=True)
        self['H3'] = Attr(30.0, obvious=True)
        self['D'] = Attr(100.0, obvious=True)
        self['H4'] = Attr(190.0, obvious=True)
        self['L3'] = Attr(70.0, obvious=True)
        self['H1'] = Attr(80.0, obvious=True)
        self['d1'] = Attr(102.5, obvious=True)
        self['d2'] = Attr(150.0, obvious=True)
        
        self['旋转角度'] = Attr(0.0, obvious=True)
        self['X'] = Attr(0.0, obvious=True)
        self['Y'] = Attr(0.0, obvious=True)
        self['Z'] = Attr(0.0, obvious=True)
        
        self['侧轮'] = Attr(None, show=True)
        self.replace()
    
    @export
    def replace(self):
        L = self['L']
        H2 = self['H2']
        L1 = self['L1']
        L2 = self['L2']
        H3 = self['H3']
        D = self['D']
        H4 = self['H4']
        L3 = self['L3']
        H1 = self['H1']
        d1 = self['d1']
        d2 = self['d2']
        
        x = self['X']
        y = self['Y']
        z = self['Z']
        Angle = self['旋转角度']
        
        basePlate = scale(L, L, H2) * translate(-0.5, -0.5, 0) * Cube()
        
        holeRadius = 8.0
        holeHeight = H2 + 10.0
        
        holeOffset = (L - L2) / 2.0
        
        hole1 = translate(holeOffset, holeOffset, -5) * scale(holeRadius, holeRadius, holeHeight) * Cube()
        hole2 = translate(-holeOffset, holeOffset, -5) * scale(holeRadius, holeRadius, holeHeight) * Cube()
        hole3 = translate(holeOffset, -holeOffset, -5) * scale(holeRadius, holeRadius, holeHeight) * Cube()
        hole4 = translate(-holeOffset, -holeOffset, -5) * scale(holeRadius, holeRadius, holeHeight) * Cube()
        
        basePlateWithHoles = basePlate - hole1 - hole2 - hole3 - hole4
        
        boltRadius = 7.0
        boltLength = 40.0
        nutRadius = 12.0
        nutHeight = 10.0
        
        bolt1 = translate(holeOffset, holeOffset, -boltLength) * scale(boltRadius, boltRadius, boltLength) * Cube()
        bolt2 = translate(-holeOffset, holeOffset, -boltLength) * scale(boltRadius, boltRadius, boltLength) * Cube()
        bolt3 = translate(holeOffset, -holeOffset, -boltLength) * scale(boltRadius, boltRadius, boltLength) * Cube()
        bolt4 = translate(-holeOffset, -holeOffset, -boltLength) * scale(boltRadius, boltRadius, boltLength) * Cube()
        
        nut1 = translate(holeOffset, holeOffset, -H3 - nutHeight) * scale(nutRadius, nutRadius, nutHeight) * Cube()
        nut2 = translate(-holeOffset, holeOffset, -H3 - nutHeight) * scale(nutRadius, nutRadius, nutHeight) * Cube()
        nut3 = translate(holeOffset, -holeOffset, -H3 - nutHeight) * scale(nutRadius, nutRadius, nutHeight) * Cube()
        nut4 = translate(-holeOffset, -holeOffset, -H3 - nutHeight) * scale(nutRadius, nutRadius, nutHeight) * Cube()
        
        baseAssembly = basePlateWithHoles + bolt1 + bolt2 + bolt3 + bolt4 + nut1 + nut2 + nut3 + nut4
        
        columnRadius = D / 2.0
        column = translate(0, 0, H2) * Cone(Vec3(0, 0, H2), Vec3(0, 0, H2 + H4), columnRadius, columnRadius)
        
        ribWidth = L3
        ribThickness = H2
        ribHeight = H4
        
        ribInnerRadius = columnRadius
        ribOuterRadius = columnRadius + ribWidth
        
        rib1 = Box(
            Vec3(ribInnerRadius, -ribThickness/2, H2),
            Vec3(ribOuterRadius, ribThickness/2, H2 + ribHeight),
            Vec3(1, 0, 0),
            Vec3(0, 0, 1),
            ribWidth,
            ribThickness,
            ribWidth,
            ribThickness
        )
        
        rib2 = rotate(Vec3(0, 0, 1), math.pi/2) * rib1
        rib3 = rotate(Vec3(0, 0, 1), math.pi) * rib1
        rib4 = rotate(Vec3(0, 0, 1), 3*math.pi/2) * rib1
        
        supportAssembly = column + rib1 + rib2 + rib3 + rib4
        
        innerCylinderRadius = D / 2.0
        innerCylinder = Cone(
            Vec3(0, 0, H2 + H4),
            Vec3(0, 0, H2 + H4 + H1),
            innerCylinderRadius,
            innerCylinderRadius
        )
        
        outerRingInnerRadius = d1
        outerRingOuterRadius = d2
        outerRingInner = Cone(
            Vec3(0, 0, H2 + H4),
            Vec3(0, 0, H2 + H4 + H1),
            outerRingInnerRadius,
            outerRingInnerRadius
        )
        outerRingOuter = Cone(
            Vec3(0, 0, H2 + H4),
            Vec3(0, 0, H2 + H4 + H1),
            outerRingOuterRadius,
            outerRingOuterRadius
        )
        outerRing = outerRingOuter - outerRingInner
        
        topDiskAssembly = innerCylinder + outerRing
        
        sideWheel = baseAssembly + supportAssembly + topDiskAssembly
        
        self['侧轮'] = translate(x, y, z) * rotate(math.pi/180 * Angle) * sideWheel

if __name__ == "__main__":
    FinalGeometry = 侧轮()
    place(FinalGeometry)
