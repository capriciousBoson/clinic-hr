<!-- EditEmployeeCard.vue -->
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import axios from "axios";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";

import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

// --- Types (adjust as your API grows)
type Party = {
  first_name?: string | null;
  last_name?: string | null;
  email?: string | null;
  gender?: string | null;
  dob?: string | null;
};
type Employee = {
  id: number;
  party?: Party | null;
};

const props = defineProps<{
  open: boolean;
  employeeId: number | null;
  initial?: Employee | null; // optional fast path
}>();
const emit = defineEmits<{ (e: "update:open", v: boolean): void }>();

// --- Validation + form shape (extend with more fields as needed)
const schema = toTypedSchema(
  z.object({
    firstname: z.string().min(1, "First name is required"),
    lastname: z.string().min(1, "Last name is required"),
    email: z.string().email("Invalid email").optional().or(z.literal("")),
    gender: z.string().min(1, "Gender is required"),
  })
);
type FormValues = {
  firstname: string;
  lastname: string;
  email: string;
  gender: string;
  dob: string;
};

const { resetForm, values } = useForm<FormValues>({
  validationSchema: schema,
  initialValues: {
    firstname: "",
    lastname: "",
    email: "",
    gender: "",
    dob: "",
  },
});

// --- Map API -> form values
function toFormValues(e: any): FormValues {
  return {
    firstname: e?.party?.first_name ?? "",
    lastname: e?.party?.last_name ?? "",
    email: e?.party?.email ?? "",
    gender: e?.party?.gender ?? "",
    dob: e?.party?.dob ?? "",
  };
}

// --- Fetch when we don't have initial
const loading = ref(false);
async function fetchEmployee(id: number) {
  loading.value = true;
  try {
    const { data } = await axios.get(`/api/emp/employeeapi/${id}/`);
    return data;
  } finally {
    loading.value = false;
  }
}

// --- Prefill whenever dialog opens or id changes
watch(
  () => [props.open, props.employeeId, props.initial] as const,
  async ([open, id, initial]) => {
    if (!open) return;
    const src = initial ?? (id ? await fetchEmployee(id) : null);
    if (src) resetForm({ values: toFormValues(src) });
  },
  { immediate: true }
);

// Header text uses current form values so it stays in sync
const headerLine = computed(() => {
    const p = props.initial?.party;
    if (!p) return "";
    const name = [p.first_name, p.last_name].filter(Boolean).join(" ");
    return [name, p.email].filter(Boolean).join(" • ");
});
</script>

<template>
    <Dialog :open="open" @update:open="v => emit('update:open', v)">
        <DialogContent :key="`${employeeId}-${open}`" class="sm:max-w-2xl w-[92vw] max-w-3xl p-0">
        <!-- Header -->
        <DialogHeader class="px-6 pt-6 pb-2">
            <DialogTitle>Edit employee</DialogTitle>
            <DialogDescription v-if="headerLine" class="mt-1">
            {{ headerLine }}
            </DialogDescription>
        </DialogHeader>

        <!-- Card -->
        <div class="px-6 pb-4">
            <div class="rounded-2xl border border-gray-200 shadow-sm">
            <div class="p-5 sm:p-6">
                <form class="grid grid-cols-1 md:grid-cols-2 gap-6" @submit.prevent>
                <!-- First name -->
                <FormField v-slot="{ componentField }" name="firstname">
                    <FormItem>
                    <FormLabel>First Name</FormLabel>
                    <FormControl>
                        <Input type="text" v-bind="componentField" :disabled="true"/>
                    </FormControl>
                    <FormMessage />
                    </FormItem>
                </FormField>

                <!-- Last name -->
                <FormField v-slot="{ componentField }" name="lastname">
                    <FormItem>
                    <FormLabel>Last Name</FormLabel>
                    <FormControl>
                        <Input type="text" v-bind="componentField" :disabled="true" />
                    </FormControl>
                    <FormMessage />
                    </FormItem>
                </FormField>


                <!-- Email -->
                <FormField v-slot="{ componentField }" name="email">
                    <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                        <Input type="email" v-bind="componentField" :disabled="loading" />
                    </FormControl>
                    <FormMessage />
                    </FormItem>
                </FormField>

                </form>
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
