<template>
    <div class="p-4">
        <h1 class="mb-2">Mode Selection</h1>
        <div class="flex space-x-0 mb-6">
            <button 
                :class="[mode.valueOf() === 'General' ? 'bg-green-600 text-white' : 'bg-gray-300']" 
                @click="setMode('General')" 
                class="py-2 px-4 rounded-tl-lg focus:outline-none transition-colors duration-200">
                General
            </button>
            <button 
                :class="[mode.valueOf() === 'Resources' ? 'bg-green-600 text-white' : 'bg-gray-300']" 
                @click="setMode('Resources')" 
                class="py-2 px-4 rounded-tr-lg focus:outline-none transition-colors duration-200">
                Resources
            </button>
            <!-- Delete icon on left side top with icon -->
            <button class="bg-red-600 text-white py-2 px-4 rounded-tr-lg focus:outline-none transition-colors duration-200"
                @click="deleteChatbotConversation"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

        </div>
        <div v-if="mode.valueOf() === 'Resources'" class="p-4">
                <label class="mb-2 text-green" for="resourceSelect">All Resource</label>
                <select id="resourceSelect" class="border p-2 rounded w-full mb-4">
                    <option v-for="document in documents" :key="document.url" disabled>{{ document.name }}</option>
                    <option v-for="video in videos" :key="video.url" disabled>{{ video.name }}</option>
                </select>
        </div>
        
    </div>
    <div class="">
        <div v-for="message in messages" :key="message.time" :class="['chat', message.sender === 'You' ? 'chat-end' : 'chat-start']">
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="../../assets/images/Chatbot.png" />
                </div>
            </div>
            <div class="chat-header">
                {{ message.sender }}
                <time class="text-xs opacity-50">{{ message.time }}</time>
            </div>
            <div :class="['chat-bubble', message.sender === 'You' ? 'chat-bubble-success' : 'chat-bubble-primary']">
                {{ message.content }}
            </div>
            <div class="chat-footer opacity-50">
                {{ message.status }}
            </div>
        </div>

        <div class="message-input flex items-center p-20">
            <input
                type="text"
                placeholder="Type your message..."
                v-model="newMessage"
                class="p-2 border border-gray-300 rounded-l-md focus:outline-none focus:border-blue-400 flex-grow w-11/12 center"
                @keyup.enter="sendChatbotConversationMessage"
            />
            <button
                @click="sendChatbotConversationMessage"
                class="btn btn-primary w-1/12 rounded-r-md"
                >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                    <path d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
            </button>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { ref } from 'vue';
import axios from 'axios';

// Typescript interface for the message object
interface Message {
    sender: string;
    content: string;
    time: string;
    status: string;
}


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

const mode = ref('General');  // Hier erstellen Sie eine ref

const setMode = (selectedMode: string) => {
    mode.value = selectedMode;  // Hier greifen Sie auf die .value-Eigenschaft der ref zu
};

const messages = ref<Message[]>([]);

const newMessage = ref('');


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

const deleteChatbotConversation = async () => {
    try {
        const response = await axios.post(`${baseUrl}/users/${userId}/subjects/${subjectId}/chats`, {
            chatbot: mode.value === 'Resources' ? 'resources' : 'general', // Verwenden Sie .value für ref in Vue 3
            prompt: 'clear'
        });

        //page reload
        location.reload();

        newMessage.value = ''; 

    } catch (error) {
        errorMessage.value = 'An error occurred while sending the message. Please try again later.';
        console.error('Error sending chat message:', error);
    }
};

const sendChatbotConversationMessage = async () => {
    messages.value.push({
            sender: 'You',
            content: newMessage.value,
            time: new Date().toLocaleTimeString(),
            status: 'Delivered'
        });
    try {
        const response = await axios.post(`${baseUrl}/users/${userId}/subjects/${subjectId}/chats`, {
            chatbot: mode.value === 'Resources' ? 'resources' : 'general', // Verwenden Sie .value für ref in Vue 3
            prompt: newMessage.value
        });

        // Fügen Sie die Antwort des Chatbots hinzu
        if (response.data && response.data.answer) {
            messages.value.push({
                sender: 'Chatbot',
                content: response.data.answer, // Hier setzen Sie die Antwort des Chatbots
                time: new Date().toLocaleTimeString(),
                status: 'Delivered'
            });
        }

        newMessage.value = ''; 

    } catch (error) {
        errorMessage.value = 'An error occurred while sending the message. Please try again later.';
        console.error('Error sending chat message:', error);
    }
};

const startChatbotConversation = async () => {
    try {
        const response = await axios.post(`${baseUrl}/users/${userId}/subjects/${subjectId}/chats`, {
            chatbot: mode.value === 'Resources' ? 'resources' : 'general', // Verwenden Sie .value für ref in Vue 3
            prompt: 'hey'
        });

        // Fügen Sie die Antwort des Chatbots hinzu
        if (response.data && response.data.answer) {
            messages.value.push({
                sender: 'Chatbot',
                content: response.data.answer, // Hier setzen Sie die Antwort des Chatbots
                time: new Date().toLocaleTimeString(),
                status: 'Delivered'
            });
        }

    } catch (error) {
        errorMessage.value = 'An error occurred while sending the message. Please try again later.';
        console.error('Error sending chat message:', error);
    }
};

onMounted(() => {
    getVideos();
    getDocuments();
    startChatbotConversation();
});
</script>

<style>
    h1 {
        font-size: 30px;
        color: #4caf50;
    }
    /* ... vorhandene Stile ... */

    button {
        border-top: 2px solid transparent;
    }

    button:focus, button:active {
        border-top-color: #4caf50;  /* Grün wie im H1-Tag */
    }

</style>
