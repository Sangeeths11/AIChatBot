<template>
    <div>
        <h1 class="p-10">Ressourcen</h1>
        
        <div class="flex justify-center mb-6 w-">
            <button class="bg-green-600 text-white px-6 py-2 rounded-tl-lg rounded-bl-lg" @click="activeTab = 'video'">Video</button>
            <button class="bg-gray-200 text-gray-600 px-6 py-2 rounded-tr-lg rounded-br-lg" @click="activeTab = 'document'">Dokument</button>
        </div>
        <div class="flex justify-center mt-6">
            <select v-if="activeTab === 'video'" v-model="selectedVideo" class="select select-bordered w-80">
                <option :disabled="true">Wähle ein Video</option>
                <option v-for="video in videos" :key="video">{{ video }}</option>
            </select>
            
            <select v-if="activeTab === 'document'" v-model="selectedDocument" class="select select-bordered w-80">
                <option :disabled="true">Wähle ein Dokument</option>
                <option v-for="document in documents" :key="document">{{ document }}</option>
            </select>
        </div>
        <div class="flex justify-center mt-6">
            <iframe v-if="activeTab === 'video' && selectedVideo" 
                width="900" height="600" 
                :src="getYoutubeLink()" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
            
            <iframe v-if="activeTab === 'document' && selectedDocument" :src="`/${selectedDocument}.pdf`" width="900" height="600"></iframe>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import axios from 'axios';
    const activeTab = ref('video');

    // Sample video and document names
    const videos = ref(['Video1', 'Video2', 'Video3']);
    const documents = ref(['Dokument1', 'Dokument2', 'Dokument3']);

    const selectedVideo = ref('');
    const selectedDocument = ref('');

    const getYoutubeLink = () => {
        return "https://www.youtube.com/embed/dQw4w9WgXcQ";
    };

    const baseUrl = 'http://127.0.0.1:5000/api'; // Replace with your actual base URL
    const userId = ref('0izCCZBtsVolmwwMIgav');
    const subjectId = ref('0izCCZBtsVolmwwMIgav')
    const videosResponse = ref([]);
    const documentsResponse = ref([]);
    const errorMessage = ref('');

    const getVideos = async () => {
        try {
            const response = await axios.get(`${baseUrl}/users/${userId}/subjects/${subjectId}/videos`);
            videosResponse.value = response.data;
        } catch (error) {
            errorMessage.value = 'An error occurred while fetching the videos. Please try again later.';
        }
    };
    const getDocuments = async () => {
        try {
            const response = await axios.get(`${baseUrl}/users/${userId}/subjects/${subjectId}/documents`);
            documentsResponse.value = response.data;
        } catch (error) {
            errorMessage.value = 'An error occurred while fetching the documents. Please try again later.';
        }
    };
</script>



<style scoped>
h1 {
    font-size: 30px;
    color: #4caf50;
}
</style>
