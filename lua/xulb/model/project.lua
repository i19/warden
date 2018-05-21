local Util = require 'xulb.agileutil.util'
local Settings = require 'xulb.settings'

local project = {}

project.spec_env = ''
project.spec_uids = {}
project.envs = {}
project.length = 0
project.spec_uid_map = {}
project.uid_suffix_env_hash = {}
project.no_uid_env = ''

function project:new()
    local table = {
        spec_env = '',
        spec_uids = {},
        envs = {},
        length = 0,
        spec_uid_map = {},
        uid_suffix_env_hash = {},
        no_uid_env = '',
    }
    setmetatable(table, { __index = self })
    return table
end

function project:get_one()
    local envs = self.envs
    for i, env in pairs(envs) do
        local length = env.length
        if length > 0 then
            local upstreams = env.upstreams
            local one_upstream = upstreams[1]
            return one_upstream
        end
    end
    return nil
end

function project:is_to_special_env()

    --检查该项目是否指定了特殊环境
    if self.spec_env == '' or self.spec_env == nil then
        return false
    end

    local uid = ngx.var.cookie_uid

    
    --检查是否来自办公室
    if self:is_from_office() == true then
        ngx.log(ngx.DEBUG, 'spec_env condition from office')
        return true
    end

    --检查是否为特定uid
    if self:is_spec_uid(uid) == true then
        ngx.log(ngx.DEBUG, 'spec_env condition spec uid')
        return true
    end

    return false
end

function project:is_from_office()
    local real_ip = ngx.var.real_ip
    if settings.office_ip_map[real_ip] == nil then
        return false
    else
        return true
    end
end

function project:is_spec_uid(uid)
    print ('project:is_spec_uid uid ', uid)
    Util:dump_table(self.spec_uid_map)
    if self.spec_uid_map[uid] == nil then
        return false
    else
        return true
    end
end

function project:get_spec_env()
    return self.envs[self.spec_env]
end

function project:get_no_uid_env()
    print(self.no_uid_env)
    return self.envs[self.no_uid_env]
end

return project