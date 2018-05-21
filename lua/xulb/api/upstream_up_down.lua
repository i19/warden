-- 处理主动检查upstream up/down请求

local InvalidNode = require 'xulb.model.invalid_node'

--获取post参数
ngx.req.read_body()
local args, err = ngx.req.get_post_args()
local info = ''
if not args then
    info = "[upstream_up_down] get post args failed:" .. err
    ngx.log(ngx.ERR, info)
    ngx.say(info)
    return
end

local host = args['host']
local port = args['port']
local oper = args['oper']
local ttl = 0

if host == nil or port == nil or oper == nil then
    info = '[upstream_up_down] params has nil, invalid request'
    ngx.log(ngx.ERR, info)
    ngx.say(info)
    return
end

if oper == 'down' then
    ttl = tonumber(args['ttl'])
    if ttl == nil then
        info = '[upstream_up_down] param ttl is nil, invalid request'
        ngx.log(ngx.ERR, info)
        ngx.say(info)
        return
    end
    InvalidNode:disable_with_ttl(host, port, ttl)
else
    InvalidNode:enable(host, port)
end

ngx.print('ok')