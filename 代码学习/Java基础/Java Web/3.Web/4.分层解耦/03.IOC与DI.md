## 分层解耦
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772812812014-2fd6c7f5-f203-4f8f-8b81-7d5cd714663a.png?x-oss-process=image%2Fformat%2Cwebp)

低耦合是要降低各个层之间的依赖关联程度，要实现解耦就不能new对象

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772813180114-b62e5d9f-21a8-41d2-8830-a05a590d5bf4.png)

## IOC与DI介绍
**控制反转IOC**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772813247016-4f43dbd9-6fee-4653-bbdd-6cc70d8af992.png)

**依赖注入DI**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772813268063-fe4d343c-a743-413d-add1-e210d9636b3f.png)

**Bean对象**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772813295315-43aea932-884a-428f-b3b7-74cb7a609546.png)

### IOC
`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">@Component</font>`、`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">@Controller</font>`、`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">@Service</font>`、`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">@Repository</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">这四个注解表示把类交给IOC容器管理</font>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772857717680-95670c6d-1881-4576-95c6-d5dda1e7778e.png)



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772857858709-a6246e08-7d6b-405a-a86e-4d95d15dcdc3.png)

### DI详解
`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">@Autowired</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">注解实现从IOC容器中找到该类型的bean，然后完成依赖注入</font>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772859008637-24788968-59ba-4349-8d29-803908a2c99d.png)

构造函数和属性的注入方法使用较多

#### 多个同类型bean的解决方案
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1772859460344-09fe6b03-161f-4826-8d33-ba143f08b642.png)

