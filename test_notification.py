from notifypy import Notify

notification = Notify()
notification.title = "测试通知"
notification.message = "这是一条测试通知"
notification.application_name = "Auto GUI"
notification.send(block=True)
