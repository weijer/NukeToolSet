import nuke


class TransformMatrix4(object):
    """represents keyframes for a 4x4 transform matrix"""

    def __init__(self):
        self.data = []  # list with entries (time, [v1,v2,...,v16])

    def deleteKey(self, time):
        # self.data = filter(lambda (t,v): t != time, self.data)
        self.data = list(filter(lambda t_v: t_v[0] != time, self.data))

    # def setKey(self,(time,value)):
    def setKey(self, time_value):
        time = time_value[0]
        value = time_value[1]
        assert (len(value) == 16)
        self.deleteKey(time)
        self.data.append((time, value))

    def applyToCurvesLayer(self, layer):
        transform = layer.getTransform()
        animations = self._getDataAsTuples()

        for i in range(0, 4):
            for j in range(0, 4):
                ac = transform.getExtraMatrixAnimCurve(i, j)
                ac.removeAllKeys()
                for (time, value) in animations[4 * i + j]:
                    ac.addKey(time, value)
                transform.setExtraMatrixAnimCurve(i, j, ac)

    def applyToArrayKnob(self, knob):
        animations = self._getDataAsAnimations()
        knob.setAnimated()
        for i in range(0, 16):
            knob.animation(i).clear()
            knob.animation(i).addKey(animations[i])

    def _getDataAsAnimations(self):
        animations = [[], [], [], [],
                      [], [], [], [],
                      [], [], [], [],
                      [], [], [], []
                      ]
        for (time, value) in self.data:
            for i in range(0, 16):
                ak = nuke.AnimationKey(time, value[i])
                animations[i].append(ak)
        return animations

    def _getDataAsTuples(self):
        animations = [[], [], [], [],
                      [], [], [], [],
                      [], [], [], [],
                      [], [], [], []
                      ]
        for (time, value) in self.data:
            for i in range(0, 16):
                t = (time, value[i])
                animations[i].append(t)
        return animations
