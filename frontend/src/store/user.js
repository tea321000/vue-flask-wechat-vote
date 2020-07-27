import {
  login,
  register,
  logout,
  getInfo,
  getStudents,
  personalChange,
  createVote,
  voteHistory,
  attendVote,
  detail,
  submitVote,
  feedback,
  watchFeedback,
  deleteVote
} from "@/api/user";
import {
  getToken,
  setToken,
  removeToken
} from "@/utils/auth";
import router, {
  resetRouter
} from "@/router";

const state = {
  token: getToken(),
  id: "",
  name: "",
  birthday: "",
  phone: "",
  roles: [],
  students: [],
  choice: [],
  vote_id: ""
};

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token;
  },
  SET_PHONE: (state, phone) => {
    state.phone = phone;
  },
  SET_ID: (state, id) => {
    state.id = id;
  },
  SET_NAME: (state, name) => {
    state.name = name;
  },
  SET_BIRTHDAY: (state, birthday) => {
    state.birthday = birthday;
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles;
  },
  SET_STUDENTS: (state, students) => {
    state.students = students;
  },
  RESET_CHOICE: state => {
    state.choice = [];
  }
};

const actions = {
  // 用户登录
  login({
    commit
  }, userInfo) {
    const {
      username,
      password
    } = userInfo;
    return new Promise((resolve, reject) => {
      login({
          username: username.trim(),
          password: password
        })
        .then(response => {
          const {
            data
          } = response;
          // console.log(data)
          commit("SET_TOKEN", data.token);
          setToken(data.token);
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  // 用户注册
  register({
    commit
  }, userInfo) {
    // console.log("用户注册");
    const {
      username,
      name,
      password,
      birthday,
      phone,
      role
    } = userInfo;
    return new Promise((resolve, reject) => {
      register({
          username: username.trim(),
          name: name.trim(),
          password: password,
          birthday: birthday,
          phone: phone,
          role: role
        })
        .then(response => {
          const {
            data
          } = response;
          resolve();
        })
        .catch(error => {
          //   console.log(error);
          //   console.log("错误");
          reject(error);
        });
    });
  },

  // 用户反馈
  feedback({
    state
  }, userInfo) {
    const {
      theme,
      content
    } = userInfo;
    return new Promise((resolve, reject) => {
      feedback({
          theme: theme.trim(),
          content: content.trim(),
          token: state.token
        })
        .then(response => {
          const {
            data
          } = response;
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // 得到所有反馈信息
  watchFeedback({
    state
  }) {
    return new Promise((resolve, reject) => {
      watchFeedback({
          token: state.token
        })
        .then(response => {
          const {
            data
          } = response;

          if (!data) {
            reject("认证失败，请重新登录");
          }
          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  //更改个人资料
  personalChange({
    commit,
    state
  }, userInfo) {
    const {
      password,
      birthday,
      phone
    } = userInfo;
    return new Promise((resolve, reject) => {
      personalChange({
          password: password,
          birthday: birthday,
          phone: phone,
          token: state.token
        })
        .then(response => {
          const {
            data
          } = response;
          // console.log(data)
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // 得到用户信息
  getInfo({
    commit,
    state
  }) {
    return new Promise((resolve, reject) => {
      getInfo({
          token: state.token
        })
        .then(response => {
          const {
            data
          } = response;

          if (!data) {
            reject("认证失败，请重新登录");
          }

          const {
            roles,
            name,
            birthday,
            phone,
            id
          } = data;
          // 角色必须是非空数组
          if (!roles || roles.length <= 0) {
            reject("getInfo: roles must be a non-null array!");
          }
          commit("SET_ROLES", roles);
          commit("SET_NAME", name);
          commit("SET_BIRTHDAY", birthday);
          commit("SET_PHONE", phone);
          commit("SET_ID", id);

          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // 得到所有学生信息
  getStudents({
    commit
  }) {
    return new Promise((resolve, reject) => {
      getStudents()
        .then(response => {
          const {
            data
          } = response;

          if (!data) {
            reject("认证失败，请重新登录");
          }

          const {
            person
          } = data;

          commit("SET_STUDENTS", person);
          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  // 得到投票历史
  voteHistory({
    state
  }) {
    return new Promise((resolve, reject) => {
      voteHistory({
          token: state.token
        })
        .then(response => {
          const {
            data
          } = response;
          // console.log(data);

          if (!data) {
            reject("认证失败，请重新登录");
          }

          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  //得到参与投票的列表
  attendVote({
    state
  }) {
    return new Promise((resolve, reject) => {
      attendVote({
          token: state.token
        })
        .then(response => {
          const {
            data
          } = response;
          // console.log(data);

          if (!data) {
            reject("认证失败，请重新登录");
          }

          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // 得到投票详情
  detail({
    state
  }, id) {
    return new Promise((resolve, reject) => {
      detail({
            token: state.token
          },
          id
        )
        .then(response => {
          const {
            data
          } = response;
          console.log(data);

          if (!data) {
            reject("认证失败，请重新登录");
          }

          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  // 删除投票
  deleteVote({
    commit,
    state
  }) {
    return new Promise((resolve, reject) => {
      // console.log(state.vote_id)
      deleteVote({
          token: state.token,
          vote_id: state.vote_id
        })
        .then(response => {
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  //投票
  submitVote({
    state,
    commit
  }, id) {
    return new Promise((resolve, reject) => {
      submitVote({
          id,
          choice: state.choice,
          token: state.token
        })
        .then(response => {
          commit("RESET_CHOICE");
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // 用户登出
  logout({
    commit,
    state
  }) {
    return new Promise((resolve, reject) => {
      logout(state.token)
        .then(() => {
          commit("SET_TOKEN", "");
          commit("SET_ROLES", []);
          removeToken();
          resetRouter();
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  //创建投票
  createVote({
    commit,
    state
  }, voteInfo) {
    const {
      theme,
      startDate1,
      startDate2,
      endDate1,
      endDate2,
      selectMode,
      anonymous,
      filter,
      selectedAcademy,
      selectedGrade,
      selectedPerson,
      content,
      image,
      multipleSelected,
      singleSelected
    } = voteInfo;
    return new Promise((resolve, reject) => {
      createVote({
          theme: theme,
          startDate1: startDate1,
          startDate2: startDate2,
          endDate1: endDate1,
          endDate2: endDate2,
          selectMode: selectMode,
          anonymous: anonymous,
          filter: filter,
          selectedAcademy: selectedAcademy,
          selectedGrade: selectedGrade,
          selectedPerson: selectedPerson,
          content: content,
          image: image,
          multipleSelected: multipleSelected,
          singleSelected: singleSelected,
          token: state.token
        })
        .then(response => {
          const {
            data
          } = response;
          // console.log(data)
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // 清除token
  resetToken({
    commit
  }) {
    return new Promise(resolve => {
      commit("SET_TOKEN", "");
      commit("SET_ROLES", []);
      removeToken();
      resolve();
    });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};