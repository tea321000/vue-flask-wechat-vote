<template>
  <div>
    <div v-if="roles==='student'" center>
      <h1 center>欢迎您，学号为{{id}}的{{name}}同学！</h1>
    </div>
    <div v-else-if="roles==='teacher'" center>
      <h1>欢迎您，编号为{{id}}的{{name}}老师！</h1>
    </div>
    <div v-else-if="roles==='administrator'" center>
      <h1>欢迎您，编号为{{id}}的{{name}}管理员！</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: "index",
  data() {
    return {
      id: this.$store.state.user.id,
      name: this.$store.state.user.name,
      roles: this.$store.state.user.roles[0]
    };
  }
};
</script>

