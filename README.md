# University System Management

This code is designed to manage university system information, including adding professors, students, and course enrollments. It supports both frontend usage for website integration and backend usage with tools like Postman and Insomnia. The code includes validation for all inputs. The data must be entered in the following order: course, professor, then student; otherwise, it won't be accepted. Below, I will demonstrate how to use this code with backend tools.

## JSON Examples

### For Student
```json
{
    "st": "40211415001",
    "fn": "نام",
    "ln": "نام‌خانوادگی",
    "p": "پدر",
    "birth": "1302/01/31",
    "ids": "98765432101",
    "borncity": "تهران",
    "address": "123 Main St, Apartment 4B",
    "postalcode": "1234512345",
    "cp": "01234567890",
    "hp": "1234567890",
    "de": "فنی و مهندسی",
    "ma": "مهندسی نفت",
    "mjd": "مهندسی نفت",
    "nid": "0250254433",
    "scid": "کد استاد",
    "lids": "کد استاد"
}

```





### For Professor

```json


{
  "lid": "111111",
  "pfn": "اسم",
  "pln": "فامیلی",
  "pbirth": "1383/01/01",
  "pborncity": "تهران",
  "paddress": "123 University St, New York, NY 10001",
  "ppostalcode": "1234512345",
  "pcp": "091919221",
  "php": "+1",
  "php_number": "5551234567",
  "pd":"فنی و مهندسی",
  "pm": "مهندسی نفت",
  "pnid": "A123456789",
  "pscid": "ریاضی"
}

```







### For Course


```json

{
  "cid": "12345",
  "cname": "ریاضی",
  "de": "فنی و مهندسی",
  "credit": "3"
}

```




====================================================================================================================================================================================================================================================================================

 ![image](https://github.com/erfnrf/lu_uni_project/assets/142250364/e6b3f31a-fc45-43f9-bd62-a41700dd6bf1)
 
![image](https://github.com/erfnrf/lu_uni_project/assets/142250364/bbfc21c2-440e-4a80-8ec7-900b3f9c858b)

![image](https://github.com/erfnrf/lu_uni_project/assets/142250364/3e3b847d-48ff-4986-86eb-4cb302f58f82)

![image](https://github.com/erfnrf/lu_uni_project/assets/142250364/cf9a3a51-d473-45e6-a9a6-0c0105543783)


بخش بالا برای گرفتن و اعتبار سنجی اطلاعات دانشجو میباشد 

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/874779db-d0b9-41ee-a63b-bf7392eb462b)

بخش بالا برای بروزرسانی اطلاعات دانشجو میباشد

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/2d5f78ee-8173-416a-b19f-b575ad18d2eb)

بخش بالا برای حذف اطلاعات دانشجو میباشد


![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/086bc7bc-09e7-47e3-8e10-7826654f75d9)




بخش بالا برای گرفتن و اعتبار سنجی اطلاعات استاد میباشد 





![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/5e390bb5-2fb9-4973-91ad-8d3393b4050a)


بخش بالا برای بروزرسانی اساتید است

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/9f7d5905-65a0-4cee-8355-1fc3264f3604)


بخش بالا برای حذف استاد وارد شده است




![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/99b81fc9-1523-4076-9572-19d464c711fe)


بخش بالا برای گرفتن و اعتبار سنجی اطلاعات دروس میباشد 


![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/d60bd27a-e0c4-465e-bbe0-c05a357263d1)



بخش بالا برای بروزرسانی دروس است


![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/c3237472-83a3-404f-86e7-bd924fc7a3aa)


بخش بالا برای حذف درس وارد شده است


====================================================================================================================================================================================================================================================================================

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/43d33aca-9811-4e54-b48e-2284e85d43b0)

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/3bb71746-860b-4277-ae90-cb26ee326333)

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/62a63d50-32b7-4a60-848f-e60291f9fb95)

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/dd28ef6e-3170-49e2-baec-0639db55be4a)


این بخش ها حالت های داده های گرفته شده را مشخص میکند که در دیتابیس ما ذخیره میشوند و دیتابیس انتظار دریافت این داده هارا دارد

====================================================================================================================================================================================================================================================================================

![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/b4fd1a18-5b14-422a-b231-9803f272dad4)


![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/ca2e630c-9b3d-413d-8986-db42e02a5a48)


![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/e08fc922-d739-44ac-8114-559c6cd59323)



====================================================================================================================================================================================================================================================================================
![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/308a8747-3854-4c01-854e-56d3367a5dce)

فایل مین 
====================================================================================================================================================================================================================================================================================

