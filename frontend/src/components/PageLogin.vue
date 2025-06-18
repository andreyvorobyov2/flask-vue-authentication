<script setup>
import { ref } from "vue";
import { http_login } from "@/http";
import router from "@/router";
import store from "@/store";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-default.css";

const username = ref("");
const password = ref("");
const toast = useToast();

const on_click_login = () => {
  console.log("on click login");
  http_login({
    username: username.value,
    password: password.value,
    on_success: login_success,
    on_error: (error_text) => {
      console.log("http_login", error_text);
      toast.open({ message: error_text, type: "error", position: "top-left" });
    },
  });
};

function login_success(response) {
  store.commit("save_username", response.data.username);
  toast.open({
    message: "Login success",
    type: "info",
    position: "top-left",
  });
  setTimeout(() => {
    router.push("/chat");
  }, 1000);
}

const on_click_signup = () => {
  router.push("signup");
};
</script>

<template>
  <div class="m-center-container">
    <div class="box">
      <div class="field">
        <label class="label">Login</label>
        <div class="control">
          <input class="input" type="text" v-model="username" />
        </div>
      </div>
      <div class="field">
        <label class="label">Password</label>
        <div class="control">
          <input
            class="input"
            type="password"
            placeholder="********"
            v-model="password"
          />
        </div>
      </div>
      <div class="fixed-grid has-1-cols">
        <div class="grid">
          <div class="cell">
            <button
              class="button is-success"
              v-on:click="on_click_login"
              style="width: 100%"
            >
              Login
            </button>
          </div>
          <div class="cell">
            <button
              class="button is-ghost"
              v-on:click="on_click_signup"
              style="width: 100%"
            >
              or signup
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
