# 臺北市國中小集中化網站系統

## 如何開發

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
