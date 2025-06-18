<script setup>
import { ref } from "vue";
import { http_signup } from "@/http";
import router from "@/router";
import store from "@/store";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-default.css";

const username = ref("");
const password = ref("");
const toast = useToast();

const on_click_signup = () => {
  http_signup({
    username: username.value,
    password: password.value,
    on_success: signup_success,
    on_error: (error_text) => {
      console.log("http_signup", error_text);
      toast.open({ message: error_text, type: "error", position: "top-left" });
    },
  });
};

function signup_success(response) {
  store.commit("save_username", response.data.username);
  toast.open({
    message: "Signup success",
    type: "info",
    position: "top-left",
  });
  setTimeout(() => {
    router.push("/chat");
  }, 1000);
}
const on_click_login = () => {
  router.push("login");
};
</script>

<template>
  <div class="m-center-container m-full-screen">
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
              class="button is-info"
              v-on:click="on_click_signup"
              style="width: 100%"
            >
              Signup
            </button>
          </div>
          <div class="cell">
            <button
              class="button is-ghost"
              v-on:click="on_click_login"
              style="width: 100%"
            >
              or login
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
