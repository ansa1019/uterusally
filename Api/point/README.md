# Point


## Table of Points

### Point

----------------------------

| Column Name | Type | Associate | notice |
|-------------|------|-----------|--------|
| user          | ForeignKey  | Django.User   |        |
| point        | IntegerField  |           |        |
| created_at   | DateTimeField |           | 自動生成   |

<br>


### Gift

----------------------------


| Column Name | Type | Associate | notice                 |
|-------------|------|-----------|------------------------|
| giver          | ForeignKey  |      Django.User     | 贈與者                    |
| receiver        | ForeignKey  |     Django.User      | 接收者,目前用username來filter |
| point        | IntegerField  |           |                        |
| created_at   | DateTimeField |           | 自動生成                   |

<br>


### Exchange

-------------------


| Column Name | Type | Associate | notice                                                          |
|-------------|------|-----------|-----------------------------------------------------------------|
| user          | ForeignKey  |      Django.User     | 贈與者                                                             |
| gift        | ForeignKey  |     Gift      | 接收者,目前用username來filter                                          |
| created_at   | DateTimeField |           | 自動生成                                                            |
|exchange_token|CharField| | 交換碼,目前是用username+product_title+product_point來生成b64code進行反向驗證來交換 |
|created_at|DateTimeField| | 自動生成                                                            |

<br>


## API-Usage


### Point-Endpoints

-----------------------------

| url                   | Type | notice          |
|-----------------------|------|-----------------|
| /api/point/userPoint/ | GET  | 取得user point    |
| /api/point/userPoint/ | POST | 使用者獲得點數/完成任務後使用 |
| /api/point/gift/      | POST  | 使用者贈送點數         |
| /api/point/exchange/  | POST  | 使用者兌換禮物         |


<br>




### Example-Js-Fetch
<br>

userPoint
-----------------------------


```js
// get user point
// /api/point/userPoint/ GET METHOD
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/point/userPoint/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

<br>

```js
// post user point when user finished task
// /api/point/userPoint/ POST METHOD

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();
formdata.append("point", "30");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/point/userPoint/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

```


<br>

gift
-----------------------------

```js
// /api/point/gift/ GET METHOD 獲取禮物點數紀錄，給或被給
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();


var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/point/gift/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

<br>

```js
// /api/point/gift/ POST METHOD 給予禮物點數


var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();
formdata.append("point", "30");
formdata.append("receiver", "bbb654123");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/point/gift/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


<br>


exchange
-----------------------------

```js
// /api/point/exchange/ GET METHOD 獲取兌換紀錄

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();


var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/point/exchange/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


```



<br>

```js
// /api/point/exchange/ POST METHOD 兌換禮物點數

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();
//formdata.append("product", "product title");
formdata.append("product", "保衛君");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/point/exchange/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```