<template>
  <section class="card">
    <header class="card-header">
      <div>
        <h2>Accounts dashboard</h2>
        <p class="subtitle">
          Overview of your Freelancer.com accounts: profile status and remaining bids.
        </p>
      </div>
      <button class="refresh-btn" @click="loadStatus" :disabled="loading">
        {{ loading ? "Loading..." : "Refresh" }}
      </button>
    </header>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div class="accounts-grid">
      <article
        v-for="acc in accounts"
        :key="acc.id"
        class="account-card"
      >
        <header class="account-header">
          <h3>{{ acc.name }}</h3>
          <span
            class="status-chip"
            :class="{
              active: acc.profile_status === 'active',
              unknown: acc.profile_status !== 'active'
            }"
          >
            {{ acc.profile_status }}
          </span>
        </header>
        <p class="profile-name">
          Profile: <strong>{{ acc.profile_name }}</strong>
        </p>
        <p class="bids">
          Remaining bids:
          <strong>
            <span v-if="acc.remaining_bids >= 0">
              {{ acc.remaining_bids }}
            </span>
            <span v-else>unknown</span>
          </strong>
        </p>
        <footer class="card-footer">
          <router-link to="/jobs">
            View jobs for this account
          </router-link>
        </footer>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const accounts = ref([]);
const loading = ref(false);
const error = ref("");

const loadStatus = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await axios.get("/api/accounts/status");
    accounts.value = res.data;
  } catch (e) {
    error.value = "Failed to load account status from API.";
  } finally {
    loading.value = false;
  }
};

onMounted(loadStatus);
</script>

<style scoped>
.card {
  background: rgba(15, 23, 42, 0.95);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

h2 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.subtitle {
  font-size: 0.9rem;
  color: #9ca3af;
}

.refresh-btn {
  background: linear-gradient(to right, #38bdf8, #4ade80);
  color: #020617;
  border: none;
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

.error {
  color: #fecaca;
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 1rem;
}

.account-card {
  padding: 1rem;
  border-radius: 0.9rem;
  border: 1px solid rgba(55, 65, 81, 0.9);
  background: radial-gradient(circle at top left, #0b1120, #020617);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.4rem;
}

h3 {
  font-size: 1rem;
  font-weight: 600;
}

.status-chip {
  font-size: 0.7rem;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.5);
}

.status-chip.active {
  background: rgba(34, 197, 94, 0.15);
  color: #bbf7d0;
  border-color: rgba(34, 197, 94, 0.65);
}

.status-chip.unknown {
  background: rgba(148, 163, 184, 0.15);
  color: #e5e7eb;
}

.profile-name,
.bids {
  font-size: 0.9rem;
  color: #e5e7eb;
  margin: 0.2rem 0;
}

.card-footer {
  margin-top: 0.5rem;
  font-size: 0.85rem;
}

.card-footer a {
  color: #38bdf8;
  text-decoration: none;
}
</style>

