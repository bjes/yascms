如何開發
========

本專案目前非常需要第一線的資訊老師加入討論與開發，若您對加入本專案開發團隊有興趣，請不吝聯繫。
以下說明建立開發環境的步驟。下面的步驟皆在 Debian 10 Buster 上驗證過可正常執行，若您的環境不一樣，
需依照不同的作業系統環境微調指令。

相依的系統套件
--------------

本專案需要在系統先行安裝一些套件或元件，才能讓專案正常的運作。以下範例皆是使用 Debian Buster 10 的環境，
若您使用的是別套 distribution，請依照環境調整以下操作。

內建的系統套件
++++++++++++++

有些套件 Debian 官方有提供，我們可以直接安裝官方提供的版本：

.. code-block:: bash
   :linenos:

   sudo apt install build-essential python3-dev python3-venv python3-pip -y


外部的套件
++++++++++

這個專案會用到 MySQL 5.7.6 或更新的版本才支援的繁體中文全文檢索的功能。但這個功能，Debian Buster 官方提供的
MariaDB 卻不支援。所以我們要另外安裝 MySQL 的分支 `Percona Server`_ 。

目前最新版的 `Percona Server`_ 為 8.0 版，官方文件關於如何在 Debian 上安裝 apt source 的步驟在
`這裡 <https://www.percona.com/doc/percona-server/LATEST/installation/apt_repo.html>`_ ，以下是執行的指令步驟：

.. code-block:: bash
   :linenos:

   sudo apt-get install gnupg2 -y
   wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
   sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
   sudo percona-release setup ps80
   sudo apt-get install percona-server-server -y

.. _Percona Server: https://www.percona.com/software/mysql-database/percona-server


將原始碼 clone 至本機
---------------------

.. code-block:: bash
   :linenos:

   git clone https://github.com/fossnio/yascms.git

建立開發環境
------------

可以選擇使用 ansible playbook 建置，或是手動建置，以下說明此兩種作法，請擇一使用。

使用 ansible playbook 建置
++++++++++++++++++++++++++

使用 pip3 安裝 ansible

.. code-block:: bash
   :linenos:

   pip3 install ansible --user

使用 ansible playbook 建置開發環境，注意執行此指令的帳號需有 sudo root 的權限

.. code-block:: bash
   :linenos:

   cd yascms
   ~/.local/bin/ansible-playbook ansible/development.yml --extra-vars "db_name=資料庫名稱 db_user=資料庫帳號 db_pass=資料庫密碼"


手動建置
++++++++

建立專案運行的 venv 環境

.. code-block:: bash
   :linenos:

   cd yascms
   python3 -m venv .venv

更新套件管理工具

.. code-block:: bash
   :linenos:

   .venv/bin/pip install --upgrade pip setuptools poetry

同步開發專案需要安裝的套件

.. code-block:: bash
   :linenos:

   poetry install


建立開發用的測試資料庫，並將資料庫 migrate 到最新版

.. code-block:: bash
   :linenos:

   cp development.ini.sample development.ini
   # 至少要修改 development.ini 的 sqlalchemy.url 設定，
   # 以對應實際的資料庫設定。請參考檔案內相關註解。
   # 修改完成後再執行以下指令
   .venv/bin/inv file.delete db.import-test-data


於本機開發環境啟動專案

.. code-block:: bash
   :linenos:

   .venv/bin/pserve development.ini --reload


執行測試
--------

.. code-block:: bash
   :linenos:

   .venv/bin/inv test.all


