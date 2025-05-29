import { initializeApp } from "firebase/app";
import {
  getAuth,
  signInWithPopup,
  GoogleAuthProvider,
  signOut,
  onAuthStateChanged,
  User,
  getIdToken,
} from "firebase/auth";

// Your web app's Firebase configuration
// Replace with your actual Firebase config when deploying
// const firebaseConfig = {
//   apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
//   authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
//   projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
//   storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
//   messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
//   appId: import.meta.env.VITE_FIREBASE_APP_ID
// };

const firebaseConfig = {
  apiKey: "AIzaSyBAy9TophFISJOCRfSxp8gt9MW75_lA41M",
  authDomain: "plaid-generic.firebaseapp.com",
  projectId: "plaid-generic",
  storageBucket: "plaid-generic.firebasestorage.app",
  messagingSenderId: "1025610681903",
  appId: "1:1025610681903:web:768a03d3ba76a79a1c80da",
  measurementId: "G-BB34M95GCL",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

// Authentication methods
export const signInWithGoogle = () => {
  return signInWithPopup(auth, googleProvider);
};

export const logout = () => {
  return signOut(auth);
};

// Get the current user's ID token
export const getCurrentUserToken = async () => {
  const user = auth.currentUser;
  if (!user) return null;

  return await getIdToken(user);
};

// Observer for auth state changes
export const onAuthChange = (callback: (user: User | null) => void) => {
  return onAuthStateChanged(auth, callback);
};

export default auth;
