"use client";

import { useState } from "react";
import Link from "next/link";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);

  return (
    <nav className="bg-blue-900 text-white sticky top-0 z-20 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold">
              Quizzy
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              href="/"
              className="hover:text-blue-400 transition-colors duration-200"
            >
              Home
            </Link>
            <Link
              href="/features"
              className="hover:text-blue-400 transition-colors duration-200"
            >
              Features
            </Link>
            <Link
              href="/pricing"
              className="hover:text-blue-400 transition-colors duration-200"
            >
              Pricing
            </Link>
            <Link
              href="/contact"
              className="hover:text-blue-400 transition-colors duration-200"
            >
              Contact
            </Link>
            <Link
              href="/login"
              className="bg-blue-700 px-4 py-2 rounded-lg hover:bg-blue-800 transition-all duration-300"
            >
              Log In
            </Link>
          </div>

          {/* Mobile Hamburger */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMenu}
              className="text-white focus:outline-none"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                {isOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16m-7 6h7"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <div
        className={`md:hidden transition-all duration-300 ease-in-out ${
          isOpen ? "max-h-64 opacity-100" : "max-h-0 opacity-0 overflow-hidden"
        }`}
      >
        <div className="bg-blue-900 px-2 pt-2 pb-3 space-y-1">
          <Link
            href="/"
            className="block px-3 py-2 text-white hover:bg-blue-800 rounded-md transition-colors duration-200"
            onClick={toggleMenu}
          >
            Home
          </Link>
          <Link
            href="/features"
            className="block px-3 py-2 text-white hover:bg-blue-800 rounded-md transition-colors duration-200"
            onClick={toggleMenu}
          >
            Features
          </Link>
          <Link
            href="/pricing"
            className="block px-3 py-2 text-white hover:bg-blue-800 rounded-md transition-colors duration-200"
            onClick={toggleMenu}
          >
            Pricing
          </Link>
          <Link
            href="/contact"
            className="block px-3 py-2 text-white hover:bg-blue-800 rounded-md transition-colors duration-200"
            onClick={toggleMenu}
          >
            Contact
          </Link>
          <Link
            href="/login"
            className="block px-3 py-2 bg-blue-700 text-white rounded-md hover:bg-blue-800 transition-all duration-200"
            onClick={toggleMenu}
          >
            Log In
          </Link>
        </div>
      </div>
    </nav>
  );
}