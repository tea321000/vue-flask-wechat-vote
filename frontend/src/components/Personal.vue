<template>
  <div>
    <el-form
      ref="personalForm"
      :model="personalForm"
      :rules="personalRules"
      auto-complete="on"
      label-position="left"
    >
      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item>学号/编号：{{id}}</el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item>姓名：{{name}}</el-form-item>
        </el-col>
      </el-row>

      <el-row v-if="roles==='student'">
        <el-col :span="12" :offset="6">
          <el-form-item>角色：学生</el-form-item>
        </el-col>
      </el-row>

      <el-row v-else-if="roles==='teacher'">
        <el-col :span="12" :offset="6">
          <el-form-item>角色：老师</el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item prop="password" label="密码：">
            <el-input
              :key="passwordType"
              v-model="personalForm.password"
              :type="passwordType"
              placeholder="密码"
              name="password"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item prop="birthday" label="生日：">
            <div class="block">
              <span class="demonstration"></span>
              <el-date-picker
                style="width:100%;"
                v-model="personalForm.birthday"
                type="date"
                placeholder="生日"
                auto-complete="on"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </div>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item prop="phone" label="手机/电话：">
            <el-input
              v-model="personalForm.phone"
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
          <el-button
            :loading="loading"
            type="primary"
            style="width:100%;margin-bottom:20px;"
            @click.native.prevent="handlePersonalChange"
          >提交修改</el-button>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import { Message } from "element-ui";
import { validPassword, validPhone, validBirthday } from "@/utils/validate";
export default {
  name: "personal",
  data() {
    const validatePassword = (rule, value, callback) => {
      if (!validPassword(value)) {
        if (value)
          callback(new Error("请输入6-15位字符，不需要修改密码请留空"));
        else callback();
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
      // console.log(value)
      if (!validBirthday(value)) {
        callback(new Error("请输入生日"));
      } else {
        callback();
      }
    };
    return {
      id: this.$store.state.user.id,
      name: this.$store.state.user.name,
      roles: this.$store.state.user.roles[0],
      personalForm: {
        birthday: this.$store.state.user.birthday,
        phone: this.$store.state.user.phone
      },
      personalRules: {
        password: [
          { required: true, trigger: "blur", validator: validatePassword }
        ],
        phone: [{ required: true, trigger: "blur", validator: validatePhone }],
        birthday: [
          { required: true, trigger: "blur", validator: validateBirthday }
        ]
      },
      passwordType: "password",
      loading: false
    };
  },
  methods: {
    handlePersonalChange() {
      this.$refs.personalForm.validate(valid => {
        if (valid) {
          this.loading = true;
          this.$store
            .dispatch("user/personalChange", this.personalForm)
            .then(() => {
              console.log(this.personalForm);
              this.loading = false;
              Message({
                message: "个人信息已成功修改",
                type: "success",
                duration: 2 * 1000
              });
              this.$store.dispatch("user/logout");
            })
            .catch(() => {
              this.loading = false;
              Message({
                message: "个人信息修改失败",
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
