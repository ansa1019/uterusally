Task
------------


## Table of Tasks

<br>

* Task
---------
| Column Name | Type                             | Associate | notice             |
|-------------|----------------------------------|-----------|--------------------|
| title       | CharField                        |           | 任務名稱               |
|point| PositiveIntegerField             | | 任務獲得的點數            |
|type| CharField/TYPE_CHOICES{在admin可選} | | 目前分為:<br/>每日/每周/活動 |
|progress| PositiveIntegerField             | | 任務目標的進度            |
|deadline| DateTimeField                    | | 結束日期，給活動任務用        |
|requirement| CharField                        | | 任務目標               |
|is_active| BooleanField                     | | 給活動任務判斷用           |


<br>


* taskRecord
---------------
| Column Name | Type                             | Associate | notice             |
|-------------|----------------------------------|-----------|--------------------|
| user        | ForeignKey                       | Django.User   |                    |
| task        | ForeignKey                       | Task      |                    |
|progress| PositiveIntegerField             | | 任務目標的進度            |
|is_done| BooleanField                     | | 是否完成               |

<br>

## API-Usage

-----------------

<br>

### Task-Endpoints
通常不會使用到這個，它們好像只會在後端新增

-----------------------------

| url                   | Type | notice      |
|-----------------------|------|-------------|
| /api/task/            | GET  | 取得所有任務|


<br>


### TaskRecord-Endpoints

-----------------------------

| url                   | Type | notice      |
|-----------------------|------|-------------|
| /api/taskRecord/      | GET  | 取得所有任務紀錄|
| /api/taskRecord/      | POST | 新增任務紀錄  |



<br>


### Example-Js-Fetch

<br>


TaskRecrod
------------

```js
// /api/taskRecord/ GET 使用者頁面顯示使用
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/task/taskRecord/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


```js
// /api/taskRecord/ POST 使用者完成任務時使用



var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Jwt Token");

var formdata = new FormData();
formdata.append("task_title", "新手任務A");
formdata.append("progress", "1"); //不填入的話就會自動是1 但它們的需求自己也沒寫這會不會改

// example
// formdata.append("task_title", "新手任務A");



var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/task/taskRecord/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```