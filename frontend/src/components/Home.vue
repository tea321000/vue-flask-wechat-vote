<template>
  <div>
    <el-container>
      <el-header>
        <el-menu class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-submenu index="1">
            <template slot="title" v-if="roles==='student'">{{name}}:学生</template>
            <template slot="title" v-else-if="roles==='teacher'">{{name}}:老师</template>
            <template slot="title" v-else-if="roles==='administrator'">{{name}}:管理员</template>
            <el-menu-item index="1-1">个人资料</el-menu-item>
            <el-menu-item index="1-2">退出登录</el-menu-item>
          </el-submenu>

          <el-submenu index="2">
            <template slot="title">投票</template>
            <el-menu-item index="2-1" v-if="roles==='student'">参与投票</el-menu-item>
            <el-menu-item index="2-1" v-else-if="roles==='teacher'">创建投票</el-menu-item>

            <el-menu-item index="2-2" v-if="roles==='student'||roles==='teacher'">投票历史</el-menu-item>
            <el-menu-item index="2-3" v-if="roles==='student'||roles==='teacher'">反馈信息</el-menu-item>
            <el-menu-item index="2-3" v-else-if="roles==='administrator'">查看反馈</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-header>
      <el-main>
        <transition>
          <keep-alive>
            <router-view/>
          </keep-alive>
        </transition>
      </el-main>
      <el-footer></el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // id: this.$store.state.user.id,
      name: this.$store.state.user.name,
      roles: this.$store.state.user.roles[0]
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      if (keyPath[0] === "1") {
        if (keyPath[1] === "1-1")
          this.$router.push({ name: "PersonalPermission" });
        else if (keyPath[1] === "1-2") this.$store.dispatch("user/logout");
      } else if (keyPath[0] === "2") {
        if (this.roles === "teacher") {
          if (keyPath[1] === "2-1") {
            this.$router.push({ name: "VotePermission" });
          } else if (keyPath[1] === "2-2") {
            this.$router.push({ name: "VoteHistoryPermission" });
          } else if (keyPath[1] === "2-3") {
            this.$router.push({ name: "feedbackPermission" });
          }
        } else if (this.roles === "student") {
          if (keyPath[1] === "2-1") {
            this.$router.push({ name: "voteAttendPermission" });
          } else if (keyPath[1] === "2-2") {
            this.$router.push({ name: "VoteHistoryPermission" });
          } else if (keyPath[1] === "2-3") {
            this.$router.push({ name: "feedbackPermission" });
          }
        } else if (this.roles === "administrator") {
          if (keyPath[1] === "2-3") {
            this.$router.push({ name: "watchFeedbackPermission" });
          }
        }
      }
    }
  }
};
</script>