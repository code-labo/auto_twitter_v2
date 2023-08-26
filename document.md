# Auto Twitter v2

## Error resolution

### Edgeのユーザーをコピーするとき

#### エラー内容
デフォルトのユーザーをコピーするときに、毎回↓のエラーが出る  

<center>
<img src="document_resources/image.png" width="500">
</center>

このファイルは、ログインしたときのキャッシュとかが残っている。  
そのため、ちゃんとコピーしないと、twitterにログインした状態でedgeを開くことができない。

#### 解決法

以下のパスにファイル自体は存在するので、個別でコピーすればよい

~~~bash
C:\Users\3meko\AppData\Local\Microsoft\Edge\User Data\BrowserMetrics\BrowserMetrics-XXXXXXXX-XXXX.pma
~~~