--配置文件
settings = {}

settings.update_config_path = '/usr/local/etc/openresty/lua/xulb/xulb_update_config.json' --用于更新存放部分配置的文件
settings.total_config_path = '/usr/local/etc/openresty/lua/xulb/xulb_total_config.json' --存放所有配置的文件，用于重启后加载配置
settings.worker_sync_config_intval = 2 --woker检查配置更新的时间间隔
settings.healthcheck_url = '/healthcheck' --所有服务的健康检查接口
settings.office_ip_map = {}
settings.node_pause_time = 3 --多少秒内请求失败node_max_failes次，就不调度到这个节点
settings.node_freeze_time = 60 --发生严重错误禁用节点后，多长时间内不能访问
settings.node_max_failes = 10 --失败多少次后不调度到这个节点

return settings