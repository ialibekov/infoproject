USER=infouser
PASSWORD=infopass
BASE=infodb

mysql -u $USER -p$PASSWORD -e "CREATE DATABASE $BASE CHARACTER SET utf8;"

