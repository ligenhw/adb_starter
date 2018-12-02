#/bin/bash

# welink启动组件名
WELINK_ACTIVITY=com.huawei.works/huawei.w3.ui.welcome.W3SplashScreenActivity
# welink 打卡tab页签坐标
WELINK_TAB=(750 1850)
# 打卡按钮坐标
SIGNED_BUTTON=(800 1100)
# 锁屏时下滑，显示输入密码界面
SLIDE_DOWN=(500 300 500 900)
# 输入锁屏密码界面 数字区域坐标 1，2，3 ... 0 , <-
p1=(60 916)
p2=(1020 1872)

startWelink() {
    adb shell am start -n $WELINK_ACTIVITY
    sleep 2
    # click yewu tab
    adb shell input tap ${WELINK_TAB[@]} 
}

signed() {
    # click daka button
    adb shell input tap ${SIGNED_BUTTON[@]}
}

secret_number() {
    local w=$(( (${p2[0]} - ${p1[0]}) / 3 ))
    local h=$(( (${p2[1]} - ${p1[1]}) / 4 )) 

    #echo $w , $h
    NUM=$1
    if [ $NUM -eq 0 ]; then
        NUM=11
    fi

    local x=$(( (($NUM + 2) % 3) * $w + ${p1[0]} + ($w / 2) ))
    local y=$(( (($NUM - 1) / 3) * $h + ${p1[1]} + ($h / 2) ))

    echo $x $y
}

unlock() {
    adb shell input keyevent 223
    adb shell input keyevent 224
    # slide down
    adb shell input swipe ${SLIDE_DOWN[@]}

    local nums=$1
    for (( i=0; i<${#nums}; i++)) {
        adb shell input tap $(secret_number ${nums:i:1})
    }
}

capture() {
    local file_name=test
    if [ "$1" != "" ]; then
        file_name=$1
    fi
    adb shell screencap /sdcard/${file_name}.png
    adb pull /sdcard/${file_name}.png
}

retry=3
now=`date`
mkdir "$now"
cd "$now"

capture start

unlock $1
sleep 2
capture unlock

startWelink
sleep 2
capture startWelink

while [ $retry -ne 0 ]; do
    signed
    capture signed_$retry
    sleep 3
    capture signed_${retry}_result
    retry=$(( $retry - 1 ))
done

capture end