"use client";

import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "@/components/service/firebase"
import axios from "axios";
import { useRouter } from "next/navigation";


export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleSubmit = (e) => {
    e.preventDefault();
    
    console.log("Email:", email, "Password:", password);
    signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const token = userCredential.user.accessToken;
    
    sessionStorage.setItem('access_token',token)
    // axios.post('http://192.168.200.56:3000/api/login', { token }).then((res)=>{
    //   const user = userCredential.user;
    //   console.log("hehe",userCredential.user.refreshToken)
    // });
    router.push("/");
    
    
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    console.log(error)
  });

  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-black to-blue-800 relative overflow-hidden">
      {/* Animated Wave Background */}
      <div className="absolute inset-0 opacity-10">
        <svg className="w-full h-full" viewBox="0 0 1440 320">
          <path
            fill="#ffffff"
            fillOpacity="0.2"
            d="M0,224L48,213.3C96,203,192,181,288,165.3C384,149,480,139,576,149.3C672,160,768,192,864,197.3C960,203,1056,181,1152,165.3C1248,149,1344,139,1392,133.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
          >
            <animate
              attributeName="d"
              dur="10s"
              repeatCount="indefinite"
              values="
                M0,224L48,213.3C96,203,192,181,288,165.3C384,149,480,139,576,149.3C672,160,768,192,864,197.3C960,203,1056,181,1152,165.3C1248,149,1344,139,1392,133.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z;
                M0,160L48,181.3C96,203,192,245,288,245.3C384,245,480,203,576,181.3C672,160,768,160,864,165.3C960,171,1056,181,1152,192C1248,203,1344,213,1392,208L1440,202.7L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z;
                M0,224L48,213.3C96,203,192,181,288,165.3C384,149,480,139,576,149.3C672,160,768,192,864,197.3C960,203,1056,181,1152,165.3C1248,149,1344,139,1392,133.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
            />
          </path>
        </svg>
      </div>

      {/* Login Card */}
      <div className="relative z-10 bg-gray-900 p-6 sm:p-8 rounded-xl shadow-2xl w-full max-w-md mx-4 transform transition-all hover:scale-105">
        <h1 className="text-2xl sm:text-3xl font-bold text-center text-white mb-2">
          Get Started Now
        </h1>
        <p className="text-center text-gray-400 mb-4 sm:mb-6 text-sm sm:text-base">
          Join 10,000+ users already thriving with us
        </p>

        <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
          {/* Email Input */}
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-300"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full px-3 sm:px-4 py-2 bg-gray-800 border border-gray-700 text-white rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 hover:border-blue-600"
              placeholder="you@example.com"
              required
            />
          </div>

          {/* Password Input */}
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-300"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-3 sm:px-4 py-2 bg-gray-800 border border-gray-700 text-white rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 hover:border-blue-600"
              placeholder="••••••••"
              required
            />
          </div>

          {/* Login Button */}
          <button
            type="submit"
            className="w-full bg-blue-700 text-white py-2 rounded-lg font-semibold hover:bg-blue-800 transition-all duration-300 transform hover:scale-105"
          >
            Log In
          </button>
        </form>

        {/* Extra Links */}
        <div className="mt-4 text-center text-sm text-gray-400">
          <a
            href="#"
            className="text-blue-400 hover:underline transition-colors duration-200"
          >
            Forgot Password?
          </a>
          <p className="mt-2">
            New here?{" "}
            <a
              href="#"
              className="text-blue-400 hover:underline transition-colors duration-200"
            >
              Sign Up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}