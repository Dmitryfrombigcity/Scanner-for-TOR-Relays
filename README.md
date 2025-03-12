## Scanner for available TOR Relays.
![pic1](https://github.com/user-attachments/assets/eae7917a-80b8-4009-bed6-7186fba2e052)
## Prerequisites
Однажды утром упали `bridges` и `Telegram` работал не быстро, а запрос на новые мосты отправил с неправильным `subject`,
тогда мне и попалась эта [ссылка](https://github.com/ValdikSS/tor-relay-scanner). 
На основе чего и была написана эта маленькая программа для облегчения жизни.
## Abstract
Основная идея была просканированить `public relays` на доступность со своего адреса.  
Tor предоставляет такой список. Однако доступ к нему заблокирован, здесь я просто воспользовался способом, предпоженным в оригинальном варианте.
Однако использование обычных `relay`  в качестве `vanilla bridge` т.е. с отсутствием `obfuscation`  
имеет ряд последствий. Нехорошие люди видят траффик, характерный для Tor, и если вас блокируют по протоколу, то стоит обратиться [сюда](https://bridges.torproject.org/options).
>BridgeDb can provide bridges with several types of Pluggable Transports, which can help obfuscate your connections to the Tor Network, making it more difficult for anyone watching your internet traffic to determine that you are using Tor.
>
Cуществуют различные виды дистрибуции мостов, `Telegram`, наверное, самый удобный. 
Мы же хотим сами подобрать что-нибудь подходящее.  
Во-первых, стоит воспользоваться `Tor Metrics` и скачать только работающие, рекомендованные `relays`, а также выбрать интересующие нас параметры.  
Каждый `relay` имеет ряд `flags` 
>"Authority" if the router is a directory authority.  
>"BadExit" if the router is believed to be useless as an exit node
   (because its ISP censors it, because it is behind a restrictive
   proxy, or for some similar reason).  
>"Exit" if the router is more useful for building
   general-purpose exit circuits than for relay circuits.  The
   path building algorithm uses this flag; see path-spec.txt.
>"Fast" if the router is suitable for high-bandwidth circuits.  
>"Guard" if the router is suitable for use as an entry guard.  
>"HSDir" if the router is considered a v2 hidden service directory.  
>"NoEdConsensus" if any Ed25519 key in the router's descriptor or
   microdesriptor does not reflect authority consensus.
>"Stable" if the router is suitable for long-lived circuits.
>"Running" if the router is currently usable over all its published
   ORPorts. (Authorities ignore IPv6 ORPorts unless configured to
   check IPv6 reachability.) Relays without this flag are omitted
   from the consensus, and current clients (since 0.2.9.4-alpha)
   assume that every listed relay has this flag.  
>"Valid" if the router has been 'validated'. Clients before
   0.2.9.4-alpha would not use routers without this flag by
   default. Currently, relays without this flag are omitted
   fromthe consensus, and current (post-0.2.9.4-alpha) clients
   assume that every listed relay has this flag.  
>"V2Dir" if the router implements the v2 directory protocol or
   higher.
>   
Нас будет интересовать `Guard`, что можно сделать, отфильтровав по параметру `guard_probability`.

### Disclaimer
Вы можете и не **In Tor metrics We Trust**, закоментировав это условие в коде, и получите 3-4 сотни записей вместо десятка.  
И хотя основная задача `Guard` это обеспечение анонимности, к нему предъявляют определённые требования по стабильности и скорости.  
Так что это на ваш выбор. [Вот здесь](https://metrics.torproject.org/rs.html) можно посмотреть подробную статитстику по `relays` и многое другое.  

## Cloning the project and installing dependencies
#### Для начала работы с проектом необходимо склонировать репозиторий на ваш компьютер.  
Для этого выполните следующую команду в терминале: 
```
git clone https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays
```
#### Перейдите в директорию проекта:
```
cd Scanner-for-TOR-Relays
```
#### Установка зависимостей
Если вы используете `pip`:  
#### Создайте и активируйте виртуальное окружение:
```
pip install virtualenv &&
virtualenv -p python3.12 venv &&
source venv/bin/activate
```
В системе должен быть python3.12, если нет, то [установите](https://www.python.org/downloads/)  
Возможно придётся указать полный путь к интерпретатору.  
*Для Windows активация будет другая:*
```
venv\Scripts\activate.bat
```
#### Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
#### Если вы предпочитаете использовать Poetry, выполните следующие шаги:
Убедитесь, что [Poetry](https://python-poetry.org/) установлен. Если нет, установите его:
```
pip install poetry
```
#### Установите зависимости проекта:
```
poetry install
```
#### Активируйте виртуальное окружение, созданное Poetry:
```
poetry shell
```
### Запустите программу:
```
python main.py
```
## Troubleshooting
Поскольку на разных системах могут быть разные ограничения на количество одновременно открытых файлов,  
я решил сделать это регулируемым.  
В файле `settings.py` можете попробовать увеличить
>**OPEN_FILES = 1000**
>
если получите ошибку  
>*Reduce the OPEN_FILES value in settings.py to avoid the "Too many open files" error.*
>
вернитесь обратно.
>**TIMEOUT = 10**
>
Устанавливает время ожидания для сетевых соединений. Дано с запасом, мне хватало и пары секунд.





                  
