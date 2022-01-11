# 臺北市國中小集中化網站系統

## DEMO 站台

<http://demo.bjes.tp.edu.tw>

最高管理者帳號密碼為 admin / admin

一般使用者有兩組帳號，一組是 user1 / user1 ，另一組是 user2 / user2 。

## 如何申請

目前的網站還有細節要調整，約莫 2020/11 月中會將學校必要的幾個細節都修正完成。

若貴校想要參與第一批次的移轉，可填寫申請表單：

h<ttps://forms.gle/kG1uoH7mK9TEdYHa6>

有任何問題，可聯繫本專案的窗口：

- 益教網 莊維誠 <rsi0430@gmail.com>
- 濱江國小 吳佳寰 <william@pylabs.org>

## 如何回報問題

若您對網站的功能有各種功能上的建議，或是發現 bugs，都歡迎回報讓我們知道！ 回報的網址在 <https://github.com/tcenc/tp_yass/issues> ，您需要先申請 [GitHub](https://github.com) 的帳號才能上去建立 issue 回報。

## 如何開發

若對參與開發有興趣，歡迎來信：

- 益教網 莊維誠 <rsi0430@gmail.com>
- 濱江國小 吳佳寰 <william@pylabs.org>

我們會建立相關的帳號權限給您。若您想將程式碼抓下來跑在自己的機器上，可參考以下步驟：


### 將原始碼 clone 至本機

```shell
export GIT_BASE_DIR=~/git
mkdir -p $GIT_BASE_DIR
cd $GIT_BASE_DIR
git clone https://webcode.tp.edu.tw/tcenc/tp_yass.git
```

### 建立開發環境

可以選擇使用 ansible playbook 建置，或是手動建置，以下說明此兩種作法，請擇一使用。

#### 使用 ansible playbook 建置

* 使用 pip3 安裝 ansible

```shell
# 在 Debian 下要先安裝 python3-pip 套件 才有 pip3 指令
pip3 install ansible --user
```

* 使用 ansible playbook 建置開發環境，注意執行此指令的帳號需有 sudo root 的權限

```shell
ansible-playbook develop.yml
```

#### 手動建置

* 建立專案運行的 venv 環境

```shell
cd tp_yass
# 在 Debian 上需要安裝 python3-venv 套件
python3 -m venv .venv
```

* 更新套件管理工具

```shell
.venv/bin/pip install --upgrade pip setuptools poetry
```

* 同步開發專案需要安裝的套件

```shell
poetry install
```


* 建立開發用的測試資料庫，並將資料庫 migrate 到最新版

```shell
cp development.ini.sample development.ini
# 至少要修改 development.ini 的 sqlalchemy.url 設定，
# 以對應實際的資料庫設定。請參考檔案內相關註解。
# 修改完成後再執行以下指令
.venv/bin/inv db.init-test file.delete
```


* 執行測試

```shell
.venv/bin/inv test.all
```

* 於本機開發環境啟動專案

```shell
.venv/bin/pserve development.ini --reload
```

## 相關投影片

- 2020/10/16 [臺北市集中化網站功能介紹與佈署申請](https://docs.google.com/presentation/d/18YZlmiMYo8hlSvAEi_SQQMwZuMp0ma3O_DngXFF33m4/edit?usp=sharing)


## 使用套件
- jQuery https://jquery.com MIT License
- jQuery Bonsai https://github.com/aexmachina/jquery-bonsai MIT License
- jQuery DateTimePicker https://github.com/xdan/datetimepicker MIT License
- jquery-qubit https://github.com/simonexmachina/jquery-qubit MIT License
- SmartMenus jQuery Website Menu Plugin https://www.smartmenus.org MIT License
