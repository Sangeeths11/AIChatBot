<template>
    <div class="header-logo"/>
    <div>
        <h1 class="p-10">Overview Subjects</h1>
        
        <!-- 6x6 grid -->
        <div class="grid grid-cols-2 gap-4 p-10">
            <!-- Using a v-for loop to generate 35 cards -->
            <div v-for="(subject, index) in subjects" :key="index" class="card bg-white p-4 rounded shadow-lg">
                <!-- Stellen Sie sicher, dass subject ein Objekt ist, das den Namen und andere Informationen enthält -->
                <!--<img :src="subject.imageUrl" alt="Fachbild" class="w-full h-32 object-cover rounded-md">-->
                <img :src="getImageUrl(subject)" alt="Fachbild" class="w-full h-32 object-cover rounded-md">
                <h1 class="mt-2 text-center">{{ subject.name }}</h1>
                <button @click="learn(subject.id)" class="absolute bottom-2 left-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded focus:outline-none">
                Lernen
                </button>
                <button @click="ressource(subject.id)" class="absolute bottom-2 left-2 ml-24 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded focus:outline-none">
                Ressourcen
                </button>
                <button @click="addSubject(subject.id)" class="absolute bottom-2 right-2 bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded focus:outline-none">
                Einstellungen
                </button>
                <!-- Delete -->
                <button @click="deleteSubject(subject.id)" class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded focus:outline-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mx-auto my-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- The last (36th) card with a plus icon -->
            <div class="card bg-white p-4 rounded shadow-lg flex items-center justify-center">
                <!-- Plus icon -->
                <button @click="addSubject('new')" class="bg-blue-500 hover:bg-blue-600 text-white w-12 h-12 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mx-auto my-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import defaultSubjectImage from '../../assets/images/default-subject-image.jpg';



const router = useRouter();
const route = useRoute();

interface Subject {
  name: string;
  imageUrl: string;
  id: string;
}

const subjects = ref<Subject[]>([]); // Ein leeres Array für die Fächer vom Typ 'Subject'

const getImageUrl = (subject: Subject): string => {
  return subject.imageUrl || defaultSubjectImage;
};

const addSubject = (subjectID : string) => {
    const id = subjectID + '&' + userID;
    router.push({ path: '/subjectSetting/' + id});
};

const learn = (subjectID : string) => {
    const id = subjectID + '&' + userID;
    router.push({ path: '/chatform/' + id});
};

const ressource = (subjectID : string) => {
    const id = subjectID + '&' + userID;
    router.push({ path: '/ressource/' + id});
};

const deleteSubject = async(subjectID : string) => {
    try {
        const response = await axios.delete(`${baseUrl}/users/${userID}/subjects/${subjectID}`);
        console.log(response.data);
        getSubjects();
    } catch (error) {
        console.error(error);
    }
};

onMounted(() => {
    getSubjects();
});
const baseUrl = 'http://127.0.0.1:5000/api'; // Replace with your actual base URL
const userID = route.params.id; // Get the user ID from the URL (the :id part

const getSubjects = async () => {
  try {
    const response = await axios.get(`${baseUrl}/users/${userID}/subjects`);
    console.log(response.data.subjects);

    // Die erhaltenen Fächer in das "subjects"-Array speichern
    subjects.value = response.data.subjects as Subject[];
    
  } catch (error) {
    console.error(error);
  }
};

</script>

<style scoped>
h1 {
    font-size: 30px;
    color: #4caf50;
}

button {
    background-color: #4caf50;
    color: white;
    border: none;
}
</style>