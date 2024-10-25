# adofaiOnPython

- [adofaiOnPython](#adofaiOnPython)
  - [基本信息 Basic Info](#基本信息-BasicInfo)
  - [计划表 Planned Feature List](#计划表-PlannedFeaturesList)
  - [使用指南 Usage Guide](#使用指南-UsageGuide)
    - [`adofai.py`](#adofaipy)

**Warning: The Following Translations are Almost All Done by Machines, so I won't be Responsible for Them. (Well, my English is so poor that I may not able to write on my owe......except this sentence.)**

本质上，`.adofai`文件就是一个`.json`，这使得读取和改变它变得很容易。
Essentially, the `.adofai` file is a `.json`, which makes reading and modifying it quite easy.



## 基本信息-BasicInfo

对于音游《冰与火之舞》谱文件的读取、编辑以及对音乐的采集与自动写谱。
For the rhythm game "A Dance of Ice and Fire", it involves reading, editing score files, and collecting music for automatic scorewriting.

目前实现的功能较少，详见下面的计划功能表。我希望实现的功能是简单的踩音和批量的轨道编辑，我认为这可以省下很多的工作。
Currently, there are fewer implemented features, see the planned feature list below for details. The functionality I hope to achieve is simple beat matching and batch track editing, which I believe can save a lot of work.

当然，我认为用这个项目去编辑特效纯粹是自讨苦吃的行为，除非你需要给每个块都加上存档点的属性（actions），不过我相信应该不会有人这么做。
Of course, I think using this project to edit visual effects is purely an act of asking for trouble, unless you need to add save point properties (actions) to every block, but I believe no one would actually do that.

如果你希望我添加额外的功能，你可以发起一个Issue，但我并不一定会注意到它。
If you wish for me to add additional features, you can open an Issue, but I may not necessarily notice it.



## 计划表-PlannedFeaturesList

+ [x] 读取和存储`.adofai`文件。    Read and store `.adofai` files.
+ [x] 旧版本`.adofai`文件向新版本的转化。    Conversion of old version `.adofai` files to the new version.
+ [x] 两次打击之间经过的角度与`.adofai`角数据的互相转化。    Conversion between the angles passed between two hits and the .adofai angle data.
+ [x] 两次打击之间经过的时间和角度的互相转化。    Conversion between the time and angles passed between two hits.
+ [ ] 一定频率范围内对`.wav`文件的踩音。    Beat matching of `.wav` files within a certain frequency range.
+ [ ] 对于手动录制的内容进行踩音。    Beat matching for manually recorded content.
+ [x] 谱面的模块化，即可以通过添加模版的方式批量制造同一种东西。（这点可能需要把旋转和倍速也记录下来）    Modularization of the chart, which means that the same thing can be mass-produced by adding templates. (This may require recording rotations and speed multipliers as well.)
+ [x] 在不改变实际打的谱子的情况下去除倍速。    Remove the speed multiplier without altering the actual chart.
+ [x] 在不改变实际打的谱子的情况下去除旋转。    Remove rotations without altering the actual chart.
+ [ ] 播放器（实际上我认为没什么必要，因为用官方的编辑器可以很方便的重新打开一个文件（只需要两次点击！））    Player (actually, I don't think it's very necessary because the official editor can easily reopen a file with just two clicks!)
+ [ ] 歌的延迟分析和bpm分析（纯属多此一举，绝对不是因为我写不明白）    Delay analysis and BPM analysis of a song (totally unnecessary, definitely not because I can't figure out how to write it)
+ [x] 输出每次打击的时间   Output the time of each hit



## 使用指南-UsageGuide

未来计划整个项目将封装到两个文件，分别是操作`.adofai`文件的`adofai.py`和进行自动采音的`collect.py`（暂定），以下分这两个部分进行描述。
The future plan is to encapsulate the entire project into two files, namely 'adofai.py' for manipulating the '.adofai' file and 'collect.py' for automatic sound harvesting (tentative). The following will describe these two parts.

### adofai.py

```python
Modules: json

class ADOFAI:
    def __init__(self, path):
        """
        Create an adofai object
        :param path: The path of .adofai file you want to load. If path == None, it'll create an empty object.
        """
    def add(self, module, remove_sep=False):
        """
        Attach the content of another object to this object ( module.settings will be abandoned )
        :param remove_sep: Remove the block at the middle or not
        :param module: same as other in __add__
        :return: None
        """
    def angleToAngleData(self, passedAngle, offset, docking, twirlFilter = lambda n, x: False):
        """
        Turn the angle passed to angleData and store in self.angleData with the giving of action "Twirl"
        :param docking: docking of a note (0 - 90 degree, including 90), input None if you want default ([0, 18, 30, 45, 60, 72]), input False to not dock
        :param offset: It means that all angles have increased offset degree
        :param passedAngle: list, the angle rotated
        :param twirlFilter: A method(f(n, x)) deciding which blocks will be given action of "Twirl", n is the floor of the block, and x is the angle (may be docked)
        :return: None
        """
    def docking(self, docking):
        """
        Different from docking in self.angleToAngleData, this method will affect self.angleData independently.
        :param docking: docking of a note (0 - 90 degree, including 90), input None if you want default ([0, 18, 30, 45, 60, 72])
        :return: None
        """
    def getActions(self, floor):
        """
        get actions of a given block
        :param floor: The number of block you want to view (start point = 0)
        :return: [dict]
        """
    def passedAngle(self):
        """
        Calculate the angle rotated by each beat
        :return: list
        """
    def passedTime(self):
        """
        Calculate the time passed by each beat (seconds)
        :return: list
        """
    def pathToAngle(self):
        """
        Turn self.pathData to self.angleData
        :return: None
        """
    def removeAction(self, floor, eventType):
        """
        Directly delete action in self.actions
        :param floor: A list include floors that will be detected, None for all
        :param eventType: 'eventType' of an action
        :return: None
        """
    def save(self, path):
        """
        Saving all content as a .adofai file
        :return: None
        """
    def timeToAngle(self, passingTime: list, bpm, speedFilter = lambda n, x: 1):
        """
        turn time to passed angle and give action of "SetSpeed"
        :param passingTime: the list describing time passed of every beat
        :param bpm: The bpm of the song
        :param speedFilter: A method(f(n, x)) deciding which blocks will be given action of "SetSpeed", n is the floor of the block, and x is the angle(may be docked).
                            If the return is 1, the block will not be given action of "SetSpeed", other will use "bpmMultiplier" = result. (x is the passed angle that takes into account changes in speed)
        :return: [passed angle]
        """

def _docking(x, dock):
    """docking helper"""
```
