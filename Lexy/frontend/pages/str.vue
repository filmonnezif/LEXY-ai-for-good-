<template>
  <div class="flex min-h-screen bg-purple-50 dark:bg-gray-900 gap-2">
    <!-- Left Sheet for mobile -->
    <Sheet :open="leftSheetOpen" @update:open="leftSheetOpen = $event">
      <SheetContent side="left" class="w-80 p-4 bg-purple-50 dark:bg-gray-900 dark:text-gray-300 ">
        <SheetHeader>
          <SheetTitle>Story time</SheetTitle>
        </SheetHeader>
      </SheetContent>
    </Sheet>
    <!-- Right Sheet for mobile -->
    <Drawer :open="rightSheetOpen" @update:open="rightSheetOpen = $event">
      <DrawerContent class = 'p-4 bg-purple-50 dark:bg-gray-900 dark:text-gray-300 '>
        <DrawerHeader>
          <DrawerTitle>Reading Tools</DrawerTitle>
        </DrawerHeader>
        <Accordion type="single" collapsible>
          <AccordionItem value="text-customization">
              <AccordionTrigger>
              <h3 class="text-gray-700 dark:text-gray-300">Customize text</h3>
              </AccordionTrigger>
              <AccordionContent>
              <div class="space-y-6">
                  <div>
                  <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Font Size</label>
                  <Slider
                      v-model="fontSizeArray"
                      :min="12"
                      :max="32"
                      :step="1"
                      class="w-full [&_.relative_.bg-primary]:bg-purple-600 [&_.relative_.border-primary]:border-purple-600"
                  />
                  <span class="text-sm text-gray-700 dark:text-gray-300">{{fontSize}}px</span>
                  </div>

                  <div>
                  <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Line Height</label>
                  <Slider
                      v-model="lineHeightArray"
                      :min="1.5"
                      :max="3"
                      :step="0.1"
                      class="w-full [&_.relative_.bg-primary]:bg-purple-600 [&_.relative_.border-primary]:border-purple-600"
                  />
                  <span class="text-sm text-gray-700 dark:text-gray-300">{{lineHeight}}</span>
                  </div>

                  <div>
                  <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Word Spacing</label>
                  <Slider
                      v-model="wordSpacingArray"
                      :min="0"
                      :max="20"
                      :step="1"
                      class="w-full [&_.relative_.bg-primary]:bg-purple-600 [&_.relative_.border-primary]:border-purple-600"
                  />
                  <span class="text-sm text-gray-700 dark:text-gray-300">{{wordSpacing}}px</span>
                  </div>

                  <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Font Type</label>
                  <Select v-model="selectedFont">
                      <SelectTrigger class="border-purple-200 dark:border-purple-800 text-gray-700 dark:text-gray-300">
                      <SelectValue placeholder="Select a font" />
                      </SelectTrigger>
                      <SelectContent class="text-sm bg-purple-50 dark:bg-gray-900 font-medium text-gray-700 dark:text-gray-300">
                      <SelectItem value="OpenDyslexic">OpenDyslexic</SelectItem>
                      <SelectItem value="Comic Sans MS">Comic Sans</SelectItem>
                      <SelectItem value="Arial">Arial</SelectItem>
                      </SelectContent>
                  </Select>
                  </div>
              </div>
              </AccordionContent>
          </AccordionItem>
          </Accordion>
          <div class="flex items-center justify-between mt-4">
          <Label class="text-md font-semibold text-gray-700 dark:text-gray-300">Focus Mode</Label>
          <Switch
              :checked="focusMode"
              @update:checked="focusMode = $event"
              class="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-gray-500 dark:data-[state=unchecked]:bg-gray-700"
          />
          </div>    
          <div class="flex items-center justify-between mt-4">
          <Label class="text-md font-semibold text-gray-700 dark:text-gray-300">Highlighter</Label>
          <Switch
              :checked="highlight"
              @update:checked="highlight = $event"
              class="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-gray-500 dark:data-[state=unchecked]:bg-gray-700"
          />
          </div>
          <div class="flex items-center justify-between mt-4 mb-4">
          <Label class="text-md font-semibold text-gray-700 dark:text-gray-300">Read Along</Label>
          <Switch
              :checked="readAlong"
              @update:checked="readAlong = $event"
              class="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-gray-500 dark:data-[state=unchecked]:bg-gray-700"
          />
          </div>
      </DrawerContent>
    </Drawer>
    <!-- Left Sidebar-->
    <div class="hidden md:block w-72 shadow-md dark:shadow-gray-400/30 p-4">
      

      <!-- Audio Tools Section -->
      <div class="space-y-4">
  <Card class="bg-purple-50/50 dark:bg-gray-800/50 p-6">
    <div class="flex flex-col items-center space-y-6">
      <!-- Logo with Status -->
      <div class="relative">
        <img 
          src="https://lexydata.blob.core.windows.net/summary/Lexy.png" 
          alt="Lexy" 
          :class="[
            'w-20 h-20 rounded-full ring-4 ring-purple-400 dark:ring-purple-600 p-1',
            isSpeaking && 'animate-border'
          ]"
        />
        <div class="absolute -top-2 -mt-2 -right-6 -mr-6">
          <Badge variant="outline" class="bg-white dark:bg-gray-800">
            <div class="flex items-center gap-2">
              <div 
                class="animate-pulse h-2 w-2 rounded-full" 
                :class="isListening ? 'bg-green-500' : isSpeaking ? 'bg-blue-500' : isProcessingRequest ? 'bg-yellow-500' : 'bg-gray-500'">
              </div>
              <span class="text-xs">
                {{ isProcessingRequest ? 'Thinking🤔' 
                   : isSpeaking ? 'Speaking🗣️' 
                   : isListening ? 'Listening👂' 
                   : 'Hey👋' }}
              </span>
            </div>
          </Badge>
        </div>
      </div>


      <!-- Dynamic Message -->
      <p class="text-center text-gray-700 dark:text-gray-300 font-medium">
        {{ chatHistory.length > 0 ? chatHistory[chatHistory.length - 1].text : 'Ask Lexy anything about your document' }}
      </p>

      <!-- Action Button -->
      <Button 
        @click="isVoiceChatActive ? stopVoiceChat() : startVoiceChat()" 
        :class="isVoiceChatActive ? 'bg-red-600 hover:bg-red-700' : 'bg-purple-600 hover:bg-purple-700'"
        class="w-48 text-white transition-all duration-300 transform hover:scale-105"
      >
        <div class="flex items-center justify-center gap-2">
          <MicrophoneIcon v-if="!isVoiceChatActive" class="h-4 w-4" />
          <StopIcon v-else class="h-4 w-4" />
          <span>{{ isVoiceChatActive ? 'Stop Chatting' : 'Talk to Lexy' }}</span>
        </div>
      </Button>
    </div>
  </Card>
</div>

<Separator class="my-8" />

      <!-- Reading Assessment Section -->
<div class="space-y-4">
  <div class="flex items-center gap-2">
    <img 
      src='https://lexydata.blob.core.windows.net/summary/Lexy.png' 
      alt="Lexy" 
      class="w-8 h-8 rounded-full ring-2 ring-purple-200 dark:ring-purple-800"
    />
    <Label class="text-lg font-semibold text-gray-700 dark:text-gray-300">Lexy's Reading Test</Label>
  </div>
  
  <!-- No Assessment State -->
  <div v-if="!hasAssessmentResults" class="bg-purple-50 dark:bg-gray-800 rounded-lg p-2 text-center">
    <BookOpenIcon class="h-12 w-12 mx-auto text-purple-600 dark:text-purple-400" />
    <div>
      <h3 class="font-medium text-gray-700 dark:text-gray-300">Test Your Reading with Lexy</h3>
      <p class="text-sm text-gray-500 dark:text-gray-400">Let's identify areas for improvement</p>
    </div>
  </div>

  <!-- Assessment Controls -->
  <Card class="bg-purple-50/50 dark:bg-gray-800/50 p-2">
    <div class="space-y-0">
      <div class="space-y-2 flex items-center justify-between p-2 mx-auto">
      <!-- Start Button -->
      <Button 
        v-if="!isRecording && !isPaused"
        @click="handlePlayPause" 
        variant="outline"
        class="w-auto border-purple-400 hover:border-purple-600 dark:border-purple-600 dark:hover:border-purple-400 bg-purple-50 dark:bg-gray-800 text-purple-600 dark:text-purple-400 mx-auto"
      >
        <PlayIcon class="w-4 h-4" v-if="!isProcessing" />
        <Loader2Icon v-if="isProcessing" class="w-4 h-4 animate-spin" />
      </Button>

      <!-- Recording State -->
      <div v-if="isRecording && !isPaused" class="flex items-center gap-2 mx-auto">
        <Button 
          @click="pauseRecording"
          variant="outline"
          class="border-purple-400 hover:border-purple-600 dark:border-purple-600 bg-purple-50 dark:bg-gray-800 text-purple-600 dark:text-purple-400 mx-auto"
        >
          <PauseIcon class="w-4 h-4" />
        </Button>
        <Badge variant="destructive" class="animate-pulse">
          <MicrophoneIcon class="w-4 h-4" />
        </Badge>
      </div>

      <!-- Paused State -->
      <div v-if="isPaused" class="flex gap-2 mx-auto">
        <Button 
          @click="resumeRecording"
          variant="outline"
          class="border-purple-400 hover:border-purple-600 dark:border-purple-600 bg-purple-50 dark:bg-gray-800 text-purple-600 dark:text-purple-400 mx-auto"
        >
          <PlayIcon class="w-4 h-4" />
        </Button>
        <Button 
          @click="assessCurrentProgress"
          variant="outline"
          class="border-green-400 hover:border-green-600 dark:border-green-600 bg-green-50 dark:bg-gray-800 text-green-600 dark:text-green-400 mx-auto"
        >
          <CheckIcon class="w-4 h-4" />
          Done
        </Button>
        <Button 
          @click="retryChunk"
          variant="outline"
          class="border-gray-400 hover:border-gray-600 dark:border-gray-600 bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 mx-auto"
        >
          <ReloadIcon class="w-4 h-4" />
        </Button>
      </div>
    </div>
    <Separator class="my-2" />

      <!-- Processing State -->
      <div v-if="isProcessing" class="text-center space-y-4">
        <p class="text-sm text-gray-600 dark:text-gray-400">Analyzing your reading...</p>
      </div>

      <!-- Results Display -->
      <div v-if="recentWpm && !isProcessing" class="space-y-6">
        <div class="flex justify-between items-center">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Reading Speed</span>
          <div class="flex items-center gap-2">
            <TrendingUpIcon class="h-4 w-4 text-green-500" v-if="isImproving" />
            <span class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{recentWpm}} WPM</span>
          </div>
        </div>
        
        <div v-if="recentErrors.length" class="space-y-3">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Words to Practice</span>
          <div class="flex flex-wrap gap-2">
            <div v-for="error in recentErrors" :key="error">
              <Badge variant="outline" class="text-sm cursor-pointer hover:bg-purple-500 hover:text-white bg-purple-100 dark:bg-gray-800 dark:text-purple-400">
                {{error}}
              </Badge>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Card>
</div>

    </div>

    
    <!-- Main content-->
    <div class="flex-1 px-0 overflow-hidden">
      <div class="max-w-4xl mx-auto relative h-full h-screen overflow-y-auto px-2">
        <div class="absolute top-20 right-10 z-10 flex gap-2">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger as-child>
                <Button 
                  v-if ="!isOriginalView"
                  @click="toggleView" 
                  class="group relative px-4 py-2 rounded-lg bg-white dark:bg-gray-800 border border-purple-200 dark:border-purple-800 text-purple-600 dark:text-purple-400 shadow-sm hover:bg-purple-50 dark:hover:bg-gray-700"
                >
                  <span class="relative z-10 flex items-center gap-2 text-sm font-medium">
                    <ArrowPathIcon class="h-4 w-4" />
                    <span>Original</span>
                  </span>
                </Button>
              </TooltipTrigger>
              <TooltipContent side="top">
                <p>Switch between original and remixed version</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger as-child>
                <Button 
                  @click="remixText" 
                  class="group relative px-4 py-2 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white shadow-lg"
                  :disabled="isRemixing || !isOriginalView"
                >
                  <template v-if="isRemixing">
                    <span class="animate-spin mr-2">⭮</span> 
                    <span class="relative z-10">Transforming...</span>
                  </template>
                  <template v-else>
                    <span class="relative z-10 flex items-center gap-2">
                      <SparklesIcon class="h-4 w-4" />
                      <span>Remix</span>
                    </span>
                  </template>
                </Button>
              </TooltipTrigger>
              <TooltipContent side="top">
                <p>Create a simplified version optimized for you.</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
        <div class="absolute top-20 left-10 z-10 flex gap-2">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger as-child>
                <Button 
                  @click="toggleTranslation" 
                  class="group relative px-4 py-2 rounded-lg bg-white dark:bg-gray-800 border border-purple-200 dark:border-purple-800 text-purple-600 dark:text-purple-400 shadow-sm hover:bg-purple-50 dark:hover:bg-gray-700"
                >
                  <span class="relative z-10 flex items-center gap-2 text-sm font-medium">
                    <LanguageIcon class="h-4 w-4" />
                    <span>{{ isArabic ? 'English' : 'عربي' }}</span>
                  </span>
                </Button>
              </TooltipTrigger>
              <TooltipContent side="top">
                <p>Toggle between English and Arabic</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
        <h1 class="text-l font-bold text-gray-700 dark:text-gray-100 mb-8 md:text-xl">
          {{ title.length > 40 
              ? title.substring(0, 20) + '...' + title.substring(title.length - 10) 
              : title 
            }}
        </h1>
        <div class="bg-gray-50 dark:bg-gray-800 p-6 shadow-sm pt-16 text-gray-700 dark:text-gray-300 relative min-h-[calc(100vh-12rem)]">
          <div class="md:hidden fixed bottom-4 left-4 right-4 flex justify-between z-50">
            <Button variant="outline" @click="leftSheetOpen = true"
            class="w-100 text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300 dark:bg-gray-800 dark:hover:bg-gray-900 border-purple-300 dark:border-purple-700 px-4"
            >
              <MegaphoneIcon class="h-4 w-4" />
            </Button>
            <Button variant="outline" @click="rightSheetOpen = true"
            class="w-100 text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300 dark:bg-gray-800 dark:hover:bg-gray-900 border-purple-300 dark:border-purple-700 px-4"
            >
              <Pencil2Icon class="h-4 w-4" />
            </Button>
          </div>
          <div id="essay-content" 
              :class="['prose dark:prose-invert', fontClass]"
              v-html="displayContent"
              :style="{
                  cursor: 'pointer',
                  '--base-font-size': `${fontSize}px`,
                  '--heading-font-size': `${fontSize * 1.3}px`,
                  fontSize: 'var(--base-font-size)',
                  lineHeight: lineHeight,
                  letterSpacing: `${letterSpacing}px`,
                  wordSpacing: `${wordSpacing}px`
              }">
              
          </div>
            <div v-if="showCountdown" class="absolute inset-0 bg-black/50 flex items-center justify-center">
            <span class="absolute top-20 text-center text-6xl text-white font-bold">{{ countdown }}</span>
            </div>
            <div v-if="showRemixOverlay" class="absolute inset-0 bg-black/70 flex items-center justify-center">
            <div class="text-center absolute top-20 space-x-auto">
              <div class="flex justify-center">
                <DotLottieVue
                src="https://lottie.host/6c4907b2-9639-4793-a854-2ca01b6605ae/t6I34zQoqp.lottie"
                autoplay
                loop
                style="width: 300px; height: 300px"
              />
              </div>
              <span class="text-4xl text-white font-bold animate-pulse">{{ remixMessage }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div 
      v-if="focusMode" 
      class="focus-overlay"
      @mousemove="updateFocusWindow"
    ><div class="overlay-section top" 
      :style="{
        height: `${focusPosition}px`
      }"
    >
      </div>
        <!-- Left overlay -->
        <div class="hidden md:block overlay-section left" 
          :style="{
            top: `${focusPosition}px`,
            height: `${lineHeight * fontSize * 1.2}px`,
            width: '22%'
          }"
        ></div>
        
        <!-- Right overlay -->
        <div class="hidden md:block overlay-section right" 
          :style="{
            top: `${focusPosition}px`,
            height: `${lineHeight * fontSize * 1.2}px`,
            left: '78%',
          }"
        ></div>
      <button 
        class="exit-focus-button bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 focus:outline-none focus:ring focus:ring-purple-300"
        @click="focusMode = false"
      >
        ✕
      </button>
      <div 
        class="focus-window"
        :style="{
          top: `${focusPosition}px`,
          height: `${lineHeight * fontSize * 1.2}px`
        }"
      ></div>
    </div>

    <!-- Right Sidebar with Controls -->
    <div class="hidden md:block w-72 shadow-md dark:shadow-gray-400/30 p-4 space-y-6">
      <!-- Text Customization Section -->
      <Accordion type="single" defaultValue="text-customization" collapsible>
        <AccordionItem value="text-customization">
          <AccordionTrigger>
            <div class="flex items-center gap-2">
              <CursorTextIcon class="h-4 w-4 text-purple-600 dark:text-purple-400" />
              <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">Text Settings</h3>
            </div>
          </AccordionTrigger>
          <AccordionContent>
            <div class="space-y-6 pt-2">
              <div>
                <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Font Size</label>
                <Slider
                  v-model="fontSizeArray"
                  :min="12"
                  :max="32"
                  :step="1"
                  class="w-full [&_.relative_.bg-primary]:bg-purple-600 [&_.relative_.border-primary]:border-purple-600"
                />
                <span class="text-sm text-gray-700 dark:text-gray-300">{{fontSize}}px</span>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Line Height</label>
                <Slider
                  v-model="lineHeightArray"
                  :min="1.5"
                  :max="3"
                  :step="0.1"
                  class="w-full [&_.relative_.bg-primary]:bg-purple-600 [&_.relative_.border-primary]:border-purple-600"
                />
                <span class="text-sm text-gray-700 dark:text-gray-300">{{lineHeight}}</span>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Word Spacing</label>
                <Slider
                  v-model="wordSpacingArray"
                  :min="0"
                  :max="20"
                  :step="1"
                  class="w-full [&_.relative_.bg-primary]:bg-purple-600 [&_.relative_.border-primary]:border-purple-600"
                />
                <span class="text-sm text-gray-700 dark:text-gray-300">{{wordSpacing}}px</span>
              </div>

              <div class="space-y-2">
                <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Font Type</label>
                <Select v-model="selectedFont">
                  <SelectTrigger class="w-full border-purple-200 dark:border-purple-800 text-gray-700 dark:text-gray-300">
                    <SelectValue placeholder="Select a font" />
                  </SelectTrigger>
                  <SelectContent class="text-sm bg-purple-50 dark:bg-gray-900 font-medium text-gray-700 dark:text-gray-300">
                    <SelectItem value="OpenDyslexic">OpenDyslexic</SelectItem>
                    <SelectItem value="Comic Sans MS">Comic Sans</SelectItem>
                    <SelectItem value="Arial">Arial</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>      
      <!-- Reading Helpers Section -->
      <div class="space-y-6">
        <div class="flex items-center gap-2">
          <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">Reading Helpers</h3>
        </div>

        <Card class="border-purple-200 dark:border-purple-800 text-gray-700 dark:text-gray-300 bg-purple-100/50 dark:bg-gray-900 -mt-4">
          <CardContent class="pt-6 space-y-2">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <EyeIcon class="h-4 w-4 text-purple-600" />
                <Label class="text-md font-medium text-gray-700 dark:text-gray-300">Focus Mode</Label>
              </div>
              <Switch
                :checked="focusMode"
                @update:checked="focusMode = $event"
                class="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-gray-500 dark:data-[state=unchecked]:bg-gray-700"
              />
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <PencilIcon class="h-4 w-4 text-purple-600" />
                <Label class="text-md font-medium text-gray-700 dark:text-gray-300">Highlighter</Label>
              </div>
              <Switch
                :checked="highlight"
                @update:checked="highlight = $event"
                class="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-gray-500 dark:data-[state=unchecked]:bg-gray-700"
              />
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <SpeakerLoudIcon class="h-4 w-4 text-purple-600" />
                <Label class="text-md font-medium text-gray-700 dark:text-gray-300">Read Along</Label>
              </div>
              <Switch
                :checked="readAlong"
                @update:checked="readAlong = $event"
                class="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-gray-500 dark:data-[state=unchecked]:bg-gray-700"
              />
            </div>
          </CardContent>
        </Card>
      </div>
      <!-- Document Analytics Section -->
      <div class="mb-6 mt-6">
          <div class="flex justify-start">
            <button 
              @click="downloadPDF" 
              class="mx-auto inline-flex items-center px-3 py-1 text-sm bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-md shadow hover:from-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-purple-400 transition transform hover:scale-105"
            >
              Download
            </button>
          </div>
          <p class="mb-2 text-sm text-gray-600 dark:text-gray-300">
            Edit and customize your document then download as pdf
          </p>
      </div>
      <Separator class="my-2" />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { BookOpenIcon, MegaphoneIcon } from '@heroicons/vue/24/outline'
import { useTextProcessor } from '~/composables/useTextProcessor'
import { useTextToSpeech } from '~/composables/useTextToSpeech'
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { debounce } from 'lodash-es'
import { Pencil2Icon, SpeakerLoudIcon } from '@radix-icons/vue'
import { PlayIcon, PauseIcon, MicrophoneIcon, ArrowRightIcon, CheckIcon, EyeIcon, PencilIcon, SparklesIcon, ArrowPathIcon, ChevronRightIcon, LanguageIcon } from '@heroicons/vue/24/solid'
import { ReloadIcon } from '@radix-icons/vue'
import { CursorTextIcon} from '@radix-icons/vue'
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'
import { Loader2Icon } from 'lucide-vue-next'
import html2pdf from 'html2pdf.js'


const chunks = ref([])
const currentChunkIndex = ref(0)
const isRecording = ref(false)
const isPaused = ref(false)
const isChunkComplete = ref(false)
const wordProgress = ref([])
const currentPosition = ref(0)
const transcriptBuffer = ref('')
const readWords = ref([])
const readWordIndices = ref(new Set())
const totalWordsRead = ref(0)

// RecordRTC setup
let RecordRTC
if (process.client) {
  const initRecordRTC = async () => {
    RecordRTC = (await import('recordrtc')).default
  }
  initRecordRTC()
}

// Recorder refs
const recorder = ref(null)
const stream = ref(null)
const recognition = ref(null)

// Computed
const currentChunkWords = computed(() => {
  if (!chunks.value[currentChunkIndex.value]) return []
  return chunks.value[currentChunkIndex.value].split(' ')
})

// Methods
const splitTextIntoChunks = (text) => {
  chunks.value = [text]
  initializeWordProgress()
}

const initializeWordProgress = () => {
  const words = currentChunkWords.value
  wordProgress.value = words.map((word, index) => ({
    word,
    isRead: false,
    timestamp: 0,
    originalIndex: index
  }))
}

const showCountdown = ref(false)
const countdown = ref('')

const startAssessment = () => {
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = convertedHtml.value
  const plainText = tempDiv.textContent || tempDiv.innerText
  // Normalize whitespace and trim extra spaces
  const normalizedText = plainText.replace(/\s+/g, ' ')
                               .replace(/\n/g, '\n\n')
                               .trim()
  initializeReading(normalizedText)
}


const startCountdown = () => {
  showCountdown.value = true
  countdown.value = 'Ready?'
  setTimeout(() => {
    startRecording()
    countdown.value = 'Go!'
    setTimeout(() => {
      showCountdown.value = false
    }, 1000)
  }, 2000)
}

const processSpeech = (transcript) => {
  transcriptBuffer.value = (transcriptBuffer.value + ' ' + transcript.toLowerCase()).slice(-200)
  console.log('transcriptBuffer.value', transcriptBuffer.value)

  let wordsToProcess = wordProgress.value.slice(currentPosition.value)
  const windowSize = Math.min(wordsToProcess.length, 3)
  
  for (let i = 0; i < windowSize; i++) {
    const wordToMatch = wordsToProcess[i].word.toLowerCase()
    const position = currentPosition.value + i
    
    if (hasCommonCharacters(wordToMatch, transcriptBuffer.value)) {
      let count = 0
      for (let j = currentPosition.value; j <= position; j++) {
        wordProgress.value[j].isRead = true
        wordProgress.value[j].timestamp = Date.now()
        readWordIndices.value.add(j)
        count++
      }
      currentPosition.value += count || 1
      totalWordsRead.value++

      if (currentPosition.value >= wordProgress.value.length - 1) {
        wordProgress.value[wordProgress.value.length - 1].isRead = true
        currentPosition.value = wordProgress.value.length
        isChunkComplete.value = true
        setTimeout(() => {
          stopRecording()
        }, 700)
        break
      }
    }
  }
}

const hasCommonCharacters = (word, buffer) => {
  const normalizedWord = word.toLowerCase()
  const recentBuffer = buffer.split(' ').slice(-3).join(' ')
  
  // For words with 3 or fewer characters, check exact match
  if (normalizedWord.length <= 3) {
    return recentBuffer.includes(normalizedWord)
  }

  // Check if first 3 characters appear in sequence in recent buffer
  const firstThreeChars = normalizedWord.substring(0, 3)
  return recentBuffer.includes(firstThreeChars)
}

const startRecording = async () => {
  try {
    isPaused.value = false
    stream.value = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: 44100,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true
      }
    })

    recorder.value = new RecordRTC(stream.value, {
      type: 'audio',
      mimeType: 'audio/wav',
      recorderType: RecordRTC.StereoAudioRecorder,
      numberOfAudioChannels: 1,
      checkForInactiveTracks: true,
      timeSlice: 1000
    })

    console.log('Recording started')
    setupSpeechRecognition()
    recorder.value.startRecording()
    recognition.value.start()
    isRecording.value = true
    console.log('it should be recording')
    
  } catch (error) {
    console.error('Error accessing microphone:', error)
  }
}

const setupSpeechRecognition = () => {
  if (!process.client) return
  
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  recognition.value = new SpeechRecognition()
  recognition.value.continuous = true
  recognition.value.interimResults = true
  
  // Adjust properties for faster recognition
  recognition.value.maxAlternatives = 1
  
  recognition.value.onresult = (event) => {
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript
      processSpeech(transcript)
    }
  }
  
  recognition.value.onend = () => {
    if (isRecording.value && !isPaused.value) {
      setTimeout(() => {
        recognition.value.start()
      }, 100)
    }
  }

  recognition.value.onerror = (event) => {
    console.log('Speech recognition error:', event.error)
    if (event.error !== 'aborted' && isRecording.value) {
      setTimeout(() => {
        recognition.value.start()
      }, 100)
    }
  }
}

const stopRecording = () => {
  if (!recorder.value || !stream.value) return

  recognition.value.stop()
  recorder.value.stopRecording(() => {
    const blob = recorder.value.getBlob()
    processReadingData(chunks.value[currentChunkIndex.value], blob)
    
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
    recorder.value = null
    isRecording.value = false
    isChunkComplete.value = true
  })
}

const initializeReading = (text) => {
  splitTextIntoChunks(text)
}

const pauseRecording = () => {
  if (recognition.value) {
    recognition.value.stop()
  }
  isPaused.value = true
  // Store current progress
  const currentProgress = {
    position: currentPosition.value,
    readWords: [...readWordIndices.value],
    buffer: transcriptBuffer.value
  }
  localStorage.setItem('assessmentProgress', JSON.stringify(currentProgress))
}

const resumeRecording = () => {
  isPaused.value = false
  // Restore progress from stored state
  const progress = JSON.parse(localStorage.getItem('assessmentProgress'))
  if (progress) {
    currentPosition.value = progress.position
    readWordIndices.value = new Set(progress.readWords)
    transcriptBuffer.value = progress.buffer
  }
  startRecording()
}

const assessCurrentProgress = async () => {
  if (!recorder.value || !stream.value) return
  
  recognition.value.stop()
  recorder.value.stopRecording(() => {
    const blob = recorder.value.getBlob()
    const currentText = chunks.value[currentChunkIndex.value]
    // Only process the text up to where the user paused
    const partialText = currentText.split(' ')
      .slice(0, currentPosition.value)
      .join(' ')
    
    processReadingData(partialText, blob)
    
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
    recorder.value = null
    isRecording.value = false
    isPaused.value = false
  })
}
// 2. Add reading assessment functionality
const handlePlayPause = () => {
  if (!isRecording.value && currentChunkIndex.value === 0) {
    // First time starting - initialize assessment
    startAssessment()
    startCountdown()
  } else if (!isRecording.value) {
    // Starting a new chunk
    startCountdown()
  } else {
    // Handle pause/resume during recording
    if (isPaused.value) {
      resumeRecording()
    } else {
      pauseRecording()
    }
  }
}

const hasAssessmentResults = computed(() => recentWpm.value > 0)
const isImproving = computed(() => {
  // Compare with previous assessments
  return true
})
const lastAssessmentDate = computed(() => {
  return new Date().toLocaleDateString()
})

const retryChunk = () => {
  isChunkComplete.value = false
  currentPosition.value = 0
  transcriptBuffer.value = ''
  readWordIndices.value = new Set()
  totalWordsRead.value = 0
  currentChunkIndex.value = 0
  initializeWordProgress()
  isRecording.value = false
  if (recorder.value) {
    recorder.value.stopRecording()
  }
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
  }
  recorder.value = null
  stream.value = null
  startCountdown()
}

const showAssessment = ref(false)
const isProcessing = ref(false)

const processReadingData = async (chunk, recording) => {
  isProcessing.value = true
  const formData = new FormData()
  formData.append('file', recording, 'chunk-recording.wav')
  formData.append('text', chunk)
  formData.append('user_id', localStorage.getItem('userId'))

  try {
    const response = await axios.post('https://dyslexai-gvbfgqdkdkg0dwhw.canadacentral-01.azurewebsites.net/test-reading', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    updateReadingResults(response.data)
  } catch (error) {
    console.error('Error processing reading data:', error)
  } finally {
    isProcessing.value = false
  }
}

const recentWpm = ref(0)
const recentErrors = ref([])

const updateReadingResults = (response) => {
  // Get existing results
  const results = JSON.parse(localStorage.getItem('readingResults'))
    
  // Update with new data
  results.wpm.push(response.wpm)
  const parsedErrors = parseErrors(response.errors)
  results.errors.push(...parsedErrors)
    
  // Save back to localStorage
  localStorage.setItem('readingResults', JSON.stringify(results))

  // Update reactive refs with recent results
  recentWpm.value = response.wpm
  recentErrors.value = parsedErrors
}

const parseErrors = (errors) => {
  return errors.map(error => error.word.toLowerCase())
}

const downloadPDF = () => {
  // Get the DOM element that contains your main content
  const element = document.getElementById('essay-content')
  if (!element) return

  // Options for html2pdf - adjust options as needed
  const opt = {
    margin:       0.5,
    filename:     'document.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { 
      scale: 2,
      // Optionally include any background or styling capture options here
    },
    jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
  }

  // Convert the element to PDF using html2pdf
  html2pdf().set(opt).from(element).save()
}

const leftSheetOpen = ref(false)
const rightSheetOpen = ref(false)

const readAlong = ref(false)
const { speak, stop } = useTextToSpeech()

const setupWordHoverListeners = () => {
  const essayContent = document.getElementById('essay-content')
  if (!essayContent) return

  const debouncedSpeak = debounce((word) => {
    if (readAlong.value) {
      speak(word)
    }
  }, 500)
  
  essayContent.addEventListener('mouseover', (e) => {
    if (focusMode.value){
    const wordContainer = e.target.closest('.word-container')
    if (wordContainer) {
      const word = wordContainer.dataset.word
      debouncedSpeak(word)
    }
    }
    else {
      const wordContainer = e.target.closest('[data-word]')
      if (wordContainer) {
        const word = wordContainer.dataset.word
        debouncedSpeak(word)
      }
    }
})

  essayContent.addEventListener('mouseout', (e) => {
    if (focusMode.value){
    const wordContainer = e.target.closest('.word-container')
    if (wordContainer) {
      debouncedSpeak.cancel()
      stop()
    }
    }
    else {
      const wordContainer = e.target.closest('[data-word]')
      if (wordContainer) {
        debouncedSpeak.cancel()
        stop()
      }
    }
})
}

const highlight = ref(false)
const { processText } = useTextProcessor()

const selectedFont = ref('OpenDyslexic')
const fontSize = ref(16)
const lineHeight = ref(2.2)
const letterSpacing = ref(0.2)
const wordSpacing = ref(16)
const route = useRoute()

const focusMode = ref(false)
watch(focusMode, (newValue) => {
  if (newValue) {
    leftSheetOpen.value = false
    rightSheetOpen.value = false
}})

const getBoldedWord = (word) => {
  let boldedHtml = ''
  if (word.length <= 2) {
    boldedHtml = `<strong style="display:inline-block;transform:scale(1.1)">${word}</strong>`
  } else if (word.length <= 4) {
    boldedHtml = `<strong style="display:inline-block;transform:scale(1.1)">${word.slice(0, 2)}</strong><span style="display:inline-block">${word.slice(2)}</span>`
  } else {
    const boldLength = Math.ceil(word.length * 0.4)
    boldedHtml = `<strong style="display:inline-block;transform:scale(1.1)">${word.slice(0, boldLength)}</strong><span style="display:inline-block">${word.slice(boldLength)}</span>`
  }
  return `<span class="word-container" data-word="${word}">${boldedHtml}</span>`
}

const applyFocusModeBolding = (content) => {
  const parts = content.split(/(<[^>]*>|\s+)/)
  return parts.map(part => {
    if (part.match(/^<.*>$/)) return part
    if (part.trim()) return getBoldedWord(part)
    return part
  }).join('')
}

const title = ref(route.query.fileName || 'Dyslexia')
const convertedHtml = ref(route.query.text || `<h1>Understanding Dyslexia</h1><p>Dyslexia is a neurological condition that affects an individual’s ability to read, write, and spell, despite normal intelligence and adequate educational opportunities. This condition is classified as a specific learning disorder and is often characterized by difficulties in phonological processing, which refers to the ability to break down and manipulate the sounds in language.</p><p>The etiology of dyslexia involves a confluence of genetic and environmental factors, often implicating atypical neural activation in regions such as the left temporal lobe. Neuroimaging studies reveal that individuals with dyslexia exhibit diminished connectivity in areas responsible for decoding orthographic symbols and mapping them to corresponding phonemes. Despite these challenges, dyslexia does not correlate with cognitive deficits; many individuals with this condition demonstrate exceptional creativity and problem-solving abilities.</p><p>Intervention strategies for dyslexia often involve structured literacy programs that employ multisensory techniques. These methodologies integrate visual, auditory, and kinesthetic modalities to reinforce neural pathways, facilitating more effective acquisition of reading skills. Moreover, assistive technologies such as text-to-speech software and immersive readers can significantly ameliorate the challenges faced by dyslexic individuals, enabling them to access information and improve comprehension.</p><p> Public awareness and accommodations are essential to ensure equitable educational experiences for individuals with dyslexia. By fostering an inclusive environment and leveraging innovative pedagogical tools, society can mitigate the stigmatization often associated with this condition and empower those affected to achieve their full potential.</p>`)
const displayContent = computed(() => {
  const content = isArabic.value ? arabicContent.value : convertedHtml.value
  let processed = processText(content, highlight.value)
  
  if (focusMode.value) {
    processed = applyFocusModeBolding(processed)
  }

  let currentWordIndex = 0
  const parts = processed.split(/(<[^>]*>|\s+)/)
  
  const processedContent = parts.map(part => {
    if (part.match(/^<.*>$/)) return part
    
    if (part.trim()) {
      const isRead = readWordIndices.value.has(currentWordIndex)
      const wordSpan = `<span
        class="word-progress ${isRead ? 'read' : ''}"
        data-word="${part}"
        data-index="${currentWordIndex}"
        style="transition: all 0.3s ease"
      >${part}</span>`
      currentWordIndex++
      return wordSpan
    }
    return part
  }).join('')

  return `<div class="${isArabic.value ? 'rtl-content' : ''}">${processedContent}</div>`
})

// a watcher to watch the highlight mode and update the displayContent accordingly
watch(highlight, (newValue) => {
  displayContent.value = processText(convertedHtml.value, newValue)
})
const fontClass = computed(() => {
  const fonts = {
    'OpenDyslexic': 'font-custom',
    'Comic Sans MS': 'font-comic',
    'Arial': 'font-arial'
  }
  return fonts[selectedFont.value]
})

const fontSizeArray = computed({
  get: () => [fontSize.value],
  set: ([value]) => fontSize.value = value
})

const lineHeightArray = computed({
  get: () => [lineHeight.value],
  set: ([value]) => lineHeight.value = value
})

const wordSpacingArray = computed({
  get: () => [wordSpacing.value],
  set: ([value]) => wordSpacing.value = value
})

const originalContent = ref(convertedHtml.value)
const remixedContent = ref(null)
const isOriginalView = ref(true)
// Add these refs with the other refs
const isRemixing = ref(false)

const toggleView = () => {
  if (!remixedContent.value && !isOriginalView.value) {
    remixText()
    return
  }
  isOriginalView.value = !isOriginalView.value
  convertedHtml.value = isOriginalView.value ? originalContent.value : remixedContent.value
}

// Update remixText method
const remixText = async () => {
  if (remixedContent.value) {
    isOriginalView.value = false
    convertedHtml.value = remixedContent.value
    return
  }

  isRemixing.value = true
  showRemixOverlay.value = true
  
  const messages = [
    'Analyzing difficult words...',
    'Finding better alternatives...',
    'Personalizing content for you...',
    'Making text more accessible...'
  ]
  
  let messageIndex = 0
  const messageInterval = setInterval(() => {
    remixMessage.value = messages[messageIndex]
    messageIndex = (messageIndex + 1) % messages.length
  }, 2000)

  try {
    const results = JSON.parse(localStorage.getItem('readingResults')) || { errors: [], wpm: [] }
    const uniqueErrorWords = [...new Set(results.errors)]
    
    // Extract text content without HTML tags
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = convertedHtml.value
    const plainText = tempDiv.textContent || tempDiv.innerText
    const words = plainText.split(/\s+/)
    
    // If text is longer than 450 words, only remix the first 450
    const textToRemix = words.length > 450 ? words.slice(0, 450).join(' ') : plainText
    
    const response = await axios.post('https://dyslexai-gvbfgqdkdkg0dwhw.canadacentral-01.azurewebsites.net/remix', {
      words: uniqueErrorWords,
      document: textToRemix
    })
    
    if (words.length > 450) {
      // Combine remixed content with remaining original content
      const remixedPart = response.data.remixed_text
      const remainingPart = convertedHtml.value.split(/\s+/).slice(450).join(' ')
      remixedContent.value = remixedPart + remainingPart
    } else {
      remixedContent.value = response.data.remixed_text
    }
    
    convertedHtml.value = remixedContent.value
    isOriginalView.value = false
    
  } catch (error) {
    console.error('Error remixing text:', error)
  } finally {
    clearInterval(messageInterval)
    isRemixing.value = false
    showRemixOverlay.value = false
  }
}

const showRemixOverlay = ref(false)
const remixMessage = ref('Remixing your document')

const isArabic = ref(false)
const arabicContent = ref(null)

const toggleTranslation = async () => {
  if (arabicContent.value && isArabic.value) {
    convertedHtml.value = originalContent.value
    isArabic.value = false
    return
  }

  try {
    const response = await axios.post('https://dyslexai-gvbfgqdkdkg0dwhw.canadacentral-01.azurewebsites.net/translate-to-arabic', {
      text: convertedHtml.value.replace(/<[^>]*>/g, '')
    })

    arabicContent.value = processText(response.data.translated_text, highlight.value)
    convertedHtml.value = arabicContent.value
    isArabic.value = true
  } catch (error) {
    console.error('Translation error:', error)
  }
}

const isVoiceChatActive = ref(false)
const chatHistory = ref([])
const ws = ref(null)
const currentAudioSource = ref(null)

const isListening = ref(false)
const isSpeaking = ref(false)
const isProcessingRequest = ref(false)

const startVoiceChat = async () => {
  const userId = localStorage.getItem('userId')
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = convertedHtml.value
  let plainText = tempDiv.textContent || tempDiv.innerText
  const words = plainText.split(/\s+/)
  if (words.length > 500) {
    plainText = words.slice(0, 500).join(' ')
  }

  ws.value = new WebSocket(`wss://dyslexai-gvbfgqdkdkg0dwhw.canadacentral-01.azurewebsites.net/ws/audio-chat/${userId}`)

  ws.value.onopen = () => {
    ws.value.send(JSON.stringify({
      type: 'context',
      content: plainText
    }))
  }
  
  ws.value.onmessage = async (event) => {
    // Pause recognition and recording while processing the response
    if (recognition.value) {
      recognition.value.stop()
      isListening.value = false
    }
    
    if (recorder.value) {
      recorder.value.pauseRecording()
    }
  
    // Process the audio response
    isSpeaking.value = true
    isProcessingRequest.value = false // Reset processing state after response
  
    const audioBlob = new Blob([event.data], { type: 'audio/wav' })
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    const audioBuffer = await audioContext.decodeAudioData(await audioBlob.arrayBuffer())
    const source = audioContext.createBufferSource()
    source.buffer = audioBuffer
    source.connect(audioContext.destination)
    
    // Save the audio source so we can abort the playback if needed:
    currentAudioSource.value = source

    source.onended = () => {
      isSpeaking.value = false
      currentAudioSource.value = null

      // Restart recognition and recording if voice chat is still active:
      if (isVoiceChatActive.value) {
        if (recognition.value) {
          recognition.value.start()
          isListening.value = true
        }
        if (recorder.value) {
          recorder.value.resumeRecording()
        }
      }
    }
    
    source.start()
  }
  
  recognition.value = new webkitSpeechRecognition()
  recognition.value.continuous = true
  recognition.value.interimResults = false
  
  recognition.value.onresult = (event) => {
    const transcript = event.results[event.results.length - 1][0].transcript
    
    // Only send new request if not processing previous one
    if (!isProcessingRequest.value) {
      isProcessingRequest.value = true
      chatHistory.value.push({ type: 'user', text: transcript })
      ws.value.send(JSON.stringify({
        type: 'message',
        message: transcript
      }))
    }
  }
  
  isVoiceChatActive.value = true
  recognition.value.start()
  isListening.value = true
}

const stopVoiceChat = () => {
  if (ws.value) {
    ws.value.close()
    ws.value = null
  }
  
  if (recognition.value) {
    recognition.value.stop()
    isListening.value = false
  }
  
  if (recorder.value) {
    recorder.value.stopRecording()
    recorder.value = null
  }
  
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
  }

  // Abort any ongoing audio playback:
  if (currentAudioSource.value) {
    currentAudioSource.value.stop()
    currentAudioSource.value = null
  }
  
  isVoiceChatActive.value = false
  isSpeaking.value = false
  chatHistory.value = []
}


const handleEscKey = (event) => {
  if (event.key === 'Escape' && focusMode.value) {
    focusMode.value = false
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
  setupWordHoverListeners()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscKey)
  debouncedSpeak.cancel()
})
</script>
<style>
.word-highlight {
  display: inline-block;
  border-radius: 3px;
  transition: all 0.2s ease;
  padding: 0 1px;
  cursor: pointer;
}
/* am gonna change this later make it better */

.max-w-4xl {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.max-w-4xl::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}

.prose {
  max-width: none !important;
}

.prose h1 {
  font-size: var(--heading-font-size) !important;
  font-weight: 700 !important;
  margin-bottom: 1em !important;
}

.prose p {
  font-size: var(--base-font-size) !important;
  margin-bottom: 2.5em !important;
}

.focus-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
  pointer-events: none;
}

.overlay-section {
  position: fixed;
  background: rgba(0, 0, 0, 0.8);
  pointer-events: none; 
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.overlay-section.left {
  left: 0;
  background: rgba(0, 0, 0, 0.5);
  height: 100vh !important;
  top: 0 !important;
}

.overlay-section.right {
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  height: 100vh !important;
  top: 0 !important;
}

.exit-focus-button {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
  z-index: 41;
  pointer-events: auto;
}

strong {
  display: inline-block;
  transform-origin: left center;
  margin: 0;
  padding: 0;
}

[dir="rtl"] strong {
  transform-origin: right center;
}

span {
  margin: 0;
  padding: 0;
}
  
.word-progress {
  display: inline-block;
  transition: all 0.3s ease;
  padding: 0 2px;
  border-radius: 2px;
  margin: 0 1px;
}

.word-progress.read {
  color: #bf1fdc; /* Purple color for read words */
  transform: scale(1.02);
  font-weight: 500;
}

[data-theme="dark"] .word-progress.read {
  color: #ad08b9; /* Lighter purple for dark mode */
}

.rtl-content {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .word-highlight {
  display: inline-block;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
@media (max-width: 768px) {
  .max-w-4xl {
    padding-top: 0.5rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-bottom: 0.5rem;
  }
  .exit-focus-button {
    top: auto;
    bottom: 20px;
    left: 50%;
    right: auto;
    transform: translateX(-50%);
  }
}

@keyframes borderPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(59,130,246, 0.7);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(59,130,246, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(59,130,246, 0);
  }
}

.animate-border {
  animation: borderPulse 1.5s infinite;
}
</style>
