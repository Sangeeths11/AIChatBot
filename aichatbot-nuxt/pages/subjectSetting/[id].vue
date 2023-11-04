<template>
    <div class="p-10">
        <h1>Subjects Settings</h1>
        
        <!-- Subject Image Upload -->
        <div class="my-6">
            <label class="block text-white-600 font-bold mb-2">Upload Subject Image:</label>
            <input type="file" accept="image/*" class="file-input file-input-bordered custom-file-input" 
            :class="documents.length !== 0 ? 'w-9/12' : 'w-full'"
            v-on="image"/>
        </div>
        
        <!-- Subject Name -->
        <div class="my-6">
            <label class="block text-white-600 font-bold mb-2">Subject Name:</label>
            <input type="text" placeholder="Enter subject name" class="p-2 border rounded"
            :disabled="documents.length !== 0 ? true : false"
            :class="documents.length !== 0 ? 'w-9/12' : 'w-full'"
            v-model="subjectName"/>
        </div>
        
        <!-- Files for the Subject -->
        <div class="my-6">
            <label class="block text-white-600 font-bold mb-2">Upload Files:</label>
            <!-- Here, you might want to loop over the files using v-for or display them dynamically -->
            <input type="file" accept="image/*" class="file-input file-input-bordered custom-file-input"
            :class="documents.length !== 0 ? 'w-9/12' : 'w-full'" 
            v-on="files"/>
        </div>

        <div class="my-6">
            <button @click="saveSettings" class="text-white-600 font-bold mb-2"
            :class="documents.length !== 0 ? 'w-9/12' : 'w-full'"
            >Save</button>
        </div>
        
        <!-- Data Sidebar -->
        <div v-if="documents.length !== 0" class="absolute right-0 top-0 h-full w-1/4 bg-white shadow-md p-4">
            <h2 class="text-gray-600 font-bold mb-4">Data Overview</h2>
            <h3 class="text-gray-600 font-bold mb-2">Documente:</h3>
            <ul>
                <li v-for="document in documents" :key=document.name class="mb-2">
                    {{document.name}}
                </li>
            </ul>
            <h3 class="text-gray-600 font-bold mb-2">Videos:</h3>
            <ul>
                <li v-for="video in videos" :key=video.name class="mb-2">
                    {{video.name}}
                </li>
            </ul>
        </div>
    </div>
</template>

<script lang="ts" setup>

    import { ref } from 'vue';
    import axios from 'axios';

    const router = useRouter();
    const route = useRoute();

    const errorMessage = ref(''); // Variable to hold the error message
    const baseUrl = 'http://127.0.0.1:5000/api'; // Replace with your actual base URL
    // const userId = ref('0izCCZBtsVolmwwMIgav');
    const image = ref('');
    const subjectName = ref('');
    const files = ref([]);

    interface Subject {
        name: string;
        conversationHistory: string[];
        id: string;
    }

    const subject = ref<Subject>({
        name: '',
        conversationHistory: [],
        id: '',
    });

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
    const getSubject = async () => {
        try {
            const response = await axios.get(`${baseUrl}/users/${userId}/subjects/${subjectId}`);
            subject.value = response.data as Subject;
            console.log(subject.value.name);
            subjectName.value = subject.value.name;
        } catch (error) {
            errorMessage.value = 'An error occurred while fetching the subjects. Please try again later.';
        }
    };

    const subjectUserID = route.params.id;


    const subjectId = (subjectUserID as string).split('&')[0];
    const userId = (subjectUserID as string).split('&')[1];

    const videos = ref<Video[]>([]); // Ein leeres Array für die Fächer vom Typ 'Video'
    const documents = ref<Document[]>([]); // Ein leeres Array für die Fächer vom Typ 'Document'

    
    interface Video {
        name: string;
        url: string;
    }

    interface Document {
        name: string;
        url: string;
    }

    const getVideos = async () => {
        try {
            const response = await axios.get(`${baseUrl}/users/${userId}/subjects/${subjectId}/videos`);
            videos.value = response.data.videos as Video[];
        } catch (error) {
            errorMessage.value = 'An error occurred while fetching the videos. Please try again later.';
        }
    };
    const getDocuments = async () => {
        try {
            const response = await axios.get(`${baseUrl}/users/${userId}/subjects/${subjectId}/documents`);
            documents.value = response.data.documents as Document[];
        } catch (error) {
            errorMessage.value = 'An error occurred while fetching the documents. Please try again later.';
        }
    };

    onMounted(() => {
        if (subjectId !== 'new') {
            getSubject();
            getDocuments();
            getVideos();
        }
    });
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
