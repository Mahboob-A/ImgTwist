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

5. Nginx Proxy Manager URL: `https://imgtwist-npm.algocode.site/`

6. Portainer URL: `https://imgtwist-portainer.algocode.site`
    - Portainer is used to manage the docker containers.

#### NOTE: 

The doamin name `algocode.site` is my own domain. I have used this domain in my various projects. I the first time I bought this domain when I was building `Leetcode` like Online DSA Judge System. I have successfully built the Online Judge which can securely execute user submitted codes, evaluate it and and generate resutls like `WA`, `AC`, `TLE`, `RE`, `CE` etc. I have named the platform as `Algocode`. Algocode does not contain `any 3rd party APIs`. Everything is built from scratch. `Algocode` is a `microservices` solution and deployed on `AWS`. You can learn more about `Algocode` from the following link: `https://github.com/mahboob-a/algocode`. 

### Quick Check: 

- A very quick check for the app is the the `Swagger` or `Redoc` or the     `healthcheck` API

    1. Swagger Doc: `https://imgtwist.algocode.site/swagger/`

    2. Redoc Doc: `https://imgtwist.algocode.site/redoc/`

    3. Healthcheck API: `https://imgtwist.algocode.site/api/v1/common/healthcheck/`

## Deployment Info

- The dockerized solution is running on an EC2 instance. 
- The URLs are fully secure i.e. has SSL certificate. 

