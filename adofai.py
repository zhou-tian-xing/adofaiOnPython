import json

class ADOFAI:
    def __init__(self, path):
        """
        Create a adofai object
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
            self.settings = []
            self.actions = []
            self.decorations = []

        # 方便后续操作
        self.floorAct = {}
        for i in range(len(self.angleData)):
            self.floorAct[i] = []
        for x in self.actions:
            self.floorAct[x["floor"]].append(x)

    def pathToAngle(self):  # 老板本的路径数据向新版本的角数据的转化
        DIC = {'R':0, 'p':15, 'J':30, 'E':45, 'T':60, 'o':75, 'U':90, 'q':105, 'G':120, 'Q':135, 'H':150,
               'W':165, 'L': 180,'x':195, 'N':210, 'Z':225, 'F':240, 'V':255, 'D':270, 'Y':285, 'B':300,
               'C':315, 'M':330, 'A':345, '5':555, '6':666, '7':777, '8':888, '!':999}  # !：中旋
        self.angleData = [DIC[i] for i in self.pathData]
        i = 0
        length = len(self.angleData)
        while i < length:
            pre = self.angleData[i - 1] if i >= 1 else 0
            if angle == 555: self.angleData[i] = (pre + 72) % 360
            if angle == 666: self.angleData[i] = (pre - 72) % 360
            if angle == 777: self.angleData[i] = (pre + 360 / 7) % 360
            if angle == 888: self.angleData[i] = (pre - 360 / 7) % 360
            i += 1

    def passingAngle(self):
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

    def getActions(self, floor):
        return self.floorAct[floor]

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({"angleData": self.angleData, "settings": self.settings, "actions": self.actions, "decorations": self.decorations})
