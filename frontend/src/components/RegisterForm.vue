<template>
  <main class="register-form" role="main">
    <h1>{{ $t("register.title") }}</h1>
    <form @submit.prevent="handleRegister" novalidate>
      <div class="form-group">
        <label for="firstName">{{ $t("register.firstName") }}</label>
        <input
          id="firstName"
          v-model="firstName"
          type="text"
          maxlength="50"
          :placeholder="$t('register.firstNamePlaceholder')"
          autocomplete="given-name"
          required
          autofocus
          :aria-invalid="errors.firstName ? 'true' : 'false'"
          aria-describedby="err-firstName"
        />
        <div
          v-if="errors.firstName"
          id="err-firstName"
          class="error"
          role="alert"
          aria-live="assertive"
        >
          {{ errors.firstName }}
        </div>
      </div>

      <div class="form-group">
        <label for="lastName">{{ $t("register.lastName") }}</label>
        <input
          id="lastName"
          v-model="lastName"
          type="text"
          maxlength="50"
          :placeholder="$t('register.lastNamePlaceholder')"
          autocomplete="family-name"
          required
          :aria-invalid="errors.lastName ? 'true' : 'false'"
          aria-describedby="err-lastName"
        />
        <div
          v-if="errors.lastName"
          id="err-lastName"
          class="error"
          role="alert"
          aria-live="assertive"
        >
          {{ errors.lastName }}
        </div>
      </div>

      <div class="form-group">
        <label for="email">{{ $t("register.email") }}</label>
        <input
          id="email"
          v-model="email"
          type="email"
          :placeholder="$t('register.emailPlaceholder')"
          autocomplete="email"
          required
          :aria-invalid="errors.email ? 'true' : 'false'"
          aria-describedby="err-email"
          :class="{ 'is-invalid': email && !validateEmail(email) }"
        />
        <div v-if="errors.email" id="err-email" class="error" role="alert" aria-live="assertive">
          {{ errors.email }}
        </div>
      </div>

      <div class="form-group">
        <label for="username">{{ $t("register.username") }}</label>
        <input
          id="username"
          v-model="username"
          type="text"
          maxlength="50"
          :placeholder="$t('register.usernamePlaceholder')"
          autocomplete="username"
          required
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
        <label for="password">{{ $t("register.password") }}</label>
        <div class="password-wrapper">
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            :placeholder="$t('register.passwordPlaceholder')"
            autocomplete="new-password"
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

      <button type="submit" class="submit-btn" :disabled="loading">
        <span v-if="loading">{{ $t("register.loading") }}</span>
        <span v-else>{{ $t("register.submit") }}</span>
      </button>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, inject, type Ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

const { t, locale } = useI18n();
const logueado = inject("logueado") as Ref<boolean>;
const router = useRouter();

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const username = ref("");
const password = ref("");

const showPassword = ref(false);
const loading = ref(false);
const errors = ref<{
  firstName: string;
  lastName: string;
  email: string;
  username: string;
  password: string;
}>({
  firstName: "",
  lastName: "",
  email: "",
  username: "",
  password: "",
});

const validateEmail = (e: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
const validatePassword = (p: string) => /^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$/.test(p);

const hasErrors = computed(() => {
  return [
    !firstName.value.trim(),
    !lastName.value.trim(),
    !validateEmail(email.value),
    !username.value.trim(),
    !validatePassword(password.value),
  ].some(Boolean);
});

const handleRegister = async () => {
  errors.value = {
    firstName: "",
    lastName: "",
    email: "",
    username: "",
    password: "",
  };

  if (Object.values(errors.value).some((e) => e)) return;

  loading.value = true;
  try {
    const resp = await fetch(`${import.meta.env.VITE_API_URL}/api/users/signup/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        firstname: firstName.value,
        lastname: lastName.value,
        email: email.value,
        password: password.value,
      }),
    });
    const result = await resp.json();

    if (!resp.ok) {
      if (result.error?.includes("email")) {
        errors.value.email = result.error;
      } else if (result.error?.includes("username")) {
        errors.value.username = result.error;
      } else {
        alert(t("register.unknownError"));
      }
    } else {
      alert(t("register.success"));
      localStorage.setItem("token", result.token);
      if (logueado) logueado.value = true;
      router.push(`/${locale.value}/`).then(() => {
        window.location.reload();
      });
    }
  } catch (err: any) {
    console.error(err);
    alert(t("register.networkError"));
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-form {
  max-width: 24rem;
  margin: 2rem auto;
  padding: 1.5rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}
@media (max-width: 480px) {
  .register-form {
    margin: 1rem;
    padding: 1rem;
  }
}

.register-form h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
.register-form label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}
.register-form input {
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
</style>
