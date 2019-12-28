---
title: Gitlab使用规范
date: 2019-12-20 18:39:12
tags: git
categories: 神奇操作
top: 82
---

## Gitlab使用规范

### 一、Git和Github关联

```

# ①查看本地是否有id_rsa和id_rsa.pub文件
# ②如果没有，运行下面命令
ssh-keygen  -t rsa –C "邮箱"
# ③ 打开id_rsa.pub(公钥)，复制内容，进入github添加ssh keys,将公匙内容复制到Key中

```

### 二、Git使用

#### 1、简单配置及命令

```

# 配置用户名和邮箱

git  config --global  user.email lh
git  config --global  user.name 1956413161@qq.com

# 初始化本地仓库(当前文件夹下会产生.git文件夹为本地代码仓库)

git init

# 克隆仓库

git clone http://.....

# 将文件添加到暂存区

git add [文件名]

# 将暂存区文件提交到仓库

git commit -m "备注信息"
git commit -a -m "备注信息" #将所有已跟踪文件中的执行修改或删除操作的文件都提交到本地仓库，不需要add
git commit --amend # 将修改合并到上一次提交中，就是不增加commit记录


# 检查是否有文件未提交

git status

# 查看修改未提交文件的差异

git diff [文件名] #默认是工作区与暂存区
git diff 

# 查看提交历史

git log
git log --pretty=oneline #显示主要内容

```
#### 2、Git版本回退

```
# 获取历史版本号

git reflog

# 回退到上一版本

git reset --hard HEAD^

# 回退指定版本号

git reset --hard [版本号] #版本号可以使用上面的命令查看

```

#### 3、分支管理

```

# 创建分支

git branch [分支名]

# 切换分支

git checkout [分支名]
git checkout -b [分支名] #创建并切换

# 分支合并

git merge [分支]

# 删除分支

git branch -d [分支名]

```
#### 4、文件推送到Github

```

# 关联Github仓库

git remote add origin [github仓库]

# 提交到Github仓库主分支

git push origin master # origin表示远程主机，master表示主分支

```