# adofaiOnPython

- [adofaiOnPython](#adofaiOnPython)
  - [基本信息  Basic Info](## 基本信息  Basic Info)
  - [计划表 planned feature list](## 计划表 planned feature list)

**Warning: The Following Translations are Almost All Done by Machines, so I won't be Responsible for Them. (Well, my English is so poor that I may not able to write on my owe......except this sentence.)**

本质上，`.adofai`文件就是一个`.json`，这使得读取和改变它变得很容易。
Essentially, the `.adofai` file is a `.json`, which makes reading and modifying it quite easy.



## 基本信息  Basic Info

对于音游《冰与火之舞》谱文件的读取、编辑以及对音乐的采集与自动写谱。
For the rhythm game "A Dance of Ice and Fire", it involves reading, editing score files, and collecting music for automatic scorewriting.

目前实现的功能较少，详见下面的计划功能表。我希望实现的功能是简单的踩音和批量的轨道编辑，我认为这可以省下很多的工作。
Currently, there are fewer implemented features, see the planned feature list below for details. The functionality I hope to achieve is simple beat matching and batch track editing, which I believe can save a lot of work.

当然，我认为用这个项目去编辑特效纯粹是自讨苦吃的行为，除非你需要给每个块都加上存档点的属性（actions），不过我相信应该不会有人这么做。
Of course, I think using this project to edit visual effects is purely an act of asking for trouble, unless you need to add save point properties (actions) to every block, but I believe no one would actually do that.

如果你希望我添加额外的功能，你可以发起一个Issue，但我并不一定会注意到它。
If you wish for me to add additional features, you can open an Issue, but I may not necessarily notice it.

## 计划表 planned feature list

+ [x] 读取和存储`.adofai`文件。    Read and store `.adofai` files.
+ [x] 旧版本`.adofai`文件向新版本的转化。    Conversion of old version `.adofai` files to the new version.
+ [ ] 两次打击之间经过的角度与`.adofai`角数据的互相转化。    Conversion between the angles passed between two hits and the .adofai angle data.
+ [ ] 两次打击之间经过的时间和角度的互相转化。    Conversion between the time and angles passed between two hits.
+ [ ] 一定频率范围内对`.wav`文件的踩音。    Beat matching of `.wav` files within a certain frequency range.
+ [ ] 对于手动录制的内容进行踩音。    Beat matching for manually recorded content.
+ [ ] 谱面的模块化，即可以通过添加模版的方式批量制造同一种东西。（这点可能需要把旋转和倍速也记录下来）    Modularization of the chart, which means that the same thing can be mass-produced by adding templates. (This may require recording rotations and speed multipliers as well.)
+ [ ] 在不改变实际打的谱子的情况下去除倍速。    Remove the speed multiplier without altering the actual chart.
+ [ ] 在不改变实际打的谱子的情况下去除旋转。    Remove rotations without altering the actual chart.
+ [ ] 播放器（实际上我认为没什么必要，因为用官方的编辑器可以很方便的重新打开一个文件（只需要两次点击！））    Player (actually, I don't think it's very necessary because the official editor can easily reopen a file with just two clicks!)
+ [ ] 歌的延迟分析和bpm分析（纯属多此一举，绝对不是因为我写不明白）    Delay analysis and BPM analysis of a song (totally unnecessary, definitely not because I can't figure out how to write it)
+ [ ] 输出每次打击的时间（或许画到一张Matplotlib图上？）    Output the time of each hit (perhaps plot it on a Matplotlib graph?)
