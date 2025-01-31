// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', 'shadcn-nuxt', '@nuxt/fonts','@nuxtjs/color-mode','@nuxtjs/i18n'],
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  },
  fonts: {
    families: [
      { name: 'OpenDyslexic', src: 'https://lexydata.blob.core.windows.net/summary/OpenDyslexic-Regular.woff', weight: 'normal' },
      { name: 'OpenDyslexic', src: 'https://lexydata.blob.core.windows.net/summary/OpenDyslexic-Bold.woff', weight: 'bold'  },
    ]
  },

  i18n: {
    locales: [
      { code: 'en', dir: 'ltr', name: 'English' },
      { code: 'ar', dir: 'rtl', name: 'العربية' }
    ],
    defaultLocale: 'en',
    strategy: 'prefix',
    vueI18n: './i18n.config.ts'
  },
  css: ['~/assets/css/fonts.css'],

  runtimeConfig: {
    ClientSecret: process.env.ClientSecret,
    Subdomain: process.env.Subdomain,
    ClientId: process.env.ClientId,
    TenantId: process.env.TenantId
  }
,
  
})