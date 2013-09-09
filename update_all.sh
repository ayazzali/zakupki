START=$(date +'%Y-%m-%d %H:%M:%S')
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "Full update start: zakupki" -m "Full update started $START (zakupki)." -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes
python /home/roveo/data/zakupki/py/update.py all 2>&1 | tee -a /home/roveo/data/zakupki/log/all.log | tee /home/roveo/data/zakupki/log/email_all.log
END=$(date +'%Y-%m-%d %H:%M:%S')
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "Full update end: zakupki" -m "Full update started $START, ended $END (zakupki)." -a /home/roveo/data/zakupki/log/email_all.log -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes