# MiMac
Medical Image Management&amp;Assistant Center

医学影响管理辅助中心

## 序

这是的我毕业设计，一个`在线`的`图像管理`平台，

此外，它的设计初衷是针对医学图像在线标注的。医学影像和普通的图像还不一样，如果想作为输入数据输入到深度学习模型中，我们除了图像本身，还需要应用于该图像的高质量标签。普通的图像除了科研人员外没有被标注的动机。但是医学图像不同，它诞生的目的就是被"打标签"，不论我们是否收集，这个信息都会产生。随着计算机视觉的发展，其应用在医学辅助诊断方面的需求日益迫切。这个平台就是为了收集、整合、利用这些数据而存在的。
  - （虽然医学图像的格式（dicm什么的）前期应该都支持不了，而且医学图像都很大，不适合做成在线管理）
    - 好在我们不关心图片本身，我们更关心肉眼可以看到的尺度，就允许我们不使用原图而是对他进行压缩后才进行后续处理

/Users/megvii 是我的家目录，请全局替换所有配置文件和代码中的该字符串为自己环境的位置

使用前请把 src/settings/base.py 目录中 mimac_default 改为适合你自己的合适的值

## 快速开始
```bash
# 确保自己在项目根目录 
cd ~/MiMac
# 启动celery
supervisord -c deploy/supervisor.conf

cd src
python manager.py resetall  # 建立数据库
python manager.py runserver  # 启动服务在 127.0.0.1:22232

# 更新数据库
python manager.py db init
python manager.py db migrate
python manager.py db upgrade


# 不优雅的关闭celery的方法
ps -ef| grep "celery" |grep -v grep| cut -c 7-11 | xargs kill -9
ps -ef| grep "superv" |grep -v grep| cut -c 7-11 | xargs kill -9
sudo unlink /tmp/supervisor.sock
```

## celery demo

```
cd logs
tail -f *
```

```
cd src
python manager.py runserver
```

访问 
127.0.0.1:22232/api/audits/1

观察celery log的变化

