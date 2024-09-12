# Content


## Table of contents
* category

| Column Name | Type |
|-------------|------|
| name| CharField  |


-------------------
* subcategory


| Column Name | Type | Associate | notice       |
|-------------|------|-----------------|--------------|
| name| CharField  |     |              |
| main| ForeignKey  | `category`   | **給副標用，詳細顯示再調整** |

-------------------
* TextEditorPost

| Column Name | Type                 | Associate   | notice                              |
|-------------|----------------------|-------------|-------------------------------------|
| title| CharField            |             |                                     |
| author| ForeignKey           | `Django.User` | **與原生的Django.User連接,其他沒什麼特別可以照常使用** |
| content|  |             | **目前是使用QuillJs來寫入,可改**              |
| like| ManyToManyField                   | `category`    |                                     |
| share| ..                   | `subcategory` |                                     |
| comment| ..                   |             |                                     |
| click| ..                   |             |                                     |
| bookmark| ..                   |             |                                     |
| desable| BooleanField        |             | **提供給不當文章隱藏判斷**                     |
| category| ManyToManyField        | `category`  |                                     |
| created_at| DateTimeField        |             | **正常來說會自動寫入**                       |
| is_official| BooleanField        |             | **預設False，正常邏輯營養師都是預設True**         |
| identity| CharField        |             | **沒有選可以自動寫入使用者名稱**                  |

-------------------

* TextEditorPostComment

<br>

| Column Name | Type                 | Associate   | notice                               |
|-------------|----------------------|-------------|--------------------------------------|
| post| ForeignKey           | `TextEditorPost` |                                      |
| author| ForeignKey           | `Django.User` | **與原生的Django.User連接,其他沒什麼特別可以照常使用**  |
| body| TextField           |  |                                      |
| images| ManyToManyField           |  | **沒寫在需求上說comment能不能給image/video,可刪** |
| videos| ManyToManyField           |  |                                      |
| desable| BooleanField           |  | **提供給不當文章隱藏判斷**                      |
| date| DateTimeField           |  | **正常來說會自動輸入，給時間排序用**                 |
| top| BooleanField           |  | **給至頂功能用**                           |


## Usage

a. textEditorPost

### 1. post


| url | Type                       | notice                                       |
|-------------|----------------------------|----------------------------------------------|
| /api/content/textEditorPost/ | POST/GET                   | **create/list**                              |
| /api/content/textEditorPost/{contentID}/ | retrieve{GET}/PATCH/DELETE | **detail/update/delete**                     |
| /api/content/userGetSelfComment/ | GET | **using TextEditorPostSerializer獲得使用者留過的言論** |
| /api/content/userGetSelfPost/ | GET | **using TextEditorPostCommentSerializer獲得使用者發過的文章** |

-------------------
以下範例都是使用postman來生成，可以參考，可以寫入的column都在上面以及models.py裡面
有些column會寫在serializer.py裡面，例如:
-------------------
```py
class TextEditorPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', read_only=True)  ## column
    category = categorySerializer(read_only=True, many=True) ## column
    html = serializers.SerializerMethodField() ##represent only column in this case
    plain = serializers.SerializerMethodField() ##represent column like above

    class Meta:
        model = TextEditorPost
        fields = "__all__"
```
-------------------
Js fetch範例
```js
// post content, editor當作使用quilljs
// quilljs編輯器的預設變數在此當作editor

var content = JSON.stringify(editor.getContents());
var html = editor.root.innerHTML;

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("title", "test87");
formdata.append("content", {"delta":content,"html":html});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPost/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


// post response
{
    "html": "some html",
    "plain": "some plain",
    "id": 6,
    "author": "bbb654123",
    "category": [],
    "created_at": "2023-09-08T23:17:19.222205Z",
    "title": "test87",
    "content": "<django_quill.fields.FieldQuill object at 0x00000152FA63AC50>",
    "like": 0,
    "share": 0,
    "comment": 0,
    "click": 0,
    "bookmark": 0,
    "desable": false
}
```

### 2. get

```js 
//list
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPost/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

""" format
[
    {
        "id": 2,
        "author": "bbb654123",
        "category": [],
        "html": "",
        "plain": "",
        "created_at": "2023-09-08T21:32:15.905998Z",
        "title": "test2",
        "content": "<django_quill.fields.FieldQuill object at 0x000001369AF03650>",
        "like": 0,
        "share": 0,
        "comment": 0,
        "click": 0,
        "bookmark": 0,
        "desable": false
    },
    {
        "id": 3,
        "author": "bbb654123",
        "category": [],
        "html": "",
        "plain": "",
        "created_at": "2023-09-08T21:36:27.236700Z",
        "title": "test3",
        "content": "<django_quill.fields.FieldQuill object at 0x000001369AF02D90>",
        "like": 0,
        "share": 0,
        "comment": 0,
        "click": 0,
        "bookmark": 0,
        "desable": false
    },
]
"""




//detail
var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPost/{contentID}/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

""" format
{
        "id": 6,
        "author": "bbb654123",
        "category": [],
        "html": "some html",
        "plain": "some plain",
        "created_at": "2023-09-08T23:17:19.222205Z",
        "title": "test87",
        "content": "<django_quill.fields.FieldQuill object at 0x0000013699775C50>",
        "like": 0,
        "share": 0,
        "comment": 0,
        "click": 0,
        "bookmark": 0,
        "desable": false
    }
"""
```

### 3. patch

```js
var content = JSON.stringify(editor.getContents());
var html = editor.root.innerHTML;

var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("title", "test87");
formdata.append("content", {"delta":content,"html":html});

var requestOptions = {
  method: 'PATCH',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPost/6/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

### 4. delete

```js
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();

var requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPost/6/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

b. TextEditorPostComment

### 1. post

```js
var formdata = new FormData();
formdata.append("post", "5");
formdata.append("body", "aabbccccc");
//formdata.append("uploaded_images", fileInput.files[0], "/C:/Users/bbb654123/Pictures/BlueStacks/Screenshot_2023.02.13_14.19.02.364.png");
formdata.append("uploaded_images", fileInput.files[0], "file path");
formdata.append("uploaded_images", fileInput.files[0], "file path");
formdata.append("uploaded_images", fileInput.files[0], "file path");
formdata.append("uploaded_images", fileInput.files[0], "file path");
formdata.append("uploaded_videos", fileInput.files[0], "file path");

var requestOptions = {
  method: 'POST',
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPostComment/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


### 2. get

```js
// get when trying to get all comments of a post
var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  body: formdata,
  redirect: 'follow'
};

// 更新後直接抓單一文章就會一起把comment拉出來
fetch("http://127.0.0.1:8000/api/content/textEditorPost/5/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


{
    "id": 5,
    "author": "bbb654123",
    "category": [
        {
            "id": 1,
            "name": "test category"
        }
    ],
    "html": "<p><strong><em><s><u>adsf.sakjfm;ef測試</u></s></em></strong></p>",
    "plain": "adsf.sakjfm;ef測試",
    "comments": [
        {
            "id": 6,
            "author": "qaq2016712",
            "images": [],
            "videos": [],
            "date": "2023-09-10T20:18:53.458585Z",
            "body": "aabbccccc",
            "desable": false,
            "top": false,
            "post": 5
        }
    ],
    "created_at": "2023-09-08T21:57:32.332675Z",
    "title": "test6",
    "content": "<django_quill.fields.FieldQuill object at 0x0000020AC8C733D0>",
    "like": 0,
    "share": 0,
    "comment": 2,
    "click": 0,
    "bookmark": 0,
    "desable": false
}


// get one of the comments

var formdata = new FormData();
formdata.append("post", "5");

var requestOptions = {
  method: 'GET',
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPostComment/6/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


{
    "id": 6,
    "author": "qaq2016712",
    "images": [],
    "videos": [],
    "date": "2023-09-10T20:18:53.458585Z",
    "body": "aabbccccc",
    "desable": false,
    "top": false,
    "post": 5
}
```

### 3. patch

```js
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("post", "5");
formdata.append("body", "aabbcccccdddd");
formdata.append("uploaded_images", fileInput.files[0], "file path");

var requestOptions = {
  method: 'PATCH',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPostComment/6/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


Post Metadata
-------------

## category

---------------------------


* GET
```js
// 建立category從database進去
var requestOptions = {
  method: 'GET',
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/category/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


'Response':
'''
    [
        {
            "id": 1,
            "name": "test category"
        }
    ]
'''
```


* Add category to post

```js
// create post
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("title", "new title");
formdata.append("content", "some content");
formdata.append("content_html", "<p>some content</p>");
//formdata.append("category", category_name);
formdata.append("category", "test category");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPost/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


* When user clicked post

element: ['like', 'share', 'click', 'bookmark']

```js
// using patch 
// element 是指當使用者按下['like', 'share', 'click', 'bookmark']時，要更新的欄位
// 如果按了第二次代表取消，再PATCH一次就會自動取消
// 參考流程->使用者點擊'http://127.0.0.1:8000/api/content/PostMetadataHandler/38/'觀看文章
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("element", "click");

var requestOptions = {
  method: 'PATCH',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};
// fetch("http://127.0.0.1:8000/api/content/PostMetadataHandler/{content:id}/", requestOptions)
fetch("http://127.0.0.1:8000/api/content/PostMetadataHandler/38/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));


'Response' :
'''
    {
        "like": [],
        "share": [],
        // 這裡的click代表使用者點擊過的使用者id
        "click": [
            1
        ],
        "bookmark": []
    }
'''

// 備註：click比較特別，是單純紀錄點擊數，如果使用者點擊過，再點擊一次也不會取消，其他都是使用者再點擊過，經由patch就會取消
```


## Idnetity/is_official update

-----------------------------

```js
// 新增文章時
// 文章出去之後這兩個正常來說不會再進行變動，所以只需要post
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer jwt token");

var formdata = new FormData();
formdata.append("title", "new title");
formdata.append("content", "some content");
formdata.append("content_html", "<p>some content</p>");
// formdata.append("category", category_name);
formdata.append("category", "test category");
// 通常這邊會使用userdetail的nickname跟原本的身分來選擇
// 但這邊邏輯它們也沒說清楚，所以先這樣預設流程
formdata.append("identity", "bbbbb6588");
// 可以用userdetail的is_rd來判斷填入1或0, 1代表官方，0代表非官方
formdata.append("is_official", "1");


var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/content/textEditorPost/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```
