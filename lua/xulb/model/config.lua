local Util = require('xulb.agileutil.util')
local Project = require('xulb.model.project')
local Env = require("xulb.model.env")
local Upstream = require("xulb.model.upstream")
local Settings = require('xulb.settings')
local Cjson = require 'cjson'
local NgxSharedDict = ngx.shared.xulb_dict

local config = {}

config.raw = '' --存放配置字符串
config.version = '' --存放当前时间戳
config.projects = {} --存放配置信息

--尝试从文件中加载配置
--成功返回nil, 出错返回err
function config:load_config()
    local config_str, err = Util:get_file_content(Settings.total_config_path)
    if err ~= nil then 
        return err
    end
    if config_str == '' then
        return 'config string is empty'
    end
    local config_data = Cjson.decode(config_str)
    for proj_name, proj_node in pairs(config_data) do
        local spec_env = proj_node.spec_env
        local spec_uids = proj_node.spec_uids
        local envs = proj_node.envs
        local no_uid_env = proj_node.no_uid_env
        local project = Project:new()
        project.spec_env = spec_env
        project.spec_uids = spec_uids
        project.spec_uid_map = self:make_uid_map(spec_uids)
        project.envs = {}
        project.length = 0
        project.uid_suffix_env_hash = {}
        project.no_uid_env = no_uid_env
        print('config no_uid_env', no_uid_env)
        for env_name, env_node in pairs(envs) do
            local uid_rate = env_node.uid_rate
            local upstreams = env_node.upstreams
            env = Env:new()
            env.uid_rate = uid_rate
            env.upstreams = {}
            env.length = 0
            for index, upstream_node in pairs(upstreams) do
                local host = upstream_node.host
                local port = upstream_node.port
                local upstream = Upstream:new()
                upstream.host = host
                upstream.port = port
                table.insert(env.upstreams, upstream)
                env.length = env.length + 1
            end
            project.envs[env_name] = env
            project.length = project.length + 1
            for i=1, uid_rate do
                table.insert(project.uid_suffix_env_hash, env_name)
            end
        end
        Util:dump_table(project.uid_suffix_env_hash)
        self.projects[proj_name] = project
    end
    self.raw = config_str
    self.version = Util:timestamp()
    return nil
end

--返回配置结构转换成json的字符串，用于调试
function config:dump()
    local config_str = Cjson.encode(self.projects)
    return config_str
end

function config:merge_config()
    local config_str = NgxSharedDict:get('raw')
    if config_str == '' then
        return 'config string is empty'
    end
    local config_data = Cjson.decode(config_str)
    for proj_name, proj_node in pairs(config_data) do
        local spec_env = proj_node.spec_env
        local spec_uids = proj_node.spec_uids
        local envs = proj_node.envs
        local no_uid_env = proj_node.no_uid_env
        local project = Project:new()
        project.spec_env = spec_env
        project.spec_uids = spec_uids
        project.spec_uid_map = self:make_uid_map(spec_uids)
        project.envs = {}
        project.length = 0
        project.uid_suffix_env_hash = {}
        project.no_uid_env = no_uid_env
        print('config no_uid_env', no_uid_env)
        for env_name, env_node in pairs(envs) do
            local uid_rate = env_node.uid_rate
            local upstreams = env_node.upstreams
            env = Env:new()
            env.uid_rate = uid_rate
            env.upstreams = {}
            env.length = 0
            for index, upstream_node in pairs(upstreams) do
                local host = upstream_node.host
                local port = upstream_node.port
                local upstream = Upstream:new()
                upstream.host = host
                upstream.port = port
                table.insert(env.upstreams, upstream)
                env.length = env.length + 1
            end
            project.envs[env_name] = env
            project.length = project.length + 1
            for i=1, uid_rate do
                table.insert(project.uid_suffix_env_hash, env_name)
            end
        end
        self.projects[proj_name] = project
    end
    self.raw = config_str
    self.version = NgxSharedDict:get('version')
    --dump所有配置到文件持久化
    local err = config:config_to_file()
    if err ~= nil then
        return err
    end
    return nil
end

--dump所有配置到文件持久化
function config:config_to_file()
    local config_str = config:dump()
    if config_str == nil then
        config_str = ''
    end
    local err = Util:put_file_content(Settings.total_config_path, config_str)
    if err == nil then
        --ngx.log(ngx.DEBUG, "write config to total file succed")
    else
        ngx.log(ngx.ERR, "write config to total file failed"..err)
    end
    return err
end

function config:make_uid_map(spec_uids)
    local uid_map = {}
    if spec_uids == '' or spec_uids == nil then
        return uid_map
    end
    uids = Util:split(spec_uids, ',')
    for i, uid in pairs(uids) do
        print (' ', i, ' ', uid)
        uid_map[uid] = 1
    end
    return uid_map
end

return config