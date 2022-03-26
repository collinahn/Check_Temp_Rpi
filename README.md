# 라즈베리파이 온도 체크 및 이상온도 감지 시 이메일 알림 v2

### Description
* crontab에 등록해놓고 일정 주기로 실행할 목적으로 작성함.
* 특정 온도가 넘었을 시 등록된 이메일로 알림을 보낸다.
* 온도 기록만 하던 v1에서 smtplib을 이용한 이메일 알림 기능이 추가되었다.

### Environment
* OS: Raspbian(32bit)
* Linux raspberrypi 5.10.17-v7l+

### Prerequisite
* bash
* Python 3.10.1


### Usage

* 첫째, settings.json 사용자화
```json
{
    "gmail_id": "메일을 발송할 이메일 계정",
    "gmail_app_pw": "앱 비밀번호(gmail의 경우, 2차 인증을 설정하고 발급 가능)",
    "mail_to":"메일을 받을 이메일 계정(없으면 발송하는 메일로 발송됨)",
    "cpu_temp":60, # cpu 온도 기준치
    "gpu_temp":60  # gpu 온도 기준치
}
```

* 둘째, 크론탭 등록 
```
 # (주의: sudo로 실행하지 않는다)
 $ crontab -e
```
```
# 30분마다, 파이썬 실행하는 bash 쉘 스크립트 실행하도록 등록 
# (주의: 실행시 유저 디렉토리에서 시작하므로 프로젝트 폴더 내부로 커서를 옮기도록 디렉토리를 변경해준다.)
*/30 * * * * cd /rpi-temp-noti && /home/pi/rpi-temp-noti/temp_noti.sh
```

* 마지막, 저장 후 크론탭 재실행
```
 $ sudo service crontab restart
```

* 실행 여부는 다음과 같은 명령어로 확인
```
 $ sudo journalctl -u cron -f
 
 # 만약 journalctl에 No MTA 에러가 보인다면 postfix 설치하고 로컬환경으로 세팅해주면 된다
 
  $ sudo apt install postfix
```

* 로컬환경으로 postfix 설치 후 다음과 같은 명령어로 출력물을 확인할 수 있다. 
```
 $ sudo tail -f /var/mail/<username>
```


### Files
* settings.json
    * (중요)메일 정보, 앱 비밀번호, 온도 기준 정보 등을 저장하는 Json 파일.
    
* shell-cmd/cpu-temp.sh
    * /sys/class/thermal/thermal_zone0/temp를 읽어 cpu온도 데이터를 읽어들이고 가공한다.
    
* shell-cmd/gpu-temp.sh
    * 앞에 "temp="문자열을 붙여서 반환하는 파일을 읽어 숫자만 반환하도록 기존 스크립트를 분리함.
    
* email_me.py
    * 이메일 발송 파이썬 클래스
    
* temp_noti.py
    * shell-cmd 폴더 내부의 두 파일을 실행해 온도를 측정하는 메인 스크립트.


