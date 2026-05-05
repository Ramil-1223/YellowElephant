#!/bin/bash

USERNAME=$(cat /run/secrets/username)
PASSWORD=$(cat /run/secrets/pass)
OSBIT32=32
OSBIT64=64
PAKET=server
PAKETNAME32=$PAKET$OSBIT32
PAKETNAME64=$PAKET$OSBIT64


if [[ -z "$USERNAME" ]];then
    echo "Имя пользователя не указано"
    exit 1
fi
if [[ -z "$PASSWORD" ]];then
    echo "Пароль не указан"
    exit 1
fi


VER=$(cat /run/secrets/1C_version)

#Подключаемся к серверу 1С
SRC=$(curl -c /tmp/cookies.txt -s -L https://releases.1c.ru)

ACTION=$(echo "$SRC" | grep -oP '(?<=form method="post" id="loginForm" action=")[^"]+(?=")')
EXECUTION=$(echo "$SRC" | grep -oP '(?<=input type="hidden" name="execution" value=")[^"]+(?=")')

curl -s -L \
    -o /dev/null \
    -b /tmp/cookies.txt \
    -c /tmp/cookies.txt \
    --data-urlencode "inviteCode=" \
    --data-urlencode "execution=$EXECUTION" \
    --data-urlencode "_eventId=submit" \
    --data-urlencode "username=$USERNAME" \
    --data-urlencode "password=$PASSWORD" \
    https://login.1c.ru"$ACTION"


if ! grep -q "TGC" /tmp/cookies.txt ;then
    echo "Ошибка аутентификации"
    exit 1
fi

clear

#Выводим список версий платформы
curl -s -b /tmp/cookies.txt https://releases.1c.ru/project/Platform83 |

#    grep 'a href="/version_files?nick=Platform83' |
#    tr -s '="  ' ' ' |
#    awk -F ' ' '{print $5}' |
#    sort -Vr | pr -T -5

#read -i "8.3." -p "Выбирите версию для загрузки (введите два последних номера версии через точку - например 14.1565: " -e VER

if [[ -z "$VER" ]];then
    echo "VERSION не выбрана"
    exit 1
fi

if [[ "8.3." = "$VER" ]];then
    echo "Введен не полный номер версии VERSION"
    exit 1
fi

VERPLATFORM=$VER
#Заменяем точки на нижнее подчеркивание в версии платформы
VERPLATFORM1=${VER//./_}
#

#Точки в версии платформы
VERPLATFORM2=${VER//./}
#


#Функция для сравнения версий
function version_platform { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }

    #Сравнение версий, если версия ниже 8.3.12.1469 то качаем после else
    if [ $(version_platform $VERPLATFORM) -ge $(version_platform "8.3.12.1469") ]; then

	#если x86_64
#	if [ ${OSBIT} == '64' ]; then

		SERVERLINK64=$(curl -s -G \
		    -b /tmp/cookies.txt \
		    --data-urlencode "nick=Platform83" \
		    --data-urlencode "ver=$VERPLATFORM" \
		    --data-urlencode "path=Platform\\$VERPLATFORM1\\${PAKETNAME64}_${VERPLATFORM1}.zip" \
		    https://releases.1c.ru/version_file | grep -m 1 -oP '(?<=a href=")[^"]+(?=">Скачать дистрибутив)')
#	fi


	#если x86
#	if [ ${OSBIT} == '32' ]; then
#		SERVERLINK32=$(curl -s -G \
#		    -b /tmp/cookies.txt \
#		    --data-urlencode "nick=Platform83" \
#		    --data-urlencode "ver=$VERPLATFORM" \
#		    --data-urlencode "path=Platform\\$VERPLATFORM1\\${PAKETNAME32}_${VERPLATFORM1}.zip" \
#		    https://releases.1c.ru/version_file | grep -m 1 -oP '(?<=a href=")[^"]+(?=">Скачать дистрибутив)')
#
#        fi
    #Сравнение версий, если версия ниже 8.3.12.1469 качем отсюда
    else

#        if [ ${OSBIT} == '64' ]; then

		SERVERLINK64=$(curl -s -G \
		    -b /tmp/cookies.txt \
		    --data-urlencode "nick=Platform83" \
		    --data-urlencode "ver=$VERPLATFORM" \
		    --data-urlencode "path=Platform\\$VERPLATFORM1\\${PAKETNAME64}_${VERPLATFORM1}.zip" \
		    https://releases.1c.ru/version_file | grep -m 1 -oP '(?<=a href=")[^"]+(?=">Скачать дистрибутив)')
#		fi

    fi




#mkdir -p /tmp/platform1c


#if [ ${OSBIT} == '64' ]; then

    echo "Закачиваем серверную часть версии $VER для архитектуры x86_64"
    curl --fail -b /tmp/cookies.txt -o /tmp/platform1c/server64_${VER}.zip -L "$SERVERLINK64"
#fi

#if [ ${OSBIT} == '32' ]; then

#    echo "Закачиваем серверную часть версии $VER для архитектуры x86"
#    curl --fail -b /tmp/cookies.txt -o /tmp/platform1c/server32_${VER}.zip -L "$SERVERLINK32"

#fi

#удаляем файл с куки
rm /tmp/cookies.txt

echo "Распаковываем платформу 1C"


#if [ ${OSBIT} == '64' ]; then
    unzip /tmp/platform1c/server64_${VER}.zip
#fi
#if [ ${OSBIT} == '32' ]; then
#    unzip /tmp/platform1c/server32_${VER}.zip
#fi


./wget_1c.sh $VER 

echo "Теперь выполните комманду по установке 1С клиента, например emerge 1c-enterprise83-client-$VER"

