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

const firebaseConfig = {
  apiKey: "AIzaSyCbDiIMa19l-XeH8kEO3MN3jXGCcuXii3w",
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
