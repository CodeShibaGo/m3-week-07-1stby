# CSRF Token

### 什麼是 CSRF 攻擊？
    CSRF(跨站請求偽造)是一種網路攻擊手法。攻擊者利用已認證用戶的身分，再用戶不知情的情況下，進行未授權的操作。
    意思是：當我登入我的網路銀行時,在未登出的情況下，不小心逛到了病毒網站，而這個網站偷偷使用我的名義，進行轉帳的動作。
### 該如何預防？
- 普遍防禦CSRF的方法有兩種:<br>
1.檢查 referer欄位<br>
2.加入驗證token
#### 檢查referer欄位
    這個方法很簡單，既然攻擊是來自於非銀行網站，那我就確認需求的來源就行了，而http協定中就有一個referer欄位記錄著這個請求是從哪個網站發出來的，只要不是銀行網站發出來的請求，網站這邊一律不接受!

    依照這樣的方式，我們可以用快速且低成本的方式來防範CSRF，只是有個問題，就是駭客能否偽造這個referer欄位呢? 如果他也可以偽裝成銀行來源，那用戶就還是會被攻擊。顯然這種方法只能初步防禦CSRF，碰到進階一點的攻擊手法就會再度被破解。
#### 加入驗證token
    CSRF的核心概念，就是銀行不知道發出請求的人是不是攻擊者，那按照這個思路，只要使用者能提出一個唯一且保密的序號，攻擊者拿不到這個序號，自然就不能偽裝成使用者，而這個序號，就是我們稱的CSRF Token，這個Token是由銀行server產生，並且加密存在session中的，其他人無法仿造，只有透過server給使用者，並在一定時間內刷新。當使用者想做任何交易的時候，銀行server就會請使用者提供CSRF Token，如果不能提供，就代表這次的請求就是攻擊者，那銀行server就不予理會。
參考文件：
 https://medium.com/@Tommmmm/csrf-%E6%94%BB%E6%93%8A%E5%8E%9F%E7%90%86-d0f2a51810ca

### 說明如何在 flask 專案中使用以下 csrf_token()語法。
 安裝 flask-wtf<br>
 `pip install flask-wtf`<br>

 從 flask_wtf 中載入 CSRFProtect，並設定 SECRET_KEY<br>

 ```python
 from flask_wtf import CSRFProtect
 app.config['SECRET_KEY'] = os.urandom(24)
 csrf = CSRFProtect(app)
 ```
 在所有表單中加入 hidden 欄位 csrf_token
```html
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <input type="text" name="email" class="form-control form-control-lg" placeholder="max@email.com">
</form>
```
在 AJAX 請求中，將 CSRF token 加入到請求頭中。例如在 jQuery 的 AJAX 請求中，可以在 beforeSend 函數中設置請求頭1。

```javascript
$.ajax({
    url: '你的URL',
    type: 'POST',
    beforeSend: function(xhr) {
        var token = $("meta[name='_csrf']").attr("content");
        var header = $("meta[name='_csrf_header']").attr("content");
        if (header && token) {
            xhr.setRequestHeader(header, token);
        }
    },
    success: function(data) {
        // 處理成功的回應
    },
    error: function(data) {
        // 處理錯誤的回應
    }
});

```
