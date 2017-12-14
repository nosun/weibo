# coding:utf-8

from subprocess import check_output, call
import time


def check_process():
    s = check_output("ps aux | grep crawler | grep -v 'grep'| wc -l", shell=True)
    s = s.strip("\n")
    return s


while True:
    if check_process() == "0":
        retCode = call(["python", "crawler.py"], shell=False)
        print retCode
    else:
        print "进程检查结果" + check_process()
    time.sleep(2)
