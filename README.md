# vue-flask-wechat-vote
基于vue_admin_template的vue+flask前后端分离微信web投票系统，可在微信公众号端设置关键词返回相应的web路由页面。

使用方法：

1、前端frontend主要通过request.js的baseURL来与后端进行通信，需要更改为自己的域名和端口；

2、后端wechat_server需要更改app.py的port和后台与微信公众号交互的wechat.py里返回的页面的url

3、图片上传接口比较特殊，需要单独处理：更改后端api.py中/upload路由返回的link，同时更改前端vote.vue的el-upload action为同样域名和端口 

4、前端根据vue_cli脚手架进行构建，根据frontend文件夹里的package.json安装相关依赖，然后输入vue ui在图形化界面中build生产环境，会在frontend文件夹下生成dist文件夹；

5、将dist文件夹复制到wechat_server文件夹下，完成所有配置
