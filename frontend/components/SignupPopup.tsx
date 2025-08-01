"use client";

import { Dialog } from "@headlessui/react";
import { useState } from "react";
import toast from "react-hot-toast";
import {
  FaUser,
  FaEnvelope,
  FaLock,
  FaPhone,
  FaGlobe,
  FaCity,
  FaIdBadge,
} from "react-icons/fa";
import { siteConfig } from "./siteConfig";

interface SignupPopupProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function SignupPopup({ isOpen, onClose }: SignupPopupProps) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [title, setTitle] = useState("");
  const [role, setRole] = useState<"student" | "educator" | "admin">("student");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [institute, setInstitute] = useState("");
  const [officialEmail, setOfficialEmail] = useState("");
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const passwordIsValid = password.length >= 6;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (
      !firstName ||
      !lastName ||
      !title ||
      !username ||
      !password ||
      !email ||
      !phone
    ) {
      toast.error("Please fill in all required fields.");
      return;
    }
    if (!passwordIsValid) {
      toast.error("Password must be at least 6 characters.");
      return;
    }

    setSubmitting(true);
    try {
      const res = await fetch("/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          title,
          role,
          username,
          password,
          email,
          phone_number: phone,
          address: address || undefined,
          city: city || undefined,
          country: country || undefined,
          official_email: officialEmail || undefined,
          education_institute: institute || undefined,
          registration_number: registrationNumber || undefined,
        }),
      });

      const json = await res.json();

      if (!res.ok) {
        toast.error(json.error || "Signup failed");
      } else if ((json as any).existing) {
        toast("You already have an account — please sign in.", {
          icon: "ℹ️",
        });
        onClose();
      } else {
        toast.success("Account created successfully!");
        onClose();
      }
    } catch (err: any) {
      console.error("Signup error:", err);
      toast.error(err.message || "Failed to sign up");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={isOpen} onClose={onClose} className="relative z-50">
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <Dialog.Panel className="w-full max-w-4xl bg-white rounded-lg shadow-lg flex overflow-hidden">
          {/* Left Section */}
          <div className="bg-blue-900 text-white w-1/3 p-8 hidden md:block">
            <h2 className="text-3xl font-bold mb-4">WELCOME TO AUTOEVAL360</h2>
            <p className="text-sm">Your Smart Exam Partner</p>
            <p className="mt-4 text-sm opacity-90">
              Join {siteConfig.title} to streamline your exam creation,
              delivery, and grading. Experience intelligent automation,
              real-time insights, and seamless results — all in one place.
            </p>
          </div>

          {/* Right Section */}
          <div className="w-full md:w-2/3 p-8 overflow-y-auto max-h-[90vh]">
            <Dialog.Title className="text-2xl font-bold text-blue-900 mb-6">
              Sign Up
            </Dialog.Title>

            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
              {/* -- form inputs as provided -- */}
              {/* For brevity, copy exactly from your original SignupPopup */}

              {/* ... */}
            </form>
          </div>
        </Dialog.Panel>
      </div>
    </Dialog>
  );
}
