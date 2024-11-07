# ImgTwist


### Image Showcase Platform for All Your Needs


## Temporary Readme Below: Just a Temporary Readme, will be removed with Update Readme. 

- Just a temporary readme, will be removed soon with update readme.

- A YT video will be added soon with the full documentation soon. 

- Rate Limiting implemented with Token Bucket Algorithm using Django Middleware 
   is implemented, but currently not enforced app wise. Please refer to the `Middleware` section or `core_apps.common` app.  

### You can test all the functionality of the app by using the following URLS:

- You just need to copy the Postman Collections (see above), import on your postman, setup the environment variable if needed, and then you can test the APIs.

#### Production URL: 

1. Main Django APP: https://imgtwist.algocode.site/

NOTE: `https://imgtwist.algocode.site/api/v1` is the `prod_url` environment of Postman. If this did not automatically set on postman, please add this environment variable on `Environment` Section of Postman. 

2. Swagger Doc: `https://imgtwist.algocode.site/swagger/`

3. Redoc Doc: `https://imgtwist.algocode.site/redoc/`

4. Django Admin: `https://imgtwist.algocode.site/imgtwist-admin/` 
    - email: `social.mehboob@gmail.com` (just a demo email)
    - password: demopwd@111



## Deployment Info

- The dockerized solution is running on an EC2 instance. 
- The URLs are fully secure i.e. has SSL certificate. 

