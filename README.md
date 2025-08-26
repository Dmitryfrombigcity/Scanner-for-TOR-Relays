## Scanner for available TOR Relays.  

![pic1](https://github.com/user-attachments/assets/eae7917a-80b8-4009-bed6-7186fba2e052)
## Prerequisites
Однажды утром упали `bridges` и `Telegram` работал не быстро, а запрос на новые мосты отправил с неправильным `subject`,
тогда мне и попалась эта [ссылка](https://github.com/ValdikSS/tor-relay-scanner). 
На основе чего и была написана эта маленькая программа для облегчения жизни.
## Abstract
Основная идея была просканированить `public relays` на доступность со своего адреса.  
Tor предоставляет такой список. Однако доступ к нему заблокирован, здесь я просто воспользовался способом, предпоженным в оригинальном варианте.  
Использование обычных `relay`  в качестве `vanilla bridge` т.е. с отсутствием `obfuscation` 
имеет ряд последствий. Нехорошие люди видят траффик, характерный для Tor, и если вас блокируют по протоколу, то стоит обратиться [сюда](https://bridges.torproject.org/options).
>BridgeDb can provide bridges with several types of Pluggable Transports, which can help obfuscate your connections to the Tor Network, making it more difficult for anyone watching your internet traffic to determine that you are using Tor.
>
Cуществуют различные виды дистрибуции мостов, `Telegram`, наверное, самый удобный. 
Мы же хотим сами подобрать что-нибудь подходящее.  
Во-первых, стоит воспользоваться `Tor Metrics` и скачать только 
- работающие,
- рекомендованные `relays`,
- а также выбрать
   - интересующие нас параметры,
   - отсортировать по заявленной скорости.  
  
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
Из этого списка нас будет интересовать `Guard`, что можно сделать, отфильтровав по параметру `guard_probability`.


## Cloning the project and installing dependencies
### Для начала работы с проектом необходимо склонировать репозиторий на ваш компьютер.  
#### Для этого выполните следующую команду в терминале: 
```
git clone https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays
```
#### Перейдите в директорию проекта:
```
cd Scanner-for-TOR-Relays
```
В системе должен быть один из поддерживаемых интерпретаторов, если нет, то [установите](https://www.python.org/downloads/)   

[![python-3.8](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.8.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.8.yml)
[![python-3.9](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.9.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.9.yml)
[![python-3.10](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.10.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.10.yml)
[![python-3.11](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.11.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.11.yml)
[![python-3.12](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.12.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.12.yml)
[![python-3.13](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.13.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/python-3.13.yml)  
[![ubuntu-latest macos-latest windows-latest](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/os_test.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/os_test.yml)

#### Установите зависимости
Если вы используете `pip`:  
#### Создайте и активируйте виртуальное окружение:
*Возможно придётся указать путь к интерпретатору.*
```
pip install virtualenv &&
virtualenv -p python3.12 venv &&
source venv/bin/activate
``` 
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
>**TIMEOUT = 5**
>
Устанавливает время ожидания для сетевых соединений. Дано с запасом, мне хватало и пары секунд.
## Startup options

Добавлены опции для фильтрации доступных `relays`
- --guard   (-g)        показывает только `relays` с `guard_probability` > 0
  
  >**guard_probability**
  >History object containing the probability of this relay to be selected for the guard position. This probability is calculated 
  >based on consensus weights, relay flags, and bandwidth weights in the consensus.
  >
- --bandwidth   (-b)    показывает только `relays` с `advertised_bandwidth` > 0
  
  >**advertised_bandwidth**  
  >Bandwidth in bytes per second that this relay is willing and capable to provide.
  >Missing if this information cannot be found.
  >
- --top (-t)           показывает пять лучших `relays` и выводит шаблоны для копирования. 
### Примеры запуска программы: 
![relays_4](https://github.com/user-attachments/assets/a37f192a-217c-4579-892f-6362a72dfc31)

----------------------------------- 
### Добавлен `Dockerfile`.  
Теперь вы можете создать образ и запустить в [`Docker`](https://www.docker.com/),
или запустить образ прямо из [`DockerHub`.](https://hub.docker.com/r/dmitryfrombigcity/tor_relays)  
[![Publish Docker image](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/actions/workflows/docker-image.yml)  
```
docker run --rm dmitryfrombigcity/tor_relays 
```
```
docker run --rm dmitryfrombigcity/tor_relays --bandwidth
```
```
docker run --rm dmitryfrombigcity/tor_relays --guard
```
```
docker run --rm dmitryfrombigcity/tor_relays --top
```

### Updates.  

- **Начиная с `v2.3`** информация с сайта `onionoo.torproject.org` кэшируется каждые 8 часов.  
- **Начиная с `v2.4`** вы можете использовать SOCKS5 Proxy, в частности от TOR, для уточнения текущей информации, если у вас заблокирован оригинальный сайт.  
  Например: 
  ```
  docker run --rm  --network=host --env HTTPS_PROXY=socks5h://localhost:9150 dmitryfrombigcity/tor_relays:latest  
  ```
- **Начиная с `v2.5`** улучшено отображение ошибок.  
  Например:

  `# URL:onionoo.torproject.org >> Error:SSLError`
   
- **Начиная с `v2.6`** добавлена опция:    
  --silent  (-s) подавляет вывод `progress bar`  
  Основная идея использования этой опции, это [cron]( https://ru.wikipedia.org/wiki/Cron)  
  Например:
  ```
  crontab -e
  ```
  ```
  0 9 * * * date >> ~/relays  && docker run --rm dmitryfrombigcity/tor_relays -ts >> ~/relays
  ```
  Будет ежедневно запускаться в 9.00 и записывать результаты в файл `relays`.  
- **Начиная с `v2.7`**
    - Создаётся переменная `NO_PROXY` по умолчанию `raw.githubusercontent.com`, что позволяет не проксировать обращение к сайту при использовании  `ALL_PROXY` `HTTPS_PROXY`,  
      однако эту переменную можно явно переписать в командной строке.  
      Например: 
      ```
      docker run --rm  --network=host --env HTTPS_PROXY=socks5h://localhost:9150  --env NO_PROXY='' dmitryfrombigcity/tor_relays:latest
      ```
    - Добавлены опции:    
      --orbot  (-o) выводит `bridges` только в формате для [Orbot](https://orbot.app).    
        Основная идея использования этой опции, это запуск на `Android` при помощи [Termux](https://termux.dev).  
      - Установка [отсюда](https://f-droid.org/packages/com.termux/) или [отсюда](https://github.com/termux/termux-app).  
      - Получите доступ к хранилищу -> [руководство](https://wiki.termux.com/wiki/Internal_and_external_storage)   
        ```
        termux-setup-storage
        ```
      - Установите необходимые пакеты -> [руководство](https://wiki.termux.com/wiki/Python)  
        ```
        pkg install python curl rust   
        ```
      - Установите необходимые зависимости ->   
        ```
        pip install requests[socks] pydantic pydantic-settings
        ```
        *без установки rust'a установить pydantic не удалось*
        
       - Так как `Docker` не работает на `Android`, скопируем необходимые файлы
         ```
         mkdir ~/storage/shares/Relays && cd ~/storage/shares/Relays && curl -o 'main.py' https://raw.githubusercontent.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/refs/heads/main/main.py && curl -o '.env' https://raw.githubusercontent.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/refs/heads/main/.env && curl -o 'arguments.py' https://raw.githubusercontent.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/refs/heads/main/arguments.py && curl -o 'exceptions.py' https://raw.githubusercontent.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/refs/heads/main/exceptions.py && curl -o 'features.py' https://raw.githubusercontent.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/refs/heads/main/features.py && curl -o 'schemas.py' https://raw.githubusercontent.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/refs/heads/main/schemas.py && curl -o 'settings.py' https://raw.githubusercontent.com/Dmitryfrombigcity/Scanner-for-TOR-Relays/refs/heads/main/settings.py
         ```
      - Запускаем, опции и переменные среды по желанию
        ```
        python main.py -o
        ```
        ```
        env all_proxy=socks5h://localhost:9050 python main.py -o
        ```    
      --browser (-r)  выводит `bridges`  в стандартном формате для `Tor`.     
      
      
   
  









                  
