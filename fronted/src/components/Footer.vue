<template>
  <div class="footer">
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <h5 class="footer-title">{{ $t('quickLinks') }}</h5>
          <ul class="list-unstyled">
            <li><RouterLink :to="`/${$i18n.locale}/`" class="footer-link">{{ $t('home') }}</RouterLink></li>
            <li><RouterLink :to="`/${$i18n.locale}/cards`" class="footer-link">{{ $t('products') }}</RouterLink></li>
            <li><RouterLink :to="`/${$i18n.locale}/aboutus`" class="footer-link">{{ $t('aboutUs') }}</RouterLink></li>
            <li><RouterLink :to="`/${$i18n.locale}/contact`" class="footer-link">{{ $t('contact') }}</RouterLink></li>
          </ul>
        </div>

        <div class="col-md-4">
          <h5 class="footer-title">{{ $t('followUs') }}</h5>
          <div class="social-icons">
            <a href="https://facebook.com" target="_blank" class="social-link">
              <i class="bi bi-facebook"></i>
            </a>
            <a href="https://twitter.com" target="_blank" class="social-link">
              <i class="bi bi-twitter"></i>
            </a>
            <a href="https://instagram.com" target="_blank" class="social-link">
              <i class="bi bi-instagram"></i>
            </a>
            <a href="https://discord.com" target="_blank" class="social-link">
              <i class="bi bi-discord"></i>
            </a>
          </div>
        </div>

        <div class="col-md-4">
          <h5 class="footer-title">{{ $t('contact') }}</h5>
          <p><i class="fas fa-envelope"></i> cardshop@gmail.com</p>
          <p><i class="fas fa-map-marker-alt"></i> Calle Magic, 123, Planeswalker City</p>
        </div>
      </div>

      <hr class="footer-divider">

      <div class="text-center">
        <p class="footer-text">© {{ new Date().getFullYear() }} CardShop - {{ $t('allRightsReserved') }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';

export default defineComponent({
    setup() {
        const { t, locale } = useI18n();

        return {
            t
        };
    }
});
</script>

<style scoped>
.footer {
  background-color: #1e1b4b; /* Fondo oscuro */
  color: #e9d8fd;  /* Color suave de texto */
  padding: 50px 0;
  border-top: 5px solid #facc15; /* Amarillo brillante */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  font-family: 'Garamond', serif;
}

.footer-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
  font-weight: bold;
  color: #facc15; /* Amarillo brillante */
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.footer-link {
  color: #e9d8fd; /* Color suave de texto */
  text-decoration: none;
  font-size: 1.1rem;
  margin-bottom: 12px;
  display: block;
  transition: color 0.3s ease, transform 0.3s ease;
}

.footer-link:hover {
  color: #facc15; /* Amarillo brillante al pasar el ratón */
  transform: translateX(5px);
}

.social-icons {
  display: flex;
  gap: 20px;
}

.social-link {
  color: #e9d8fd; /* Color suave de texto */
  font-size: 1.6rem;
  transition: color 0.3s ease, transform 0.3s ease;
}

.social-link:hover {
  color: #facc15; /* Amarillo brillante al pasar el ratón */
  transform: scale(1.1);
}

.footer-divider {
  border-color: rgba(255, 255, 255, 0.2);
  margin: 30px 0;
}

.footer-text {
  font-size: 1rem;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .footer {
    padding: 30px 15px;
  }

  .footer-title {
    font-size: 1.3rem;
  }

  .footer-link {
    font-size: 1rem;
  }

  .social-link {
    font-size: 1.5rem;
  }
}
</style>


<!-- <style scoped>
.footer {
  background-color: #3e2723;
  color: #f1e0c6; 
  padding: 50px 0;
  border-top: 5px solid #f39c12;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  font-family: 'Garamond', serif;
}

.footer-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
  font-weight: bold;
  color: #f39c12; 
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.footer-link {
  color: #f1e0c6;
  text-decoration: none;
  font-size: 1.1rem;
  margin-bottom: 12px;
  display: block;
  transition: color 0.3s ease, transform 0.3s ease;
}

.footer-link:hover {
  color: #f39c12; /* Dorado al pasar el ratón */
  transform: translateX(5px);
}

.social-icons {
  display: flex;
  gap: 20px;
}

.social-link {
  color: #f1e0c6;
  font-size: 1.6rem;
  transition: color 0.3s ease, transform 0.3s ease;
}

.social-link:hover {
  color: #f39c12; 
  transform: scale(1.1);
}

.footer-divider {
  border-color: rgba(255, 255, 255, 0.2);
  margin: 30px 0;
}

.footer-text {
  font-size: 1rem;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .footer {
    padding: 30px 15px;
  }

  .footer-title {
    font-size: 1.3rem;
  }

  .footer-link {
    font-size: 1rem;
  }

  .social-link {
    font-size: 1.5rem;
  }
}
</style> -->
