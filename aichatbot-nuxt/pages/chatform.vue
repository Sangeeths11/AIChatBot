<!-- src/components/ChatComponent.vue -->
<template>
    <div class="chat chat-start">
        <div class="chat-image avatar">
            <div class="w-10 rounded-full">
                <img src="../assets/images/Chatbot.png" />
            </div>
        </div>
        <div class="chat-header">
            Obi-Wan Kenobi
            <time class="text-xs opacity-50">12:45</time>
        </div>
        <div class="chat-bubble chat-bubble-primary">You were the Chosen One!</div>
        <div class="chat-footer opacity-50">
            Delivered
        </div>
        </div>
        <div class="chat chat-end">
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="../assets/images/Chatbot.png" alt="Image 1" />
                </div>
            </div>
            <div class="chat-header">
                Anakin
                <time class="text-xs opacity-50">12:46</time>
            </div>
        <div class="chat-bubble chat-bubble-success">I hate you!</div>
        <div class="chat-footer opacity-50">
            Seen at 12:46
        </div>
    </div>
    
    <div class="message-input">
        <input
            type="text"
            placeholder="Type your message..."
            v-model="newMessage"
            class="p-2 border border-gray-300 rounded-l-md focus:outline-none focus:border-blue-400 flex-grow w-11/12"
        />
        <button
            @click="sendMessage"
            class="btn btn-primary rounded-r-md px-4 w-1/12"
            >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
        </button>
    </div>
</template>
  
  <script>
    export default {
        name: 'ChatComponent',
        data() {
            return {
            newMessage: '', // Store the new message input
        };
    },
    methods: {
        sendMessage() {
        // You can handle sending the message here
        // For now, let's just log the message to the console
        console.log('Message sent:', this.newMessage);

        // Clear the input field after sending the message
        this.newMessage = '';
        },
    },
    }
  </script>
  
  <style>
  /* You can adjust more styles as per your needs */
  </style>
  