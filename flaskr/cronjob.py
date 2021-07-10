from apscheduler.schedulers.blocking import BlockingScheduler

from flaskr.alerts import main

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(alerts, "interval", seconds=10)

scheduler.start()
