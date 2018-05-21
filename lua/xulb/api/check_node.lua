local InvalidNode = require 'xulb.model.invalid_node'

local check_node = {}

function check_node:check()
    local http_status = ngx.status
    local upstream_ip = ngx.ctx.upstream_ip
    local upstream_port = ngx.ctx.upstream_port
    
    if ngx.req.get_method() ~= "GET" and upstream_ip ~= nil and upstream_port ~= nil then
        if http_status >= 500 then
            InvalidNode:disable(upstream_ip, upstream_port)
            ngx.log(ngx.ERR, '[check node] disable node,'..upstream_ip..':'..upstream_port)
        end
    end
end

return check_node