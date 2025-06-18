<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { http_userlist, http_logout } from "@/http";
import { create_socket } from "@/socket";
import store from "@/store";
import router from "@/router";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-default.css";

const STATUS = {
  ONLINE: "Online",
  OFFLINE: "Offline",
  CONNECTING: "Connecting",
};

const toast = useToast();

/* properties */
const userlist = ref([]);
const selected_user = ref({});
const messages = ref([]);
const message_text = ref("");
const send_button_disabled = ref(false);
const connection_status = ref("Offline");
const socket = ref(null);

/* event handlers */
const on_select_user = (user) => {
  selected_user.value = user;
};

watch(
  selected_user,
  (new_value, old_value) => {
    if (selected_user.value.username == undefined) {
      send_button_disabled.value = true;
    } else {
      send_button_disabled.value = false;
      socket.value.emit("load_messages", selected_user.value.username);
      clear_unread_messages_count(selected_user.value.username);
    }
  },
  { immediate: true }
);

const on_click_logout = () => {
  http_logout({
    on_success: (response) => {
      console.log(response);
      store.commit("save_username", "");
      router.go("/login");
      toast.open({
        message: "Logout success",
        type: "info",
        position: "top-left",
      });
    },
    on_error: (error_text) => {
      console.log(error_text);
      toast.open({ message: error_text, type: "error", position: "top-left" });
    },
  });
};

const on_click_connection_button = () => {
  switch (connection_status.value) {
    case STATUS.ONLINE: {
      socket.value.disconnect();
      break;
    }
    case STATUS.OFFLINE: {
      connect();
      break;
    }
    case STATUS.CONNECTING: {
      socket.value.close();
      socket.value = null;
      connection_status.value = STATUS.OFFLINE;
      break;
    }
  }
};

const on_click_send_message = () => {
  socket.value.emit(
    "send_message_to_user",
    selected_user.value.username,
    message_text.value
  );
  message_text.value = "";
};

const scroll_message = ref(null);

const scroll_message_ref = (el) => {
  scroll_message.value = el;
};

onMounted(() => {
  connect();
});

function connect() {
  create_socket({
    on_success: (_socket) => {
      socket.value = _socket;
      socket.value.on("connect", set_connection_enable);
      socket.value.on("connect_error", set_connection_disable);
      socket.value.on("disconnect", set_connection_disable);

      socket.value.on("user_connect", (data) => {
        update_userlist();
      });

      socket.value.on("user_disconnect", (data) => {
        update_userlist();
      });

      socket.value.on("messages_loaded", (data) => {
        messages.value = data.messages;
        // message is read, send response
        socket.value.emit("read_message_confirm", selected_user.value.username);
      });

      socket.value.on("receive_message_from_user", (data) => {
        if (
          data.from != selected_user.value.username &&
          data.from != store.state.username
        ) {
          // notify new message
          increase_unread_messages_count(data.from);

          toast.open({
            message: `${data.from} ${data.message}`,
            type: "info",
            position: "top-left",
          });

          if (data.from != selected_user.value.username) {
            return;
          }
        }

        // show message
        messages.value.push({
          from: data.from,
          to: data.to,
          date: data.date,
          message: data.message,
        });

        // message is read, send response
        socket.value.emit("read_message_confirm", selected_user.value.username);

        // scroll is down
        setTimeout(() => {
          scroll_message.value.scrollIntoView({
            behavior: "smooth",
            block: "end",
          });
        }, 500);

        console.log(scroll_message.value);
      });
    },
    on_error: (error) => {
      console.log("create cocket", error);
      toast.open({ message: error, type: "error", position: "top-left" });
    },
  });
}

function set_connection_enable() {
  connection_status.value = STATUS.ONLINE;
  update_userlist();
  toast.open({
    message: "Connected to server",
    type: "success",
    position: "top-left",
  });
}

function set_connection_disable(error) {
  if (socket.value.active) {
    // try to reconnect
    connection_status.value = STATUS.CONNECTING;
    offline_userlist();
    toast.open({
      message: "Reconnecting... " + error,
      type: "warning",
      position: "top-left",
    });
  } else {
    connection_status.value = STATUS.OFFLINE;
    offline_userlist();
    toast.open({
      message: "Connection closed",
      type: "error",
      position: "top-left",
    });
  }
}

function update_userlist() {
  http_userlist({
    online_only: false,
    on_success: (response) => {
      userlist.value = response.data;
      console.log("update_userlist", response);
    },
    on_error: (error_text) => {
      toast.open({
        message: error_text,
        type: "error",
        position: "top-left",
      });
      // console.log("update_userlist", error_text);
    },
  });
}

function offline_userlist() {
  userlist.value.forEach((item, i, arr) => {
    item.connection_status = STATUS.OFFLINE;
    item.count_unread_messages = 0;
  });
}

function increase_unread_messages_count(from_username) {
  const message_sender = userlist.value.filter((item, i, arr) => {
    return item.username == from_username;
  });
  message_sender.forEach((item, i, arr) => {
    item.count_unread_messages += 1;
  });
}

function clear_unread_messages_count(from_username) {
  const message_sender = userlist.value.filter((item, i, arr) => {
    return item.username == from_username;
  });
  message_sender.forEach((item, i, arr) => {
    item.count_unread_messages = 0;
  });
}

// status label
const status_label_class = computed(() => ({
  "has-text-success": connection_status.value == STATUS.ONLINE,
  "has-text-danger": connection_status.value == STATUS.OFFLINE,
  "has-text-warning": connection_status.value == STATUS.CONNECTING,
}));

// status buttons: connect, disconnect, cancel reconnect
const status_button_class = computed(() => ({
  "is-success": connection_status.value == STATUS.OFFLINE,
  "is-danger":
    connection_status.value == STATUS.ONLINE ||
    connection_status.value == STATUS.CONNECTING,
}));

const status_button_title = ref("");
watch(
  connection_status,
  (new_value, old_value) => {
    // executed immediately, then again when `source` changes
    switch (new_value) {
      case STATUS.ONLINE:
        status_button_title.value = "Disconnect";
        break;
      case STATUS.OFFLINE:
        status_button_title.value = "Connect";
        break;
      case STATUS.CONNECTING:
        status_button_title.value = "Cancel";
        break;
    }
  },
  { immediate: true }
);

// who is sender
function message_class(msg) {
  return {
    "is-link m-message-is-mine": msg.from == store.state.username,
    "m-message-not-is-mine": msg.to == store.state.username,
  };
}
</script>

<template>
  <div class="m-center-container">
    <div class="box main">
      <div class="columns">
        <div class="column is-2">
          <!-- userlist -->
          <article class="panel is-info" style="height: 100%">
            <p class="panel-heading">Users</p>
            <div class="m-scr2">
              <div v-for="user in userlist">
                <a class="panel-block" v-on:click="on_select_user(user)">
                  <span
                    class="panel-icon"
                    v-bind:class="[
                      user.socket_status == STATUS.ONLINE
                        ? ' has-text-success'
                        : ' has-text-danger',
                    ]"
                  >
                    <i class="fas fa-user-circle" aria-hidden="true"></i>
                  </span>
                  {{
                    user.username +
                    (user.username == store.state.username ? " (you)" : "")
                  }}

                  <span
                    v-if="user.count_unread_messages"
                    class="tag is-danger"
                    style="border-radius: 50%; margin-left: 5px"
                    >{{ user.count_unread_messages }}
                  </span>
                </a>
              </div>
            </div>
          </article>
          <!-- /userlist -->
        </div>

        <div class="column">
          <div class="columns">
            <div class="column messages">
              <!-- main form -->
              <div class="card" style="height: 100%">
                <header class="card-header">
                  <!-- selected user -->
                  <p class="card-header-title">
                    <!-- {{ selected_user.username }} -->
                    <button
                      v-if="selected_user.username"
                      class="card-header-icon"
                      aria-label="status"
                    >
                      <span
                        class="icon-text has-text-success has-text-weight-medium"
                        :class="status_label_class"
                      >
                        <span>
                          {{ selected_user.username }} :
                          {{ selected_user.socket_status }}</span
                        >

                        <span class="icon" :class="status_label_class">
                          <i class="fas fa-user-circle"></i>
                        </span>
                      </span>
                    </button>
                  </p>
                  <!-- / selected user -->

                  <!-- logout button -->
                  <button
                    class="button is-warning is-light m-status-buttons"
                    v-on:click="on_click_logout"
                  >
                    Logout
                  </button>

                  <!-- connection button -->
                  <button
                    class="button is-light m-status-buttons"
                    :class="status_button_class"
                    v-on:click="on_click_connection_button"
                  >
                    {{ status_button_title }}
                  </button>

                  <!-- connection status label -->
                  <button class="card-header-icon" aria-label="status">
                    <span
                      class="icon-text has-text-success has-text-weight-medium"
                      :class="status_label_class"
                    >
                      <span>
                        {{ store.state.username }} :
                        {{ connection_status }}</span
                      >

                      <span class="icon" :class="status_label_class">
                        <i class="fas fa-user-circle"></i>
                      </span>
                    </span>
                  </button>
                  <!-- / connection status label -->
                </header>

                <!-- messages -->
                <div class="card-content">
                  <div class="content">
                    <div class="m-scrl">
                      <div
                        :ref="scroll_message_ref"
                        class="m-message-container"
                      >
                        <!-- message is-info m-message-not-is-mine -->

                        <article
                          v-for="msg in messages"
                          class="message"
                          :class="message_class(msg)"
                        >
                          <div class="message-header">
                            <p>{{ msg.from }}</p>
                            <p>{{ msg.date }}</p>
                            <!-- <button class="delete" aria-label="delete"></button> -->
                          </div>
                          <div class="message-body">
                            {{ msg.message }}
                          </div>
                        </article>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- /messages -->
              </div>
            </div>
          </div>

          <!-- message -->
          <div class="box">
            <div class="columns">
              <div class="column">
                <textarea
                  v-model="message_text"
                  rows="2"
                  class="textarea is-info"
                  placeholder="Message"
                ></textarea>
              </div>
              <div class="column is-1">
                <button
                  :disabled="send_button_disabled"
                  v-on:click="on_click_send_message"
                  class="button is-primary"
                  style="height: 100%; width: 100%"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
          <!-- message -->
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.m-status-buttons {
  margin: 5px;
  width: 100px;
}
.m-scrl {
  /* background-color: #1f77cf; */
  max-height: calc(100vh - 315px);
  overflow-x: hidden;
  overflow-y: auto;
  padding: 35px;
}

.m-scr2 {
  max-height: calc(100vh - 150px);
  overflow-x: hidden;
  overflow-y: auto;
  /* padding: 35px; */
}
.m-message-container {
  display: flex;
  flex-direction: column;
}
.m-message-not-is-mine {
  margin-right: 20%;
}
.m-message-is-mine {
  margin-left: 20%;
}
.client-status {
  display: flex;
}
.cell {
  border: solid;
  display: block;
  background-color: aquamarine;
}
.messages {
  height: calc(100vh - 200px) !important;
}
.main {
  /* background-color: aqua; */
  display: block;
  height: 100vh;
  width: 100%;
  padding: 50px;
}
</style>
