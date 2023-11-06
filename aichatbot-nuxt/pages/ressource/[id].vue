<template>
    <div>
        <h1 class="p-10">Ressourcen</h1>
        
        <div class="flex justify-center mb-6 w-">
            <button class="bg-gray-200 text-gray-600 px-6 py-2"
            :class="activeTab === 'video' ? 'bg-green-600 text-white' : ''" 
            @click="activeTab = 'video'">Video</button>
            <button class="bg-gray-200 text-gray-600 px-6 py-2" 
            :class="activeTab === 'document' ? 'bg-green-600 text-white' : ''"
            @click="activeTab = 'document'">Dokument</button>
        </div>
        <div class="flex justify-center mt-6">
            <select v-if="activeTab === 'video'" v-model="selectedVideo" class="select select-bordered w-80">
                <option :disabled="true">Wähle ein Video</option>
                <option v-for="video in videos" :key="video.url">{{ video.name }}</option>
            </select>
            
            <select v-if="activeTab === 'document'" v-model="selectedDocument" class="select select-bordered w-80">
                <option :disabled="true">Wähle ein Dokument</option>
                <option v-for="document in documents" :key="document.url">{{ document.name }}</option>
            </select>
        </div>
        <div class="flex justify-center mt-6">
            <iframe v-if="activeTab === 'video' && selectedVideo" 
                width="900" height="600" 
                :src=getVideoUrl(selectedVideo) 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
            
            <iframe v-if="activeTab === 'document' && selectedDocument" 
                width="900" height="600" 
                :src=getDocumentUrl(selectedDocument)
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import axios from 'axios';

    const activeTab = ref('video');

    // Sample video and document names
    // const videos = ref(['Video1', 'Video2', 'Video3']);
    // const documents = ref(['Dokument1', 'Dokument2', 'Dokument3']);

    const videos = ref<Video[]>([]); // Ein leeres Array für die Fächer vom Typ 'Video'
    const documents = ref<Document[]>([]); // Ein leeres Array für die Fächer vom Typ 'Document'

    const selectedVideo = ref('');
    const selectedDocument = ref('');

    interface Video {
        name: string;
        url: string;
    }

    interface Document {
        name: string;
        url: string;
    }

    const getVideoUrl = (videoName: string) => {
        console.log(videoName);
        const video = videos.value.find(video => video.name === videoName);
        return video?.url;
    };

    const getDocumentUrl = (documentName: string) => {
        console.log(documentName);
        const document = documents.value.find(document => document.name === documentName);
        return document?.url;
    };

    const baseUrl = 'http://127.0.0.1:5000/api'; // Replace with your actual base URL
    // const userId = '0izCCZBtsVolmwwMIgav';
    // const subjectId = 'yXR6ea6BeOt8KABr7PZQ'
    const errorMessage = ref('');

    const route = useRoute();
    const subjectUserID = route.params.id;


    const subjectId = (subjectUserID as string).split('&')[0];
    const userId = (subjectUserID as string).split('&')[1];

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
        getVideos();
        getDocuments();
    });
</script>



<style scoped>
h1 {
    font-size: 30px;
    color: #4caf50;
}
</style>
