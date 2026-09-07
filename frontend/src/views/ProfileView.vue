<template>
  <section class="card">
    <header class="card-header">
      <div>
        <h2>Profile Optimizer</h2>
        <p class="subtitle">
          Pick a job you like, write your idea for that job, and generate a suggested profile headline + overview.
        </p>
      </div>
    </header>

    <div v-if="selectedJob" class="selected-job">
      <h3>Selected job:</h3>
      <p class="title">{{ selectedJob.title }}</p>
      <p class="desc">
        {{ selectedJob.description }}
      </p>
    </div>
    <div v-else class="selected-job empty">
      <p>No job selected. Go to the Jobs tab and choose a job.</p>
    </div>

    <label class="field">
      <span>Your idea for this project (will be used to optimize profile):</span>
      <textarea
        v-model="idea"
        rows="4"
        placeholder="Example: I will build the FastAPI backend, design database schema, and write clean, well-tested code..."
      />
    </label>

    <button class="generate-btn" @click="generate" :disabled="!idea || !selectedJob || loading">
      {{ loading ? "Generating..." : "Generate optimized profile" }}
    </button>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="response" class="result">
      <h3>Suggested headline</h3>
      <p class="headline">{{ response.optimized_headline }}</p>

      <h3>Suggested overview</h3>
      <pre class="overview">{{ response.optimized_overview }}</pre>

      <p v-if="response.notes" class="notes">{{ response.notes }}</p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const idea = ref("");
const selectedJob = ref(null);
const loading = ref(false);
const error = ref("");
const response = ref(null);

const getActiveAccountId = () => {
  return sessionStorage.getItem("activeAccountId") || "";
};

onMounted(() => {
  const saved = sessionStorage.getItem("selectedJob");
  if (saved) {
    selectedJob.value = JSON.parse(saved);
  }
});

const generate = async () => {
  if (!selectedJob.value) return;
  loading.value = true;
  error.value = "";
  response.value = null;
  try {
    const accountId = getActiveAccountId();
    const res = await axios.post("/api/profile/optimize", {
      job_id: selectedJob.value.id,
      idea: idea.value,
      account_id: accountId || null,
    });
    response.value = res.data;
  } catch (e) {
    error.value = "Failed to generate optimized profile.";
  } finally {
    loading.value = false;
  }
};
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

.selected-job {
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(55, 65, 81, 0.9);
  background: radial-gradient(circle at top left, #020617, #0b1120);
  margin-bottom: 1rem;
}

.selected-job.empty {
  color: #9ca3af;
}

.title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.desc {
  font-size: 0.9rem;
  color: #e5e7eb;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
}

textarea {
  background: #020617;
  border-radius: 0.6rem;
  padding: 0.6rem 0.75rem;
  border: 1px solid rgba(71, 85, 105, 0.9);
  color: #e5e7eb;
  resize: vertical;
  min-height: 5rem;
}

.generate-btn {
  background: linear-gradient(to right, #38bdf8, #6366f1);
  color: #e5e7eb;
  border: none;
  padding: 0.55rem 1.1rem;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 0.8rem;
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

.error {
  color: #fecaca;
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
}

.result {
  border-top: 1px solid rgba(55, 65, 81, 0.9);
  padding-top: 0.8rem;
}

.headline {
  font-weight: 600;
  margin-top: 0.25rem;
  margin-bottom: 0.75rem;
}

.overview {
  background: #020617;
  border-radius: 0.6rem;
  padding: 0.75rem;
  border: 1px solid rgba(71, 85, 105, 0.9);
  white-space: pre-wrap;
  font-size: 0.9rem;
  margin-bottom: 0.6rem;
}

.notes {
  font-size: 0.85rem;
  color: #9ca3af;
}
</style>

