// lib/firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth'; // Import the auth module
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT,
};

// Initialize Firebase App
const firebaseApp = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get the auth instance
const auth = getAuth(firebaseApp);
const db = getFirestore(firebaseApp);
export { db,firebaseApp, auth };