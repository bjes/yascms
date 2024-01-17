如何單機佈署
============

yascms 支援單一佈署，但目前支援的作業系統只有 Debian Buster 10。

請先安裝好一台 Debian Buster 後，將程式碼的 repo 抓下來搬移至確定目錄後，將設定檔設好，
最後使用 root 權限執行專案根目錄下的 install 即可全自動佈署完成。以下簡單的示範操作步驟：

1. 確認作業系統已有 git 套件。

.. code-block:: bash
   
   # 用 root 權限執行
   apt install git -y

2. 下載原始碼並搬移至想要的目錄位置。

.. code-block:: bash
   
   # 以下都是用 root 權限執行
   # 比方把專案都放到 /srv/www 目錄下，網站網域為 tpyass-demo.fossn.io
   mkdir -p /srv/www
   cd /srv/www
   git clone https://webcode.tp.edu.tw/tcenc/yascms tpyass-demo.fossn.io
   cd tpyass-demo.fossn.io
   cp ansible/production.conf.sample ansible/production.conf
   # 修改完 ansible/production.conf 的設定值後執行佈署
   # 由於會產生 dhparam.pem 會需要一點時間請耐心等候
   ./install

3. 網站佈署完成，可使用瀏覽器瀏覽網站。預設的管理者帳密是 admin / admin4yascms　。
