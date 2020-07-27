<template>
  <div>
    <h3 v-if="roles==='student'">您是学生，无权查看此页</h3>
    <el-form
      ref="voteForm"
      :model="voteForm"
      label-width="80px"
      auto-complete="on"
      :rules="voteRules"
    >
      <el-form-item label="活动主题" prop="theme">
        <el-input v-model="voteForm.theme" name="theme" type="text"></el-input>
      </el-form-item>

      <el-form-item label="活动内容">
        <el-input type="textarea" v-model="voteForm.content"></el-input>
      </el-form-item>

      <el-form-item label="活动图片">
        <!-- <input name="file" type="file" @change="onChange" :multiple="multiple"> -->
        <el-upload
          class="avatar-uploader"
          action="http://www.yourdomain.xyz:yourport/vote/upload"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <img v-if="imageUrl" :src="imageUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-form-item>

      <el-form-item label="开始时间">
        <el-col :span="24">
          <el-date-picker
            type="date"
            placeholder="选择日期"
            v-model="voteForm.startDate1"
            style="width: 100%;"
            ref="startDate1"
            value-format="yyyy-MM-dd"
            format="yyyy-MM-dd"
          ></el-date-picker>
        </el-col>
        <el-col :span="24">
          <el-time-picker
            placeholder="选择时间"
            v-model="voteForm.startDate2"
            style="width: 100%;"
            value-format="HH:mm:ss"
            format="HH:mm:ss"
            ref="startDate2"
          ></el-time-picker>
        </el-col>
      </el-form-item>

      <el-form-item label="结束时间" prop="endDate">
        <el-col :span="24">
          <el-date-picker
            type="date"
            placeholder="选择日期"
            v-model="voteForm.endDate1"
            style="width: 100%;"
            ref="endDate1"
            value-format="yyyy-MM-dd"
            format="yyyy-MM-dd"
          ></el-date-picker>
        </el-col>
        <el-col :span="24">
          <el-time-picker
            placeholder="选择时间"
            v-model="voteForm.endDate2"
            style="width: 100%;"
            value-format="HH:mm:ss"
            format="HH:mm:ss"
            ref="endDate2"
          ></el-time-picker>
        </el-col>
      </el-form-item>

      <el-form-item label="单选/多选">
        <el-switch v-model="voteForm.selectMode" ref="selectedMode"></el-switch>
      </el-form-item>

      <el-form-item label="多选" v-if="voteForm.selectMode===true" prop="selected">
        <el-input placeholder="请输入组别_选项" v-model="tmpInput" class="input-with-select">
          <el-button slot="append" icon="el-icon-circle-plus-outline" @click="onMultipleSelected"></el-button>
        </el-input>
        <el-checkbox-group ref="multipleSelected">
          <!-- <el-checkbox-group v-model="voteForm.type"> -->
          <!-- <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>
          <el-checkbox label="地推活动" name="type"></el-checkbox>
          <el-checkbox label="线下主题活动" name="type"></el-checkbox>
          <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>-->

          <!-- <el-checkbox v-for="item in voteForm.multipleSelected" :label="item" name="type"></el-checkbox> -->

          <div v-for="(item,index) in voteForm.multipleSelected">
            <el-button
              size="mini"
              type="primary"
              icon="el-icon-delete"
              @click="deleteMutipleOption(index)"
            ></el-button>
            <el-checkbox :label="item" name="type"></el-checkbox>
          </div>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="单选" v-else-if="voteForm.selectMode===false" prop="selected">
        <el-input placeholder="请输入组别_选项" v-model="tmpInput" class="input-with-select">
          <el-button slot="append" icon="el-icon-circle-plus-outline" @click="onSingleSelected"></el-button>
        </el-input>
        <el-radio-group ref="singleSelected">
          <!-- <el-radio-group v-model="voteForm.resource"> -->
          <!-- <el-radio label="线上品牌商赞助"></el-radio>
          <el-radio label="线下场地免费"></el-radio>-->

          <!-- <el-radio v-for="item in voteForm.singleSelected" :label="item"></el-radio> -->
          <div v-for="(item,index) in voteForm.singleSelected">
            <el-button
              size="mini"
              type="primary"
              icon="el-icon-delete"
              @click="deleteSingleOption(index)"
            ></el-button>
            <el-radio :label="item"></el-radio>
          </div>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="筛选">
        <el-radio-group v-model="voteForm.filter">
          <el-radio label="全校" :disabled="radio_disabled"></el-radio>
          <el-radio label="学院"></el-radio>
          <el-radio label="年级"></el-radio>
          <el-radio label="个人"></el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="学院" v-if="voteForm.filter==='学院'">
        <el-checkbox-group v-model="voteForm.selectedAcademy">
          <el-checkbox v-for="item in academy" :label="item" name="type" :key="item.id"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="年级" v-else-if="voteForm.filter==='年级'">
        <el-checkbox-group v-model="voteForm.selectedGrade">
          <el-checkbox v-for="item in grade" :label="item" name="type" :key="item.id"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="个人" v-else-if="voteForm.filter==='个人'">
        <el-input v-model="person_filter" placeholder="请输入查询的个人"></el-input>
        <el-checkbox-group v-model="voteForm.selectedPerson" v-if="person_filter.length===0">
          <el-checkbox v-for="item in person" :label="item" name="type" :key="item.id"></el-checkbox>
        </el-checkbox-group>
        <el-checkbox-group v-model="voteForm.selectedPerson" v-else="person_filter.length>0">
          <el-checkbox v-for="item in personFilterResult" :label="item" name="type" :key="item.id"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="是否匿名">
        <el-switch v-model="voteForm.anonymous"></el-switch>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click.native.prevent="handleVote">立即创建</el-button>
        <!-- <el-button>取消</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { validBlank, validDate, validSelected } from "@/utils/validate";
import { Message } from "element-ui";

var date = new Date();
export default {
  created() {
    this.$store
      .dispatch("user/getStudents")
      .then(() => {
        Message({
          message: "成功获取学生信息",
          type: "success",
          duration: 2 * 1000
        });
        this.person = this.$store.state.user.students;
      })
      .catch(() => {
        Message({
          message: "无法获取学生信息",
          type: "error",
          duration: 2 * 1000
        });
      });
  },
  data() {
    const validateTheme = (rule, value, callback) => {
      if (!validBlank(value)) {
        callback(new Error("请输入主题"));
      } else {
        callback();
      }
    };
    const validateEndDate = (rule, value, callback) => {
      if (
        !validDate(
          this.$refs.startDate1.$children[0].$options.propsData.value,
          this.$refs.startDate2.$children[0].$options.propsData.value,
          this.$refs.endDate1.$children[0].$options.propsData.value,
          this.$refs.endDate2.$children[0].$options.propsData.value
        )
      ) {
        callback(new Error("请输入正确的结束日期"));
      } else {
        callback();
      }
    };

    const validateSelected = (rule, value, callback) => {
      // console.log(this.$refs.selectedMode.$options.propsData.value);
      // console.log(this.$refs.singleSelected);
      if (this.$refs.selectedMode.$options.propsData.value) {
        if (!validSelected(this.$refs.multipleSelected.$children.length)) {
          callback(new Error("请输入超过两个选项！"));
        } else {
          callback();
        }
      } else {
        if (!validSelected(this.$refs.singleSelected.$children.length)) {
          callback(new Error("请输入超过两个选项！"));
        } else {
          callback();
        }
      }
    };

    return {
      roles: this.$store.state.user.roles[0],
      voteForm: {
        theme: "",
        startDate1: date.toLocaleDateString(),
        startDate2: date.toLocaleTimeString("chinese", { hour12: false }),
        endDate1: "",
        endDate2: "",
        selectMode: false,
        anonymous: false,
        filter: "全校",
        selectedAcademy: [],
        selectedGrade: [],
        selectedPerson: [],
        content: "",
        image: "",
        multipleSelected: [],
        singleSelected: []
      },
      voteRules: {
        theme: [{ required: true, trigger: "blur", validator: validateTheme }],
        endDate: [
          { required: true, trigger: "blur", validator: validateEndDate }
        ],

        selected: [
          { required: true, trigger: "blur", validator: validateSelected }
        ]
      },
      academy: [
        "机电工程学院",
        "信息与通信学院",
        "计算机与信息安全学院",
        "艺术与设计学院",
        "商学院",
        "外国语学院",
        "数学与计算科学学院",
        "电子工程与自动化学院"
      ],
      grade: [2015, 2016, 2017, 2018],
      person: [],
      previewImage: "",
      tmpInput: "",
      imageUrl: "",
      person_filter: "",
      personFilterResult: []
    };
  },
  computed: {
    radio_disabled() {
      if (
        this.voteForm.selectedAcademy.length === 0 &&
        this.voteForm.selectedGrade.length === 0 &&
        this.voteForm.selectedPerson.length === 0
      ) {
        return false;
      } else {
        return true;
      }
    }
    // multiple() {
    //   return false;
    // }
  },
  watch: {
    person_filter: function(newFilter, oldFilter) {
      this.personFilter();
    }
  },
  methods: {
    deleteMutipleOption(index) {
      this.voteForm.multipleSelected.splice(index, 1);
    },
    deleteSingleOption(index) {
      this.voteForm.singleSelected.splice(index, 1);
    },
    personFilter() {
      this.personFilterResult = [];
      for (var item of this.person) {
        if (item.indexOf(this.person_filter) > -1) {
          this.personFilterResult.push(item);
        }
      }
    },
    onMultipleSelected() {
      if (this.tmpInput) {
        this.voteForm.multipleSelected.push(this.tmpInput);
        // console.log(this.voteForm.multipleSelected);
      }
    },
    onSingleSelected() {
      if (this.tmpInput) {
        this.voteForm.singleSelected.push(this.tmpInput);
        // console.log(this.voteForm.singleSelected);
      }
    },
    handleAvatarSuccess(res, file) {
      // console.log(res["link"]);
      this.voteForm.image = res["link"];
      this.imageUrl = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传图片只能是 JPG 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传图片大小不能超过 2MB!");
      }
      return isJPG && isLt2M;
    },
    handleVote() {
      // console.log("submit!");
      this.$refs.voteForm.validate(valid => {
        if (valid) {
          this.loading = true;

          this.$store
            .dispatch("user/createVote", this.voteForm)
            .then(() => {
              this.$router.push({ name: "IndexPermission" });
              this.loading = false;
              Message({
                message: "新建投票成功",
                type: "success",
                duration: 5 * 1000
              });
            })
            .catch(() => {
              this.loading = false;
              Message({
                message: "新建投票失败，请检查‘组别_选项’格式是否正确",
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
<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}

::-ms-browse,
[type="file"] {
  display: inline-block;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  -webkit-appearance: none;
  text-align: center;
  box-sizing: border-box;
  outline: none;
  margin: 0;
  transition: 0.1s;
  font-weight: 500;
  padding: 9px 15px;
  font-size: 12px;
  border-radius: 3px;
  border: 1px solid #00c3ff;
  background: #00c3ff;
  color: #fff;
}
::-webkit-file-upload-button {
  display: inline-block;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  -webkit-appearance: none;
  text-align: center;
  box-sizing: border-box;
  outline: none;
  margin: 0;
  transition: 0.1s;
  font-weight: 500;
  padding: 9px 15px;
  font-size: 12px;
  border-radius: 3px;
  border: 1px solid #00c3ff;
  background: #00c3ff;
  color: #fff;
}
</style>
