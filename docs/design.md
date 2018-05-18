# 设计

## 开发规范

### 后端代码基于 pep8 规范进行编写

### todo_list 说明
- doing  正在做的，太蠢了所以到现在还没做完
- done  已经完成的bug（bug里面藏代码说的就是我）
- todo 必须做的，完成所有的 todo 立马开始做
- pending  不重要或者有代替方案，完成所有的 todo，就去做
- abandon  没空做啦QAQ，完成所有的 pending 就去做

### git_message 说明
- feat：新功能（feature）
- fix：修补bug
- docs：文档（documentation）
- drop: 删除文件
- test: 添加 UnitTest

## 后端

### 用户 (done)
- Register (done)
  - 创建用户 (done) 
  - 创建用户文件夹 (done)
- Login (done)
- Logout (done)
- FindPassword (abandon)
- OAuth2 (abandon)

### 组织(pending)
同一个组织可以方便的share文件
### 文件 (doing)
```text
这里对于label文件特别说明一下，它和用什么网络(VGG/CNN/restnet)应该是没有关系的，只和图片和图片所属的任务类型有关
结构应该是：
{
    'alg':1001,
    'data':{
        'key':{
            0:'cat',
            1:'dog',
        },
        'value':0.2,
    }
}
alg的取值范围在my_app.common.constant.ImageAlgorithm
data里面的值通常是各种预定义和当前的值，比如这是一个有猫病的二分类，二分类还有另一种写法，见下
{
    'alg':1001,
    'data':{
        'key':['cat', 'dog'],
        'weight':[0.2, 0.78],
        'value':1
    }
}
这里的 value 保存的是下标，从0开始计数
统一规定，这种写法属于多分类中分类数k = 2的情况
```
- 上传图片 (doing)
  - 选择文件所属的任务类型 (done)
    - 基类 (done)
    - 二分类 (done)
    - 二分类--有猫病 (done)
    - 多分类 (done)
    ...
  - 上传 (done)
  - 更新db，放入图像，关联用户，获得图像ID （文件处于待标注状态）(done)
  - 在该用户的文件夹下放置文件，uri为image_id.[type]  (done)
  - 为文件添加标注文件，uri为image_id.label（本质是json） (done)
  - 异步任务开始进行预标注（这里有两种实现策略） (doing)
    - 一个是本地跑 (doing)
      - 前提是单张图片本地预标注的时间控制在1分钟内 (doing)
      - 预标注结束后，db里更新图像状态为 DONE_LABEL
    - 一个是发送图片到远程高性能服务器：hiformance/GCP/AWS/Aliyun (pending)
      - 发送图片
      - 做完后访问一个本地的端口，告知成功
        - 本地需要新增一个API
      - 本地API被访问后，db里更新图像状态为 NORMAL
- 展示 (done)
  - 图片压缩 (pending)(函数ok了，待接入，感觉现在的方式不是很优雅)
  - 下载 (done)
- 下载 (done)
- 删除 (done)
- 冻结 (done)
- 重命名 (done)
- 标注 (done)
  - 不同的任务类型会有不同的前端后端API，后端逻辑见后面的算法章节
- 分享 (pending) (高优先级)
  - 文件本身不会增加，“可编辑uid” append一份
- 给予副本 (abandon)
  - 文件本身不会拷贝，uri不变，生成新的fid
  
### 消息 (pending) (高优先级)
- 给xxx发消息
- 显示消息
  - 为了加速，消息采用了并查集+链表进行设计
- 回复某条消息

### 文章 (pending)
- 发布文章
  - 如果文章过长，会存成链表的样子
- 编辑文章
  - 编辑内容
  - 删除
  - 冻结

### 算法 (doing)
- 算法
  - classification (done)
    - 二分类 (done)
      - VGG/rest-net
      - 可配置 (pending)
        - 类型的名称，(done)
        - 使用的算法，(pending)
        - 模型的uri，(done)
        - 训练间隔, (todo)
    - 多分类 (pending)
  - detection (pending)
    - 病灶识别
    - 异物识别
  - segmentation (pending)
    - 病灶分割
    - 器官分割
    - 血管分割
    - 细胞分割
- 行为(doing)
  - 标注(done)
    - 前端解析图片对应的label文件存储的信息作为初始值
    - 提交标注后修改图片对应的label文件
  - 训练(pending) (高优先级)
    - 按照配置的时间循环的进行训练
    - 训练的时候有个坑，
  - 预标注(doing)
    - 图片被上传的时候就会进行预测，把结果存入label文件

### Unittest （pending）

## 前端 (abandon)
- 我的前端跟`屎`一样我没啥想说的
  - 本来是想用iview的，暂时不想了，随缘吧
  - 写完论文后用 bootstrap 看情况美化一下吧

## 其他 (pending)
- 高可用
  - 自动化部署 (git-cli)
  - 容器 (docker)
- 高并发
  - 负载均衡 (nginx)
  - 分布式部署 (k8s)
- CDN
- AliyunOSS

















