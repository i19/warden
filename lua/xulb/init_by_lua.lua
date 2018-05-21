local Config = require('xulb.model.config')
local NgxSharedDict = ngx.shared.xulb_dict

--尝试从文件加载配置
local err = Config:load_config()
if err ~= nil then
    ngx.log(ngx.ERR, '[init_by_lua_file] load config from file failed:'..err)
    return
end
ngx.log(ngx.INFO, '[init_by_lua_file] load config from file succed')

--将配置，版本信息写入共享内存
NgxSharedDict:set('raw', Config.raw)
NgxSharedDict:set('version', Config.version)
ngx.log(ngx.INFO, '[init_by_lua_file] write raw, version info to shared dict succed')