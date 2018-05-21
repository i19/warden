# Changelog

### 新增
- api-server，同步配置前对openresty, env, env中upstream节点数，env比例等诸多检查， environment支持自定义指定
- lua 配置更新、合并模块
- 基于uid尾数比例的动态分配调度；指定uid 特殊environment的调度；无uid的调度
- 被动检查
- 在nginx之外的主动检查