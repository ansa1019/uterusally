# User Profile

## Table of Contents

- [Content](#content)
  - [Table](#table-of-contents)
  - [Usage](#usage)


## Table
* profile

<br/>

| Column Name | Type | Associate | notice                                                                     |
|-------------|------|-----------------|----------------------------------------------------------------------------|
| user| ForeignKey |`Django.User`| **與原生的Django.User連接,其他沒什麼特別可以照常使用**                                        |
|user_name| CharField           |  | **姓名**                          |
|email| EmailField | | **unique=True** |
|user_image| ImageField | | **會丟到user_image的資料夾，回傳url**                                                |
|nickname| CharField | | **unique=True，出事會回傳"profile with this nickname already exists."<br/>可以用此在前端防呆** |
|gender| CharField | |                                                                            |
|birthday| DateField | |                                                                            |
|phone| CharField | |                                                                            |
|address| CharField | |                                                                            |
|page_music| FileField | | **會丟到user_page_music的資料夾，回傳url**                                                 |

<br/>

-------------------

* bodyProfile

<br/>

| Column Name | Type                 | Associate   | notice                          |
|-------------|----------------------|-------------|---------------------------------|
| user| ForeignKey           | `Django.User` |                                 |
| height| PositiveIntegerField           |  | **身高**                          |
| weight| PositiveIntegerField           |  | **體重**                          |
| family_planning| CharField           |  | **家庭計畫**                        |
| medical_history| CharField           |  | **病史，可以做成`ArrayField`儲存，如果有需求** |
| other_medical_history| TextField           |  | **其他病史**                        |
| doctor_advice| TextField           |  | **醫囑**                          |
| allergy| CharField           |  | **過敏**                          |
| marriage| BooleanField           |  | **婚姻狀況**                        |


## Usage

a. profile
----------------------------------------------------------------------------------------------------------------------------

| url                                   | Type                       | notice                                                   |
|---------------------------------------|----------------------------|----------------------------------------------------------|
| api/userprofile/profile/              | POST/GET                   | **create/<br/>`list`目前設計成直接get就能得到使用者資料}**               |
| /api/userprofile/profile/{content_ID} | retrieve{GET}/PATCH/DELETE | **`detail`{同list，也可使用/content_id來query/}<br/>/update/delete** |


<br/>


### 1. post


<br/>

-------------------

Js fetch範例
----------------------------------------------------------------------------------------------------------------------------

<br/>

### 1. post

----------------------------------------------------------------------------------------------------------------------------

<br/>


```js
// post profile
// 寫無的地方推空的也可以，有些設計頁面上的布林值也好判斷

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();

formdata.append("user_image", fileInput.files[0], "File path");
formdata.append("nickname", "qaq");
formdata.append("gender", "男");
formdata.append("birthday", "2000-06-09");
formdata.append("phone", "0978878787");
formdata.append("address", "神奇地方");
formdata.append("page_music", fileInput.files[0], "File path");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/profile/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

"""  response
  {
      "id": 6,
      "user": 2,
      "user_image": "http://127.0.0.1:8000/user_image/Screenshot_2023.02.18_04.04.00.253_TGCmsBG.png",
      "nickname": "qaq",
      "gender": "男",
      "birthday": "2000-06-09",
      "phone": "0978878787",
      "address": "神奇地方",
      "page_music": "http://127.0.0.1:8000/user_page_music/01_-_Main_Theme_-_Stars_at_Our_Backs_8Ct6HoM.m4a"
  }
"""


```

### 2. get

----------------------------------------------------------------------------------------------------------------------------

<br/>


```js 
// list and detail
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/profile/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

// 如果是用api/userprofile/profile/{object_id}/的話，回傳的就不會是list
"""  response
[
    {
        "id": 6,
        "user": 2,
        "user_image": "http://127.0.0.1:8000/user_image/Screenshot_2023.02.18_04.04.00.253_TGCmsBG.png",
        "nickname": "qaq",
        "gender": "男",
        "birthday": "2000-06-09",
        "phone": "0978878787",
        "address": "神奇地方",
        "page_music": "http://127.0.0.1:8000/user_page_music/01_-_Main_Theme_-_Stars_at_Our_Backs_8Ct6HoM.m4a"
    }
]
"""

```

### 3. patch/put

----------------------------------------------------------------------------------------------------------------------------

<br/>


```js
// patch/put其實都可以，不太建議用put，避免寫錯整塊資料不見

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("user_image", fileInput.files[0], "/path/to/file{當不輸入的時候Postman會這樣顯示}");
formdata.append("nickname", "qaq");
formdata.append("gender", "男");
formdata.append("birthday", "2000-06-09");
formdata.append("phone", "0978878787");
formdata.append("address", "神奇地方");
formdata.append("page_music", fileInput.files[0], "File path");

var requestOptions = {
  method: 'PATCH',
  //method: 'PUT',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/profile/6/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


"""  response
{
    "id": 6,
    "user": 2,
    "user_image": null,
    "nickname": "qaq",
    "gender": "男",
    "birthday": "2000-06-09",
    "phone": "0978878787",
    "address": "神奇地方",
    "page_music": "http://127.0.0.1:8000/user_page_music/01_-_Main_Theme_-_Stars_at_Our_Backs_lopgOYc.m4a"
}
"""

```

### 4. delete

----------------------------------------------------------------------------------------------------------------------------

<br/>


```js
// 不知道什麼狀況會用到，但是先寫著
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();


var requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/profile/6/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


b. bodyProfile
----------------------------------------------------------------------------------------------------------------------------

| url                                   | Type                       | notice                                                   |
|---------------------------------------|----------------------------|----------------------------------------------------------|
| api/userprofile/bodyProfile/              | POST/GET                   | **create/<br/>`list`目前設計成直接get就能得到使用者資料}**               |
| /api/userprofile/bodyProfile/{content_ID} | retrieve{GET}/PATCH/DELETE | **`detail`{同list，也可使用/content_id來query/}<br/>/update/delete** |



<br/>


### 1. post

----------------------------------------------------------------------------------------------------------------------------

<br/>


```js
// 寫無的地方推空的也可以，有些設計頁面上的布林值也好判斷
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("height", "199");
formdata.append("weight", "89");
formdata.append("family_planning", "");
formdata.append("expecting", "");
formdata.append("medical_history", "");
formdata.append("other_medical_history", "");
formdata.append("medication", "");
formdata.append("doctor_advice", "");
formdata.append("allergy", "");
formdata.append("marriage", "");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/bodyProfile/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


""" response
{
    "id": 3,
    "user": 3,
    "height": 199,
    "weight": 89,
    "family_planning": "",
    "expecting": "",
    "medical_history": "",
    "other_medical_history": "",
    "medication": "",
    "doctor_advice": "",
    "allergy": "",
    "marriage": false
}
"""

```

<br/>


### 2. get

----------------------------------------------------------------------------------------------------------------------------

<br/>


```js
// 同profile，get的時候就會自動抓user

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/bodyProfile/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

// 如果是用api/userprofile/bodyProfile/{object_id}/的話，回傳的就不會是list
""" response
[
    {
        "id": 3,
        "user": 3,
        "height": 199,
        "weight": 89,
        "family_planning": "",
        "expecting": "",
        "medical_history": "",
        "other_medical_history": "",
        "medication": "",
        "doctor_advice": "",
        "allergy": "",
        "marriage": false
    }
]
"""

```

<br/>

### 3. patch

----------------------------------------------------------------------------------------------------------------------------

<br/>


```js
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

// 因為這邊是用patch，所以不用把所有的欄位都填滿，只要填要改的就好
// 如果是用put的話，請把所有欄位都填滿原本response的值
var formdata = new FormData();
formdata.append("marriage", "1");

var requestOptions = {
  method: 'PATCH',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/bodyProfile/3/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));



""" response
{
    "id": 3,
    "user": 3,
    "height": 199,
    "weight": 89,
    "family_planning": "",
    "expecting": "",
    "medical_history": "",
    "other_medical_history": "",
    "medication": "",
    "doctor_advice": "",
    "allergy": "",
    "marriage": true
}
"""
```

<br/>


c. subscribe
----------------------------------------------------------------------------------------------------------------------------

| url                                   | Type     | notice                        |
|---------------------------------------|----------|-------------------------------|
| api/userprofile/subscribe/              | POST/GET | post一次訂閱，第二次退訂/GET就輸出登入的人的sub |


<br/>


### 1. post

----------------------------------------------------------------------------------------------------------------------------

<br/>

```js
// 訂閱動作
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
// 直接塞入要被訂閱的人名就好，nickname也行
formdata.append("subscribe", "aaa654123");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/subscribe/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


```js
// 獲得訂閱的人
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/userprofile/subscribe/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


""" response
{
    "subscribe": [
        "qaq2016712",
        "aaa654123",
        "qazwsx08ghj",
        "ccc654123"
    ]
}
"""
```