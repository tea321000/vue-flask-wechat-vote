(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0daf2f"],{"6e7a":function(e,t,r){"use strict";r.r(t);var a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("Feedback")],1)},n=[],o=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("el-form",{ref:"feedbackForm",attrs:{model:e.feedbackForm,"auto-complete":"on",rules:e.feedbackRules}},[r("el-form-item",{attrs:{label:"反馈主题",prop:"theme"}},[r("el-input",{attrs:{name:"theme",type:"text"},model:{value:e.feedbackForm.theme,callback:function(t){e.$set(e.feedbackForm,"theme",t)},expression:"feedbackForm.theme"}})],1),r("el-form-item",{attrs:{label:"反馈内容",prop:"content"}},[r("el-input",{attrs:{type:"textarea"},model:{value:e.feedbackForm.content,callback:function(t){e.$set(e.feedbackForm,"content",t)},expression:"feedbackForm.content"}})],1),r("el-form-item",[r("el-button",{attrs:{type:"primary"},nativeOn:{click:function(t){return t.preventDefault(),e.handleFeedback(t)}}},[e._v("反馈意见")])],1)],1)],1)},c=[],s=r("61f7"),l=r("5c96"),i={name:"feedback",data(){const e=(e,t,r)=>{Object(s["b"])(t)?r():r(new Error("请输入反馈主题"))},t=(e,t,r)=>{Object(s["b"])(t)?r():r(new Error("请输入反馈内容"))};return{roles:this.$store.state.user.roles[0],feedbackForm:{theme:"",content:""},feedbackRules:{theme:[{required:!0,trigger:"blur",validator:e}],content:[{required:!0,trigger:"blur",validator:t}]}}},methods:{handleFeedback(){this.$refs.feedbackForm.validate(e=>{if(!e)return console.log("错误的提交！"),!1;this.loading=!0,this.$store.dispatch("user/feedback",this.feedbackForm).then(()=>{this.$router.push({name:"IndexPermission"}),this.loading=!1,Object(l["Message"])({message:"反馈意见成功",type:"success",duration:5e3})}).catch(()=>{this.loading=!1,Object(l["Message"])({message:"反馈意见失败",type:"error",duration:5e3})})})}}},d=i,u=r("2877"),m=Object(u["a"])(d,o,c,!1,null,null,null),b=m.exports,f={name:"feedback",components:{Feedback:b}},h=f,k=Object(u["a"])(h,a,n,!1,null,null,null);t["default"]=k.exports}}]);
//# sourceMappingURL=chunk-2d0daf2f.1632929b.js.map