<script setup lang="ts">
import AppSidebar from '@/components/AppSidebar.vue'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { RouterView } from 'vue-router'
</script>

<template>
  <SidebarProvider>
    <div class="flex min-h-screen">
      <!-- Sidebar stays fixed-width -->
      <AppSidebar />

      <!-- Main content fills the rest -->
      <main class="flex-1 bg-muted p-8">
        <RouterView />
      </main>
    </div>
  </SidebarProvider>
</template>