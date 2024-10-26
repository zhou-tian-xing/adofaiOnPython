import json

DEFAULT = {
    "version": 15,
    "artist": "",
    "specialArtistType": "None",
    "artistPermission": "",
    "song": "",
    "author": "",
    "separateCountdownTime": True,
    "previewImage": "",
    "previewIcon": "",
    "previewIconColor": "003f52",
    "previewSongStart": 0,
    "previewSongDuration": 10,
    "seizureWarning": False,
    "levelDesc": "",
    "levelTags": "",
    "artistLinks": "",
    "speedTrialAim": 0,
    "difficulty": 1,
    "requiredMods": [],
    "songFilename": "",
    "bpm": 100,
    "volume": 100,
    "offset": 0,
    "pitch": 100,
    "hitsound": "Kick",
    "hitsoundVolume": 100,
    "countdownTicks": 4,
    "trackColorType": "Single",
    "trackColor": "debb7b",
    "secondaryTrackColor": "ffffff",
    "trackColorAnimDuration": 2,
    "trackColorPulse": "None",
    "trackPulseLength": 10,
    "trackStyle": "Standard",
    "trackTexture": "",
    "trackTextureScale": 1,
    "trackGlowIntensity": 100,
    "trackAnimation": "None",
    "beatsAhead": 3,
    "trackDisappearAnimation": "None",
    "beatsBehind": 4,
    "backgroundColor": "000000",
    "showDefaultBGIfNoImage": True,
    "showDefaultBGTile": False,
    "defaultBGTileColor": "101121",
    "defaultBGShapeType": "Default",
    "defaultBGShapeColor": "ffffff",
    "bgImage": "",
    "bgImageColor": "ffffff",
    "parallax": [100, 100],
    "bgDisplayMode": "FitToScreen",
    "imageSmoothing": True,
    "lockRot": False,
    "loopBG": False,
    "scalingRatio": 100,
    "relativeTo": "Player",
    "position": [0, 0],
    "rotation": 0,
    "zoom": 100,
    "pulseOnFloor": True,
    "bgVideo": "",
    "loopVideo": False,
    "vidOffset": 0,
    "floorIconOutlines": False,
    "stickToFloors": True,
    "planetEase": "Linear",
    "planetEaseParts": 1,
    "planetEasePartBehavior": "Mirror",
    "defaultTextColor": "ffffff",
    "defaultTextShadowColor": "00000050",
    "congratsText": "",
    "perfectText": "",
    "legacyFlash": False,
    "legacyCamRelativeTo": False,
    "legacySpriteTiles": False,
    "legacyTween": False,
    "disableV15Features": False
}

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


class ADOFAI:  # 为了方便操作文件搞了一个类
    def __init__(self, path):
        """
        Create an adofai object
        :param path: The path of .adofai file you want to load. If path == None, it'll create an empty object.
        """
        self._path = path
        if path is not None:
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

        self.completeSettings()

        # 方便后续操作
        self.floorAct = {}
        for i in range(len(self.angleData) + 1):
            self.floorAct[i] = []
        for x in self.actions:
            self.floorAct[x["floor"]].append(x)

    def completeSettings(self):
        for key in DEFAULT:
            if not key in self.settings:
                self.settings[key] = DEFAULT[key]

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
        out = []
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
        pitch = self.settings["pitch"] if "pitch" in self.settings else 100
        K = pitch / self.settings["bpm"] * 0.00333333333333333333  # 上面两式的整合
        total = len(self.angleData)  # 要打的块的数量=描述的方向的数量
        out = []
        i = 1
        D = True  # 方向，是逆时针还是顺时针
        while i < total:
            # 由于指示的是方向，所以大于360和小于0的角都毫无意义。
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

    def timeToAngle(self, passingTime: list, bpm, speedFilter=lambda n, x: 1):
        """
        turn time to passed angle and give action of "SetSpeed"
        :param passingTime: the list describing time passed of every beat
        :param bpm: The bpm of the song
        :param speedFilter: A method(f(n, x)) deciding which blocks will be given action of "SetSpeed", n is the floor of the block, and x is the angle(may be docked).
                            If the return is 1, the block will not be given action of "SetSpeed", other will use "bpmMultiplier" = result. (x is the passed angle that takes into account changes in speed)
        :return: [passed angle]
        """
        k = bpm * 3
        angle = []
        spd = 1
        self.settings["bpm"] = bpm
        self.removeAction(None, "SetSpeed")
        n = 0
        for t in passingTime:
            if t:
                speed_change = speedFilter(n, k * t * spd)
                if speed_change != 1:
                    spd *= speed_change
                    self.actions.append(
                        {"floor": n + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100,
                         "bpmMultiplier": speed_change, "angleOffset": 0})
                angle.append(k * t * spd)
                n += 1
        self._floorActUpdate()
        return angle

    def angleToAngleData(self, passedAngle, offset, docking, twirlFilter=lambda n, x: False):
        """
        Turn the angle passed to angleData and store in self.angleData with the giving of action "Twirl"
        :param docking: docking of a note (0 - 90 degree, including 90), input None if you want default ([0, 18, 30, 45, 60, 72]), input False to not dock
        :param offset: It means that all angles have increased offset degree
        :param passedAngle: list, the angle rotated
        :param twirlFilter: A method(f(n, x)) deciding which blocks will be given action of "Twirl", n is the floor of the block, and x is the angle (may be docked)
        :return: None
        """
        passedAngle = [180] + passedAngle  # 开头还有一个180度
        dock = [0, 15, 30, 45, 60, 75, 90] if docking is None else docking
        if dock:
            passedAngle = [_docking(x, dock) for x in passedAngle]
        self.angleData = []
        self.removeAction(None, "Twirl")
        angle = 0
        Twirl = 1
        n = 0
        for x in passedAngle:
            if x:
                if twirlFilter(n, x):
                    Twirl = -Twirl
                    self.actions.append({'floor': n, 'eventType': 'Twirl'})
                angle = angle - x * Twirl + 180 + offset
                self.angleData.append(round(angle % 360, 4))
                n += 1
            if x > 360:
                print("[WARN] passedAngle = {} > 360, result may be error.".format(x))
        self._floorActUpdate()

    def _floorActUpdate(self):
        self.floorAct = {}
        for i in range(len(self.angleData) + 1):
            self.floorAct[i] = []
        for x in self.actions:
            self.floorAct[x["floor"]].append(x)

    def removeAction(self, floor, eventType):
        """
        Directly delete action in self.actions
        :param floor: A list include floors that will be detected, None for all
        :param eventType: 'eventType' of an action
        :return: None
        """
        for i in range(len(self.actions)):
            if floor is None:
                if self.actions[i]["eventType"] == eventType:
                    del self.actions[i]
            elif self.actions[i]["floor"] in floor:
                if self.actions[i]["eventType"] == eventType:
                    del self.actions[i]
        self._floorActUpdate()

    def docking(self, docking):
        """
        Different from docking in self.angleToAngleData, this method will affect self.angleData independently.
        :param docking: docking of a note (0 - 90 degree, including 90), input None if you want default ([0, 18, 30, 45, 60, 72])
        :return: None
        """
        docking = [0, 15, 30, 45, 60, 75, 90] if docking is None else docking
        self.angleData = [_docking(x, docking) for x in self.angleData]

    def getActions(self, floor):
        """
        get actions of a given block
        :param floor: The number of block you want to view (start point = 0)
        :return: [dict]
        """
        return self.floorAct[floor]

    def add(self, module, remove_sep=False):
        """
        Attach the content of another object to this object ( module.settings will be abandoned )
        :param remove_sep: Remove the block at the middle or not
        :param module: same as other in __add__
        :return: None
        """
        if remove_sep:
            floor0 = len(self.angleData) - 2
            self.angleData += module.angleData[1:]
        else:
            floor0 = len(self.angleData) - 1
            self.angleData += module.angleData
        for i in range(len(module.actions)):
            y = module.actions[i].copy()
            y["floor"] += floor0
            self.actions.append(y)
        self.decorations = self.decorations + module.decorations
        self._floorActUpdate()

    def save(self, path):
        """
        Saving all content as a .adofai file
        :return: None
        """
        with open(path, 'w') as f:
            json.dump({"angleData": self.angleData, "settings": self.settings, "actions": self.actions,
                       "decorations": self.decorations}, f)
