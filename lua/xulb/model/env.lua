local InvalidNode = require 'xulb.model.invalid_node'
local Settings = require 'xulb.settings'
local Math = require "math"

local env = {}

env.uid_rate = 0
env.upstreams = {}
env.length = 0
env.position = 0

function env:new()
    local table = {
        uid_rate = 0,
        upstreams = {},
        length = 0,
        position = 0,
    }
    setmetatable(table, { __index = self })
    return table
end

function env:get_one()
    if self.length == 0 then
        return nil
    end
    local loop = 0
    for i=1, self.length do
        if self.position + 1 > self.length then
            self.position = 1
        else
            self.position = self.position + 1
        end
        ngx.log(ngx.DEBUG, 'worker_id:'..ngx.worker.id())
        ngx.log(ngx.DEBUG, 'position:'..self.position)
        local upstream = self.upstreams[self.position]
        local count = InvalidNode:count(upstream.host, upstream.port)
        if count < Settings.node_max_failes then
            return upstream
        end
        ngx.log(ngx.DEBUG, '[get_one] pass one node,'..upstream['host']..':'..upstream['port']) 
    end
    return self.upstreams[Math.random(self.length)]
end

return env