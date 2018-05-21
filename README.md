## openresty upstream 动态调度


```
export addr=$IP:$PORT
```

#### group
```
创建group

curl -X PUT $addr/api/group/test_group

删除group

curl -X DELETE $addr/api/group/test_group

查看所有group

curl -X GET $addr/api/group
```

#### openresty
```
创建openresty

curl -X PUT $addr/api/openresty/test_group/127.0.0.1/80

删除openresty

curl -X DELETE $addr/api/openresty/test_group/127.0.0.1/80

获取组内所有openresty

curl -X GET $addr/api/openresty/test_group
```

#### project 
```
创建project

curl -X PUT $addr/api/project/test_group/test_proj

删除project

curl -X DELETE $addr/api/project/test_group/test_proj

获取组内所有project

curl -X GET $addr/api/project/test_group
```

#### environment
```
创建项目的环境

curl -X PUT $addr/api/enviroment/test_group/test_proj/test_env

删除项目的环境

curl -X DELETE $addr/api/enviroment/test_group/test_proj/test_env

获取项目所有环境

curl -X GET $addr/api/enviroment/test_group/test_proj

```

#### upstream
```
为环境添加upstream

curl -X PUT $addr/api/upstream/test_group/test_proj/test_env/127.0.0.1/9031

删除upstream

curl -X DELETE $addr/api/upstream/test_group/test_proj/test_env/127.0.0.1/9031

查看环境中所有upstream

curl -X GET $addr/api/upstream/test_group/test_proj/test_env
```

#### 灰度和特殊环境设置
```
设置项目的环境uid尾数灰度比例(总和必须为100，环境名称必须全，否则报错)

curl -X POST $addr/api/enviroment/test_group/test_proj -d 'test_env1=10&test_en2=20&test_env3=30&test_en4=40'

设置项目的特殊环境名称(名字必须在该项目的环境中，特定uid的走特殊环境)
清空项目的特殊环境(不传环境名即可)

curl -X PUT $addr/api/special_env/test_group/test_proj/test_env2

设置无uid环境名称(名字必须在该项目的环境中，无uid的请求走此环境, 同步配置前必须设置)
curl -X PUT $addr/api/no_uid_env/test_group/test_proj/test_env3

设置项目走特殊环境的uid

curl -X PUT $addr/api/special_uid/test_group/test_proj/123,456,789

清空项目走特殊环境的uid(与上个api一样，不传uid即可)

curl -X PUT $addr/api/special_uid/test_group/test_proj/
```

#### 同步配置
```
同步组中指定项目的配置

curl -X POST $addr/api/config/test_group/test_proj
```

#### 健康检查
```
curl -X GET $addr/api/health
```