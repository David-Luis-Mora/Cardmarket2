<template>
  <section class="aboutus-section">
    <div class="aboutus-card">
      <h1 class="aboutus-title">{{ $t("aboutus.title") }}</h1>

      <p class="aboutus-text" v-html="$t('aboutus.text1')"></p>

      <p class="aboutus-text">
        <span v-html="$t('aboutus.text2_prefix')"></span>

        <!-- Enlace al login -->
        <router-link :to="{ name: 'Login', params: { lang: $i18n.locale } }" class="aboutus-link">
          {{ $t("aboutus.loginLink") }}
        </router-link>

        <span v-html="$t('aboutus.text2_suffix')"></span>
      </p>

      <p class="aboutus-text" v-html="$t('aboutus.text3')"></p>

      <div class="aboutus-button-container">
        <!-- Enlace al register -->
        <router-link
          :to="{ name: 'Register', params: { lang: $i18n.locale } }"
          class="aboutus-button"
        >
          ⚡ {{ $t("aboutus.button") }}
        </router-link>
      </div>
    </div>

    <div class="magic-glow glow-top-left"></div>
    <div class="magic-glow glow-bottom-right"></div>
  </section>
</template>
<script setup></script>

<style scoped>
.aboutus-section {
  position: relative;
  min-height: 100vh;
  padding: 5rem 1.5rem;
  color: #ffffff;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.aboutus-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border-radius: 20px;
  padding: 3rem;
  max-width: 800px;
  width: 100%;
  z-index: 10;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
}

.aboutus-title {
  font-size: 3rem;
  font-weight: bold;
  color: #d8b4fe;
  text-align: center;
  margin-bottom: 2rem;
  text-shadow: 0 0 8px #9333ea;
}

.aboutus-text {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #e9d8fd;
  margin-bottom: 1.5rem;
}

.highlight {
  color: #facc15;
  font-weight: 600;
}

.aboutus-link {
  color: #60a5fa;
  text-decoration: none;
  transition: color 0.3s ease;
}

.aboutus-link:hover {
  color: #3b82f6;
  text-decoration: underline;
}

.aboutus-button-container {
  text-align: center;
  margin-top: 2.5rem;
}

.aboutus-button {
  background: linear-gradient(to right, #6d28d9, #4338ca);
  color: white;
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 9999px;
  text-decoration: none;
  transition: transform 0.2s ease, background 0.3s ease;
  box-shadow: 0 4px 14px rgba(109, 40, 217, 0.4);
}

.aboutus-button:hover {
  transform: scale(1.05);
  background: linear-gradient(to right, #7c3aed, #4f46e5);
}

.magic-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 1;
  animation: pulse 6s infinite alternate;
}

.glow-top-left {
  top: 50px;
  left: 50px;
  width: 200px;
  height: 200px;
  background: rgba(168, 85, 247, 0.3);
}

.glow-bottom-right {
  bottom: 50px;
  right: 50px;
  width: 300px;
  height: 300px;
  background: rgba(99, 102, 241, 0.3);
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
</style>
