<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import axios from "axios";  
import {  CalendarDate, DateFormatter, getLocalTimeZone, parseDate, today } from "@internationalized/date"
import { Button } from '@/components/ui/button'
import { CalendarIcon } from "lucide-vue-next"
import { toDate } from "reka-ui/date"
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
    NumberField,
    NumberFieldContent,
    NumberFieldDecrement,
    NumberFieldIncrement,
    NumberFieldInput,
} from '@/components/ui/number-field'

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'

const df = new DateFormatter("en-US", {
    dateStyle: "long",
})


const formSchema = toTypedSchema(
    z.object({
        firstname: z.string().min(1, "First name is required"),
        lastname: z.string().min(1, "Last name is required"),
        email: z.string().email("Invalid email address"),
        mobile: z.string().regex(/^(\+1)?[2-9]\d{2}[2-9](?!11)\d{6}$/, "Invalid US mobile number"),
        employee_hiring_date: z.string().min(1, "Hire date is required"),
        state: z.string().min(1, "State is required"),

        ssn: z
            .string()
            .optional()
            .refine((v) => !v || /^\d{3}-\d{2}-\d{4}$/.test(v), {
            message: "SSN must be XXX-XX-XXXX",
            }),
        city: z.string().optional(),
        dob: z.string().optional(),
        address_full: z.string().optional(),
        address_zip: z.string().optional(),
        marital_status: z.enum(["Single", "Married", "Divorced"]).optional(),
        gender: z.enum(["Male", "Female", "Other"]).optional(),
        dependants_count: z.coerce.number().int().min(0).max(10).default(0),
        compensation_type: z.enum(["Salaried", "Hourly"]).optional(),
    })
)

const placeholder = ref()

const { handleSubmit, setFieldValue, values } = useForm({
    validationSchema: formSchema,
})

const value = computed({
    get: () => values.dob ? parseDate(values.dob) : undefined,
    set: val => {
        if(val) {
        setFieldValue('dob', val.toString());
        } else {
        setFieldValue('dob', undefined);
        }
    },
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


const s = (v: unknown) => (v == null ? "" : String(v)).trim();
const lower = (v: unknown) => s(v).toLowerCase();

const onSubmit = handleSubmit(async (values) => {
    try {
        console.log("onSubmit fired", values);

        const addIf = (obj: Record<string, any>, key: string, val: any) => {
            if (val === undefined || val === null) return;
            const str = typeof val === "string" ? val.trim() : val;
            if (str === "" || (Number.isNaN(str) && typeof str === "number")) return;
            obj[key] = str;
        };

        // --- REQUIRED party fields ---
        const party: Record<string, any> = {
            email: s(values.email),
            phone_number: s(values.mobile),
            address_state: s(values.state),
        };

    // --- OPTIONAL party fields (validate only if provided) ---
    addIf(party, "address_full", s(values.address_full));
    addIf(party, "address_city", s(values.city));
    addIf(party, "address_zip", s(values.address_zip));

        // --- REQUIRED top-level fields ---
        const payload: Record<string, any> = {
            party,
            first_name: s(values.firstname),
            last_name: s(values.lastname),
            date_hired: s(values.employee_hiring_date),
        };

    // --- OPTIONAL top-level fields (only if provided) ---
    addIf(payload, "dob", s(values.dob)); // expect YYYY-MM-DD
    if (values.gender) payload.gender = lower(values.gender);
    if (values.ssn) payload.ssn = s(values.ssn).replace(/-/g, "");
    if (values.compensation_type) payload.compensation_type = lower(values.compensation_type);
    if (values.marital_status) payload.marital_status = lower(values.marital_status);
    if (
        values.dependants_count !== undefined &&
        values.dependants_count !== null &&
        `${values.dependants_count}`.trim() !== ""
    ) {
        payload.dependants = Number(values.dependants_count);
    }
    if (values.date_offboarded) payload.date_offboarded = s(values.date_offboarded);

    console.log("Submitting payload:", payload);


        const apiBaseUrl = "http://127.0.0.1:8000/api"; // from .env
        const endpoint = `${apiBaseUrl}/emp/employeeapi/`
        console.log("Endpoint---------------------",endpoint)
        const res = await axios.post(endpoint, payload, {
            auth: {
                username: 'prabh',  
                password: 'wasd1234'  
            },
            headers: {
                "Content-Type": "application/json",
            },
        });

    console.log("API Response:", res.data);
    alert("Form submitted successfully!");
    } catch (err) {
    console.error("Submit error:", err);
    alert("Something went wrong. See console for details.");
    }
});



</script>


<template>
    <div class="flex justify-center  w-full">
    <div class="w-full max-w-4xl bg-white p-10 rounded-xl shadow-md">
        <form @submit.prevent= "onSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FormField v-slot="{ componentField }" name="firstname">
                <FormItem>
                    <RequiredLabel required>First Name</RequiredLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter First Name" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="lastname">
                <FormItem>
                    <RequiredLabel required>Last Name</RequiredLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter Last Name" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="dob">
                <FormItem>
                <FormLabel>Date Of Birth</FormLabel>
                <FormControl>
                    <Input type="date" v-bind="componentField" />
                </FormControl>
                </FormItem>
            </FormField>

            <FormField name="gender" v-slot="{ value, handleChange }">
                <FormItem>
                    <FormLabel>Gender</FormLabel>
                    <DropdownMenu>
                    <DropdownMenuTrigger as-child>
                        <FormControl>
                        <Button
                            variant="outline"
                            :class="{
                            'w-full justify-start font-normal': true,
                            'text-muted-foreground': !value,
                            }"
                        >
                            {{ value || 'Select gender' }}
                        </Button>
                        </FormControl>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem @click="handleChange('Male')">Male</DropdownMenuItem>
                        <DropdownMenuItem @click="handleChange('Female')">Female</DropdownMenuItem>
                        <DropdownMenuItem @click="handleChange('Other')">Other</DropdownMenuItem>
                    </DropdownMenuContent>
                    </DropdownMenu>
                    <FormMessage />
                </FormItem>
            </FormField>

            
            <FormField v-slot="{ componentField }" name="mobile">
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




                <!-- Email -->
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



            <FormField v-slot="{ componentField }" name="ssn">
                <FormItem>
                    <FormLabel>Social Security Number</FormLabel>
                    <FormControl>
                    <Input
                        type="text"
                        placeholder="XXX-XX-XXXX"
                        v-bind="componentField"
                    />
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>

            <FormField v-slot="{ value, componentField }" name="compensation_type">
                <FormItem>
                    <FormLabel>Compensation Type</FormLabel>
                    <FormControl>
                    <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                        <Button
                            variant="outline"
                            :class="{
                            'w-full justify-start font-normal': true,
                            'text-muted-foreground': !value, // grey when no value
                            }"
                        >
                            {{ value || 'Select compensation type' }}
                        </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                        <DropdownMenuItem @click="setFieldValue('compensation_type', 'Salaried')">
                            Salaried
                        </DropdownMenuItem>
                        <DropdownMenuItem @click="setFieldValue('compensation_type', 'Hourly')">
                            Hourly
                        </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>


            <FormField v-slot="{ value, componentField }" name="marital_status">
                <FormItem>
                    <FormLabel>Marital Status</FormLabel>
                    <FormControl>
                    <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                        <Button variant="outline" :class="{
                            'w-full justify-start font-normal': true,
                            'text-muted-foreground': !value, // grey when no value
                        }">
                            {{ value || 'Select marital status' }}
                        </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                        <DropdownMenuItem @click="setFieldValue('marital_status', 'Single')">
                            Single
                        </DropdownMenuItem>
                        <DropdownMenuItem @click="setFieldValue('marital_status', 'Married')">
                            Married
                        </DropdownMenuItem>
                        <DropdownMenuItem @click="setFieldValue('marital_status', 'Divorced')">
                            Divorced
                        </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>


            <FormField name="dependants_count" v-slot="{ value, setValue }">
                <FormItem>
                <FormLabel>Dependants Count</FormLabel>
                <NumberField
                    :model-value="value ?? 0"
                    @update:model-value="v => setValue(Math.min(Math.max(v, 0), 10))"
                >
                    <NumberFieldContent>
                    <NumberFieldDecrement />
                    <FormControl>
                        <NumberFieldInput :min="0" :max="10" />
                    </FormControl>
                    <NumberFieldIncrement />
                    </NumberFieldContent>
                </NumberField>
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

            <FormField v-slot="{ componentField }" name="city">
                <FormItem>
                    <FormLabel>City</FormLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter City" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>


            <FormField name="state" v-slot="{ value, handleChange }">
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

            <FormField v-slot="{ componentField }" name="employee_hiring_date">
                <FormItem>
                <RequiredLabel required>Employee Hiring Date</RequiredLabel>
                <FormControl>
                    <Input type="date" v-bind="componentField" />
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
