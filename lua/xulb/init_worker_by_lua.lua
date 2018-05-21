local Config = require('xulb.model.config')
local Settings = require('xulb.settings')
local NgxSharedDict = ngx.shared.xulb_dict

local function sync_config_timer()
    if NgxSharedDict:get('version') == nil then
      --'master not load config, worker not compare config version'
    else
      if Config.version ~= NgxSharedDict:get('version') then
        ngx.log(ngx.INFO, 'worker config version is diff, ready merge config')
        Config:merge_config()
        ngx.log(ngx.INFO, 'worker merger config finish')
      end
    end
    local ok, err = ngx.timer.at(Settings.worker_sync_config_intval, sync_config_timer)
    if not ok then
      ngx.log(ngx.ERR, '[init_worker_by_lua] create timer failed:'..err)
    end
end

local ok, err = ngx.timer.at(Settings.worker_sync_config_intval, sync_config_timer)
if not ok then
  ngx.log(ngx.ERR, '[init_worker_by_lua] create timer failed:'..err)
else
  ngx.log(ngx.INFO, '[init_worker_by_lua] create timer succed')
end