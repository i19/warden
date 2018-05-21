-- balancer 通过 user 判断当前项目是否处于灰度状态，然后根据策略（目前只根据用户）决定将请求指向哪个后端组

local Balancer = require 'xulb.model.balancer'

local balancer = {}

function balancer:connect(proj_name)
    Balancer:check_upstream()
    Balancer:dispatch(proj_name)
end

return balancer