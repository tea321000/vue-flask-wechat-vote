<template>
  <div>
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="当前状态" name="1">
        <div v-if="data.permission===true&&data.time_limit===true&&roles[0]==='student'">可以进行投票</div>
        <div v-else-if="roles[0]==='teacher'">您是老师，不可进行投票</div>
        <div v-else-if="data.permission===false">您没有该投票的权限或已经投过票，不可投票</div>
        <div v-else-if="data.time_limit===false">投票时间已过或未开始，不可投票</div>
        <div v-if="data.academy">投票限制学院为：</div>
        <div v-for="item in data.academy" :key="item">{{item}}</div>
        <div v-if="data.grade">投票限制年级为：</div>
        <div v-for="item in data.grade" :key="item">{{item}}</div>
        <div v-if="data.person">投票限制个人为：</div>
        <div v-for="item in data.person" :key="item">{{item}}</div>
        <div v-if="data.anonymous">该投票是匿名投票，将不显示投票历史</div>
      </el-collapse-item>
      <el-collapse-item title="投票标题" name="2">
        <div>{{data.title}}</div>
      </el-collapse-item>
      <el-collapse-item v-if="data.content" title="投票内容" name="3">
        <div>{{data.content}}</div>
      </el-collapse-item>
      <el-collapse-item title="投票时间" name="4">
        <div>{{data.time_start|formatDate}}至{{data.time_end|formatDate}}</div>
      </el-collapse-item>
      <el-collapse-item v-if="data.pic" title="投票图片" name="5">
        <img :src="data.pic" class="image">
      </el-collapse-item>
      <el-collapse-item title="投票链接和二维码" name="6">
        <div>投票地址链接为:</div>
        <a :href="qrLink">{{qrLink}}</a>
        <div>二维码:</div>
        <qrcode :value="qrLink" :options="{ width: 300 }"></qrcode>
      </el-collapse-item>
      <el-collapse-item v-if="data.anonymous===false&&data.history.length>0" title="投票历史" name="7">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="投票者学号:">
                  <span>{{ props.row.user_id }}</span>
                </el-form-item>
                <el-form-item label="投票者姓名:">
                  <span>{{ props.row.user_name }}</span>
                </el-form-item>
                <el-form-item label="投票选项:">
                  <span>{{ props.row.vote_content }}</span>
                </el-form-item>
                <el-form-item label="当前该选项票数:">
                  <span>{{ props.row.vote_count }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column label="投票者学号" prop="user_id"></el-table-column>
          <el-table-column label="投票者姓名" prop="user_name"></el-table-column>
        </el-table>
      </el-collapse-item>
      <el-collapse-item title="投票选项及图表" name="8">
        <el-collapse v-model="optionActiveName" accordion>
          <el-collapse-item v-for="(group,index) in data.group" :title="group" :name="index">
            <div v-if="data.multiple===false">
              <el-radio-group
                v-model="choice[index]"
                v-if="data.permission===true&&data.time_limit===true"
              >
                <el-radio
                  v-for="item in filter_option(group)"
                  :label="item.key"
                  :key="item.key"
                >{{item.option.name}} 投票数量：{{item.option.value}}</el-radio>
              </el-radio-group>
              <el-radio-group v-else>
                <el-radio
                  disable
                  v-for="item,index) in filter_option(group)"
                  :label="index"
                >{{item.option.name}} 投票数量：{{item.option.value}}</el-radio>
              </el-radio-group>
            </div>
            <div v-else>
              <el-checkbox-group
                v-model="choice[index]"
                v-if="data.permission===true&&data.time_limit===true"
              >
                <el-checkbox
                  v-for="item in filter_option(group)"
                  :label="item.key"
                  :key="item.key"
                >{{item.option.name}} 投票数量：{{item.option.value}}</el-checkbox>
                <!-- <el-checkbox label="禁用" disabled></el-checkbox> -->
              </el-checkbox-group>
              <el-checkbox-group v-else>
                <el-checkbox
                  disable
                  v-for="(item,index) in filter_option(group)"
                  :label="index"
                >{{item.option.name}} 投票数量：{{item.option.value}}</el-checkbox>
              </el-checkbox-group>
            </div>
          </el-collapse-item>
        </el-collapse>

        <el-button
          v-if="data.permission===true&&data.time_limit===true"
          type="primary"
          @click="handleVote"
          :disabled="submitDisabled"
        >提交</el-button>

        <v-chart
          :options="chart_option"
          autoresize
          ref="pie"
          style="width:100%;height: 100%;min-width: 300px;min-height: 600px;"
        />
        <el-select
          v-model="selectedValue"
          placeholder="请选择要显示的组别"
          @change="handleSelected"
          :key="$route.params.id"
        >
          <el-option v-for="group in data.group" :key="group" :label="group" :value="group"></el-option>
        </el-select>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
import { Message } from "element-ui";
import { formatDate } from "@/utils/datetime.js";
//引入ECHARTS
import ECharts from "vue-echarts";
import "echarts/lib/chart/pie";

export default {
  name: "detail",
  components: {
    "v-chart": ECharts
  },
  created() {
    this.detailStatic();
  },
  data() {
    return {
      data: [],
      tableData: [],
      qrLink: window.location.href,
      activeNames: ["1", "2", "3", "4", "5", "6", "7", "8"],
      optionActiveName: "1",
      roles: this.$store.state.user.roles,
      choice: [],
      submitDisabled: false,
      selectedValue: "",
      chart_option: {},
      chart_template: {
        title: {
          text: "投票图表",
          subtext: "",
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          x: "left",
          data: []
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            magicType: {
              show: true,
              type: ["pie", "funnel"],
              option: {
                funnel: {
                  x: "25%",
                  width: "50%",
                  funnelAlign: "left",
                  max: 1548
                }
              }
            },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        calculable: true,
        series: [
          {
            name: "投票图表",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: []
          }
        ]
      }
    };
  },
  watch: {
    // 同一组件原来的组件实例会被复用，所以生命周期钩子不会再被调用
    // 因此需要侦听路由变化，来加载数据
    $route(to, from) {
      if (to.name === "voteDetailPermission") {
        this.detailStatic();
      }
    }
  },
  filters: {
    formatDate(time) {
      let date = new Date(time + "+0800");
      return formatDate(date, "yyyy-MM-dd hh:mm");
    }
  },
  computed: {
    computed_choice() {
      return function(group) {
        return this.choice.group;
      };
    }
  },
  methods: {
    handleSelected() {
      // console.log(this.selectedValue);
      this.refreshChart();
    },
    makeGroup() {
      // console.log(this.data.group)
      for (var key in this.data.group) {
        if (this.data.multiple === true) {
          this.choice[key] = [];
        } else if (this.data.multiple === false) {
          this.choice[key] = 0;
        }
      }
      // console.log(this.choice)
    },
    filter_option(group) {
      //console.log(group);
      var group_option = [];
      for (var key in this.data.options) {
        //console.log(item);
        if (this.data.options[key].group === group) {
          group_option.push({
            option: this.data.options[key],
            key: parseInt(key)
          });
        }
      }
      return group_option;
    },
    filter_chart_option(group) {
      var group_option = [];
      for (var item of this.data.options) {
        //console.log(item);
        if (item.group === group) {
          group_option.push(item);
        }
      }
      return group_option;
    },
    refreshChart() {
      if (this.data.group.indexOf(this.selectedValue) >= 0) {
        let pie_chart = this.chart_template;
        pie_chart.series[0].data = this.filter_chart_option(this.selectedValue);
        this.chart_option = pie_chart;
        // this.handleResize();
      }
    },
    detailStatic() {
      this.$store
        .dispatch("user/detail", this.$route.params.id)
        .then(data => {
          console.log(data);
          this.data = data;
          this.tableData = this.data.history;
          this.selectedValue = this.data.group[0];
          this.refreshChart();
          this.makeGroup();
        })
        .catch(() => {
          Message({
            message: "无法获取目前开放的投票",
            type: "error",
            duration: 2 * 1000
          });
        });
    },

    handleChange(val) {
      // console.log(val);
    },
    handleResize() {
      window.addEventListener(
        "resize",
        () => {
          this.$refs.pie.resize();
        },
        false
      );
    },
    handleVote() {
      // console.log(this.$route.params.id);
      console.log(this.choice);
      this.$store.state.user.choice = this.choice;
      this.$store
        .dispatch("user/submitVote", this.$route.params.id)
        .then(() => {
          Message({
            message: "提交投票成功",
            type: "success",
            duration: 2 * 1000
          });
          this.submitDisabled = true;
        })
        .catch(() => {
          Message({
            message: "提交投票失败,您可能已经投过",
            type: "error",
            duration: 2 * 1000
          });
        });
    }
  }
};
</script>

<style scoped>
.image {
  width: 70%;
  height: 70%;
}
/* .echarts {
  width: 100%;
  min-width: 300px;
  min-height: 600px;
  height: 100%;
} */
</style>