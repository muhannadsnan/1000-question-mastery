<template>
  <div class="min-h-screen bg-slate-100 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-slate-800 mb-2 text-center">Topic Background Demo</h1>
      <p class="text-slate-500 text-center mb-8">Preview how questions look with category-themed SVG backgrounds</p>

      <!-- Topic Grid -->
      <div class="grid gap-6">
        <div
          v-for="topic in topics"
          :key="topic.name"
          class="bg-white rounded-2xl shadow-lg overflow-hidden"
        >
          <!-- Topic Header -->
          <div class="px-4 py-3 border-b border-slate-100">
            <span
              class="inline-block px-3 py-1 rounded-full text-sm font-semibold"
              :class="topic.badgeClass"
            >
              {{ topic.name }}
            </span>
            <span class="text-slate-400 text-sm ml-2">{{ topic.categories.join(', ') }}</span>
          </div>

          <!-- Question Cards with Background -->
          <div class="grid md:grid-cols-2 gap-4 p-4">
            <div
              v-for="(bg, idx) in [1, 2]"
              :key="idx"
              class="relative rounded-xl p-6 min-h-[280px] flex flex-col"
              :style="{
                backgroundImage: `url('/backgrounds/${topic.bgKey}-${bg}.svg')`,
                backgroundSize: '280px auto',
                backgroundRepeat: 'repeat',
                backgroundColor: topic.bgColor
              }"
            >
              <!-- Question Text -->
              <div class="bg-white/80 backdrop-blur-sm rounded-xl p-4 mb-4 shadow-sm">
                <p class="text-lg font-semibold text-slate-800">{{ topic.sampleQuestions[idx - 1] }}</p>
              </div>

              <!-- Options -->
              <div class="space-y-2 mt-auto">
                <button
                  v-for="(opt, i) in ['Option A', 'Option B', 'Option C', 'Option D']"
                  :key="i"
                  class="w-full px-4 py-3 rounded-xl text-left transition-all flex items-center gap-3"
                  :class="i === 0 ? 'bg-white/90 border-2 border-primary-400 shadow-sm' : 'bg-white/70 border border-slate-200'"
                >
                  <span
                    class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold shrink-0"
                    :class="i === 0 ? 'bg-primary-500 text-white' : 'bg-slate-100 text-slate-600'"
                  >
                    {{ ['A', 'B', 'C', 'D'][i] }}
                  </span>
                  <span class="font-medium text-slate-700">{{ opt }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Back Button -->
      <div class="text-center mt-8">
        <NuxtLink to="/" class="btn-secondary">
          Back to Home
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const topics = [
  {
    name: 'Math',
    bgKey: 'math',
    bgColor: '#EFF6FF',
    badgeClass: 'bg-blue-100 text-blue-700',
    categories: ['math', 'numbers', 'counting', 'patterns', 'logic'],
    sampleQuestions: ['What is 7 × 8?', 'How many sides does a hexagon have?']
  },
  {
    name: 'Science',
    bgKey: 'science',
    bgColor: '#ECFDF5',
    badgeClass: 'bg-emerald-100 text-emerald-700',
    categories: ['science', 'physics', 'biology', 'medicine'],
    sampleQuestions: ['What planet is known as the Red Planet?', 'What gas do plants release?']
  },
  {
    name: 'Geography',
    bgKey: 'geography',
    bgColor: '#ECFEFF',
    badgeClass: 'bg-cyan-100 text-cyan-700',
    categories: ['geography', 'places', 'oceans', 'weather'],
    sampleQuestions: ['What is the largest continent?', 'What is the longest river?']
  },
  {
    name: 'History',
    bgKey: 'history',
    bgColor: '#FFFBEB',
    badgeClass: 'bg-amber-100 text-amber-700',
    categories: ['history', 'presidents', 'archaeology'],
    sampleQuestions: ['Who was the first US President?', 'What year did WWII end?']
  },
  {
    name: 'Animals',
    bgKey: 'animals',
    bgColor: '#F0FDF4',
    badgeClass: 'bg-green-100 text-green-700',
    categories: ['animals', 'pets', 'dinosaurs', 'nature'],
    sampleQuestions: ['What sound does a cow make?', 'How many legs does a spider have?']
  },
  {
    name: 'Music',
    bgKey: 'music',
    bgColor: '#FDF2F8',
    badgeClass: 'bg-pink-100 text-pink-700',
    categories: ['music', 'classical'],
    sampleQuestions: ['What instrument has 88 keys?', 'How many strings on a guitar?']
  },
  {
    name: 'Art',
    bgKey: 'art',
    bgColor: '#FDF4FF',
    badgeClass: 'bg-fuchsia-100 text-fuchsia-700',
    categories: ['art', 'architecture'],
    sampleQuestions: ['Who painted the Mona Lisa?', 'Who sculpted David?']
  },
  {
    name: 'Literature',
    bgKey: 'literature',
    bgColor: '#FFF1F2',
    badgeClass: 'bg-rose-100 text-rose-700',
    categories: ['literature', 'books', 'vocabulary', 'grammar'],
    sampleQuestions: ['Who wrote Romeo and Juliet?', 'Who wrote 1984?']
  },
  {
    name: 'Sports',
    bgKey: 'sports',
    bgColor: '#FFF7ED',
    badgeClass: 'bg-orange-100 text-orange-700',
    categories: ['sports'],
    sampleQuestions: ['How many players on a soccer team?', 'What sport uses a puck?']
  },
  {
    name: 'Technology',
    bgKey: 'technology',
    bgColor: '#F0F9FF',
    badgeClass: 'bg-sky-100 text-sky-700',
    categories: ['technology', 'gaming', 'computer-science'],
    sampleQuestions: ['What company makes the iPhone?', 'What game features Minecraft?']
  },
  {
    name: 'Entertainment',
    bgKey: 'entertainment',
    bgColor: '#F5F3FF',
    badgeClass: 'bg-violet-100 text-violet-700',
    categories: ['movies', 'tv-shows', 'pop-culture', 'streaming'],
    sampleQuestions: ['Who plays Iron Man?', 'What streaming service has Stranger Things?']
  },
  {
    name: 'Food',
    bgKey: 'food',
    bgColor: '#F7FEE7',
    badgeClass: 'bg-lime-100 text-lime-700',
    categories: ['food', 'cooking'],
    sampleQuestions: ['What do bees make?', 'What color is a ripe tomato?']
  },
  {
    name: 'Body & Health',
    bgKey: 'body',
    bgColor: '#FEF2F2',
    badgeClass: 'bg-red-100 text-red-700',
    categories: ['body', 'health', 'hygiene'],
    sampleQuestions: ['How many bones in the human body?', 'What is the largest organ?']
  },
  {
    name: 'General',
    bgKey: 'general',
    bgColor: '#F8FAFC',
    badgeClass: 'bg-slate-100 text-slate-700',
    categories: ['general', 'daily', 'everyday'],
    sampleQuestions: ['How many days in a week?', 'What season comes after winter?']
  },
]
</script>
