from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.schedulers import base
from task.views import task_update
"""
update_task是給APScheduler使用的
這邊目前是註解掉的，預計是要改成使用celery來更新任務的進度
如果懶得修改就直接uncomment掉這個function，就會自動啟用APScheduler
"""

# def update_task():
#     scheduler = BackgroundScheduler()
#     scheduler.start(paused=True)
#     scheduler.print_jobs()
#     for job in scheduler.get_jobs():
#         print("name: %s, trigger: %s, next run: %s, handler: %s" % (
#             job.name, job.trigger, job.next_run_time, job.func))


