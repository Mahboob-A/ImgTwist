<br/>
<div align="center">
<a href="https://github.com/Mahboob-A/imgtwist/">
<img src="https://github.com/user-attachments/assets/7c0e6379-467e-44ac-a9c9-ce1b5c6b10a5" alt="ImgTwist Logo" width="700" height="400">
</a>
<h3 align="center">ImgTwist - Image Hosting Platform for All Your Needs</h3>
<p align="center">
A Generalized Image Hosting Platform Just Like Image Twist!
<br/>
<br/>
<a href="https://github.com/Mahboob-A/imgtwist/"><strong>Read the blog »</strong></a>
<br/>
<br/>
<a href="https://github.com/Mahboob-A/imgtwist/">ImgTwist</a>  

</p>
</div>

<hr>

<h3>Key Features</h3>
<ul>
    <li><strong>Rate Limiting:</strong> Implemented using the Token Bucket Algorithm through Django Middleware. Check out the <code>Middleware</code> section in <code>core_apps.common</code> for details. 
        <em>(Note: Rate limiting is currently implemented but not enforced on a per-app basis.)</em></li>
    <li><strong>Postman Testing:</strong> Import the provided Postman Collection, set up any necessary environment variables, and test all API functionalities.</li>
</ul>

<hr>

<h3>Application Links</h3>

<h4>Production URL</h4>
<ul>
    <li><strong>Main Application:</strong> <a href="https://imgtwist.algocode.site/">ImgTwist - Main Django App</a></li>
    <ul>
        <li><strong>API Base URL:</strong> <a href="https://imgtwist.algocode.site/api/v1">https://imgtwist.algocode.site/api/v1</a> 
        <br><em>(Note: This should be set as the <code>prod_url</code> environment variable in Postman if not automatically detected)</em></li>
    </ul>
</ul>

<h4>API Documentation</h4>
<ul>
    <li><strong>Swagger Documentation:</strong> <a href="https://imgtwist.algocode.site/swagger/">https://imgtwist.algocode.site/swagger/</a></li>
    <li><strong>Redoc Documentation:</strong> <a href="https://imgtwist.algocode.site/redoc/">https://imgtwist.algocode.site/redoc/</a></li>
</ul>

<h4>Administrative Portals</h4>
<ul>
    <li><strong>Django Admin:</strong> <a href="https://imgtwist.algocode.site/imgtwist-admin/">https://imgtwist.algocode.site/imgtwist-admin/</a></li>
    <ul>
        <li><strong>Demo Login:</strong></li>
        <li>Email: <code>social.mehboob@gmail.com</code></li>
        <li>Password: <code>demopwd@111</code></li>
    </ul>
    <li><strong>Nginx Proxy Manager:</strong> <a href="https://imgtwist-npm.algocode.site/">https://imgtwist-npm.algocode.site/</a></li>
    <li><strong>Portainer for Docker Management:</strong> <a href="https://imgtwist-portainer.algocode.site/">https://imgtwist-portainer.algocode.site/</a></li>
</ul>

<hr>

<h3>Quick Health Check Options</h3>
<ul>
    <li><strong>Swagger:</strong> <a href="https://imgtwist.algocode.site/swagger/">https://imgtwist.algocode.site/swagger/</a></li>
    <li><strong>Redoc:</strong> <a href="https://imgtwist.algocode.site/redoc/">https://imgtwist.algocode.site/redoc/</a></li>
    <li><strong>Healthcheck API:</strong> <a href="https://imgtwist.algocode.site/api/v1/common/healthcheck/">https://imgtwist.algocode.site/api/v1/common/healthcheck/</a></li>
</ul>

<hr>

<h3>Deployment Details</h3>
<ul>
    <li>The application is a fully dockerized solution running on an EC2 instance with SSL-secured URLs for all endpoints.</li>
</ul>

<hr>

<h3>About <code>Algocode.site</code></h3>
<p>The domain <code>algocode.site</code> serves multiple projects. It was initially purchased for an Online DSA Judge System project (<code>Algocode</code>) that simulates platforms like LeetCode. <code>Algocode</code> was designed to securely execute and evaluate user-submitted code, generate results (<code>WA</code>, <code>AC</code>, <code>TLE</code>, <code>RE</code>, <code>CE</code>, etc.), and provide a microservices architecture deployed on AWS. 
<a href="https://github.com/mahboob-a/algocode">Learn more here</a>.</p>

<hr>

<h2>YouTube Demonstration</h2>
<p><a href="https://youtu.be/O0axE83WZs0" target="_blank">Watch the demonstration on YouTube</a></p>

<table border="1" cellpadding="5" cellspacing="0">
    <thead>
        <tr>
            <th>Timestamp</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>00:00</td><td>Introduction</td></tr>
        <tr><td>02:20</td><td>Feature Explanation</td></tr>
        <tr><td>03:05</td><td>Postman API Testing Begin</td></tr>
        <tr><td>03:50</td><td>Healthcheck API</td></tr>
        <tr><td>03:55</td><td>Production URL with SSL</td></tr>
        <tr><td>04:20</td><td>Algocode Introduction - An Online Judge in Microservices</td></tr>
        <tr><td>06:00</td><td>User Management APIs</td></tr>
        <tr><td>07:50</td><td>Product APIs (Get Product, All Products, Create Product, Update Product, Delete Product, Multi Image Upload)</td></tr>
        <tr><td>12:46</td><td>Bloopers</td></tr>
        <tr><td>12:50</td><td>Serve Image with Sub-Domain with SSL</td></tr>
        <tr><td>16:45</td><td>Product Image APIs (Multi Image Delete)</td></tr>
        <tr><td>20:20</td><td>Category APIs</td></tr>
        <tr><td>21:00</td><td>ImgTwist Admin Portal</td></tr>
        <tr><td>21:15</td><td>Swagger API Doc</td></tr>
        <tr><td>21:33</td><td>Redoc API Doc</td></tr>
        <tr><td>21:40</td><td>Portainer Portal for Docker Management</td></tr>
        <tr><td>23:10</td><td>AES EC2 Server SSH</td></tr>
        <tr><td>24:20</td><td>Inside EC2 Server</td></tr>
        <tr><td>24:45</td><td>List Docker Containers</td></tr>
        <tr><td>25:10</td><td>Exec Django Container</td></tr>
        <tr><td>25:40</td><td>Deployment Script</td></tr>
        <tr><td>26:00</td><td>Outro</td></tr>
    </tbody>
</table>


