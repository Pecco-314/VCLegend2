# VCLegend2
用于爬取若干组B站视频的播放量，并以文件形式保存。可以快速生成每日简报（包括播放量、增量、达到目标预计天数）。

### 配置文件config.txt的使用：
* Group <Name>：添加组名为Name的新组
* Goal <Views> ：设置当前组的目标为Views
* Congrats <String>: 设置当前组的祝贺语为String，对于已达到目标的视频而言，在简报中预计天数一项会被替换为祝贺语
* Video <Name><Av>：为当前组添加名为Name且av号为Av的视频
