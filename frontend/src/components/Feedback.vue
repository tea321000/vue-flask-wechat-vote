<template>
  <div>
    <el-form ref="feedbackForm" :model="feedbackForm" auto-complete="on" :rules="feedbackRules">
      <el-form-item label="反馈主题" prop="theme">
        <el-input v-model="feedbackForm.theme" name="theme" type="text"></el-input>
      </el-form-item>
      <el-form-item label="反馈内容" prop="content">
        <el-input type="textarea" v-model="feedbackForm.content"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click.native.prevent="handleFeedback">反馈意见</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { validBlank } from "@/utils/validate";
import { Message } from "element-ui";
export default {
  name: "feedback",
  data() {
    const validateTheme = (rule, value, callback) => {
      if (!validBlank(value)) {
        callback(new Error("请输入反馈主题"));
      } else {
        callback();
      }
    };
    const validateContent = (rule, value, callback) => {
      if (!validBlank(value)) {
        callback(new Error("请输入反馈内容"));
      } else {
        callback();
      }
    };
    return {
      roles: this.$store.state.user.roles[0],
      feedbackForm: {
        theme: "",
        content: ""
      },
      feedbackRules: {
        theme: [{ required: true, trigger: "blur", validator: validateTheme }],
        content: [
          { required: true, trigger: "blur", validator: validateContent }
        ]
      }
    };
  },
  methods: {
    handleFeedback() {
      this.$refs.feedbackForm.validate(valid => {
        if (valid) {
          this.loading = true;
          this.$store
            .dispatch("user/feedback", this.feedbackForm)
            .then(() => {
              this.$router.push({ name: "IndexPermission" });
              this.loading = false;
              Message({
                message: "反馈意见成功",
                type: "success",
                duration: 5 * 1000
              });
            })
            .catch(() => {
              this.loading = false;
              Message({
                message: "反馈意见失败",
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
