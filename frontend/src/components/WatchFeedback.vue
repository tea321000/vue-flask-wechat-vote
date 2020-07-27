<template>
  <div>
    <h3>当前反馈意见表格</h3>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="反馈者学号/编号:">
              <span>{{ props.row.user_id }}</span>
            </el-form-item>
            <el-form-item label="反馈者姓名:">
              <span>{{ props.row.user_name }}</span>
            </el-form-item>
            <el-form-item label="反馈主题:">
              <span>{{ props.row.feedback_theme }}</span>
            </el-form-item>
            <el-form-item label="反馈内容:">
              <span>{{ props.row.feedback_content }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column label="反馈者学号/编号" prop="user_id"></el-table-column>
      <el-table-column label="反馈者姓名" prop="user_name"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import { Message } from "element-ui";
export default {
  name: "watch_feedback",
  created() {
    this.feedbackStatic();
  },
  data() {
    return {
      roles: this.$store.state.user.roles[0],
      tableData: []
    };
  },
  watch: {
    // 同一组件原来的组件实例会被复用，所以生命周期钩子不会再被调用
    // 因此需要侦听路由变化，来加载数据
    $route(to, from) {
      if (to.name === "watchFeedbackPermission") this.feedbackStatic();
    }
  },
  methods: {
    feedbackStatic() {
      this.$store
        .dispatch("user/watchFeedback")
        .then(data => {
          console.log(data);
          this.tableData = data;
        })
        .catch(() => {
          Message({
            message: "无法获取反馈信息",
            type: "error",
            duration: 2 * 1000
          });
        });
    }
  }
};
</script>
