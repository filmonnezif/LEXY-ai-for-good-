<template>
    <div class="min-h-screen flex flex-col items-center justify-center bg-purple-50 dark:bg-gray-900 p-4 overflow-hidden relative">
      <!-- Animated Background Elements -->
    <div class="fixed inset-0 pointer-events-none">
      <!-- Top left circle -->
      <div class="absolute top-20 left-20 w-32 h-32 bg-purple-200/50 dark:bg-violet-600/30 rounded-full animate-float-slow"></div>
      <!-- Bottom left circle -->
      <div class="absolute bottom-10 left-40 w-10 h-10 bg-purple-300/50 dark:bg-violet-500/30 rounded-full animate-float" style="animation-delay: 1s"></div>
      <div class="absolute top-20 right-20 w-10 h-10 bg-purple-300/50 dark:bg-violet-500/30 rounded-full animate-float" style="animation-delay: 1s"></div>
      <div 
        class="absolute bottom-20 right-20 w-32 h-32 
        bg-purple-200/50 dark:bg-purple-800/30 
        rounded-full animate-float-slow"
      ></div>

    </div>

    <!-- Main Content -->
    <div class="relative">
  <!-- Avatar Container -->
  <div class="flex items-center space-x-4 mt-10">
    <Avatar class="h-70 w-60 bg-purple-50 dark:bg-gray-900" >
      <AvatarImage src='https://lexydata.blob.core.windows.net/summary/Lexy.png' alt="DyslexAI Logo" />
      <AvatarFallback> </AvatarFallback>
    </Avatar>
  </div>
  
  <!-- Floating Characters Container -->
  <div class="floating-characters absolute inset-0">
    <TransitionGroup 
      name="float" 
      tag="div" 
      class="absolute inset-0 pointer-events-none overflow-hidden"
    >
      <div
        v-for="char in floatingChars"
        :key="char.id"
        :style="{
          left: `${char.x}%`,
          color: char.color,
          transform: `translateY(${char.y}px)`,
          opacity: char.opacity,
          fontSize: '1rem'
        }"
        class="absolute text-2xl font-bold transition-all duration-300"
      >
        {{ char.value }}
      </div>
    </TransitionGroup>
  </div>
</div>
      <div class="relative z-10 container mx-auto px-4 -mt-[70px]">
        <div class="text-center space-y-8">
        <h1 class="text-4xl md:text-7xl font-bold tracking-[0.2em] md:tracking-[0.3em] text-purple-600 dark:text--100 transition-colors duration-300 flex justify-center">
          <template v-if="$i18n.locale === 'ar'">
            <span class="animate-slide-right">y</span>
            <span class="animate-slide-bottom">x</span>
            <span class="animate-slide-top">e</span>
            <span class="animate-slide-left">L</span>
          </template>
          <template v-else>
            <span class="animate-slide-left">L</span>
            <span class="animate-slide-top">e</span>
            <span class="animate-slide-bottom">x</span>
            <span class="animate-slide-right">y</span>
          </template>
        </h1>

        
        <p class="text-2xl tracking-[0.2em] text-gray-700 dark:text-gray-300 max-w-3xl mx-auto" style="word-spacing: 0.7em">
          {{ $t('hero.subtitle') }}
        </p>

        <Button 
          variant="outline" 
          size="lg" 
          class="mt-8 border-purple-400 dark:border-violet-500 hover:bg-purple-100 animate-bounce-slow"
          @click="$router.push('/calibrate')"
        >
          {{ $t('hero.tryDemo') }}
        </Button>   
      </div>
    </div>
    </div>
        
</template>


<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
  
const floatingChars = ref([])
let charId = 0
const colors = [
  '#9333EA', // Purple
  '#6366F1', // Indigo
  '#EC4899', // Pink
  '#8B5CF6', // Violet
  '#A855F7',  // Purple-500
  '#F59E0B', // Yellow
  '#F472B6', // Pink-500
  '#22D3EE', // Sky-500
  '#10B981', // Green-500
  '#3B82F6', // Blue-500
  '#F87171', // Red-500
]

const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

function createChar(side) {
  const x = side === 'left' ? 25 : 70
  return {
    id: charId++,
    value: characters[Math.floor(Math.random() * characters.length)],
    x: x,
    y: 150,
    opacity: 1,
    color: colors[Math.floor(Math.random() * colors.length)],
    // zigzag properties
    direction: Math.random() < 0.5 ? 'left' : 'right',
    zigzagAmount: Math.random() * 20 // zigzag width
  }
}

function animateChars() {
  floatingChars.value = floatingChars.value.filter(char => char.opacity > 0)
  
  floatingChars.value.forEach(char => {
    char.y -= 0.3 // slower upward movement
    char.opacity -= 0.0023 // Slower fade out
    
    //zigzag motion
    if (char.direction === 'left') {
      char.x -= Math.sin(char.y / 10) * 0.2
      if (char.x <= char.zigzagAmount) char.direction = 'right'
    } else {
      char.x += Math.sin(char.y / 10) * 0.2
      if (char.x >= 100 - char.zigzagAmount) char.direction = 'left'
    }
  })

  if (Math.random() < 0.05) {
    floatingChars.value.push(createChar(Math.random() < 0.5 ? 'left' : 'right'))
  }
}

let animationFrame
function animate() {
  animateChars()
  animationFrame = requestAnimationFrame(animate)
}

onMounted(() => {
  animate()
})

onUnmounted(() => {
  cancelAnimationFrame(animationFrame)
})
</script>


<style scoped>
.float-enter-active,
.float-leave-active {
  transition: all 0.5s ease;
}

.float-enter-from,
.float-leave-to {
  opacity: 0;
  transform: translateY(20px);
}



.floating-characters {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}


@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes float-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes slide-in {
  from { 
    opacity: 0; 
    transform: translateY(20px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

@keyframes fade-in {
  from { 
    opacity: 0; 
  }
  to { 
    opacity: 1; 
  }
}

@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}

.animate-float-slow {
  animation: float-slow 5s ease-in-out infinite;
}

.animate-slide-in {
  animation: slide-in 1s ease-out;
}

.animate-fade-in {
  animation: fade-in 1.5s ease-out;
}

.animate-bounce-slow {
  animation: bounce-slow 2s ease-in-out infinite;
}
@keyframes slide-left {
  from { 
    opacity: 0;
    transform: translateX(-100px);
  }
  to { 
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slide-top {
  from { 
    opacity: 0;
    transform: translateY(-100px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-bottom {
  from { 
    opacity: 0;
    transform: translateY(100px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-right {
  from { 
    opacity: 0;
    transform: translateX(100px);
  }
  to { 
    opacity: 1;
    transform: translateX(0);
  }
}

.animate-slide-left {
  animation: slide-left 1s ease-out forwards;
  animation-delay: 0.3s;
  opacity: 0;
}

.animate-slide-top {
  animation: slide-top 1s ease-out forwards;
  animation-delay: 0.6s;
  opacity: 0;
}

.animate-slide-top-fast {
  animation: slide-top 1s ease-out forwards;
  animation-delay: 2s;
  opacity: 0;
}

.animate-slide-bottom {
  animation: slide-bottom 1s ease-out forwards;
  animation-delay: 0.9s;
  opacity: 0;
  
}

.animate-slide-right {
  animation: slide-right 1s ease-out forwards;
  animation-delay: 1.2s;
  opacity: 0;
}
@keyframes slide-left {
  from { 
    opacity: 0;
    transform: translateX(-1000px);
  }
  to { 
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slide-top {
  from { 
    opacity: 0;
    transform: translateY(-800px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-bottom {
  from { 
    opacity: 0;
    transform: translateY(800px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-right {
  from { 
    opacity: 0;
    transform: translateX(1000px);
  }
  to { 
    opacity: 1;
    transform: translateX(0);
  }
}
@media (max-width: 768px) {
  @keyframes slide-left {
    from { 
      opacity: 0;
      transform: translateX(-50px);
    }
    to { 
      opacity: 1;
      transform: translateX(0);
    }
  }

  @keyframes slide-top {
    from { 
      opacity: 0;
      transform: translateY(-50px);
    }
    to { 
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes slide-bottom {
    from { 
      opacity: 0;
      transform: translateY(50px);
    }
    to { 
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes slide-right {
    from { 
      opacity: 0;
      transform: translateX(50px);
    }
    to { 
      opacity: 1;
      transform: translateX(0);
    }
  }

  .animate-slide-left,
  .animate-slide-top,
  .animate-slide-bottom,
  .animate-slide-right {
    animation-duration: 0.8s;
  }
}
</style>