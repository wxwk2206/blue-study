## String概述
String类，定义在Java.lang包下，无需导包。Java中所有字符串文字（例如“abc”）都为此类的对象

注意点：字符串的内容是不可变的，它的对象在创建后不能被更改，字符串拼接会产生一个新的字符串

## 创建字符串的方法
1. 直接赋值

```java
String s = "abc"
```

2. new +   public String（） 空白字符串不含任何内容

```java
String s1 = new String（）;
System.out.println（"1" + s1 "2"）;//12
```

3. new + public String（String original）根据传入的字符串，创建新的字符串对象

```java
String s2 = new String（s）;
System.out.println（s2）;//abc
```

4. new + public String（char[] chs）根据字符数组，创建字符串对象

```java
char[] chs = {'a','b','c','d','e'};
String s3 = new String（chs）;
System.out.println（s3）;//abcde
```

5. new + public String（byte[] chs）根据字节数组，创建字符串对象

```java
byte[] bytes = {97,98,99,100,101};
String s4 = new String（bytes）;
System.out.println（s4）;//abcde
//ASCII码表中，97对应a，98对应b...
```

**直接赋值与new关键字的区别**

直接赋值：代码简单，节约内存

字符串常量池，StringTable（串池）：用来存储字符串

直接赋值的方式获取字符串对象，此时存储在串池当中

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772018466341-a37e8d0a-23fc-42d8-bce7-35fe683c062b.png)<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772018576961-1d6bf697-6cb4-48a2-baba-789b15a299a1.png)

## 字符串中的常见操作
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772018712333-ba137cbe-bbe0-4516-bfb8-63b4bedd1c2f.png)

每一个字符串对应着一个成员方法

## 字符串中的常见成员方法
### 比较
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772019008523-b0912302-6183-48ff-aae7-b7d41556d736.png)

==号比较的是什么

基本数据类型：比较的是数据值

引用数据类型：比较的是内存地址

要比较引用数据类型中的数据要用到字符串比较方法

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772019302519-f14272c1-6b07-46e5-b6f7-7c77fc4e6f66.png)

### 遍历
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772023467005-a0df8b55-fb8d-4826-b47a-e2d774526eec.png)

### 截取
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772025472909-9046f1ab-cab5-4990-8654-c31ae5d3c32f.png)

！！！只有返回值才是截取之后的结果

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772025619846-5f0d51e9-c639-4d1e-9b97-9a4ef43f9171.png)

### 替换
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772025905064-56016690-cfeb-4834-9407-26f492838ff6.png)

## StringBulider
StringBulider是字符串的一个工具类，可以在拼接字符串的时候效率更高

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772026982980-628c0db6-937b-4c53-af47-f03562a81901.png)

### 构造方法
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772027160284-62f811c6-93fe-4fc4-b1f6-6ddf99cd8511.png)

### 常用方法
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772027205605-b2f6c52a-991b-4dd5-953d-3f0f7c6197c7.png)

