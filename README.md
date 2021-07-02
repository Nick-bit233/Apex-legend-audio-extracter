
# 已修复MSD问题，现已可正常使用
感谢@Lyxica 
# APEX音频提取器0.2.4

基于MSD命令行提取器写的（简陋）GUI程序，用来提取APEX里的语音和音效
MSD的github地址：https://github.com/Lyxica/Miles-10-Sound-Dumper

-----------------------------
* 使用说明
1. 将release包里的MSD.exe文件拷贝到你的Apex游戏目录
（即r5Apex.exe所在的目录，steam端或橘子端均可）
2. 复制游戏目录地址，打开main文件夹中的Apex_audio_extracter.exe，粘贴或手动选择游戏目录地址，点击扫描，等待几秒
（默认音频保存地址可以不用修改，也可以选择为你要想存储音频缓存的位置）
3. 点击“读取音频列表”，然后双击某一项即可预览音频
   - 默认情况下，音频播放12段，请等待音频全部播放完毕后再关闭弹窗。
   - 按下esc可以快速跳过一段音频，连续按下4次esc强制终止所有的音频播放 
   - 右侧搜索栏用于按照规则搜索音频名称（不区分大小写）
* 【按照人物搜索对话语音，选择人物后会会读取若干动作，其中
	- bc一般为游戏中事件交互的语音（打药、缩圈、受到伤害等）
	- menu一般为开场语音
	- glad一般为台词语音
	- effort一般为人物动作音效
】
4. 点击下方按钮即可保存音频文件，提取完成后自动打开目录
-----------------------------
* Q&A
1. 怎么修改中文语音？
    * 两个方法
	1. 进入游戏目录下的\audio\ship文件夹，将general_english.mstr和general_english_path_1.mstr
文件移动到文件夹外的位置，重新打开提取器扫描即可（使用后记得将文件还原）
	2. 在\audio文件夹下新建文件夹，将“\audio\ship”文件夹中除general_english.mstr和general_english_path_1.mstr
的文件拷贝到新文件夹，并将“\audio\[新文件夹名]”填入“游戏音频文件路径”重新扫描
（好处是不用来回移动文件，但亲测音频文件大小约为10G，硬盘空间不足慎重考虑）

2. 语音播放不了怎么回事
    因为MSD的工作原理是利用游戏中事件代号激活语音，然后录制下来，因此要提取音频必须先播放录音，部分情况下由于其bug会无法播放，重试即可。由于游戏音频文件极其复杂，还有ttf2的废料，因此部分过短或无效的语音内容是空的

-------------------------------------
已修改：现在每次抓取可以获得12个语音，基本包含了所有语音的变种，但可能存在重复语音
-------------------------------------
已知的bug：
因为一次播放多个语音，若要取消请连续按多次esc
重复点击扫描和读取列表按钮可能导致播放语音时多个线程重叠播放，如要修改\audio源文件的位置，请重启程序再试


