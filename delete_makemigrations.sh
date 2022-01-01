#!/bin/bash

# 删除所有迁移文件
cd apps

lists=$(ls)
for i in $lists;do
	rm -f $i/migrations/000*.py
done
