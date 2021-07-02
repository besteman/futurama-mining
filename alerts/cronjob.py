from apscheduler.schedulers.blocking import BlockingScheduler

from main import main

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", seconds=3600)

scheduler.start()
