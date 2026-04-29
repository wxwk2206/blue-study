## 一、初始化，配置，克隆
```bash
# 初始化本地仓库（在项目文件夹执行）
git init

# 查看当前配置
git config --list

# 设置用户名（全局）
git config --global user.name "你的名字"

# 设置邮箱（全局）
git config --global user.email "你的邮箱"

#记录访问远程代码库的密码
git config --global credential.helper store   

# 克隆远程仓库到本地
git clone 仓库地址
```

<!-- 这是一张图片，ocr 内容为： -->
![569](https://cdn.nlark.com/yuque/0/2026/png/62702379/1776822586018-c1392986-16cd-4b71-8d49-18466280fbda.png)

## 二、日常提交（常用）
```bash
# 查看文件状态（最常用！）
git status

# 添加单个文件到暂存区
git add 文件名

# 添加所有修改/新增文件
git add .

# 提交到本地仓库（必须写备注）
git commit -m "提交说明"

#  add + commit 一步完成（只对已跟踪文件生效）
git commit -am "提交说明"

#查看所有的提交历史
git reflog

#查看当前版本之前的提交历史
git log

# 查看简洁提交日志
git log --oneline

# 查看图形化分支+日志
git log --graph --oneline --all
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/62702379/1776826056043-5e397b5a-67a5-4a6c-a3da-b4d449264107.png)

## 三、远程仓库操作（GitHub）
```bash
# 关联远程仓库
git remote add origin 仓库地址

# 查看远程仓库
git remote -v

# 拉取远程最新代码（不自动合并）
git fetch

# 拉取并合并远程代码（常用）
git pull

# 推送到远程仓库
git push origin main

# 第一次推送分支（绑定上游）
git push -u origin 分支名
```

## 四、分支操作
```bash
# 查看所有本地分支
git branch

# 查看本地+远程所有分支
git branch -a

# 创建新分支
git branch 分支名

# 切换分支
git checkout 分支名
# 或新版指令 
git switch 分支名

# 创建并直接切换到新分支
git checkout -b 分支名
git switch -c 分支名

# 合并指定分支到当前分支
git merge 分支名

# 删除本地分支
git branch -d 分支名
```

## 五、撤销 / 回退（非常实用）
```bash
# 撤销工作区修改（恢复到最近一次提交）
git checkout 提交id 文件名
git restore 文件名

# 撤销暂存区文件（回到工作区）
git reset HEAD 文件名
git restore --staged 文件名

# 回退到上一个提交（保留代码到工作区）
git reset HEAD^  (git reset --mixed HEAD^)默认为--mixed
# 回退到上一个提交（保留代码到暂存区）
git reset --soft HEAD^

# 彻底回退到上一个提交（丢弃所有修改，谨慎！）
git reset --hard HEAD^
```

## 六、储藏（临时保存未提交代码）
```bash
# 储藏当前修改
git stash

# 查看储藏列表
git stash list

# 恢复最近一次储藏
git stash pop

# 删除所有储藏
git stash clear
```

## 七、标签（版本发布）
```bash
# 创建标签
git tag v1.0

# 推送标签到远程
git push origin v1.0

# 查看所有标签
git tag
```

---

