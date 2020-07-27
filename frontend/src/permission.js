import router from './router'
import store from './store'
import {
  Message
} from 'element-ui'
import NProgress from 'nprogress' // 进度条
import 'nprogress/nprogress.css'
import {
  getToken
} from '@/utils/auth' // 从cookie获取token

NProgress.configure({
  showSpinner: false
}) // 进度条配置

const whiteList = ['/login'] // 不重定向的白名单

router.beforeEach(async (to, from, next) => {
  // 进度条开始
  NProgress.start()

  // 检查用户是否已经登录
  const hasToken = getToken()

  if (hasToken) {
    if (to.path === '/login') {
      // 已经登录重定向至主页
      next({
        path: '/'
      })
      NProgress.done()
    } else {
      // 检查用户是否获得了相应的角色权限
      const hasRoles = store.state.user.roles && store.state.user.roles.length > 0
      if (hasRoles) {
        next()
      } else {
        try {
          // 异步请求角色权限
          //角色必须是对象数组，如['admin'] 或,['developer','editor']
          const {
            roles
          } = await store.dispatch('user/getInfo')

          //根据角色生成异步路由
          const accessRoutes = await store.dispatch('permission/generateRoutes', roles)

          // 动态添加可访问路由
          router.addRoutes(accessRoutes)

          // 保证添加路由已完成
          // 设置replace: true, 所以浏览器不会留下返回的history记录
          next({
            ...to,
            replace: true
          })
        } catch (error) {
          // 移除token然后重定向至登录页面
          await store.dispatch('user/resetToken')
          Message.error(error || 'Has Error')
          next(`/login?redirect=${to.path}`)
          NProgress.done()
        }
      }
    }
  } else {
    /*没有token*/

    if (whiteList.indexOf(to.path) !== -1) {
      // 在白名单，直接放行
      next()
    } else {
      // 不在白名单，返回登录页面，添加query参数redirect供登录后跳转至该路由
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  // 进度条完成
  NProgress.done()
})