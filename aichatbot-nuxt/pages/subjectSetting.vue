<template>
    <div class="p-10">
        <h1>Subjects Settings</h1>
        
        <!-- Subject Image Upload -->
        <div class="my-6">
            <label class="block text-white-600 font-bold mb-2">Upload Subject Image:</label>
            <input type="file" accept="image/*" class="file-input file-input-bordered custom-file-input w-9/12" v-on="image"/>

        </div>
        
        <!-- Subject Name -->
        <div class="my-6">
            <label class="block text-white-600 font-bold mb-2">Subject Name:</label>
            <input type="text" placeholder="Enter subject name" class="p-2 border rounded w-9/12" v-model="subjectName"/>
        </div>
        
        <!-- Files for the Subject -->
        <div class="my-6">
            <label class="block text-white-600 font-bold mb-2">Upload Files:</label>
            <!-- Here, you might want to loop over the files using v-for or display them dynamically -->
            <input type="file" accept="image/*" class="file-input file-input-bordered custom-file-input w-9/12" v-on="files"/>
        </div>

        <div class="my-6">
            <button @click="saveSettings" class="w-9/12 text-white-600 font-bold mb-2">Save</button>
        </div>
        

        <!-- Data Sidebar -->
        <div class="absolute right-0 top-0 h-full w-1/4 bg-white shadow-md p-4">
            <h2 class="text-gray-600 font-bold mb-4">Data Overview</h2>
            <ul>
                <li class="mb-2">File1.docx</li>
                <li class="mb-2">File2.pdf</li>
                <li class="mb-2">Folder1/</li>
                <!-- ... -->
            </ul>
        </div>
    </div>
</template>

<script lang="ts" setup>

    import { ref } from 'vue';
    import axios from 'axios';

    const router = useRouter();
    const errorMessage = ref(''); // Variable to hold the error message
    const baseUrl = 'http://127.0.0.1:5000/api'; // Replace with your actual base URL
    const userId = ref('0izCCZBtsVolmwwMIgav');
    const image = ref('');
    const subjectName = ref('');
    const files = ref([]);

    const saveSettings = async () => {
        try {
            const response = await axios.post(`${baseUrl}/users/${userId}/subjects`, {
                name: subjectName.value,
            });
            console.log(response.data);
            const documentResponse = await axios.post(`${baseUrl}/documents`, {
                name: files.value,
            });
            console.log(documentResponse.data);
            // Handle success - you can redirect or show a success message
        } catch (error) {
        errorMessage.value = 'An error occurred during login. Please try again later.';
        console.error(error);
        // Handle errors - you can show error messages to the user
        }
    }
</script>

<style scoped>
h1, h2 {
    font-size: 30px;
    color: #4caf50;
}

button {
    background-color: #4caf50;
    color: white;
    border: none;
    cursor: pointer;
    padding: 10px 20px;
    border-radius: 5px;
}

.card {
    background-color: #f5f5f5;
}

input[type="file"] {
    cursor: pointer;
}

.custom-file-input::before {
    background-color: #4caf50;
}

.custom-file-input:focus::before {
    border-color: #4caf50;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.5);
}

</style>
