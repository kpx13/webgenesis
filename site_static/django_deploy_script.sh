#! /bin/bash
 
# аргументы ниже нужно заполнить!
PROJECT_NAME="django_empty_project"                                 # * название проекта
GITHUB_PROJECT="https://github.com/kpx13/django_empty_project.git"  # * адрес гитхаб-репозитория
DB_ROOT_PASSWORD="asdf"                                             # * пароль рута от MySQL
DB_NAME="mysql_db_name"                                             # * конфиг БД (должен совпадать с конфигом в settings.py) название БД
DB_USER="mysql_db_user"                                             # * юзер
DB_PASSWORD="mysql_db_password"                                     # * пароль
 
APACHE_SERVER_NAME="yoursite.ru"                                    # домен
GITHUB_EMAIL="annkpx@gmail.com"                                     # конфиг для гитхаба, эмейл
GITHUB_USERNAME='annkpx'                                            # конфиг для гитхаба, юзернэйм
# конец аргументов
 
APACHE_LISTEN="$(hostname --ip-address):80"
THIS_PATH=$PWD
PROJECT_ROOT=$THIS_PATH/$PROJECT_NAME
 
# установка базовых пакетов
distr_install ()
{
    echo "Устанавливаем ПО..."
    sudo apt-get update
    yes | sudo apt-get install apache2 libapache2-mod-wsgi # необходимо для работы связки apache + django
    yes | sudo apt-get install python-dev python-pip # необходимо для работы связки  python + mysql
    yes | sudo apt-get install libjpeg62 libjpeg62-dev libfreetype6 libfreetype6-dev zlib1g-dev # необходимо для графики и шрифтов
    
    # MySQL + Python
    read -p "Сейчас будет устанавливаться MySQL, в синем окне Вы должны 2 раза ввести пароль рута для базы: $DB_ROOT_PASSWORD" 
    sudo apt-get install mysql-server
    yes | sudo apt-get install python-mysqldb
}
 
# выкачивание репозитория с кодом
git_init ()
{
    # если будет использоваться не git, а что-то другое, эту функцию нужно переписать
    yes | sudo apt-get install git
    echo "Клонируем репозиторий с гитхаба..."
    echo "192.30.252.128 github.com" | sudo tee --append /etc/hosts   # всвязи с суицидниками на гитхабе
    git clone $GITHUB_PROJECT
    echo ".*
*.pyc
env/
logs/
static/" > $PROJECT_ROOT/.gitignore   # стандартный файл .gitignore, можно отредактировать
    git config --global user.email $GITHUB_EMAIL
    git config --global user.name $GITHUB_USERNAME
}
 
# удовлетворение зависимостей
project_req ()
{
    echo "Устанавливаем зависимости..."
    cat $PROJECT_ROOT/apt-requirements | xargs sudo apt-get install # установка apt-зависимостей
    sudo pip install -r $PROJECT_ROOT/requirements # установка pip-зависимостей 
}
 
# создание базы MySQL
create_db ()
{
    # если будет использоваться другая база, заменить эту часть
    mysql -u root -p$DB_ROOT_PASSWORD -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD'"
    mysql -u root -p$DB_ROOT_PASSWORD -e "CREATE DATABASE $DB_NAME"
    mysql -u root -p$DB_ROOT_PASSWORD -e "GRANT ALL ON $DB_NAME.* TO $DB_USER@localhost"
    echo "БД установлена..."
}
 
# инициализация в джанго
django ()
{
    cd $PROJECT_ROOT
    
    echo "Собираем статику..."
    mkdir media 2>/dev/null
    mkdir media/uploads 2>/dev/null
    python manage.py collectstatic
    
    echo "Синхронизируем БД..."
    python manage.py syncdb
}
 
# установка apache
apache_set()
{
    # настройка связки с apache
    cd $PROJECT_ROOT
    echo "Alias /media/ $PROJECT_ROOT/media/
<Directory $PROJECT_ROOT/media>
            Order allow,deny
            Options -Indexes
            Allow from all
            IndexOptions FancyIndexing
</Directory>

Alias /static/ $PROJECT_ROOT/static/
<Directory $PROJECT_ROOT/static>
            Order allow,deny
            Options -Indexes
            Allow from all
            IndexOptions FancyIndexing
</Directory>

WSGIScriptAlias / $PROJECT_ROOT/wsgi.py
" > httpd.conf
 
    echo "<VirtualHost $APACHE_LISTEN >
        ServerName $APACHE_SERVER_NAME
        CustomLog $PROJECT_ROOT/logs/access.log combined
        DocumentRoot $PROJECT_ROOT
        ErrorLog $PROJECT_ROOT/logs/error.log
        ServerAlias www.$APACHE_SERVER_NAME

        Include '$PROJECT_ROOT/httpd.conf'
</VirtualHost>

WSGIPythonPath $PROJECT_ROOT
" | sudo tee /etc/apache2/sites-enabled/$PROJECT_NAME
 
    chmod -R ugo+rw media/
    chmod -R a+rw media/
    mkdir logs 2>/dev/null
    sudo /etc/init.d/apache2 restart
}
 
# деплой под ключ на пустой машине
all () 
{
    echo "Выполняем деплой проекта под ключ."
    distr_install
    git_init
    project_req
    create_db
    django
    apache_set
    echo "Скрипт отработан."
    exit
}
 
 
 
clear
clear
 
echo "
Скрипт выполняется последовательно, по шагам. Можно запустить выполнение сразу всех шагов используя пункт меню 7 или пройти по всем меню подряд для пущего контроля.

Меню:"
 
OPTIONS="ПО Гит Зависимости БазаДанных Джанго apache ВСЁ Выход"
select opt in $OPTIONS
do
    case $opt in
        "ПО")             distr_install   ;;  
        "Гит")            git_init        ;;
        "Зависимости")    project_req     ;;
        "БазаДанных")     create_db       ;;
        "Джанго")         django          ;;
        "apache")         apache_set      ;;
        "ВСЁ")            all             ;;
        "Выход")          exit            ;;
    esac
done

