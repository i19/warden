local upstream = {}

upstream.host = ''
upstream.port = 0

function upstream:new()
    local table = {
        host = '',
        port = 0,
    }
    setmetatable(table, { __index = self })
    return table
end

return upstream