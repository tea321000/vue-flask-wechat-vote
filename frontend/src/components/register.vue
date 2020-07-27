<template>
  <div class="register-container">
    <el-form
      ref="registerForm"
      :model="registerForm"
      :rules="registerRules"
      class="register-form"
      auto-complete="on"
      label-position="left"
    >
      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
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
          <el-form-item prop="name">
            <el-input
              v-model="registerForm.name"
              placeholder="姓名"
              name="name"
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
              v-model="registerForm.password"
              :type="passwordType"
              placeholder="密码"
              name="password"
              auto-complete="on"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item prop="birthday">
            <div class="block">
              <span class="demonstration"></span>
              <el-date-picker
                style="width:100%;"
                v-model="registerForm.birthday"
                type="date"
                placeholder="生日"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </div>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item prop="phone">
            <el-input
              v-model="registerForm.phone"
              placeholder="手机/电话"
              name="phone"
              type="text"
              auto-complete="on"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item prop="role">
            <el-radio v-model="registerForm.role" label="student">学生</el-radio>
            <el-radio v-model="registerForm.role" label="teacher">老师</el-radio>
            <el-radio v-model="registerForm.role" label="administrator">管理员</el-radio>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-button
            :loading="loading"
            type="primary"
            style="width:100%;margin-bottom:30px;"
            @click.native.prevent="handleRegister"
          >注册</el-button>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import { Message } from "element-ui";
import {
  validUsername,
  validName,
  validPassword,
  validPhone,
  validBirthday
} from "@/utils/validate";

export default {
  name: "Register",
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error("请输入6-10位数字"));
      } else {
        callback();
      }
    };
    const validateName = (rule, value, callback) => {
      if (!validName(value)) {
        callback(new Error("请输入正确的姓名"));
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
    const validatePhone = (rule, value, callback) => {
      if (!validPhone(value)) {
        callback(new Error("请输入正确手机号/电话"));
      } else {
        callback();
      }
    };
    const validateBirthday = (rule, value, callback) => {
      if (!validBirthday(value)) {
        callback(new Error("请输入生日"));
      } else {
        callback();
      }
    };
    return {
      registerForm: {
        username: "",
        name: "",
        password: "",
        birthday: "",
        phone: "",
        role: "student"
      },
      registerRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUsername }
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword }
        ],
        phone: [{ required: true, trigger: "blur", validator: validatePhone }],
        name: [{ required: true, trigger: "blur", validator: validateName }],
        birthday: [
          { required: true, trigger: "blur", validator: validateBirthday }
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
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          // console.log("注册");
          this.loading = true;
          this.$store
            .dispatch("user/register", this.registerForm)
            .then(() => {
              // this.$router.push({ path: this.redirect || "/" });
              this.loading = false;
              Message({
                message: "完成注册，请登录",
                type: "success",
                duration: 5 * 1000
              });
            })
            .catch(() => {
              this.loading = false;
              Message({
                message: "注册失败",
                type: "error",
                duration: 5 * 1000
              });
              // console.log(err);
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
