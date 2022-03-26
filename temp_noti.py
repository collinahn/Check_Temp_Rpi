import os 

from json_parser import JsonParser

def send_mail_if_hot(temp: tuple[float, float]) -> bool:
    from email_me import SendMail
    mail_to = JsonParser('mail_to').value or JsonParser('gmail_id').value
    ctemp, gtemp = temp

    sm = SendMail()
    return sm.send_mail(
        content=sm.create_mail(
            title='Temperature Anomaly Notice',
            html_contents=f'current status<br />cpu temp = {ctemp}\'C<br />gpu temp = {gtemp}\'C'
        ),
        receivers=mail_to
    )

cpu_temp = os.popen('bash ./shell-cmd/cpu-temp.sh').read()
gpu_temp = os.popen('bash ./shell-cmd/gpu-temp.sh').read()

try:
    cpu_temp = float(cpu_temp.replace('\'C\n', ''))
    gpu_temp = float(gpu_temp.replace('\'C\n', ''))
except ValueError as ve:
    print('wrong value')
    cpu_temp = 0.0
    gpu_temp = 0.0

print(f'{cpu_temp = }, {gpu_temp = }')

cpu_std = JsonParser('cpu_temp').value
gpu_std = JsonParser('gpu_temp').value

if (
    cpu_temp > cpu_std or 
    gpu_temp > gpu_std
):
    send_mail_if_hot((cpu_temp, gpu_temp))

else:
    print('rpi in good condition')
