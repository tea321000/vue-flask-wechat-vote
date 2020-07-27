import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home";
import Login from "./views/login.vue";

Vue.use(Router);

/**
 * 固定路由
 * 不需要权限
 * 所有角色均可访问
 * */
export const constantRoutes = [
  {
    path: "/login",
    name: "login",
    component: Login
  }
];

/**
 * 异步路由
 * 需要通过角色动态添加
 */
export const asyncRoutes = [
  {
    path: "/",
    component: Home,
    meta: {
      title: "permission",
      roles: ["student", "teacher"]
    },
    children: [
      {
        path: "/",
        component: function() {
          return import(/* webpackChunkName: "Home" */ "./views/Index");
        },
        name: "IndexPermission",
        meta: {
          title: "IndexPermission",
          roles: ["student", "teacher"]
        }
      },
      {
        path: "personal",
        component: function() {
          return import(/* webpackChunkName: "Home" */ "./views/Personal");
        },
        name: "PersonalPermission",
        meta: {
          title: "PersonalPermission",
          roles: ["student", "teacher"]
        }
      },
      {
        path: "attend",
        component: resolve => require(["./views/Attend"], resolve),
        name: "voteAttendPermission",
        meta: {
          title: "voteAttendPermission",
          roles: ["student"]
        }
      },
      {
        path: "feedback",
        component: resolve => require(["./views/Feedback"], resolve),
        name: "feedbackPermission",
        meta: {
          title: "feedbackPermission",
          roles: ["student", "teacher"]
        }
      },
      {
        path: "watchfeedback",
        component: resolve => require(["./views/WatchFeedback"], resolve),

        name: "watchFeedbackPermission",
        meta: {
          title: "watchFeedbackPermission",
          roles: ["administrator"]
        }
      },
      {
        path: "detail/:id",
        component: resolve => require(["./views/Detail"], resolve),
        name: "voteDetailPermission",
        meta: {
          title: "voteDetailPermission",
          roles: ["student", "teacher"]
        }
      },
      {
        path: "vote",
        component: resolve => require(["./views/Vote"], resolve),
        name: "VotePermission",
        meta: {
          title: "VotePermission",
          roles: ["teacher"]
        }
      },
      {
        path: "history",
        component: resolve => require(["./views/VoteHistory"], resolve),
        name: "VoteHistoryPermission",
        meta: {
          title: "VoteHistoryPermission",
          roles: ["teacher", "student"]
        }
      }
    ]
  }
];

const createRouter = () =>
  new Router({
    mode: "history", // history模式，需要设备支持
    scrollBehavior: () => ({
      y: 0
    }),
    routes: constantRoutes
  });

const router = createRouter();

export function resetRouter() {
  const newRouter = createRouter();
  router.matcher = newRouter.matcher; // reset router
}

export default router;
