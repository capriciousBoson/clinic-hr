<script setup lang="ts">
import {FormLabel} from '@/components/ui/form'
defineProps<{ required?: boolean }>()
</script>

<!-- components/ui/RequiredLabel.vue -->
<template>
    <FormLabel class="flex items-center gap-1">
        <slot />
        <span v-if="required" class="text-red-500">*</span>
    </FormLabel>
</template>

