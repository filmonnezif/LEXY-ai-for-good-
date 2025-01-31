<template>
<div class="flex items-center space-x-4">
    <Button
    @click="togglePlay"
    variant="outline"
    size="icon"
    class="w-8 h-8 text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300"
    >
    <PlayIcon v-if="!isPlaying" class="h-4 w-4" />
    <PauseIcon v-else class="h-4 w-4" />
    </Button>
    
    <div class="flex-1 flex items-center space-x-2">
    <span class="text-sm">{{ formatTime(currentTime) }}</span>
    <input
        type="range"
        min="0"
        :max="duration"
        :value="currentTime"
        @input="seek"
        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
    />
    <span class="text-sm">{{ formatTime(duration) }}</span>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Howl } from 'howler'
import { PlayIcon, PauseIcon } from '@heroicons/vue/24/solid'

const isPlaying = ref(false)
const volume = ref(100)
const sound = ref(null)
const currentTime = ref(0)
const duration = ref(0)

const props = defineProps({
src: {
    type: String,
    required: true
}
})

onMounted(() => {
sound.value = new Howl({
    src: [props.src],
    volume: volume.value / 100,
    onend: () => {
    isPlaying.value = false
    currentTime.value = 0
    },
    onload: () => {
    duration.value = sound.value.duration()
    },
    onplay: () => {
    requestAnimationFrame(updateProgress)
    }
})
})

const updateProgress = () => {
if (sound.value && isPlaying.value) {
    currentTime.value = sound.value.seek()
    requestAnimationFrame(updateProgress)
}
}

const seek = (event) => {
const seekTime = parseFloat(event.target.value)
if (sound.value) {
    sound.value.seek(seekTime)
    currentTime.value = seekTime
}
}

const formatTime = (seconds) => {
const minutes = Math.floor(seconds / 60)
const remainingSeconds = Math.floor(seconds % 60)
return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

const togglePlay = () => {
if (!sound.value) return

if (isPlaying.value) {
    sound.value.pause()
} else {
    sound.value.play()
}
isPlaying.value = !isPlaying.value
}

onUnmounted(() => {
if (sound.value) {
    sound.value.unload()
}
})
</script>

<style scoped>
input[type="range"] {
accent-color: #9333ea;
}
</style>
  