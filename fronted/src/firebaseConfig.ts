
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyBqHdvZoWI_aotNA0sc8VxaKuoyBPBZNcg",
    authDomain: "tienda-d42bd.firebaseapp.com",
    projectId: "tienda-d42bd",
    storageBucket: "tienda-d42bd.appspot.com",
    messagingSenderId: "625481979906",
    appId: "1:625481979906:web:3ab8fc0c9d0be5cc0faf1b"
  };


const app = initializeApp(firebaseConfig);


export const auth = getAuth(app);
export const db = getFirestore(app);
