# Welcome to guard.sda1.net
## これは何
公開プロキシや防弾ホストなどのIPやCIDRをかき集めて包括的なIPブロックリストを作成しました。すぐに使えるnginxテンプレートやjsonデータが備わっています！

## リスト一覧

### nginx設定ファイル
 - `https://guard.sda1.net/data/nginx/block-public-proxy.conf`
    * パブリックプロキシをブロックするnginx設定ファイル

 -  `https://guard.sda1.net/data/nginx/block-bulletproof.conf`
    * 防弾ホストのCIDRをブロックするnginx設定ファイル

### ipset
 - `https://guard.sda1.net/data/ipset/public-proxy.ipset`
    * パブリックプロキシのipset

 -  `https://guard.sda1.net/data/ipset/bulletproof.ipset`
    * 防弾ホストのCIDRのipset
