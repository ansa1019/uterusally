from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'


    # def ready(self):
    #     from task.task_scheduler import task_updater
    #     task_updater.update_task()





