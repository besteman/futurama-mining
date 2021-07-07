from apscheduler.schedulers.blocking import BlockingScheduler

from flaskr.alerts import alerts

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(alert, "interval", seconds=10)

scheduler.start()
