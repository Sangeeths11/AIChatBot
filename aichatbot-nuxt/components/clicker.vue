<template >
    <div>
        <button class="btn btn-primary">{{ msg }}</button>
    </div>
</template>
<script lang="ts" setup>
defineProps({
    msg: {
        type: String,
        required: true
        asd
    }
})
</script>