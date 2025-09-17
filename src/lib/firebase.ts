import { initializeApp, getApp, getApps } from 'firebase/app';

const firebaseConfig = {
  apiKey: "test-key-321",
  authDomain: "vibe-demo-467221.firebaseapp.com",
  projectId: "vibe-demo-467221",
  storageBucket: "vibe-demo-467221.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abcdef1234567890"
};

// Initialize Firebase
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

export { app };
