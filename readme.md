# My Django template

## 启动
```shell
# 重载 uvicorn 的 worker 获得更好的性能
gunicorn -c deploy/run.py skill_test.asgi:application
```

## 改进
```shell
- 集中apps管理及自定义app生成模板
- 数据库链接池
- 对model.Model进行改进
- 分app分库
- 加强的migrate命令
- 环境变量启动
- hashid集成
- commit规范集成
- 提供常用方法集
- 提供更多单测工具
```

## 性能分析
```shell
# 实时
sudo py-spy top --pid 17010 --idle --gil --subprocesses
# 火焰图
sudo py-spy record --pid 17010 --idle --gil --subprocesses
```

## 清理迁移文件
```shell
cd apps

lists=$(ls)
for i in $lists;do
	ls -d $i/migrations/* | grep -v '__init__.py' | xargs rm -rf
done
```
