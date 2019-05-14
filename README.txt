臺北市國中小集中化網站系統
==========================

如何開發
--------

- 將原始碼 clone 至本機

    export GIT_BASE_DIR=~/git
    mkdir -p $GIT_BASE_DIR
    cd $GIT_BASE_DIR
    git clone https://code.fossn.io/fossn/tp_yass.git

- 建立專案運行的 venv 環境

    cd tp_yass
    python3 -m venv .venv

- 更新套件管理工具

    .venv/bin/pip install --upgrade pip setuptools pipenv

- 同步開發專案需要安裝的套件

    .venv/bin/pipenv sync --dev

- 建立開發用的測試資料庫，並將資料庫 migrate 到最新版

    cp development.ini.sample development.ini
    # 至少要修改 development.ini 的 sqlalchemy.url 設定，
    # 以對應實際的資料庫設定。請參考檔案內相關註解。
    # 修改完成後再執行以下指令
    .venv/bin/inv db.init-test

- 執行測試

    .venv/bin/inv test.all

- 於本機開發環境啟動專案

    .venv/bin/pserve development.ini --reload
