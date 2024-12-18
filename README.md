# adofaiOnPython

- [adofaiOnPython](#adofaiOnPython)
  - [基本信息 Basic Info](#基本信息-BasicInfo)
  - [计划表 Planned Feature List](#计划表-PlannedFeaturesList)
  - [使用指南 Usage Guide](#使用指南-UsageGuide)
    - [`adofai.py`](#adofaipy)
  - [例子 Examples](#例子Examples)
    - [1](#1)
    - [2](#2)
    - [3](#3)
    - [4](#4)

**Warning: The Following Translations are Almost All Done by Machines, so I won't be Responsible for Them. (Well, my English is so poor that I may not able to write on my own......except this sentence.)**

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
+ [x] 输出音频    Output audio
+ [ ] 歌的延迟分析和bpm分析（纯属多此一举，绝对不是因为我写不明白）    Delay analysis and BPM analysis of a song (totally unnecessary, definitely not because I can't figure out how to write it)
+ [x] 输出每次打击的时间   Output the time of each hit
+ [ ] `.midi`文件转化为乐谱   Convert `.midi` files to sheet music



## 使用指南-UsageGuide

未来计划整个项目将封装到两个文件，分别是操作`.adofai`文件的`adofai.py`和进行自动采音的`sampling.py`，以下分这两个部分进行描述。
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
    def make(self, beatAudioPath, outputPath):
        """
        Synthesize score into .wav files
        :param beatAudioPath: path of beat-sound (.wav file)
        :param outputPath: path of output file
        :return: None
        """

def _docking(x, dock):
    """docking helper"""
```



## 例子Examples

### 1

以下代码创建并保存了一个长两秒钟、KPS=440的`test.adofai`文件。其中每一次两次打击之间角度小于45°时都为块附加了类型为"Twirl"的Action。
The following code creates and saves a two second, KPS=440 `. adofai` file. When the angle between each two strikes is less than 45 degrees, an Action of type "Twirl" is attached to the block.

```python
a = ADOFAI(None)
a.angleToAngleData(a.timeToAngle([1 / 440] * 880, 600), 0, False, lambda n, x: x < 45)
a.save("test.adofai")
```



### 2

以下代码读取`test.adofai`并移除了其中floor在1和10之间（不包含1和10）的旋转，但保持效果不变。最终将修改后的结果覆盖原先文件。
The following code reads `test.adofai` and removes the rotation of the floor between 1 and 10 (excluding 1 and 10), but keeps the effect unchanged. The final modified result will overwrite the original file.

```python
a = ADOFAI("test.adofai")
floors = [x["floor"] for x in a.actions if x["eventType"] == "Twirl"]
def f(n, x):
    if n in floors and not 1 < n < 10:
        return True
    return False
a.angleToAngleData(a.passedAngle(), 0, False, f)
a.save("test.adofai")
```

总之，只需要灵活的应用passedAngle, passedTime, timeToAngle, angleToAngleData四个方法就可以实现对旋转和加速Action的操作。
In short, it is only necessary to flexibly apply the four methods of PassedAngle, PassedTime, timeToAngle, and angleToAngleData to achieve the operation of Twirl and SetSpeed actions.




### 3

以下代码实现220Hz、441Hz、659Hz声音的混合（注意不要出现整数倍，因为会重合，而音效播放是没有音量的）。
The following code implements the mixing of 220Hz, 441Hz, and 659Hz sounds (be careful not to use integer multiples as they may overlap, and the sound effect playback has no volume).

```python
a = ADOFAI(None)
timelist = [1/220 * x for x in range(441)] + [1/441 * x for x in range(883)] + [1/659 * x for x in range(1323)]
timelist.sort()
passtime = [timelist[i] - timelist[i - 1] for i in range(1, len(timelist))]
a.angleToAngleData(a.timeToAngle(passtime, 1000), 0, False, lambda n, x: x < 31)
a.save("test.adofai")
```



### 4

以下代码产生的谱子是一条好看的曲线（但可能没什么用），或许在数学上是一条知名的曲线。
The spectrum generated by the following code is a beautiful curve (but may not be very useful), perhaps a well-known curve in mathematics.

```python
a = ADOFAI(None)
timelist = [1/1000 * x for x in range(1, 1001)]
a.angleToAngleData(a.timeToAngle(timelist, 120), 0, False, lambda n, x: False)
a.save("test.adofai")
```
![image](https://github.com/user-attachments/assets/99bae2ea-eab8-49e0-821e-8d8567bc505c)
