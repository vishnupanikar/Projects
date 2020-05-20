import os
import shutil
import glob
from datetime import date , datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from Scripts.Dash_board import start_server

path = os.getcwd()+'/Data/'

def script_scheduler():
    datafiles = os.listdir(path)
    for file in datafiles:
        if file == 'raw_data1.csv':
            pass
        else:
            try:
                os.remove(path+file)
            except Exception as e:
                print('No File Found :: ', e)
    shutil.rmtree(os.getcwd()+'/Scripts/__pycache__')

    with open('Scripts/Scraping.py') as Script:
        exec(Script.read())
    with open('Scripts/Data_collection.py') as Script:
        exec(Script.read())

    csvfiles = glob.glob('*.csv')
    for file in csvfiles:
        shutil.move(os.getcwd()+'/'+file,path)

    start_server()

scheduler = BlockingScheduler()
scheduler.add_job(script_scheduler , 'interval', hours = 12)

script_scheduler()
scheduler.start()
