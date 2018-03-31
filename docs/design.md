# 设计初稿

## 后端

### 用户

#### Service
- Register
- Login
- Logout
- FindPassword
- OAuth2 (op)
#### MySQL
- username
- password
- uid
  - 顺次增加
  - 和当天的日期一起加盐md5编码，生成当日有效的邀请码
- father_uid
- email
- tel
- data
#### tmpData
- token
- 
### 组织
#### MySQL
- gid
### 文件
- 图片文件
- 标注文件
#### Service
- 上传
- 下载
- 删除
- 重命名
  改变filename不改变uri
- 分享
  - 文件本身不会增加，“可编辑uid” append一份
- 给予副本
  - 文件本身不会拷贝，uri不变，生成新的fid
#### MySQL
- uri
- fid
- filename
- filetype
- owner_uid
- open_level
  - 0 不能被分享
  - 1 只能owner分享
  - 2 任何uid_list中的人可以分享
- uid_list
  - 
- disabled
  - 可能被我从后台禁掉

### 消息
#### MySQL
- iid
- from
- to
- timestamp
- next
- data




























