START=$(date +"%Y-%m-%d %H-%M-%S")
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "ZAKUPKI full update started $START" -m $"Full update started at $START\n\n" -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes
python3 /home/roveo/data/zakupki/py/update.py full 2>&1 | tee -a /home/roveo/data/zakupki/log/full_update.log | tee /home/roveo/data/zakupki/log/full_email.log
python3 /home/roveo/data/zakupki/py/update.py daily 2>&1 | tee -a /home/roveo/data/zakupki/log/daily_update.log | tee /home/roveo/data/zakupki/log/daily_email.log
END=$(date +"%Y-%m-%d %H-%M-%S")
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "ZAKUPKI full update ended $END" -m $"Full executed started $START, ended $END\n\n" -a /home/roveo/data/zakupki/log/full_email.log /home/roveo/data/zakupki/log/daily_email.log -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes