<template>
  <main class="login-form" role="main">
    <h1>{{ $t("login.title") }}</h1>
    <form @submit.prevent="handleLogin" novalidate>
      <div class="form-group">
        <label for="username">{{ $t("login.username") }}</label>
        <input
          id="username"
          v-model="username"
          type="text"
          maxlength="50"
          placeholder="Felipe123"
          autocomplete="username"
          required
          autofocus
          :aria-invalid="errors.username ? 'true' : 'false'"
          aria-describedby="err-username"
        />
        <div
          v-if="errors.username"
          id="err-username"
          class="error"
          role="alert"
          aria-live="assertive"
        >
          {{ errors.username }}
        </div>
      </div>

      <div class="form-group password-group">
        <label for="password">{{ $t("login.password") }}</label>
        <div class="password-wrapper">
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••••"
            autocomplete="current-password"
            required
            :aria-invalid="errors.password ? 'true' : 'false'"
            aria-describedby="err-password"
          />
          <button
            type="button"
            class="toggle-pw"
            @click="showPassword = !showPassword"
            :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
          >
            {{ showPassword ? "🙈" : "👁️" }}
          </button>
        </div>
        <div
          v-if="errors.password"
          id="err-password"
          class="error"
          role="alert"
          aria-live="assertive"
        >
          {{ errors.password }}
        </div>
      </div>

      <button type="submit" :disabled="loading || hasErrors" class="submit-btn">
        <span v-if="loading">{{ $t("login.loading") }}</span>
        <span v-else>{{ $t("login.submit") }}</span>
      </button>

      <p class="no-account">
        {{ $t("login.noAccount") }}
        <router-link :to="`/${locale}/register`">{{ $t("login.register") }}</router-link>
      </p>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

const { t, locale } = useI18n();
const router = useRouter();

const username = ref("");
const password = ref("");
const errors = ref({
  username: "",
  password: "",
});
const showPassword = ref(false);
const loading = ref(false);

const hasErrors = computed(() => {
  return Boolean(errors.value.username) || Boolean(errors.value.password);
});

const handleLogin = async () => {
  errors.value = {
    username: "",
    password: "",
  };

  if (!username.value.trim()) {
    errors.value.username = t("login.userRequired");
    return;
  }

  if (!password.value.trim()) {
    errors.value.password = t("login.passwordRequired");
    return;
  }

  loading.value = true;
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/users/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      const token = data.token;
      localStorage.setItem("token", token);
      if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user));
      }
      alert(t("login.loginSuccess"));
      router.push(`/${locale.value}/`).then(() => {
        window.location.reload();
      });
    } else {
      if (data.error === "Invalid credentials") {
        errors.value.password = t("login.incorrectCredentials");
      } else {
        alert(t("login.unexpectedError"));
      }
    }
  } catch (err) {
    console.error(err);
    alert(t("login.networkError"));
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-form {
  max-width: 24rem;
  margin: 2rem auto;
  padding: 1.5rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}
@media (max-width: 480px) {
  .login-form {
    margin: 1rem;
    padding: 1rem;
  }
}

.login-form h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
.login-form label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}
.login-form input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #bbb;
  border-radius: 0.25rem;
}
.password-group .password-wrapper {
  position: relative;
}
.toggle-pw {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}
.error {
  color: #b00;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
.submit-btn {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}
.submit-btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
.submit-btn:not([disabled]):hover {
  background-color: #0056b3;
}
.no-account {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}
</style>
