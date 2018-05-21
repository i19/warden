#coding=utf-8

import web
from decouple import config
import router.router as router
import sys
sys.path.append('../')
import task.upstream_health_check_task.upstream_health_check_task as upstream_health_check_task

sys.argv.append(config('PORT'))
if config('DEBUG') == 'false': web.config.debug = False
urls = router.routers
app = web.application(urls, globals())
application = app.wsgifunc()
if config('UPSTREAM_CHECK_ENABLE') == 'true': upstream_health_check_task.start()
if __name__ == '__main__': 
    app.run()