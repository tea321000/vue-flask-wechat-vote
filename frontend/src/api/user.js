import request from "@/utils/request";

export function login(data) {
  return request({
    url: "/vote/login",
    method: "post",
    data
  });
}

export function register(data) {
  return request({
    url: "/vote/register",
    method: "post",
    data
  });
}

export function personalChange(data) {
  return request({
    url: "/vote/personal",
    method: "post",
    data
  });
}

export function getInfo(data) {
  return request({
    url: "/vote/info",
    method: "post",
    data
    // method: 'get',
    // params: {
    //   token
    // }
  });
}

export function logout() {
  return request({
    url: "/vote/logout",
    method: "post"
  });
}

export function getStudents() {
  return request({
    url: "/vote/students",
    method: "post"
  });
}

export function voteHistory(data) {
  return request({
    url: "/vote/history",
    method: "post",
    data
  });
}

export function attendVote(data) {
  return request({
    url: "/vote/attend",
    method: "post",
    data
  });
}

export function detail(data, id) {
  return request({
    url: "/vote/detail/" + id + "/",
    method: "post",
    data
  });
}

export function createVote(data) {
  return request({
    url: "/vote/create",
    method: "post",
    data
  });
}

export function submitVote(data) {
  return request({
    url: "/vote/submit",
    method: "post",
    data
  });
}

export function feedback(data) {
  return request({
    url: "/vote/feedback",
    method: "post",
    data
  });
}

export function watchFeedback(data) {
  return request({
    url: "/vote/watchfeedback",
    method: "post",
    data
  });
}

export function deleteVote(data) {
  return request({
    url: "/vote/deletevote",
    method: "post",
    data
  });
}