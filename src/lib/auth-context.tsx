"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import {
  User,
  onAuthStateChanged,
  signInWithPopup,
  signOut as firebaseSignOut,
} from "firebase/auth";
import { auth, googleProvider } from "./firebase";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isInternal: boolean;
  signIn: () => Promise<void>;
  signOut: () => Promise<void>;
}

const ALLOWED_DOMAINS = ["aredaatelier.com", "goco.bz"];

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  isInternal: false,
  signIn: async () => {},
  signOut: async () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const isInternal =
    !!user?.email &&
    ALLOWED_DOMAINS.some((d) => user.email!.endsWith(`@${d}`));

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => {
      setUser(u);
      setLoading(false);
    });
    return unsub;
  }, []);

  const signIn = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
    } catch (err) {
      console.error("Sign-in failed:", err);
    }
  };

  const signOut = async () => {
    await firebaseSignOut(auth);
  };

  return (
    <AuthContext.Provider value={{ user, loading, isInternal, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
