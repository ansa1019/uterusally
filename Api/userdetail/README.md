# User Detail


## Table
* postStoraged

<br/>

| Column Name | Type      | Associate | notice                              |
|-------------|-----------|-----------------|-------------------------------------|
| user        | ForeignKey |`Django.User`| **與原生的Django.User連接,其他沒什麼特別可以照常使用** |
| post        | ForeignKey |  | **姓名**                              |
| storage_name       | CharField | | 資料夾名稱，預設是未命名資料夾       |


-------------------------
## API
### postStoraged
* **Method**: GET
* **URL**: /api/userdetail/postStoraged/
* **Description**: 取得使用者的所有資料夾
* **Response**: 
    ```json
      {
        "id": 2,
        "post": [
            "小產後補品推薦！",
            "月經來/經痛喝什麼？這幾種飲品比黑糖水還要好",
            "測試",
            "0329發文測試"
        ],
        "storage_name": "111",
        "user": 1
      }
    ```
* **Example**:
    ```javascript
      var myHeaders = new Headers();
      myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyOTI3MDczLCJpYXQiOjE3MTI4NjcxMzMsImp0aSI6Ijc5NGM5OTUwMTNlZjQ4NGQ4ZGJkMjU5MWUxN2I0MGMwIiwidXNlcl9pZCI6MX0.GSZSGJL35gNQQM0vczJ0X8M0lmw_BIrznMEPxU0pkPU");

      var formdata = new FormData();

      var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
      };

      fetch("http://127.0.0.1:8000/api/userdetail/postStoraged/", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
    ```

* **Method**: POST/UPDATE
* **URL**: /api/userdetail/postStoraged/
* **Description**: 新增或修改使用者的資料夾
* **Request**:
    ```json
      {
            "message": "新增成功"
      }
    ```
* **Example**:
    ```javascript
      // 新增的時候也會自動判斷有沒有新的，如果有就會自動加入
      var myHeaders = new Headers();
      myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyOTI3MDczLCJpYXQiOjE3MTI4NjcxMzMsImp0aSI6Ijc5NGM5OTUwMTNlZjQ4NGQ4ZGJkMjU5MWUxN2I0MGMwIiwidXNlcl9pZCI6MX0.GSZSGJL35gNQQM0vczJ0X8M0lmw_BIrznMEPxU0pkPU");

      var formdata = new FormData();
      formdata.append("storage_name", "111");
      formdata.append("post_title", "測試");

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
      };

      fetch("http://127.0.0.1:8000/api/userdetail/postStoraged/", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
    ```
