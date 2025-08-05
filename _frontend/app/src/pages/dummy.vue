<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'


import {  CalendarDate, DateFormatter, getLocalTimeZone, parseDate, today } from "@internationalized/date"
import { Button } from '@/components/ui/button'
import { CalendarIcon } from "lucide-vue-next"
import { toDate } from "reka-ui/date"
import { computed, h, ref } from "vue"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import {
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'

const df = new DateFormatter("en-US", {
    dateStyle: "long",
})

const formSchema = toTypedSchema(z.object({
    firstname: z.string().min(1, "First name is required"),
    lastname: z.string().min(1, "Last name is required"),
    dob: z.string().refine(v => v, { message: "A date of birth is required." }),
    address_full: z.string().min(1, "Address is required"),
    address_zip: z.string().min(1, "Zip code is required"),
}))

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

const onSubmit = handleSubmit((values) => {
    console.log("Submitting")
})


</script>


<template>
    <div class="flex justify-center  w-full">
    <div class="w-full max-w-4xl bg-white p-10 rounded-xl shadow-md">
        <form @submit.prevent= "onSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FormField v-slot="{ componentField }" name="firstname">
                <FormItem>
                    <FormLabel>First Name</FormLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter First Name" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="lastname">
                <FormItem>
                    <FormLabel>Last Name</FormLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter Last Name" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

            <FormField name="dob">
      <FormItem class="flex flex-col">
        <FormLabel>Date of birth</FormLabel>
        <Popover>
          <PopoverTrigger as-child>
            <FormControl>
              <Button
                variant="outline" :class="{
  'w-[240px] ps-3 text-start font-normal': true,
  'text-muted-foreground': !value
}"
              >
                <span>{{ value ? df.format(toDate(value)) : "Pick a date" }}</span>
                <CalendarIcon class="ms-auto h-4 w-4 opacity-50" />
              </Button>
              <input hidden>
            </FormControl>
          </PopoverTrigger>
          <PopoverContent class="w-auto p-0">
            <Calendar
              v-model:placeholder="placeholder"
              :model-value="value"
              calendar-label="Date of birth"
              initial-focus
              :min-value="new CalendarDate(1900, 1, 1)"
              :max-value="today(getLocalTimeZone())"
              @update:model-value="(v) => {
                if (v) {
                  setFieldValue('dob', v.toString())
                }
                else {
                  setFieldValue('dob', undefined)
                }
              }"
            />
          </PopoverContent>
        </Popover>
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


            <FormField v-slot="{ componentField }" name="address_zip">
                <FormItem>
                    <FormLabel>Zip code</FormLabel>
                    <FormControl>
                        <Input type="text" placeholder="Enter zip code" v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

        </form>
    </div>
    </div>
</template>
