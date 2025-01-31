
<template>
  <div :dir="$i18n.locale === 'ar' ? 'rtl' : 'ltr'" class="min-h-screen hide-scrollbar">
    <header class="w-full px-6 py-4 border-b flex items-center justify-between sticky top-0 z-40 bg-purple-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300">
      <div class="flex items-center space-x-4">
        <Avatar class="h-15 w-10 bg-purple-50 dark:bg-gray-900 animate-float-slow rounded-none">
          <AvatarImage src="https://lexydata.blob.core.windows.net/summary/Lexycrop.png" alt="DyslexAI Logo" />
          <AvatarFallback>LY</AvatarFallback>
        </Avatar>
        <span class="text-xl font-bold">Lexy</span>
      </div>

      <div class="flex items-center space-x-6">
        <Select v-model="$i18n.locale" class="relative bg-purple-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300">
          <SelectTrigger>
            <SelectValue placeholder="Select Language" />
          </SelectTrigger>
          <SelectContent class="text-sm font-medium text-gray-700 dark:text-gray-300 bg-purple-50 dark:bg-gray-900">
            <SelectItem 
              v-for="locale in $i18n.locales" 
              :key="locale.code" 
              :value="locale.code"
            >
              {{ locale.name }}
            </SelectItem>
          </SelectContent>
        </Select>


        <Button variant="ghost" size="icon" @click="toggleTheme">
          <SunIcon v-if="colorMode.value === 'dark'" class="h-5 w-5" />
          <MoonIcon v-else class="h-5 w-5" />
        </Button>
      </div>
    </header>
    <NuxtPage class="min-h-[calc(100vh-header-height)]" />
  </div>
</template>
<script setup>
import { useColorMode } from '#imports'
import { SunIcon, MoonIcon } from '@radix-icons/vue'

const colorMode = useColorMode()

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
}
</script>


<style scoped>
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

:root {
  --header-height: 72px; 
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes float-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-float {
  animation: float 4s ease-in-out infinite;
}

.animate-float-slow {
  animation: float-slow 5s ease-in-out infinite;
}


@media screen and (max-width: 768px) {
  html, body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    width: 100vw;
    height: 100vh;
    position: fixed;
  }
}
</style>
