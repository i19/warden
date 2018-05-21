--日志
--参考：https://github.com/openresty/lua-nginx-module#nginx-log-level-constants

local log = {}

function log:debug(log_info)
    ngx.log(ngx.DEBUG, log_info)
end

function log:info(log_info)
    ngx.log(ngx.INFO, log_info)
end

function log:warning(log_info)
    ngx.log(ngx.WARN, log_info)
end

function log:error(log_info)
    ngx.log(ngx.ERR, log_info)
end

return log