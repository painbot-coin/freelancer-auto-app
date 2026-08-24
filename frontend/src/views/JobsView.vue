<template>
  <section class="card">
    <header class="card-header">
      <div>
        <h2>Freelance Jobs</h2>
        <p class="subtitle">
          Automatic check will later plug in real marketplaces. For now, review demo jobs and mark the ones you like.
        </p>
      </div>
      <button class="refresh-btn" @click="fetchJobs" :disabled="loading">
        {{ loading ? "Loading..." : "Refresh" }}
      </button>
    </header>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div class="jobs-list">
      <article
        v-for="job in jobs"
        :key="job.id"
        class="job-item"
        :class="{ interesting: job.is_interesting }"
        @click="toggleInteresting(job)"
      >
        <header class="job-header">
          <div>
            <h3>{{ job.title }}</h3>
            <p class="budget" v-if="job.budget">
              Budget: ${{ job.budget }}
            </p>
          </div>
          <span class="chip" v-if="job.is_interesting">Interested</span>
        </header>
        <p class="description">
          {{ job.description }}
        </p>
        <footer class="job-footer">
          <a v-if="job.url" :href="job.url" target="_blank" @click.stop>
            Open job post
          </a>
          <router-link
            to="/profile"
            class="profile-link"
            @click.stop="setSelectedJob(job)"
          >
            Optimize my profile for this
          </router-link>
        </footer>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const jobs = ref([]);
const loading = ref(false);
const error = ref("");
const router = useRouter();

const getActiveAccountId = () => {
  return sessionStorage.getItem("activeAccountId") || "";
};

const fetchJobs = async () => {
  loading.value = true;
  error.value = "";
  try {
    const accountId = getActiveAccountId();
    const res = await axios.get("/api/jobs", {
      params: accountId ? { account_id: accountId } : {},
    });
    jobs.value = res.data;
  } catch (e) {
    error.value = "Failed to load jobs from API.";
  } finally {
    loading.value = false;
  }
};

const toggleInteresting = (job) => {
  job.is_interesting = !job.is_interesting;
};

const setSelectedJob = (job) => {
  // Minimal cross-view state: store in sessionStorage so Profile page can read it
  sessionStorage.setItem("selectedJob", JSON.stringify(job));
};

onMounted(fetchJobs);
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

.jobs-list {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.job-item {
  padding: 1rem;
  border-radius: 0.9rem;
  border: 1px solid rgba(55, 65, 81, 0.9);
  background: radial-gradient(circle at top left, #0b1120, #020617);
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
}

.job-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 40px rgba(15, 23, 42, 0.7);
  border-color: #38bdf8;
}

.job-item.interesting {
  border-color: #22c55e;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.35rem;
}

h3 {
  font-size: 1rem;
  font-weight: 600;
}

.budget {
  font-size: 0.85rem;
  color: #a3e635;
}

.chip {
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  background: rgba(34, 197, 94, 0.15);
  color: #bbf7d0;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.description {
  font-size: 0.9rem;
  color: #e5e7eb;
  margin-bottom: 0.5rem;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

a {
  color: #38bdf8;
}

.profile-link {
  color: #e5e7eb;
  text-decoration: none;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.4);
}
</style>

