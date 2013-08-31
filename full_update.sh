START=$(date +"%Y-%m-%d %H-%M-%S")
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "ZAKUPKI all update started $START" -m $"All update started at $START\n\n" -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes
python3 /home/roveo/data/zakupki/py/update.py all 2>&1 | tee -a /home/roveo/data/zakupki/log/all_update.log | tee /home/roveo/data/zakupki/log/all_email.log
python3 /home/roveo/data/zakupki/py/update.py inc 2>&1 | tee -a /home/roveo/data/zakupki/log/inc_update.log | tee /home/roveo/data/zakupki/log/inc_email.log
END=$(date +"%Y-%m-%d %H-%M-%S")
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "ZAKUPKI all update ended $END" -m $"All update executed started $START, ended $END\n\n" -a /home/roveo/data/zakupki/log/all_email.log /home/roveo/data/zakupki/log/inc_email.log -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes