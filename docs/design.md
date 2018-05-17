# 设计
- doing  正在做的，太蠢了所以到现在还没做完
- done  已经完成的bug（bug里面藏代码说的就是我）
- todo 必须做的，完成所有的todo立马开始做
- pending  不重要或者有代替方案，完成所有的todo，就去做
- abandon  没空做啦QAQ，完成所有的pending就去做

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

### 文件 (doing)
```text
这里对于label文件特别说明一下，它和用什么预测算法应该是没有关系的，只和图片和图片所属的任务类型有关
结构应该是：
{
    'type':1001,
    'data':{
        'key':{
            0:'cat',
            1:'dog',
        },
        'value':0.2,
    }
}
type的取值范围在my_app.common.constant.ImageType
data里面的值通常是各种预定义和当前的值，比如这是一个有猫病的二分类，二分类还有另一种写法，见下
{
    'type':1001,
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
      - 预标注结束后，db里更新图像状态为 NORMAL
    - 一个是发送图片到远程高性能服务器：hiformance/GCP/AWS/Aliyun (pending)
      - 发送图片
      - 做完后访问一个本地的端口，告知成功
        - 本地需要新增一个API
      - 本地API被访问后，db里更新图像状态为 NORMAL
- 展示 (doing)
  - 图片压缩 (done)
  - 下载 (doing)
- 下载 (doing)
- 删除 (todo)
- 冻结 (todo)
- 重命名 (todo)
  - 改db的name字段 (todo)
- 标注 (todo)
  - 不同的任务类型会有不同的前端后端API，后端逻辑见后面的算法章节
- 分享 (pending)
  - 文件本身不会增加，“可编辑uid” append一份
- 给予副本 (abandon)
  - 文件本身不会拷贝，uri不变，生成新的fid
  
### 消息 (pending)
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
  - classification (doing)
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
  - 标注(todo)
    - 前端解析图片对应的label文件存储的信息作为初始值
    - 提交标注后修改图片对应的label文件
  - 训练(doing)
    - 按照配置的时间循环的进行训练
  - 预标注(doing)
    - 图片被上传的时候就会进行预测，把结果存入label文件

### Unittest （pending）

## 前端 (abandon)
- 我的前端跟`屎`一样我没啥想说的
  - 本来是想用iview的，暂时不想了，随缘吧
 
## 其他 (pending)
- 高可用
  - 自动化部署 (git-cli)
  - 容器 (docker)
- 高并发
  - 负载均衡 (nginx)
  - 分布式部署 (k8s)
- CDN
- AliyunOSS




















