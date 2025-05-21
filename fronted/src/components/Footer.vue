<template>
  <footer class="footer" role="contentinfo" aria-labelledby="footer-heading">
    <div class="footer-container">
      <h2 id="footer-heading" class="sr-only">{{ $t("footer.accessibleTitle") }}</h2>

      <nav class="footer-section" aria-labelledby="footer-quicklinks-title">
        <h3 id="footer-quicklinks-title" class="footer-title">
          {{ $t("quickLinks") }}
        </h3>
        <ul class="footer-list">
          <li v-for="link in quickLinks" :key="link.name">
            <RouterLink :to="link.to" class="footer-link">{{ $t(link.name) }}</RouterLink>
          </li>
        </ul>
      </nav>

      <section class="footer-section" aria-labelledby="footer-social-title">
        <h3 id="footer-social-title" class="footer-title">
          {{ $t("followUs") }}
        </h3>
        <ul class="social-list">
          <li v-for="social in socialLinks" :key="social.label">
            <a
              :href="social.href"
              class="social-link"
              target="_blank"
              rel="noopener noreferrer"
              :aria-label="social.ariaLabel"
            >
              <i :class="social.iconClass" aria-hidden="true"></i>
            </a>
          </li>
        </ul>
      </section>

      <address class="footer-section" aria-labelledby="footer-contact-title" role="region">
        <h3 id="footer-contact-title" class="footer-title">
          {{ $t("contact") }}
        </h3>
        <dl class="contact-list">
          <div>
            <dt class="contact-term">
              <i class="fas fa-envelope" aria-hidden="true"></i>
              <span class="sr-only">{{ $t("email") }}:</span>
            </dt>
            <dd class="contact-detail">cardshop2204@gmail.com</dd>
          </div>
          <div>
            <dt class="contact-term">
              <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
              <span class="sr-only">{{ $t("address") }}:</span>
            </dt>
            <dd class="contact-detail">Calle Magic, 123, Planeswalker City</dd>
          </div>
        </dl>
      </address>
    </div>

    <div class="footer-bottom">
      <p class="footer-text">
        © {{ new Date().getFullYear() }} CardShop –
        {{ $t("allRightsReserved") }}
      </p>
    </div>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

export default defineComponent({
  name: "AppFooter",
  setup() {
    const { locale } = useI18n();
    const quickLinks = [
      { name: "home", to: `/${locale.value}/` },
      { name: "mainproducts", to: `/${locale.value}/cards` },
      { name: "aboutUs", to: `/${locale.value}/aboutus` },
    ];
    const socialLinks = [
      {
        href: "https://facebook.com",
        iconClass: "bi bi-facebook",
        ariaLabel: "Facebook (nueva pestaña)",
      },
      {
        href: "https://twitter.com",
        iconClass: "bi bi-twitter",
        ariaLabel: "Twitter (nueva pestaña)",
      },
      {
        href: "https://instagram.com",
        iconClass: "bi bi-instagram",
        ariaLabel: "Instagram (nueva pestaña)",
      },
      {
        href: "https://discord.com",
        iconClass: "bi bi-discord",
        ariaLabel: "Discord (nueva pestaña)",
      },
    ];
    return { quickLinks, socialLinks };
  },
});
</script>

<style scoped>
.sr-only {
  position: absolute !important;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.footer {
  background-color: #1e1b4b;
  color: #e9d8fd;
  padding: 2rem 1rem;
  border-top: 0.5rem solid #facc15;
  font-family: "Garamond", serif;
}
.footer-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
}

.footer-title {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #facc15;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.footer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-link {
  display: block;
  margin-bottom: 0.5rem;
  color: inherit;
  text-decoration: none;
  font-size: 1rem;
  transition: transform 0.2s ease, color 0.2s ease;
}
.footer-link:hover,
.footer-link:focus {
  color: #facc15;
  transform: translateX(0.25rem);
}
.footer-link:focus-visible {
  outline: 2px dashed #facc15;
  outline-offset: 4px;
}

.social-list {
  display: flex;
  gap: 1rem;
  padding: 0;
  margin: 0;
  list-style: none;
}
.social-link {
  font-size: 1.5rem;
  color: inherit;
  display: inline-block;
  transition: transform 0.2s ease, color 0.2s ease;
}
.social-link:hover,
.social-link:focus {
  color: #facc15;
  transform: scale(1.1);
}
.social-link:focus-visible {
  outline: 2px dashed #facc15;
}

.contact-list {
  margin: 0;
  padding: 0;
}
.contact-term,
.contact-detail {
  display: inline-block;
}

.contact-detail {
  font-size: 1rem;
  margin-left: 0.5rem;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 1rem;
  margin-top: 2rem;
  text-align: center;
}
.footer-text {
  font-size: 0.875rem;
  opacity: 0.7;
}

@media (max-width: 400px) {
  .footer-title {
    font-size: 1rem;
  }
  .social-list {
    justify-content: center;
  }
}
</style>
