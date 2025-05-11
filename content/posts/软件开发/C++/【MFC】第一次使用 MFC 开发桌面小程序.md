---
categories:
- 软件开发
date: 2022-04-23 18:15:14.208366
draft: false
id: mfc
tags:
- c++
- mfc
- 软件开发
title: 【MFC】第一次使用 MFC 开发桌面小程序
url: posts/mfc
---

# 闲话

2020WUHAN，闲在家没事做，之前也用C语言写了一个小的游戏脚本，只有黑框框，趁这个时间就想给它弄个界面出来。

笔者其实只有非常粗略的编程技术，仅仅略懂C语言和Java。游戏脚本需要非常精准的时间控制函数，而且需要模拟键盘输出，响应键盘输入，运行在windows上，考虑到java的效率问题，选择了C++进行开发。

听说QT和MFC都不错，其实也考虑过imgui，但是那个教程资源很少，有也基本都是英文的，看起来着实费劲。
#### QT
感觉qt很适合新手，折腾了一番，没一天的时间就把界面折腾出来了，也基本完善了所有功能。但是，qt很不靠谱！做好了程序没法导出exe。用windeployqt工具导出错，查了一下，貌似是现在的版本5.14.0，有这个bug，没法导出。

<!-- more -->

卸了，装上5.13.3，可以成功导出。但是！我是高分屏，5.13.3界面会自动启用win10缩放，而且禁用缩放也没用。这导致编辑gui的界面被放得过大，不仅操作不方便，而且生成的程序窗口大小和那个不一致，放大ui也不放大字体。5.13.3也不能用。

各种难受。（刚看了眼，5.14.1发布了，想来是可以导出程序了，但怎么说，这种开源项目，出这种莫名其妙的bug，其实很难受。弃了）

#### MFC
听说mfc并不适合新手，确实，但是，visual studio 2019 为mfc 开发提供了很多便捷操作，查查资料，其实并没有那么难（笔者可是0基础，C++都是现学的）

vs2019 提供了哪些便捷操作呢？拖放编辑UI（这个和qt一样），类向导可以直接添加消息函数、重载函数，全图形交互式操作（这就不叫敲代码了吧……一键添加代码？）

当然，比起来MFC还是更难，但是mfc发展至今，资料也非常多，常见问题都能找得到，且微软不会像qt这样出一些莫名其妙的bug，mfc发展非常完善。vs2019也比qt creator好用得多（开发qt时我用的vscode写代码），调式功能非常不错，不像qt，出个错误又没有提示信息，有时候摸不着头脑。

# 学习c++
[菜鸟驿站](https://www.runoob.com/)

非常棒的网站，快速学习主要知识，直接上手，不懂的地方再找资料细看。

# 学习mfc开发
[VC驿站](https://www.cctry.com)

里面有很多C++相关的教程，笔者专注于看MFC开发那一块。

[实用VC++编程之玩转控件](https://www.bilibili.com/video/av38392055)

站长在b站上发的mfc教程视频，非常详细，讲解也很清楚。

# mfc小程序需要学哪些

仅对于笔者需要的功能来说啊：

 - 创建对话框
 - 使用按钮、文本框、Spin、ComboBox等基础控件
 - 控件设置
 - 添加控件响应
 - 添加菜单
 - 禁止对话框窗口缩放
 - 重载函数使得F1，Esc，Enter键失效
 - 弹出第二个窗口
 - 注册全局热键
 - 读写文件

 一一说来。

#### 创建对话框程序
使用vs2019模板创建即可，运行，弹出一个窗口。

 - ***基于对话框 + 无增强的MFC控件 + 在静态库中使用MFC***

没有mfc模板可能是没有装这个组件，百度即可。具体创建跟着vc驿站的教程视频来。

#### 添加控件
图形交互式操作

设置控件变量名：***右键控件——添加变量——设置名称***
（变量名更易于自己识别，编写控件事件更方便）

#### 添加响应

 ***- 右键控件——添加事件处理程序——选择类列表：CXXXDlg——更改函数名——选择事件类型***

下面有事件说明，大多数时候默认事件是最合适的

添加完成后，会直接跳转到cpp文件中，函数声明、创建，vs2019全部为你做好了，直接在里面添事件代码就行。
#### 控件设置
###### Spin Control

```cpp
	//设置DamageA和DamageB的Spin
	UDACCEL aclA, aclB;
	aclA.nInc = 2;
	aclB.nInc = 10;
	m_Spin_DamageA.SetRange(0, 9999);
	m_Spin_DamageA.SetAccel(2, &aclA);
	m_Spin_DamageA.SetBuddy(GetDlgItem(IDC_EDIT1));

	m_Spin_DamageB.SetRange(0, 9999);
	m_Spin_DamageB.SetAccel(2, &aclB);
	m_Spin_DamageB.SetBuddy(GetDlgItem(IDC_EDIT2));
```
说明：
 - m_Spin_DamageA 是编辑框的变量名
 - SetRange 设置 Spin 范围
 - SetAccel 设置 Spin 步长，就是点一下增加 / 减少多少
 - SetBuddy 将 Spin 与编辑框联系在一起
 - 注意在资源视图设置 Alignment 属性为 Right ——右附加

 ###### Edit Control

设置编辑框在只读状态时，不显示光标，但也能完成复制操作

```cpp
//处理使Edit控件在只读状态下不显示光标
void CAutoCCMFCDlg::OnEnSetfocusEdit()
{
	// TODO: 在此添加控件通知处理程序代码

	//间接判断Edit控件是否为只读状态
	bool ifReadOnly = (m_ComboBox.GetCurSel() <= 4);
	//隐藏Edit光标
	if (ifReadOnly)
	{
		m_Edit_DamageA.HideCaret();
		m_Edit_DamageB.HideCaret();
	}
}
```

 

#### 添加菜单

 ***- 资源视图——右键项目——添加资源——菜单——新建***

编辑菜单的操作和QT一致。其实更好，vs2019可以直接输入中文，qt不行，只能直接粘贴进去。

#### 为菜单添加事件
与为控件添加响应，操作基本一致

#### 弹出第二个窗口
参考

[MFC实现窗口跳转](https://blog.csdn.net/qq_15029743/article/details/80467194)

添加完成后，运行会报错（这应该是也属于莫名其妙的bug了吧……）

参考这个，注释掉那个声明就行了

[error LNK2005](https://blog.csdn.net/caoshiying/article/details/52168078)

#### 禁用F1，Esc，Enter
默认mfc对话框程序，按F1弹出帮助文档，按Esc和Enter自动退出程序。这不行，得禁用。

有个 PreTranslateMessage() 的方法，我觉得不得行，这等于说把这三个键直接禁用了，类似于热键之类的，都不能使用了，感觉不合理。

只需要禁用三个键的响应函数即可，具体方法是重载这些函数。

```cpp
//重载OnOK使其失效
void CAutoCCMFCDlg::OnOK()
{
	// TODO: 在此添加专用代码和/或调用基类

	//CDialogEx::OnOK();
}

//重载OnCancel使其失效
void CAutoCCMFCDlg::OnCancel()
{
	// TODO: 在此添加专用代码和/或调用基类

	//CDialogEx::OnCancel();
}

//重载onclose使点击X按钮时关闭窗口
void CAutoCCMFCDlg::OnClose()
{
	//EndDialog(IDCANCEL);	//关闭窗口
	//CDialog::OnClose();
	CDialog::OnCancel();
}

//重载OnHelpInfo函数处理WM_HELPINFO消息使其失效
BOOL CAutoCCMFCDlg::OnHelpInfo(HELPINFO* pHelpInfo)
{
	// TODO: 在此添加消息处理程序代码和/或调用默认值

	//return CDialog::OnHelpInfo(pHelpInfo);
	return true;
}
```
注释应该比较详细。

 - OnOK() 是响应Enter键的，重载它使其失效。 
 - OnCancel() 是响应Esc键的。 
 - OnClose()  重载上面两个函数之后，程序不仅按Esc、Enter不退出，点击关闭的红叉叉也不退出，只能通过任务管理器退出了。重载这个函数，使得关闭按钮可用。
 - OnHelpInfo() 重载WinHelp() 函数没用，必须重载这个，它才是响应F1的。

 如何添加这些函数？当然你也可以去声明，然后添加函数体。但对于新手，可不知道这些需要添加哪些函数才能满足需求。

还是类向导，选择类名 CXXXDlg。

 - OnOK() 和 OnCancel() 是添加虚函数。
 - OnClose() 和 OnHelpInfo() 是添加消息处理事件，分别是WM_CLOSE 和 WM_HELPINFO 。

下面都有事件和虚函数介绍，很方便新手查看选择。一键添加。

#### 注册全局热键
窗口初始化处添加，注册热键
```cpp
RegisterHotKey(GetSafeHwnd(), 9, MOD_CONTROL, VK_F2);
```
这里注册的是Ctrl + F2。

 - 第一个参数——获得窗口句柄
 - 第二个参数——不知道是干什么用的，笔者随便添了一个数字都行
 - 第三个参数——MOD_CONTROL 代表 Ctrl，还有其他几个参数，代表Win，Alt 之类的。
 - 第四个参数——按键Acall码

 然后
 - ***类向导——消息——WM_HOTKEY***

 添加事件代码

 

```cpp
/**
 * 响应全局热键
 *
 */

void CAutoCCMFCDlg::OnHotKey(UINT nHotKeyId, UINT nKey1, UINT nKey2)
{
	// TODO: 在此添加消息处理程序代码和/或调用默认值

	if (nKey2 == VK_F1)
	{
		//视为"启用"按钮被点击
		OnBnClickedButtonStart();
	}
	else if(nKey2 == VK_F2)
	{
		//视为"禁用"按钮被点击
		OnBnClickedButtonEnd();
	}

	CDialog::OnHotKey(nHotKeyId, nKey1, nKey2);
}
```
nKey1 代表 Ctrl，nKey2 代表F1、F2，直接用 == 判断即可，实现识别多个热键。

#### 禁止窗口缩放
简单有效

[禁止窗口缩放
](https://blog.csdn.net/DSQ235612/article/details/90257157)

#### 读写文件
配置信息都存储在类中，写入txt文件很简单，读取叫我很难了。看了一篇文章，直接写入类，什么都不用管，到时候读取类就行了。

[C++二进制文件的读取和写入](https://blog.csdn.net/u013693952/article/details/93194350)

emmm，我是直接C过来的，代码基本一致……感谢……

# 使用Git
实在是太有用了，虽然只有我一个人开发，但是。可以回退版本太棒了！

开发过程中出了点问题，窗口初始化会报错，貌似是内存泄露。怎么都找不到原因，幸好我两小时前建立了新分支。回退，比较，重写。太方便了……当然能找出错误更好，笔者这不是找不到嘛……

# GitHub
文件很多，代码贴不了。传到GitHub上了。

[AutoCC](https://github.com/vksir/AutoCC_MFC)

# 还使用了哪些API
（这应该叫什么，感觉叫功能不合适，API合适吗？还是叫技术？技术太高大上了吧。）
#### 多线程
std::thred 比 pthread 使用方便太多，就是没有 pthread_cancel() 功能。

另外，假如一个函数使用 std::tread 创建了一个线程，该函数结束后，线程也会被终止。而使用 pthread 创建一个线程后，函数结束，线程并不会被终止，它还会继续运行下去。

想要 std::tread 达到 pthread 这种效果，需要再线程创建后使用 detach() 函数，分离线程。

vs2019 并不支持 pthread，而有的版本的 mingw64 也不支持 std::tread，很难。
#### 按键映射

```cpp
#include <Windows.h>

//检测E键是否被按下
GetKeyState('E') < 0
//模拟Q键按下
keybd_event('Q', 0, 0, 0);
//模拟Q键弹起
keybd_event('Q', 0, KEYEVENTF_KEYUP, 0);
```
仅windows下生效

#### 精准延时

```cpp
#include <windows.h>

//精度极高的计时器
double GetTickCountH()
{
	__int64 Freq = 0;
	__int64 Count = 0;
	if(QueryPerformanceFrequency((LARGE_INTEGER*)&Freq)
		&& Freq > 0
		&& QueryPerformanceCounter((LARGE_INTEGER*)&Count)) {
		//乘以1000，把秒化为毫秒
		return (double)Count / (double)Freq * 1000.0;
	}
	return 0.0;
}
//高精度延时，占用CPU极高
void delayHigh(double dMilliseconds) 
{
	__int64 nFreq = 0; //频率
	__int64 nStart = 0; //起始计数
	if(QueryPerformanceCounter((LARGE_INTEGER*)&nStart)
		&& QueryPerformanceFrequency((LARGE_INTEGER*)&nFreq)
		&& nFreq > 0) {
		__int64 nEnd = 0; //终止计数
		double k = 1000.0 / (double)nFreq; //将计数转换为毫秒
		while(1) {
			QueryPerformanceCounter((LARGE_INTEGER*)&nEnd);
			if(dMilliseconds <= (double)(nEnd - nStart) * k) {
				break;
			}
		}
	}
}
//精度稍低，占用CPU低
void delayLow(double dMilliseconds) 
{
	HANDLE hTimer = CreateWaitableTimer(NULL,TRUE,NULL);
	if(hTimer) {
		__int64 nWait = -(__int64)(dMilliseconds * 10000.0);
		SetWaitableTimer(hTimer,(LARGE_INTEGER*)&nWait,0,NULL,NULL,FALSE);
		WaitForSingleObject(hTimer,INFINITE);
		CloseHandle(hTimer);
	}
}

//综合上两种方法的优点，精度高，占用CPU低
/**
 * q为延时精度，设置为20能达到和delayHigh一样的效果
 * q值越小，占用CPU越低
 * 设置为17能取精度和CPU之前的最佳平衡
 * 
 */
void delayHL(double dMilliseconds, int q) {	
	__int64 nFreq = 0; //频率
	__int64 nStart = 0; //起始计数
	if(QueryPerformanceCounter((LARGE_INTEGER*)&nStart)
		&& QueryPerformanceFrequency((LARGE_INTEGER*)&nFreq)
		&& nFreq > 0) {
		__int64 nEnd = 0; //终止计数
		double k = 1000.0 / (double)nFreq; //将计数转换为毫秒
		delayLow(dMilliseconds - q);
		while(1) {
			QueryPerformanceCounter((LARGE_INTEGER*)&nEnd);
			if(dMilliseconds <= (double)(nEnd - nStart) * k) {
				break;
			}
		}
	}
}

//外置指针，计时器
class Timer {
    public:
        Timer();                                 
        void setPoint();
        bool ifTimeUp(double dMilliseconds);
        double howLong();
    
    private:
        __int64 nStart;
        __int64 nFreq;
        __int64 nEnd;
        double k;
};

//初始化
Timer::Timer() {
	setPoint();
}

//设置时间起点
void Timer::setPoint() {
	QueryPerformanceCounter((LARGE_INTEGER*)&nStart);
	QueryPerformanceFrequency((LARGE_INTEGER*)&nFreq);
	k = 1000.0 / (double)nFreq;
}

//判断是否超时
bool Timer::ifTimeUp(double dMilliseconds) {
	QueryPerformanceCounter((LARGE_INTEGER*)&nEnd);
	return dMilliseconds <= (double)(nEnd - nStart) * k;
}

//返回经过时长
double Timer::howLong() {
	QueryPerformanceCounter((LARGE_INTEGER*)&nEnd);
	double count = (double)(nEnd - nStart) * k;
	setPoint();
	cout << "How Long: " << count << endl;
	return count;
}
```
参考了

[Windows高精度时间](https://www.cnblogs.com/hanford/p/6163676.html)

事实上delayHigh太耗CPU了，只能短时间使用，而delayLow的误差到达了0~17ms，有点大。
在这两个基础上，定义了delayHL，高精度且占用CPU低，误差不超过0.5ms。

#### Tips
###### extern
extern可以跨文件，共用一个变量，同一个值。

在头文件中

```cpp
extern int a;
```
在源文件中

```cpp
int a;
```
然后其他文件引用这个头文件，就可以调用这个变量了。

###### static
static 不能跨文件，可以在不同文件中都定义同一个变量名的变量，但不同的文件中，这个变量的值不同。

不要在头文件中定义static，没有意义，且很多个头文件定义了相同变量名的 static ，会报错。在源文件中定义就好了。其他文件如果要用，再定义一遍，相同变量名也无所谓。

在不同文件定义相同变量名的变量，会报错，加上  static 即可。

#### 函数引用调用
改变传入的参数的值。

对比起指针函数，感觉引用函数写法更简单，用起来也简单。

参考

[函数引用调用](https://www.runoob.com/cplusplus/cpp-function-call-by-reference.html)

也可以在外部定义变量，然后函数中直接调用变量，改变变量值。但想来这样开发并不严谨，小程序可以这么干，大项目开发应该不得行。

# 还有什么功能没有实现
###### 程序图标
做一个ico文件替换掉那个初始图标就行，笔者还没来得及做。

###### 是最小化窗口到控制台
有点麻烦，感觉也不是很必要，不做了（主要是有了新的“玩具”，不想再玩MFC了）

###### 设置字体
告辞。
真的很麻烦，对比起Qt设置字体，mfc设置字体简直太难。![AutoCC程序截图](https://img-blog.csdnimg.cn/20200131021102552.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTA0NjM5MA==,size_16,color_FFFFFF,t_70)
这个彩色 AutoCC 是怎么回事儿呢？

在 word 里面设置字体样式，截图，然后导入到图片控件？

不不不，mfc没有那么智能，它不会自动缩放图片大小。貌似要实现自动缩放图片大小也很难，需要绘制图片吧。我选择放弃！

截图，然后用ps改变图片大小，再导入……

# 这个程序是做什么的
忍者必须死，一键连招，游戏脚本

# 新玩具
Electron！

这个貌似适用性好，界面美观，跨平台，Vs code就是用它写的。

只做界面，还能调用C++库？

效率 + 美观

2020WUHAN还有很久吧……就学这个了！

# VS2019 上的 One Dark Pro
![VS2019 One Dark Pro](https://img-blog.csdnimg.cn/20200131024950350.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTA0NjM5MA==,size_16,color_FFFFFF,t_70)
偏冷色调，更加冷静，感觉比 vs code 上的花花绿绿的 One Dark Pro 更漂亮。但我也不知道怎么弄过去啊……Orz

字体是JetBrains Mono，支持连字符，Consolas用多了找点新鲜感。

End
