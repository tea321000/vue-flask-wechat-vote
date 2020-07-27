import axios from "axios";
import store from "@/store";
import { getToken } from "@/utils/auth";
import { Message } from "element-ui";
// import {
//   login
// } from '../api/user';
// import router from '@/router'
// create an axios instance
const service = axios.create({
  // baseURL: process.env.VUE_APP_BASE_API, // api 的 base_url
  baseURL: "http://www.yourdomain.xyz:yourport",
  withCredentials: true, // 跨域请求时发送 cookies
  timeout: 5000 // request timeout
});

// request interceptor
service.interceptors.request.use(
  config => {
    // Do something before request is sent
    if (store.getters.token) {
      // 让每个请求携带token-- ['X-Token']为自定义key 请根据实际情况自行修改
      config.headers["token"] = getToken();
    }
    return config;
  },
  error => {
    // Do something with request error
    console.log(error); // for debug
    Promise.reject(error);
  }
);

// response interceptor
service.interceptors.response.use(
  function(response) {
    const res = response;
    // console.log(res)
    if (res.status == 202) {
      Message({
        message: "你已被登出，可以继续留在该页面，或者重新登录",
        type: "info",
        duration: 2 * 1000
      });
    } else return response.data;
    // //200:登录成功；201:注册成功；
    // if (res.code !== 200 || res.code !== 201) {
    //   Message({
    //     message: res.message,
    //     type: 'error',
    //     duration: 5 * 1000
    //   })
    //   // 400:未填写用户名或密码；401:用户名或密码错误；402：用户名已存在；405:非法的token; 406:学号/编号和姓名输入错误;  407:Token 过期了;410:找不到详情
    //   if (res.code === 400 || res.code === 401 || res.code === 402 || res.code === 405 || res.code === 406 || res.code === 407) {
    //     // 请自行在引入 MessageBox
    //     // import { Message, MessageBox } from 'element-ui'
    //     MessageBox.confirm('你已被登出，可以取消继续留在该页面，或者重新登录', '确定登出', {
    //       confirmButtonText: '重新登录',
    //       cancelButtonText: '取消',
    //       type: 'warning'
    //     }).then(() => {
    //       store.dispatch('user/resetToken').then(() => {
    //         location.reload() // 为了重新实例化vue-router对象 避免bug
    //       })
    //     })
    //   }
    //   return Promise.reject('error')
    // } else {

    // }
  },
  function(error) {
    // console.log(error.response.status); // for debug
    return Promise.reject(error);
  }
);

export default service;
