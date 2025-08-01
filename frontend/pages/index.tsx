"use client";

import { useState } from "react";
import SignupPopup from "../components/SignupPopup";
import SignInPopup from "../components/SignInPopup";

export default function Home() {
  const [showSignup, setShowSignup] = useState(false);
  const [showSignin, setShowSignin] = useState(false);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <h1 className="text-4xl font-bold mb-8">Welcome to AUTOEVAL360</h1>
      <div className="space-x-4">
        <button
          className="px-6 py-3 bg-blue-900 text-white rounded-md hover:bg-blue-800"
          onClick={() => setShowSignin(true)}
        >
          Sign In
        </button>
        <button
          className="px-6 py-3 border border-blue-900 text-blue-900 rounded-md hover:bg-blue-50"
          onClick={() => setShowSignup(true)}
        >
          Sign Up
        </button>
      </div>

      <SignupPopup isOpen={showSignup} onClose={() => setShowSignup(false)} />
      <SignInPopup
        isOpen={showSignin}
        onClose={() => setShowSignin(false)}
      />

    </div>
  );
}
