local Settings = require 'xulb.settings'

local invalid_node = {}

invalid_node.nodes = ngx.shared.xulb_dict
invalid_node.prefix = 'invalid_node_'

function  invalid_node:add(ip, port)
    local key = invalid_node.prefix .. ip .. ':'..port
    ngx.log(ngx.ERR, 'add invalid upstream node ,key:'..key)
    local new_val, _, _ = invalid_node.nodes:incr(key, 1)
    if new_val == nil then
        invalid_node.nodes:set(key, 1, Settings.node_pause_time)
    end
end

function invalid_node:disable(ip, port)
    local key = invalid_node.prefix .. ip .. ':'..port
    ngx.log(ngx.ERR, 'disable upstream node, key:'..key)
    local new_val, _, _ = invalid_node.nodes:incr(key, 9999)
    if new_val == nil then
        invalid_node.nodes:set(key, 9999, Settings.node_freeze_time)
    end
end

function invalid_node:count(ip, port)
    local key = invalid_node.prefix .. ip .. ':'..port
    local val = invalid_node.nodes:get(key)
    if val == nil then
        return 0
    else
        return val
    end
end

function invalid_node:disable_with_ttl(ip, port, ttl)
    local key = invalid_node.prefix .. ip .. ':'..port
    ngx.log(ngx.INFO, '[upstream_up_down] disable_with_ttl upstream node, key:'..key)
    invalid_node.nodes:set(key, 9999, ttl)
end

function invalid_node:enable(ip, port)
    local key = invalid_node.prefix .. ip .. ':'..port
    ngx.log(ngx.INFO, '[upstream_up_down] enable upstream node, key:'..key)
    invalid_node.nodes:delete(key)
end

return invalid_node