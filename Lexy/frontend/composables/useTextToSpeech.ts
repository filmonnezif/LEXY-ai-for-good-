import { ref } from 'vue'

export function useTextToSpeech() {
  const speaking = ref(false)
  const speechSynthesis = typeof window !== 'undefined' ? window.speechSynthesis : null
  
  const speak = (text: string) => {
    if (!speechSynthesis || speaking.value) return
    
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = 0.9
    utterance.pitch = 1
    
    utterance.onstart = () => {
      speaking.value = true
    }
    
    utterance.onend = () => {
      speaking.value = false
    }
    
    speechSynthesis.speak(utterance)
  }
  
  const stop = () => {
    if (speechSynthesis) {
      speechSynthesis.cancel()
      speaking.value = false
    }
  }
  
  return {
    speak,
    stop,
    speaking
  }
}
