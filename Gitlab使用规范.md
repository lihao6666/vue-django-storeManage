---
title: Gitlab使用规范
date: 2019-12-20 18:39:12
tags: git
categories: 神奇操作
top: 82
---

## Gitlab使用规范

### 一、Git使用

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

# 检查是否有文件未提交

git status

# 查看修改未提交文件的差异

git diff [文件名]

# 查看提交历史

git log

