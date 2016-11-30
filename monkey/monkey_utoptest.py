#encoding:utf-8
import os
import time
import re

###############################################################
#########                  Monkey测试                 #########
#########                作者：Nil                    #########
#########                版本  V1.0.1                 ###### ###
#
#########                时间：2016.11.10             #########
###############################################################

packageName="com.qttecx.utop.activity"
logdir='/Users/admin/Documents/autotest/utoplog'

remote_path='/Users/admin/Documents/autotest/utoplog'



os.system("adb -s cf615425 shell cat /system/build.prop >/Users/admin/Documents/autotest/utoplog/phone.txt")

f = "/Users/admin/Documents/autotest/utoplog/phone.txt"

version = '0'

model = '0'

brand = '0'

def getcmd(cmd):
    f = open(cmd,"r")  #open(路径+文件名,读写模式)#
    lines = f.readlines()    #依次读取每行#
    global brand
    global version
    global model
    for line in lines:
        line=line.split('=') #分隔符对字符串进行切片，分割=后面的内容
        if (line[0]=='ro.build.version.release'):
            version = line[1]
        if (line[0]=='ro.product.device'):
            model = line[1]
        if (line[0]=='ro.product.brand'):
            brand = line[1]
    return version,model,brand


version,model,brand=getcmd(f)
print version,model,brand
os.remove(f)


#print "使用Logcat清空Phone中log"
os.popen("adb logcat -c")

#print"暂停2秒..."
print "wait"
time.sleep(2)

now1 = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))

#print"开始执行Monkey命令"
monkeylogname=logdir+"/"+now1+"monkey.log"
print monkeylogname
cmd="adb -s cf615425 shell monkey -p com.qttecx.utop.activity --ignore-timeouts --monitor-native-crashes -v -v 20000 >%s" %(monkeylogname)

os.popen(cmd)   


#print"手机截屏"
os.popen("adb shell screencap -p /sdcard/monkey_run.png")

#print"拷贝截屏图片至电脑"
cmd1="adb pull /sdcard/monkey_run.png %s" %(logdir)
os.popen(cmd1)
print "rename"
oldname=logdir+"/"+r"monkey_run.png"
if (os.path.exists(oldname)):
    print "file is exist"
else:
    print "file isn't exist"
newname=logdir+"/"+now1+r"monkey.png"
os.rename(oldname, newname)

#print"使用Logcat导出日志"

logcatname=logdir+"/"+now1+r"logcat.log"
cmd2="adb logcat -d >%s" %(logcatname)
os.popen(cmd2)

#print"导出traces文件"

tracesname=logdir+"/"+now1+r"traces.log"
cmd3="adb shell cat /data/anr/traces.txt>%s" %(tracesname)
os.popen(cmd3)

######################
#获取error
######################
print "获取error"

NullPointer="java.lang.NullPointerException"
IllegalState="java.lang.IllegalStateException"
IllegalArgument="java.lang.IllegalArgumentException"
ArrayIndexOutOfBounds="java.lang.ArrayIndexOutOfBoundsException"
RuntimeException="java.lang.RuntimeException"
SecurityException="java.lang.SecurityException"

def geterror():
    f = open(logcatname,"r")
    lines = f.readlines()
    errfile="%s/error.log" %(remote_path)
    if (os.path.exists(errfile)):
        os.remove(errfile)
    fr = open(errfile,"a")
    fr.write(version)
    fr.write("\n")
    fr.write(model)
    fr.write("\n")
    fr.write(brand)
    fr.write("\n")
    fr.write(now1)
    fr.write("\n")

    count=0
    for line in lines:
        if ( re.findall(NullPointer,line) or re.findall(IllegalState,line) or re.findall(IllegalArgument,line) or re.findall(ArrayIndexOutOfBounds,line) or re.findall(RuntimeException,line) or re.findall(SecurityException,line) ):
            a=lines.index(line)
            count +=1
            for var in range(a,a+22):
                print lines[var]
                fr.write(lines[var])
            fr.write("\n")
        f.close()
    fr.close()
    return count


number=geterror()
print number


