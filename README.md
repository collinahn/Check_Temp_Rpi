# RaspberryPi Temperature Check v1

### Description
* 간이 서버 역할을 하고 있는 라즈베리파이4B의 위치를 팬 소음 때문에 좀 더 더운 쪽으로 옮겼다.
* 작동중 온도가 염려되어서 온도 모니터링을 하고자 만든 쉘 스크립트.
* v2를 만든다면 일정 온도 이상으로 올라가면 이메일로 경고 문구를 보내주도록 만들 예정이다.

### Environment
* OS: Raspbian 32bit
* Linux raspberrypi 5.10.17-v7l+
* nohup으로 실행

### Prerequisite
* bash shell

### Files
* temp.sh
    * 루트 디렉토리에 위치.
    * /sys/class/thermal/thermal_zone0/temp를 읽어 cpu온도 데이터를 읽어들이고 가공한다.
    * gpu 온도는 다른 방식으로 읽어들이는데, 앞에 "temp="문자열을 붙여서 반환하므로 숫자만 저장한다.
```
#!/bin/bash

TEMP_CPU_RAW=`cat /sys/class/thermal/thermal_zone0/temp`
TEMP_CPU_INT=$((${TEMP_CPU_RAW}/1000))
TEMP_CPU_TEMP=$((${TEMP_CPU_RAW}/100))
TEMP_CPU_DECIMAL=$((${TEMP_CPU_TEMP} % ${TEMP_CPU_INT}))

TEMP_GPU=`/opt/vc/bin/vcgencmd measure_temp`
TEMP_GPU=${TEMP_GPU//temp=/}
```


* templog/checktemp.sh
    * temp.sh 파일을 적당한 시간에 한 번 실행시킨다.
    * 표준출력을 로그파일(templog/checktemp.log)로 저장한다.

### Usage
* nohup & 명령으로 백그라운드에서 세션이 종료되어도 동작하도록 실행
```
cd templog 

#표준출력 기록 안하는 경우
$ nohup ./checktemp.sh > /dev/null & 

# 표준출력과 표준에러를 각기 다른 파일에 쓰는 경우
$ nphup ./checktemp.sh 1 > output.log 2 > error.log &

# 둘 다 파일에 쓰는 경우
$ nohup ./checktemp.sh > out.log 2>&1 &
```
