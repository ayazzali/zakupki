START=$(date +'%Y-%m-%d %H:%M:%S')
python /home/roveo/data/zakupki/py/update.py all -p -c 2>&1 | tee -a /home/roveo/data/zakupki/log/inc.log | tee /home/roveo/data/zakupki/log/email_inc.log
END=$(date +'%Y-%m-%d %H:%M:%S')
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "Incremental update: zakupki" -m "Incremental update started $START, ended $END (zakupki)." -a /home/roveo/data/zakupki/log/email_inc.log -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes