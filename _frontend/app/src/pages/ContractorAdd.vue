<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import {createContractor} from "@/typescript/contractors"; 
import { Button } from '@/components/ui/button'
import { computed, h, ref } from "vue"
import RequiredLabel from '@/components/ui/required-label.vue'
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
import { Input } from '@/components/ui/input'

const formSchema = toTypedSchema(
    z.object({
        contractor_name: z.string().min(1, "First name is required"),
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
)

const placeholder = ref()

const { handleSubmit, setFieldValue, values } = useForm({
    validationSchema: formSchema,
})


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


const loading = ref(false);
const error = ref<string | null>(null);

const onSubmit = handleSubmit(async (values) => {
    console.log(values)
    try {
        loading.value = true; error.value = null;
        const created = await createContractor(values);   // ← one-liner
        console.log("API Response:", created);

        alert("Contractor added successfully!");
    } catch (err: any) {
        console.error("Submit error:", err);
        // alert("Something went wrong. See console for details.");
    } finally {
        loading.value = false;
    }
});



</script>

<template>
    <div class="flex justify-center  w-full">
    <div class="w-full max-w-4xl bg-white p-10 rounded-xl shadow-md">
        <form @submit.prevent= "onSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-6">

            <FormField v-slot="{ componentField }" name="contractor_name">
                <FormItem>
                    <RequiredLabel required>Contractor Name</RequiredLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter Contractor Name" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>


            <FormField v-slot="{ componentField }" name="phone_number">
                <FormItem>
                    <RequiredLabel required>Mobile Number</RequiredLabel>
                    <FormControl>
                    <Input
                        type="tel"
                        placeholder="Enter US mobile number"
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
                        placeholder="Enter email address"
                        v-bind="componentField"
                    />
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>


            <FormField v-slot="{ componentField }" name="tin">
                <FormItem>
                    <FormLabel>Taxpayer Identification Number</FormLabel>
                    <FormControl>
                    <Input
                        type="text"
                        placeholder="XXXXXXXXX"
                        v-bind="componentField"
                    />
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>


            <FormField v-slot="{ componentField }" name="address_full">
                <FormItem>
                    <FormLabel>Address</FormLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter Address" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="address_city">
                <FormItem>
                    <FormLabel>City</FormLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter City" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>


            <FormField name="address_state" v-slot="{ value, handleChange }">
                <FormItem>
                    <RequiredLabel required>State</RequiredLabel>
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
                    <FormLabel>Zip code</FormLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter zip code" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>



            <div class="col-span-2 flex justify-center">
                <Button type="submit" class="px-6">
                    Submit
                </Button>
            </div>

        </form>
    </div>
    </div>
</template>


