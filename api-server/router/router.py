#coding=utf-8

routers = (
    '/api/group', 'controller.group.Group',
    '/api/group/(.*)','controller.group.Group',
    '/api/openresty/(.*)/(.*)/(.*)', 'controller.openresty.Openresty',
    '/api/openresty/(.*)', 'controller.openresty.Openresty',
    '/api/project/(.*)/(.*)', 'controller.project.Project',
    '/api/project/(.*)', 'controller.project.Project',
    '/api/enviroment/(.*)/(.*)/(.*)', 'controller.environment.Environment',
    '/api/enviroment/(.*)/(.*)',  'controller.environment.Environment',
    '/api/upstream/(.*)/(.*)/(.*)/(.*)/(.*)', 'controller.upstream.Upstream',
    '/api/upstream/(.*)/(.*)/(.*)', 'controller.upstream.Upstream',
    '/api/special_env/(.*)/(.*)/(.*)', 'controller.special_env.SpecialEnv',
    '/api/special_uid/(.*)/(.*)/(.*)', 'controller.special_uid.SpecialUid',
    '/api/no_uid_env/(.*)/(.*)/(.*)', 'controller.no_uid.NoUidEnv',
    '/api/config/(.*)/(.*)', 'controller.config.Config',
    '/api/health', 'controller.health.Health',
)