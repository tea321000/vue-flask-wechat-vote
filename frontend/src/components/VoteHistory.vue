<template>
  <div>
    <el-row>
      <h3 v-if="roles==='teacher'">创建投票历史</h3>
      <h3 v-else-if="roles==='student'">参与投票历史</h3>
    </el-row>
    <h4 v-if="data.length===0">暂无投票历史信息！</h4>
    <div v-if="roles==='student'">
      <el-row v-for="(item,index) in data" :key="item.id" style="padding: 14px;">
        <!-- <el-col :span="10" v-for="(o, index) in 3" :key="o" :offset="index > 0 ? 2 : 0"> -->
        <el-card :body-style="{ padding: '0px' }">
          <div style="padding: 14px;">
            <span>{{item.title}}</span>
            <h5 v-if="item.anonymous===true">匿名投票</h5>
            <h5 v-else-if="item.anonymous===false">实名投票</h5>
            <h5 v-if="item.multiple===true">多选</h5>
            <h5 v-else-if="item.multiple===false">单选</h5>
            <div class="bottom clearfix">
              <time class="time">{{item.time_start|formatDate}}至{{item.time_end|formatDate}}</time>
              <el-button type="text" @click="getDetail(item.id)" class="button">查看</el-button>
            </div>
          </div>
        </el-card>
      </el-row>
    </div>
    <div v-else-if="roles==='teacher'">
      <el-row v-for="(item,index) in data" :key="item.id" style="padding: 14px;">
        <!-- <el-col :span="10" v-for="(o, index) in 3" :key="o" :offset="index > 0 ? 2 : 0"> -->
        <el-card :body-style="{ padding: '0px' }">
          <div style="padding: 14px;">
            <span>{{item.title}}</span>
            <h5 v-if="item.anonymous===true">匿名投票</h5>
            <h5 v-else-if="item.anonymous===false">实名投票</h5>
            <h5 v-if="item.multiple===true">多选</h5>
            <h5 v-else-if="item.multiple===false">单选</h5>
            <div class="bottom clearfix">
              <time class="time">{{item.time_start|formatDate}}至{{item.time_end|formatDate}}</time>
              <el-row>
                <el-button type="text" @click="getDetail(item.id)" class="button">查看</el-button>
                <el-col :span="23">
                  <el-button type="text" @click="deleteVote(item.id)" class="button">删除</el-button>
                </el-col>
              </el-row>
            </div>
          </div>
        </el-card>
      </el-row>
    </div>
  </div>
</template>

<script>
import { Message } from "element-ui";
import { formatDate } from "@/utils/datetime.js";
export default {
  name: "vote_history",
  created() {
    this.getVoteHistory();
  },
  filters: {
    formatDate(time) {
      let date = new Date(time + "+0800");
      return formatDate(date, "yyyy-MM-dd hh:mm");
      //此处formatDate是一个函数，将其封装在common/js/date.js里面，便于全局使用
    }
  },
  watch: {
    // 同一组件原来的组件实例会被复用，所以生命周期钩子不会再被调用
    // 因此需要侦听路由变化，来加载数据
    $route(to, from) {
      if (to.name === "VoteHistoryPermission") this.getVoteHistory();
    }
  },
  data() {
    return {
      data: [],
      roles: this.$store.state.user.roles[0]
    };
  },
  methods: {
    getDetail(id) {
      this.$router.push({ path: `/detail/${id}` });
    },
    deleteVote(id) {
      this.$confirm("此操作将永久删除该投票, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          this.$store.state.user.vote_id = id;
          this.$store
            .dispatch("user/deleteVote")
            .then(() => {
              // this.data = data;
              Message({
                message: "成功删除投票，请重新刷新页面",
                type: "success",
                duration: 2 * 1000
              });
              // this.$router.push({ name: VoteHistoryPermission });
            })
            .catch(() => {
              Message({
                message: "删除投票失败",
                type: "error",
                duration: 2 * 1000
              });
            });
          // this.$message({
          //   type: "success",
          //   message: "删除成功!"
          // });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    getVoteHistory() {
      this.$store
        .dispatch("user/voteHistory")
        .then(data => {
          console.log(data);
          this.data = data;
          Message({
            message: "成功获取投票历史",
            type: "success",
            duration: 2 * 1000
          });
        })
        .catch(() => {
          Message({
            message: "无法获取投票历史",
            type: "error",
            duration: 2 * 1000
          });
        });
    }
  }
};
</script>

<style scoped>
.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
</style>