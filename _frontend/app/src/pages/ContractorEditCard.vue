<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { getContractor, updateContractor } from "@/typescript/contractors";
import RequiredLabel from '@/components/ui/required-label.vue'

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

import {
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";


const usStates = [
    { code: "AL", name: "Alabama" },
    { code: "AK", name: "Alaska" },
    { code: "AZ", name: "Arizona" },
    { code: "AR", name: "Arkansas" },
    { code: "CA", name: "California" },
    { code: "CO", name: "Colorado" },
    { code: "CT", name: "Connecticut" },
    { code: "DE", name: "Delaware" },
    { code: "FL", name: "Florida" },
    { code: "GA", name: "Georgia" },
    { code: "HI", name: "Hawaii" },
    { code: "ID", name: "Idaho" },
    { code: "IL", name: "Illinois" },
    { code: "IN", name: "Indiana" },
    { code: "IA", name: "Iowa" },
    { code: "KS", name: "Kansas" },
    { code: "KY", name: "Kentucky" },
    { code: "LA", name: "Louisiana" },
    { code: "ME", name: "Maine" },
    { code: "MD", name: "Maryland" },
    { code: "MA", name: "Massachusetts" },
    { code: "MI", name: "Michigan" },
    { code: "MN", name: "Minnesota" },
    { code: "MS", name: "Mississippi" },
    { code: "MO", name: "Missouri" },
    { code: "MT", name: "Montana" },
    { code: "NE", name: "Nebraska" },
    { code: "NV", name: "Nevada" },
    { code: "NH", name: "New Hampshire" },
    { code: "NJ", name: "New Jersey" },
    { code: "NM", name: "New Mexico" },
    { code: "NY", name: "New York" },
    { code: "NC", name: "North Carolina" },
    { code: "ND", name: "North Dakota" },
    { code: "OH", name: "Ohio" },
    { code: "OK", name: "Oklahoma" },
    { code: "OR", name: "Oregon" },
    { code: "PA", name: "Pennsylvania" },
    { code: "RI", name: "Rhode Island" },
    { code: "SC", name: "South Carolina" },
    { code: "SD", name: "South Dakota" },
    { code: "TN", name: "Tennessee" },
    { code: "TX", name: "Texas" },
    { code: "UT", name: "Utah" },
    { code: "VT", name: "Vermont" },
    { code: "VA", name: "Virginia" },
    { code: "WA", name: "Washington" },
    { code: "WV", name: "West Virginia" },
    { code: "WI", name: "Wisconsin" },
    { code: "WY", name: "Wyoming" }
]


const props = defineProps<{
    open: boolean;
    contractorId: number | null;
    initial?: Contractor | null;
}>();

const emit = defineEmits<{
    (e: "update:open", v: boolean): void;
    (e: "save", payload: any): void;     // you’ll send your form data back
    (e: "cancel"): void;
}>();

const schema = toTypedSchema(
    z.object({
        contractor_name: z.string().min(1, "contractor name is required"),
        email: z.string().email("Invalid email address"),
        phone_number: z.string().regex(/^(\+1)?[2-9]\d{2}[2-9](?!11)\d{6}$/, "Invalid US mobile number"),
        address_state: z.string().min(1, "State is required"),
        address_city: z.string().optional(),
        address_full: z.string().optional(),
        address_zip: z.string().optional(),
        tin: z
            .string()
            .optional()
            .transform(v => (v ?? "")) // ensure a string
            .refine(v => v === "" || v.replace(/\D/g, "").length === 9, {
                message: "TIN must have 9 digits",
            })
    })
);

type FormValues = {
    contractor_name: string;
    email: string;
    phone_number: string;
    address_state: string;
    address_city: string;
    address_full: string;
    address_zip: string;
    tin: string;
};

const { resetForm, values, handleSubmit } = useForm<FormValues>({
    validationSchema: schema,
    initialValues: {
        contractor_name: "",
        email: "",
        phone_number: "",
        address_state: "",
        address_city: "",
        address_full: "",
        address_zip: "",
        tin: "",
    },
});

function toFormValues(c: any): FormValues {
    return {
        address_city: c?.party?.address_city ?? "",
        address_state: c?.party?.address_state ?? "",
        address_full: c?.party?.address_full ?? "",
        address_zip: c?.party?.address_zip ?? "",
        email: c?.party?.email ?? "",
        phone_number: c?.party?.phone_number ?? "",
        tin: c?.tin ?? "",
        contractor_name: c?.contractor_name ?? "",
    };
}

const loading = ref(false);
const error = ref<string | null>(null);
const data = ref<Contractor | null>(null);

const contractor = computed(() => data.value ?? props.initial ?? null);


async function fetchById(id: number) {
    loading.value = true; error.value = null;
    try {
        data.value = await getContractor(id);
    } catch (e: any) {
        error.value = e?.message || "Failed to load contractor";
    } finally {
        loading.value = false;
    }
}


watch(
    () => [props.open, props.contractorId, props.initial] as const,
    async ([open, id, initial]) => {
        if (!open) return;
        const src = initial ?? (id ? await fetchById(id) : null);
        if (src) resetForm({ values: toFormValues(src) });
    },
    { immediate: true }
);


function onClose() {
    emit("update:open", false);
    emit("cancel");
}

const onSave = handleSubmit(async (vals) => {
    if (!props.contractorId && !contractor.value?.id) {
        error.value = "Missing contractor id for update";
        return;
    }
    loading.value = true; error.value = null;

    try {
        const id = (props.contractorId ?? contractor.value?.id)!;
        const baseline = data.value ?? props.initial; // reuse what you already fetched
        const updated = await updateContractor(id, vals, baseline);

        data.value = updated;
        emit("save", updated);
        emit("update:open", false);
        alert("Contractor edited successfully");
    } catch (e: any) {
        const apiMsg = e?.response?.data ?? e?.message ?? "Failed to save changes";
        error.value = typeof apiMsg === "string" ? apiMsg : JSON.stringify(apiMsg);
    } finally {
        loading.value = false;
    }
});


</script>




<template>
    <Dialog :open="open" @update:open="v => emit('update:open', v)">
        <!-- No overflow-hidden + scroll container for zoomed layouts -->
        <DialogContent class="sm:max-w-2xl p-0">
        <div class="max-h-[85vh] overflow-y-auto">
            <div class="p-6">
            <DialogHeader class="p-0 mb-4">
                <DialogTitle>Edit contractor</DialogTitle>
                <DialogDescription v-if="contractor">
                {{ contractor.contractor_name }} • {{ contractor.party?.email || "—" }}
                </DialogDescription>
            </DialogHeader>

            <div v-if="loading" class="p-4 text-sm text-muted-foreground">Loading…</div>
            <div v-else-if="error" class="p-4 text-sm text-red-600">{{ error }}</div>

            <Card v-else>
                <!-- Keep content visible so popovers/selects aren’t clipped; form grid lives here -->
                <CardContent class="p-6 overflow-visible">

                    <form @submit.prevent= "onSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <FormField v-slot="{ componentField }" name="contractor_name">
                            <FormItem>
                            <FormLabel>Contractor Name</FormLabel>
                            <FormControl>
                                <Input type="text" 
                                    v-bind="componentField" 
                                    :placeholder="!values.party?.contractor_name ? 'Enter Contractor Name' : ''"/>
                            </FormControl>
                            <FormMessage />
                            </FormItem>
                        </FormField>

                        <FormField v-slot="{ componentField }" name="phone_number">
                            <FormItem>
                                <RequiredLabel required>Mobile Number</RequiredLabel>
                                <FormControl>
                                <Input
                                    type="tel"
                                    :placeholder="!values.party?.phone_number ? 'Enter Mobile Number' : ''"
                                    v-bind="componentField"
                                />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        </FormField>

                        <FormField v-slot="{ componentField }" name="email">
                            <FormItem>
                                <RequiredLabel required>Email Address</RequiredLabel>
                                <FormControl>
                                <Input
                                    type="email"
                                    :placeholder="!values.party?.email ? 'Enter Email Address' : ''"
                                    v-bind="componentField"
                                />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        </FormField>

                        <FormField v-slot="{ componentField }" name="tin">
                            <FormItem>
                                <FormLabel>Social Security Number</FormLabel>
                                <FormControl>
                                    <Input type="text" 
                                    v-bind="componentField" 
                                    :placeholder="!values.party?.tin ? 'XXXXXXXXX' : ''"/>
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        </FormField>

                        <FormField v-slot="{ componentField }" name="address_full">
                            <FormItem>
                                <FormLabel>Address</FormLabel>
                                <FormControl>
                                    <Input type="text" 
                                    :placeholder="!values.party?.address_full ? 'Enter Full Address' : ''"
                                    v-bind="componentField" />
                                </FormControl>
                            </FormItem>
                        </FormField>

                        <FormField v-slot="{ componentField }" name="address_city">
                            <FormItem>
                                <FormLabel>City</FormLabel>
                                <FormControl>
                                    <Input type="text" 
                                    :placeholder="!values.party?.address_city ? 'Enter City' : ''"
                                    v-bind="componentField" />
                                </FormControl>
                            </FormItem>
                        </FormField>

                        <FormField name="address_state" v-slot="{ value, handleChange }">
                            <FormItem>
                                <FormLabel>State</FormLabel>
                                <FormControl>
                                <DropdownMenu>
                                    <DropdownMenuTrigger class="w-full border px-4 py-2 rounded-md text-left text-muted-foreground">
                                    {{ value || "Select a state" }}
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent class="w-full max-h-60 overflow-y-auto">
                                    <DropdownMenuItem
                                        v-for="state in usStates"
                                        :key="state.code"
                                        @select="handleChange(state.code)"
                                        class="cursor-pointer"
                                    >
                                        {{ state.name }}
                                    </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        </FormField>

                        <FormField v-slot="{ componentField }" name="address_zip">
                            <FormItem>
                                <FormLabel>Zip Code</FormLabel>
                                <FormControl>
                                    <Input type="text" 
                                    :placeholder="!values.party?.address_zip ? 'Enter Zip Code' : ''"
                                    v-bind="componentField" />
                                </FormControl>
                            </FormItem>
                        </FormField>

                    </form>
                
                </CardContent>

                <!-- Sticky footer so actions are always visible even when scrolled/zoomed -->
                <CardFooter class="justify-end gap-2 border-t p-4 sticky bottom-0 bg-background">
                <Button variant="ghost" @click="onClose">Close</Button>
                <Button :disabled="loading" @click="onSave">Save changes</Button>
                </CardFooter>
            </Card>
            </div>
        </div>
        </DialogContent>
    </Dialog>
</template>
