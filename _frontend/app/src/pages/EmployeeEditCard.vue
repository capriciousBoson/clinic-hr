<script setup lang="ts">
import { computed } from "vue";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

type Party = { first_name?: string | null; last_name?: string | null; email?: string | null };
type Employee = { id: number; party?: Party | null };

const props = defineProps<{
  open: boolean;
  employeeId: number | null;
  initial?: Employee | null; // pass the row from the table for header info
}>();
const emit = defineEmits<{ (e: "update:open", v: boolean): void }>();

// Header text: "First Last • email"
const headerLine = computed(() => {
  const p = props.initial?.party;
  if (!p) return "";
  const name = [p.first_name, p.last_name].filter(Boolean).join(" ");
  return [name, p.email].filter(Boolean).join(" • ");
});
</script>


<!-- src/pages/EditEmployeeCard.vue -->
<template>
  <Dialog :open="open" @update:open="v => emit('update:open', v)">
    <DialogContent
      :key="employeeId"
      class="sm:max-w-2xl w-[92vw] max-w-3xl p-0"
    >
      <!-- Header like View Details -->
      <DialogHeader class="px-6 pt-6 pb-2">
        <DialogTitle>Edit employee</DialogTitle>
        <DialogDescription v-if="headerLine" class="mt-1">
          {{ headerLine }}
        </DialogDescription>
      </DialogHeader>

      <!-- Card shell (intentionally empty for now) -->
      <div class="px-6 pb-4">
        <div class="rounded-2xl border border-gray-200 shadow-sm">
          <div class="p-5 sm:p-6">
            <div class="border-t border-gray-200"></div>
            <!-- TODO: add editable fields here later -->
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="border-t px-6 py-4 flex justify-end gap-2 sticky bottom-0 bg-background">
        <Button variant="ghost" @click="emit('update:open', false)">Close</Button>
        <Button disabled>Save changes</Button>
      </div>
    </DialogContent>
  </Dialog>
</template>
