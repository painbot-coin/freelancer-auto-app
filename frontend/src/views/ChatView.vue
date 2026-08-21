<template>
  <section class="card">
    <header class="card-header">
      <div>
        <h2>Chat assistant</h2>
        <p class="subtitle">
          Use this space to think through bids, notes, and strategies while you browse jobs.
        </p>
      </div>
      <button class="refresh-btn" @click="loadHistory" :disabled="loading">
        {{ loading ? "Loading..." : "Reload" }}
      </button>
    </header>

    <div class="chat-window" ref="scrollContainer">
      <div v-for="(msg, index) in messages" :key="index" class="msg-row" :class="msg.sender">
        <span class="badge" v-if="msg.sender === 'assistant'">Assistant</span>
        <span class="badge user" v-else>You</span>
        <p class="bubble">
          {{ msg.message }}
        </p>
      </div>
    </div>

    <form class="composer" @submit.prevent="send">
      <input
        v-model="input"
        type="text"
        placeholder="Write your thoughts or questions here..."
      />
      <button type="submit" :disabled="!input.trim() || sending">
        {{ sending ? "Sending..." : "Send" }}
      </button>
    </form>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import axios from "axios";

const messages = ref([]);
const input = ref("");
const loading = ref(false);
const sending = ref(false);
const scrollContainer = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight;
  }
};

const loadHistory = async () => {
  loading.value = true;
  try {
    const res = await axios.get("/api/chat");
    messages.value = res.data;
    await scrollToBottom();
  } catch (e) {
    // ignore for now
  } finally {
    loading.value = false;
  }
};

const send = async () => {
  const text = input.value.trim();
  if (!text) return;
  sending.value = true;
  try {
    const res = await axios.post("/api/chat", {
      sender: "user",
      message: text,
    });
    messages.value = res.data;
    input.value = "";
    await scrollToBottom();
  } catch (e) {
    // ignore for now
  } finally {
    sending.value = false;
  }
};

onMounted(loadHistory);
</script>

<style scoped>
.card {
  background: rgba(15, 23, 42, 0.95);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.2);
  display: flex;
  flex-direction: column;
  height: calc(100vh - 150px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.subtitle {
  font-size: 0.9rem;
  color: #9ca3af;
}

.refresh-btn {
  background: linear-gradient(to right, #38bdf8, #4ade80);
  color: #020617;
  border: none;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
}

.chat-window {
  flex: 1;
  border-radius: 0.75rem;
  border: 1px solid rgba(55, 65, 81, 0.9);
  background: radial-gradient(circle at top left, #020617, #0b1120);
  padding: 0.75rem;
  overflow-y: auto;
  margin-bottom: 0.75rem;
}

.msg-row {
  max-width: 70%;
  margin-bottom: 0.45rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.msg-row.user {
  margin-left: auto;
  align-items: flex-end;
}

.msg-row.assistant {
  margin-right: auto;
  align-items: flex-start;
}

.badge {
  font-size: 0.7rem;
  color: #a5b4fc;
}

.badge.user {
  color: #6ee7b7;
}

.bubble {
  background: #1e293b;
  border-radius: 0.75rem;
  padding: 0.45rem 0.7rem;
  font-size: 0.9rem;
}

.msg-row.user .bubble {
  background: #4b5563;
}

.composer {
  display: flex;
  gap: 0.55rem;
}

input {
  flex: 1;
  background: #020617;
  border-radius: 999px;
  padding: 0.5rem 0.8rem;
  border: 1px solid rgba(71, 85, 105, 0.9);
  color: #e5e7eb;
}

button[type="submit"] {
  background: linear-gradient(to right, #38bdf8, #6366f1);
  color: #e5e7eb;
  border: none;
  border-radius: 999px;
  padding: 0.45rem 0.9rem;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
}

button[disabled] {
  opacity: 0.6;
  cursor: default;
}
</style>

