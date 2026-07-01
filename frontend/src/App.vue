<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="brand">
        <h1>Freelancer Auto App</h1>
        <p class="brand-sub">FastAPI + Vue helper for your Freelancer profiles</p>
      </div>
      <div class="header-right">
        <div class="account-select">
          <label>
            <span>Account</span>
            <select v-model="selectedAccountId" @change="persistAccount">
              <option v-if="accounts.length === 0" disabled value="">
                No accounts configured
              </option>
              <option
                v-for="acc in accounts"
                :key="acc.id"
                :value="acc.id"
              >
                {{ acc.name }}
              </option>
            </select>
          </label>
        </div>
        <nav>
          <router-link to="/jobs">Jobs</router-link>
          <router-link to="/profile">Profile Optimizer</router-link>
          <router-link to="/chat">Chat</router-link>
        </nav>
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const accounts = ref([]);
const selectedAccountId = ref("");
const STORAGE_KEY = "activeAccountId";

const loadAccounts = async () => {
  try {
    const res = await axios.get("/api/accounts");
    accounts.value = res.data;
    const saved = sessionStorage.getItem(STORAGE_KEY);
    if (saved && res.data.some((a) => a.id === saved)) {
      selectedAccountId.value = saved;
    } else if (res.data.length > 0) {
      selectedAccountId.value = res.data[0].id;
      sessionStorage.setItem(STORAGE_KEY, selectedAccountId.value);
    }
  } catch {
    // ignore for now; UI will just show no accounts
  }
};

const persistAccount = () => {
  if (selectedAccountId.value) {
    sessionStorage.setItem(STORAGE_KEY, selectedAccountId.value);
  }
};

onMounted(loadAccounts);
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #050816;
  color: #e5e7eb;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.app-header {
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  background: radial-gradient(circle at top left, #1e293b, #020617);
  box-shadow: 0 1px 0 rgba(148, 163, 184, 0.2);
}

.brand {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

h1 {
  font-size: 1.25rem;
  font-weight: 600;
}

.brand-sub {
  font-size: 0.8rem;
  color: #9ca3af;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

nav {
  display: flex;
  gap: 1rem;
}

a {
  color: #9ca3af;
  text-decoration: none;
  font-size: 0.95rem;
}

a.router-link-active {
  color: #38bdf8;
  border-bottom: 2px solid #38bdf8;
  padding-bottom: 0.15rem;
}

.account-select label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #9ca3af;
}

.account-select select {
  background: #020617;
  color: #e5e7eb;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.6);
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
}

.app-main {
  flex: 1;
  padding: 1.5rem 2rem 2rem;
}
</style>

