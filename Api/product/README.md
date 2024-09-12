# Product

## Table of Product


| Name | Description | Type |
|------|-------------|------|
| product_title | Name of product | `string` |
| product_point | point of product | `number` |
|amount | Amount of product | `number` |
| product_description | Description of product | `string` |
| product_image | Image of product | `string` |
| product_category | Category of product | `string` |


## Usage

----------------------

```js
// 基本上這邊只給get，其他都是用資料庫去測試
var requestOptions = {
  method: 'GET',
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/api/product/product/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```


## search/ordered product

-----------------------------

可以從這邊參考，有個filter的按鈕

[http://{django-backend-ip}/api/product/product/](http://127.0.0.1:8000/api/product/productRecommend/?ordering=-exchaged)