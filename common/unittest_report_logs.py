import time
import datetime
import os
now_dir = os.path.dirname(os.path.dirname(__file__))
now_time = datetime.datetime.now()
str_time = now_time.strftime("%Y-%m-%d")
log_dir = now_dir + '/log/'


def info_log(text):
    date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
    log_text = "[INFO]{}: {}\n".format(date, text)
    log_name = "{}_info.log".format(str_time)
    # print(os.path.dirname(__file__))
    with open(log_dir + log_name, "a") as f:
        f.write(log_text)
    f.close()


def error_log(text):
    date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
    log_text = "[ERROR]{}: {}\n".format(date, text)
    # print(log_text)
    log_name = "{}_info.log".format(str_time)
    with open(log_dir + log_name, "a") as f:
        f.write(log_text)
    f.close()

