local String = require "string"

local util = {}

--返回当前时间戳
function util:timestamp()
    return os.time()
end

--将content写入到path路径的文件中
--成功返回nil, 出错返回err
function util:put_file_content(filepath, content)
    local file, err = io.open(filepath, 'w')
    if err ~= nil then
        return err
    end
    file:write(content)
    file:close()
    return nil
end

--读取文件内容
--成功返回内容,nil, 出错返回'', err
function util:get_file_content(filepath)
    local file, err = io.open(filepath, 'r')
    if err ~= nil then
        return '', err
    end
    local content  = file:read('*all')
    file:close()
    return content, nil
end

--判断字符串开头
function util:startwith(match, pattern)
    return String.sub(match, 1, String.len(pattern)) == pattern
end

--分割字符串
function util:split(inputstr, sep)
    if sep == nil then
        sep = "%s"
    end
    local t={} ; i=1
    for str in String.gmatch(inputstr, "([^"..sep.."]+)") do
        t[i] = str
        i = i + 1
    end
    return t
end

function util:dump_table(table)
    for i, v in pairs(table) do
        print('dump ', i, ' ', v)
    end
end

return util