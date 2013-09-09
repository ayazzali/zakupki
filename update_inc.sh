START=$(date +'%Y-%m-%d %H:%M:%S')
# python /home/roveo/py/update.py inc
END=$(date +'%Y-%m-%d %H:%M:%S')
echo 
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "Incremental update: zakupki" -m "Incremental update started $START, ended $END (zakupki)." -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes