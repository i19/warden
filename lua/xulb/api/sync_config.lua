-- 处理同步配置的请求

local Util = require('xulb.agileutil.util')
local Settings = require('xulb.settings')
local NgxSharedDict = ngx.shared.xulb_dict

--获取post参数
ngx.req.read_body()
local args, err = ngx.req.get_post_args()
local info = ''
if not args then
    info = '[sync_config] get post args failed:' .. err
    ngx.log(ngx.ERR, info)
    ngx.say(info)
    return
end

local config_str = args['config']
if config_str == nil then
    ngx.log(ngx.ERR, '[sync_config] param config is nil, invalid request')
    ngx.say('[sync_config] invalid request')
    return
end
ngx.log(ngx.DEBUG, '[sync_config] config str:'..config_str)

--写入到文件
err = Util:put_file_content(Settings.update_config_path, config_str)
if err ~= nil then
    info = '[sync_config] write config str to file failed:' .. err
    ngx.log(ngx.ERR, info)
    ngx.say(info)
    return
end
ngx.log(ngx.INFO, '[sync_config] write config to file succed')

--写入共享内存
NgxSharedDict:set('raw', config_str)
NgxSharedDict:set('version', Util:timestamp())
ngx.log(ngx.INFO, '[sync_config] write config to shared dict succed')

ngx.print('ok')