<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { updateEmployee } from "@/typescript/getEmployees";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
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
} from '@/components/ui/form'


const props = defineProps<{
    open: boolean;
    initial?: Employee | null;
    busy?: boolean;
}>();

const emit = defineEmits<{
    (e: "update:open", v: boolean): void;
    (e: "close"): void;
    (e: "offboard"): void; // parent will handle actual action
}>();

function titleCase(v?: string | null) {
    if (!v) return "";
    return v
        .toString()
        .toLowerCase()
        .replace(/\b\w/g, (c) => c.toUpperCase());
}

const headerLine = computed(() => {
    const e = props.initial;
    if (!e) return "";
    const tokens: string[] = [];
    const name = [e.first_name, e.last_name].filter(Boolean).join(" ");
    if (name) tokens.push(name);
    if (e.party?.email) tokens.push(e.party.email);
    return tokens.join(" • ");
});

const schema = toTypedSchema(
    z.object({
        date_offboarded: z.string().min(1, "Offboarding date is required."),
    })
);


type FormValues = {
    date_offboarded: string;
}

const { handleSubmit, values, resetForm } = useForm<FormValues>({
    validationSchema: schema,
    initialValues: { date_offboarded: "" },
});


function onClose() {
    emit("update:open", false);
    emit("close");
}

const loading = ref(false);
const error = ref<string | null>(null);
const data = ref<Employee | null>(null);

const emp = computed(() => data.value ?? props.initial ?? null);



const onOffboard = handleSubmit(async (vals) => {
    console.log("Inside function")
    if (!props.employeeId && !emp.value?.id) {
        error.value = "Missing employee id for update";
        return;
    }
    loading.value = true; error.value = null;

    try {
        const id = (props.employeeId ?? emp.value?.id)!;
        const baseline = data.value ?? props.initial; // reuse what you already fetched
        const updated = await updateEmployee(id, vals, baseline); // only date_offboarded in vals

        data.value = updated;
        emit("offboard", updated);
        emit("update:open", false);
    } catch (e: any) {
        const apiMsg = e?.response?.data ?? e?.message ?? "Failed to save changes";
        error.value = typeof apiMsg === "string" ? apiMsg : JSON.stringify(apiMsg);
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <Dialog :open="open" @update:open="(v) => emit('update:open', v)">
        <DialogContent class="sm:max-w-2xl p-0">
        <div class="max-h-[85vh] overflow-y-auto">
            <div class="p-6">
            <DialogHeader class="p-0 mb-4">
                <DialogTitle>Offboard employee</DialogTitle>
                <DialogDescription v-if="initial">
                {{ headerLine }}
                </DialogDescription>
            </DialogHeader>

            <Card>
                <CardContent class="p-6 overflow-visible">
                <form @submit.prevent= "onSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <FormField v-slot="{ componentField }" name="date_offboarded">
                        <FormItem>
                        <FormLabel>Employee Offboarding Date</FormLabel>
                        <FormControl>
                            <Input type="date" v-bind="componentField" class="w-full" />
                        </FormControl>
                        </FormItem>
                    </FormField>

                </form>
                </CardContent>

                <!-- Sticky footer like your edit card -->
                <CardFooter class="justify-end gap-2 border-t p-4 sticky bottom-0 bg-background">
                <Button variant="ghost" :disabled="busy" @click="onClose">Close</Button>
                <Button variant="destructive" :disabled="busy" @click="onOffboard">Offboard</Button>
                </CardFooter>
            </Card>
            </div>
        </div>
        </DialogContent>
    </Dialog>
</template>

<style scoped>
/* No extra styles needed; follows your existing shadcn/ui classes */
</style>
