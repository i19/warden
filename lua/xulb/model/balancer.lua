local Config = require 'xulb.model.config'
local NgxBalancer = require "ngx.balancer"
local InvalidNode = require 'xulb.model.invalid_node'
local String = require "string"

local balancer = {}

function balancer:set_upstream(ip, port)
    ngx.log(ngx.DEBUG, 'upstream ip:'..ip)
    ngx.log(ngx.DEBUG, 'upstream port:'..port)
    NgxBalancer.set_current_peer(ip, port)
    ngx.ctx.upstream_ip = ip
    ngx.ctx.upstream_port = port
    --ngx.ctx.upstream = upstream_name
end

function balancer:check_upstream()
    local state_name, _ = NgxBalancer.get_last_failure()
    if state_name == 'next' then
        InvalidNode:add(ngx.ctx.upstream_ip, ngx.ctx.upstream_port)
    elseif state_name == 'failed' then
        InvalidNode:disable(ngx.ctx.upstream_ip, ngx.ctx.upstream_port)
    else
        local _, err = NgxBalancer.set_more_tries(2)
        if err ~= nil then
            ngx.log(ngx.ERR,"failed to set retry:".. err)
        end
    end
    return nil
end

function balancer:dispatch(proj_name)
    local proj = Config.projects[proj_name]
    if proj == nil then
        ngx.log(ngx.ERR, "in config no this project name:"..proj_name)
        return ngx.exit(500)
    end

    local uid = ngx.var.cookie_uid
    if uid == nil or uid == '' then
        --没有uid，走无uid环境
        ngx.log(ngx.DEBUG, '[balancer] to no uid env')
        local no_uid_env = proj:get_no_uid_env()
        if no_uid_env == nil then
            ngx.log(ngx.ERR, '[balancer] get no uid env is nil')
            return ngx.exit(500)
        end
        local upstream = no_uid_env:get_one()
        if upstream == nil then
            ngx.log(ngx.ERR, "no aval upstream node in no uid env")
            return ngx.exit(500)
        end
        balancer:set_upstream(upstream.host, upstream.port)
    else
        --有uid
        if proj:is_to_special_env() == true then
            --走特殊环境
            ngx.log(ngx.DEBUG, '[balancer] to spec env')
            local spec_env = proj:get_spec_env()
            if spec_env == nil then
                ngx.log(ngx.ERR, '[balancer] get spec env is nil')
                return ngx.exit(500)
            end
            local upstream = spec_env:get_one()
            if upstream == nil then
                ngx.log(ngx.ERR, "no aval upstream node in spec env")
                return ngx.exit(500)
            end
            balancer:set_upstream(upstream.host, upstream.port)
        else
            --走普通环境，uid尾数比例调度
            local pos = uid_suffix(uid)
            local env_name = proj.uid_suffix_env_hash[pos]
            ngx.log(ngx.DEBUG, 'pos:'..pos..' env_name:'..env_name)
            local env = proj.envs[env_name]
            if env == nil then
                ngx.log(ngx.ERR, 'no env name:'..env_name)
                return ngx.exit(500)
            end
            local upstream = env:get_one()
            if upstream == nil then
                ngx.log(ngx.ERR, 'no aval upstream node in env:'..env_name)
                return ngx.exit(500)
            end
            balancer:set_upstream(upstream.host, upstream.port)
        end
    end
end

function uid_suffix(uid)
    local n = tonumber(String.sub(uid, -2, -1))
    if n == nil then 
        --为了避免非法uid的出现nil导致crash
        n = 1
    end
    return n
end

return balancer