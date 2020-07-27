<template>
  <div :style="note">
    <div class="login-container">
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        auto-complete="on"
        label-position="left"
      >
        <div class="title-container" align="center">
          <h1 class="title">用户登录</h1>
        </div>
        <el-row>
          <el-col :span="12" :offset="6">
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="学号/编号"
                name="username"
                type="text"
                auto-complete="on"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12" :offset="6">
            <el-form-item prop="password">
              <el-input
                :key="passwordType"
                v-model="loginForm.password"
                :type="passwordType"
                placeholder="密码"
                name="password"
                auto-complete="on"
                @keyup.enter.native="handleLogin"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12" :offset="6">
            <el-button
              :loading="loading"
              type="primary"
              style="width:100%;margin-bottom:20px;"
              @click.native.prevent="handleLogin"
            >登录</el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12" :offset="6">
            <el-button
              type="info"
              style="width:100%;margin-bottom:30px;"
              @click="showDialog=true"
            >注册</el-button>
          </el-col>
        </el-row>
      </el-form>
      <el-dialog title="注册" :visible.sync="showDialog" center :fullscreen="true">
        <Register/>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { validUsername, validPassword } from "@/utils/validate";
import Register from "@/components/register";
import { Message } from "element-ui";

export default {
  name: "Login",
  components: {
    Register
  },
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error("请输入6-10位数字"));
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      if (!validPassword(value)) {
        callback(new Error("请输入6-15位字符"));
      } else {
        callback();
      }
    };

    return {
      note: {
        backgroundImage: "url(" + require("@/assets/g.jpg") + ")",
        backgroundRepeat: "no-repeat",
        // width: "100%",
        height: "100%",

        backgroundSize: "100% 100%",
        // marginTop: "20%",
        padding: "20%"
      },
      loginForm: {
        username: "",
        password: ""
      },
      loginRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUsername }
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword }
        ]
      },
      passwordType: "password",
      loading: false,
      showDialog: false,
      redirect: undefined
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  created() {
    // window.addEventListener('storage', this.afterQRScan)
  },
  destroyed() {
    // window.removeEventListener('storage', this.afterQRScan)
  },
  methods: {
    // showPwd() {
    //   if (this.passwordType === "password") {
    //     this.passwordType = "";
    //   } else {
    //     this.passwordType = "password";
    //   }
    // },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true;
          this.$store
            .dispatch("user/login", this.loginForm)
            .then(() => {
              Message({
                message: "完成登录，即将重定向到主页",
                type: "success",
                duration: 2 * 1000
              });
              this.$router.push({ path: this.redirect || "/" });
              this.loading = false;
            })
            .catch(() => {
              Message({
                message: "登录失败，请检查学号/编号和密码",
                type: "error",
                duration: 5 * 1000
              });
              this.loading = false;
            });
        } else {
          console.log("错误的提交！");
          return false;
        }
      });
    }
  }
};
</script>
