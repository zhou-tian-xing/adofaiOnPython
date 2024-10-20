import json


def _docking(x, dock):  # 最近元素
    """docking helper"""
    m = x % 90
    n = x // 90
    min_diff = 100
    closest_num = None

    for num in dock:
        diff = abs(num - m)
        if diff <= min_diff:
            min_diff = diff
            closest_num = num
    return closest_num + n * 90


class ADOFAI:
    def __init__(self, path):
        """
        Create an adofai object
        :param path: The path of .adofai file you want to load. If path == None, it'll create an empty object.
        """
        if path is not None:
            self._path = path
            with open(path, 'r', encoding="utf-8-sig") as f:
                A = json.load(f)
            if "pathData" in A:
                self.pathData = A["pathData"]
                self.pathToAngle()
            else:
                self.angleData = A["angleData"]
            self.settings = A["settings"]
            self.actions = A["actions"]
            self.decorations = A["decorations"]
        else:
            self.angleData = []
            self.settings = {}
            self.actions = []
            self.decorations = []

        # 方便后续操作
        self.floorAct = {}
        for i in range(len(self.angleData)):
            self.floorAct[i] = []
        for x in self.actions:
            self.floorAct[x["floor"]].append(x)

    def pathToAngle(self):  # 老板本的路径数据向新版本的角数据的转化
        """
        Turn self.pathData to self.angleData
        :return: None
        """
        DIC = {'R': 0, 'p': 15, 'J': 30, 'E': 45, 'T': 60, 'o': 75, 'U': 90, 'q': 105, 'G': 120, 'Q': 135, 'H': 150,
               'W': 165, 'L': 180, 'x': 195, 'N': 210, 'Z': 225, 'F': 240, 'V': 255, 'D': 270, 'Y': 285, 'B': 300,
               'C': 315, 'M': 330, 'A': 345, '5': 555, '6': 666, '7': 777, '8': 888, '!': 999}  # !：中旋
        self.angleData = [DIC[i] for i in self.pathData]
        i = 0
        length = len(self.angleData)
        while i < length:
            pre = self.angleData[i - 1] if i >= 1 else 0
            if self.angleData[i] == 555:
                self.angleData[i] = (pre + 72) % 360
            elif self.angleData[i] == 666:
                self.angleData[i] = (pre - 72) % 360
            elif self.angleData[i] == 777:
                self.angleData[i] = (pre + 360 / 7) % 360
            elif self.angleData[i] == 888:
                self.angleData[i] = (pre - 360 / 7) % 360
            i += 1

    def passedAngle(self):
        """
        Calculate the angle rotated by each beat
        :return: list
        """
        total = len(self.angleData)  # 要打的块的数量=描述的方向的数量
        out = [180]  # 第一个永远是180
        i = 1
        D = True  # 方向，是逆时针还是顺时针
        while i < total:
            if self.angleData[i] != 999:
                a = self.angleData[i - 1] - self.angleData[i] + 180
            else:
                # 对于中旋来说，其块的方向不同，等价于把原先的方向加了180度，因为比如一个中旋向上的话，经过它之后意味着一个向下的正常块连接后面的轨道
                # 然后中旋后面一个的计算没有意义，因为999度本身就是一个标识符，所以i += 1
                a = self.angleData[i - 1] - self.angleData[i + 1]
                i += 1
            if {'floor': i, 'eventType': 'Twirl'} in self.floorAct[i]:
                D = not D
            a = a if D else 360 - a
            out.append(a % 360)
            i += 1
        return out

    def passedTime(self):
        """
        Calculate the time passed by each beat (seconds)
        :return: list
        """
        # pitch = self.settings["pitch"] / 100  # 音高（化为0到1之间）
        # spd = 0.333333333333333333 / self.settings["bpm"]  # second per degree(angle), 没算上音高
        K = self.settings["pitch"] / self.settings["bpm"] * 0.00333333333333333333  # 上面两式的整合
        total = len(self.angleData)  # 要打的块的数量=描述的方向的数量
        out = [180 * K]  # 第一个永远是180
        i = 1
        D = True  # 方向，是逆时针还是顺时针
        while i < total:
            if self.angleData[i] != 999:
                a = self.angleData[i - 1] - self.angleData[i] + 180
            else:
                # 对于中旋来说，其块的方向不同，等价于把原先的方向加了180度，因为比如一个中旋向上的话，经过它之后意味着一个向下的正常块连接后面的轨道
                # 然后中旋后面一个的计算没有意义，因为999度本身就是一个标识符，所以i += 1
                a = self.angleData[i - 1] - self.angleData[i + 1]
                i += 1
            for act in self.floorAct[i]:  # act检测
                if act["eventType"] == "SetSpeed":
                    if act["speedType"] == "Bpm":
                        K *= act["beatsPerMinute"] / self.settings["bpm"]
                    else:
                        K /= act["bpmMultiplier"]
                if act["eventType"] == "Twirl":
                    D = not D
            a = a if D else 360 - a
            out.append(a % 360 * K)
            i += 1
        return out

    def timeToAngle(self, passingTime: list, bpm, offset, docking):
        """
        turn time to angleData and store in self.angleData (without actions)
        :param passingTime: the list describing time passed of every beat
        :param docking: docking of a note (0 - 90 degree, including 90), input None if you want default ([0, 18, 30, 45, 60, 72]), input False to not dock
        :param offset: It means that all angles have increased offset degree
        :param bpm: The bpm of the song
        :return: None
        """
        k = bpm * 3
        angle = [k * t for t in passingTime]
        self.settings["bpm"] = bpm
        self.angleToAngleData(angle, offset, docking)

    def angleToAngleData(self, passedAngle, offset, docking):
        """
        Turn the angle rotated to angleData and store in self.angleData (without effect)
        :param docking: docking of a note (0 - 90 degree, including 90), input None if you want default ([0, 18, 30, 45, 60, 72]), input False to not dock
        :param offset: It means that all angles have increased offset degree
        :param passedAngle: list, the angle rotated
        :return: None
        """
        dock = [0, 15, 30, 45, 60, 75] if docking is None else docking
        if docking:
            passedAngle = [_docking(x % 360, dock) for x in passedAngle]
        self.angleData = [180]
        angle = 0
        for x in passedAngle:
            if x:
                angle = angle - x + 180 + offset
                self.angleData.append(angle % 360)

    def docking(self, docking):
        """
        Different from docking in self.angleToAngleData, this method will affect self.angleData independently.
        :param docking: docking of a note (0 - 90 degree, including 90), input None if you want default ([0, 18, 30, 45, 60, 72])
        :return: None
        """
        docking = [0, 15, 30, 45, 60, 75] if docking is None else docking
        self.angleData = [_docking(x, docking) for x in self.angleData]

    def getActions(self, floor):
        """
        get actions of a given block
        :param floor: The number of block you want to view (start point = 0)
        :return: [dict]
        """
        return self.floorAct[floor]

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({"angleData": self.angleData, "settings": self.settings, "actions": self.actions,
                       "decorations": self.decorations}, f)
