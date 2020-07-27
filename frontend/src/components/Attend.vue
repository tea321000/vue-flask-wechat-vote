<template>
  <div>
    <el-row>
      <h3>目前开放的投票</h3>
      <h3 v-if="roles==='teacher'">您是老师，无权查看此页</h3>
    </el-row>

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
</template>

<script>
import { Message } from "element-ui";
import { formatDate } from "@/utils/datetime.js";
export default {
  name: "attend",
  created() {
    this.getOpenVote();
  },
  filters: {
    formatDate(time) {
      let date = new Date(time + "+0800");
      console.log(date);
      return formatDate(date, "yyyy-MM-dd hh:mm");
      //此处formatDate是一个函数，将其封装在common/js/date.js里面，便于全局使用
    }
  },
  watch: {
    // 同一组件原来的组件实例会被复用，所以生命周期钩子不会再被调用
    // 因此需要侦听路由变化，来加载数据
    $route(to, from) {
      if (to.name === "voteAttendPermission") this.getOpenVote();
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
    getOpenVote() {
      this.$store
        .dispatch("user/attendVote")
        .then(data => {
          console.log(data);
          this.data = data;
          Message({
            message: "成功获取目前开放的投票",
            type: "success",
            duration: 2 * 1000
          });
        })
        .catch(() => {
          Message({
            message: "无法获取目前开放的投票",
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