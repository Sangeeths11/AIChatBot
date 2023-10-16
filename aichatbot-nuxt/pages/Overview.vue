<template>
    <div>
        <h1 class="p-10">Overview Subejects</h1>
        
        <!-- 6x6 grid -->
        <div class="grid grid-cols-2 gap-4 p-10">
            <!-- Using a v-for loop to generate 35 cards -->
            <div v-for="i in 4" :key="i" class="card bg-white p-4 rounded shadow-lg">
                <!-- Sample image (replace with actual image paths) -->
                <img src="path_to_images/image_placeholder.png" alt="Subject Image" class="w-full h-32 object-cover rounded-md">
                <h2 class="mt-2 text-center">Subject {{ i }}</h2>
                <button class="absolute bottom-2 left-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded focus:outline-none">
                    Lernen
                </button>
            </div>

            <!-- The last (36th) card with a plus icon -->
            <div class="card bg-white p-4 rounded shadow-lg flex items-center justify-center">
                <!-- Plus icon -->
                <button class="bg-blue-500 hover:bg-blue-600 text-white w-12 h-12 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mx-auto my-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
h1 {
    font-size: 30px;
    color: #4caf50;
}
</style>
