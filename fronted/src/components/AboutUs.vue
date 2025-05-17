<template>
  <section class="aboutus-section" aria-labelledby="aboutus-title" role="region">
    <div class="aboutus-card">
      <h1 id="aboutus-title" class="aboutus-title">
        {{ $t("aboutus.title") }}
      </h1>

      <article class="aboutus-content">
        <p class="aboutus-text" v-html="$t('aboutus.text1')"></p>

        <p class="aboutus-text">
          <span v-html="$t('aboutus.text2_prefix')"></span>

          <router-link
            :to="{ name: 'Login', params: { lang: $i18n.locale } }"
            class="aboutus-link"
            aria-label="Ir a iniciar sesión"
          >
            {{ $t("aboutus.loginLink") }}
          </router-link>

          <span v-html="$t('aboutus.text2_suffix')"></span>
        </p>

        <p class="aboutus-text" v-html="$t('aboutus.text3')"></p>
      </article>

      <div class="aboutus-button-container">
        <router-link
          :to="{ name: 'Register', params: { lang: $i18n.locale } }"
          class="aboutus-button"
          aria-label="Ir a registrarse"
        >
          <span aria-hidden="true">⚡</span>
          {{ $t("aboutus.button") }}
        </router-link>
      </div>
    </div>

    <div class="magic-glow glow-top-left" aria-hidden="true"></div>
    <div class="magic-glow glow-bottom-right" aria-hidden="true"></div>
  </section>
</template>

<script setup lang="ts"></script>

<style scoped>
:root {
  --bg-card: rgba(255, 255, 255, 0.08);
  --border-card: rgba(255, 255, 255, 0.1);
  --text-light: #e9d8fd;
  --accent-1: #d8b4fe;
  --accent-2: #9333ea;
  --link: #60a5fa;
  --link-hover: #3b82f6;
  --btn-gradient: linear-gradient(to right, #6d28d9, #4338ca);
  --btn-gradient-hover: linear-gradient(to right, #7c3aed, #4f46e5);
}

.aboutus-section {
  position: relative;
  min-height: 100vh;
  padding: 5rem 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  overflow: hidden;
}

.aboutus-card {
  background: var(--bg-card);
  border: 1px solid var(--border-card);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
  padding: 3rem;
  max-width: 50rem;
  width: 100%;
  z-index: 10;
  background-color: #1a202c;
  box-shadow: 0 0 2rem rgba(0, 0, 0, 0.3);
}

.aboutus-title {
  font-size: 3rem;
  font-weight: bold;
  color: var(--accent-1);
  text-align: center;
  margin-bottom: 2rem;
  text-shadow: 0 0 0.5rem var(--accent-2);
}

.aboutus-text {
  font-size: 1.25rem;
  line-height: 1.75;
  color: var(--text-light);
  margin-bottom: 1.5rem;
}

.aboutus-link {
  color: var(--link);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}
.aboutus-link:hover,
.aboutus-link:focus {
  color: var(--link-hover);
  outline: 3px solid var(--link-hover);
  outline-offset: 2px;
  text-decoration: underline;
}

.aboutus-button-container {
  text-align: center;
  margin-top: 2.5rem;
}
.aboutus-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--btn-gradient);
  color: #fff;
  padding: 0.75rem 2rem;
  font-size: 1.125rem;
  font-weight: bold;
  border-radius: 9999px;
  text-decoration: none;
  transition: transform 0.2s ease, background 0.3s ease;
  box-shadow: 0 0.25rem 1rem rgba(109, 40, 217, 0.4);
}
.aboutus-button:hover,
.aboutus-button:focus {
  transform: scale(1.05);
  background: var(--btn-gradient-hover);
  outline: 3px solid var(--btn-gradient-hover);
  outline-offset: 2px;
}

.magic-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 1;
  animation: pulse 6s infinite alternate;
}
.glow-top-left {
  top: 3rem;
  left: 3rem;
  width: 12rem;
  height: 12rem;
  background: rgba(168, 85, 247, 0.3);
}
.glow-bottom-right {
  bottom: 3rem;
  right: 3rem;
  width: 16rem;
  height: 16rem;
  background: rgba(99, 102, 241, 0.3);
}

@media (prefers-reduced-motion: reduce) {
  .magic-glow {
    animation: none;
  }
}

@keyframes pulse {
  from {
    transform: scale(1);
    opacity: 0.4;
  }
  to {
    transform: scale(1.2);
    opacity: 0.7;
  }
}

@media (max-width: 48rem) {
  .aboutus-section {
    padding: 3rem 1rem;
  }
  .aboutus-card {
    padding: 2rem;
  }
  .aboutus-title {
    font-size: 2.25rem;
  }
  .aboutus-text {
    font-size: 1.125rem;
  }
  .aboutus-button {
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
  }
}
</style>
