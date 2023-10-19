<template>
    <div class="p-20">
        <div v-for="message in messages" :key="message.time" :class="['chat', message.sender === 'You' ? 'chat-end' : 'chat-start']">
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="../assets/images/Chatbot.png" />
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
                @keyup.enter="sendMessage"
            />
            <button
                @click="sendMessage"
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
// Typescript interface for the message object
interface Message {
    sender: string;
    content: string;
    time: string;
    status: string;
}


const messages = ref<Message[]>([]);

const newMessage = ref('');

const sendMessage = () => {
    if (newMessage.value.trim() !== '') {
        messages.value.push({
            sender: 'You',
            content: newMessage.value,
            time: new Date().toLocaleTimeString(),
            status: 'Delivered'
        });
        newMessage.value = '';

        setTimeout(() => {
            messages.value.push({
                sender: 'Chatbot',
                content: 'I received your message!',
                time: new Date().toLocaleTimeString(),
                status: 'Delivered'
            });
        }, 1000);
    }
};
</script>

  <style>
  /* You can adjust more styles as per your needs */
  </style>
