# flutterCheckResource
Flutter项目中无用图片的检测及清理

## 一、背景
随着项目规模或者迭代周期的增加，项目中会保留部分已经不在使用的图片，这些资源的存在，会增加包体积。
在优化app大小时，常采用的手段之一就是对不在使用的图片进行清理。

## 二、原理
在flutter中使用asset中的图片的时候，都是根据图片路径加载图片，如：Image.asset(“assets/account/watsapp.png”),
根据图片的这样使用方式，我们就可以使用图片的名字或者图片的相对路径（assets/account/watsapp.png），在dart文件中搜索，如果在dart文件中我们找到该匹配的字符串，我们就认为该图片已经存在。
【也存在误判的情况，我们在异常说明这部分中解释说明，也欢迎大家补充】

## 三、实现方法

使用Python，获取项目中所有添加的图片绝对路径，并用存储到List中，然后读取dart文件，看在dart文件中是否存在与图片名称（watsapp.png）或者图片相对路径（assets/account/watsapp.png）相同的字符串，如果找到匹配的字符串，就认为图片在项目中使用，然后将图片地址从集合中移除，分析完所有dart文件，最后还在集合中的图片就可以认为是项目中已经不在使用的图片。
