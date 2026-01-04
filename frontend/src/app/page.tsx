'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function LandingPage() {
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  const features = [
    {
      id: 'checklist',
      title: 'Smart Course Checklist',
      description: 'Track your BCS degree requirements with an interactive, hierarchical checklist.',
      details: 'Organize your courses by specialization and course categories. See your progress at a glance with visual indicators for completed requirements.',
      icon: '✓',
    },
    {
      id: 'search',
      title: 'Course Search & Discovery',
      description: 'Easily search and add courses to your degree plan.',
      details: 'Search courses by code and number, then add them to your taken, planned, or wishlist categories. Get instant feedback on course prerequisites.',
      icon: '🔍',
    },
    {
      id: 'planning',
      title: 'Flexible Course Planning',
      description: 'Plan your courses across different categories to match your schedule.',
      details: 'Organize courses into "Taken", "Planned", and "Wishlist" sections. See your progress update automatically as you add or remove courses.',
      icon: '📋',
    },
    {
      id: 'progress',
      title: 'Progress Tracking',
      description: 'Monitor your degree completion at a glance.',
      details: 'Watch your progress bar fill as you complete courses. See which requirements are done and which still need work.',
      icon: '📊',
    },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">UWPathr</h1>
          <div className="flex items-center gap-6">
            <div className="relative group">
              <button className="text-gray-700 hover:text-gray-900 font-medium flex items-center gap-2">
                Resources
                <svg
                  className="w-4 h-4 transition-transform group-hover:rotate-180"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute left-0 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                <a href="https://cs.uwaterloo.ca" target="_blank" rel="noopener noreferrer" className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors">UW CS Home Page</a>
                <a href="https://uwaterloo.ca/computer-science/advising" target="_blank" rel="noopener noreferrer" className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors border-t border-gray-100">Academic Advising</a>
                <a href="https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/home" target="_blank" rel="noopener noreferrer" className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors border-t border-gray-100">Academic Calendar</a>
                <a href="mailto:info@uwpathr.rocks" className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors border-t border-gray-100">Support</a>
              </div>
            </div>
            <Link
              href="/auth/login"
              className="text-gray-700 hover:text-gray-900 font-medium"
            >
              Login
            </Link>
            <Link
              href="/auth/register"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Register
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Plan Your CS Degree with Confidence
          </h2>
          <p className="text-xl text-gray-700 mb-8 max-w-3xl mx-auto">
            UWPathr is your personal guide to completing your Bachelor of Computer Science degree at the University of Waterloo. Discover courses and stay on top of your progress without worrying about missing requirements.
          </p>
          <Link
            href="/auth/register"
            className="inline-block px-8 py-3 bg-blue-600 text-white text-lg font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Get Started
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-gray-900 mb-12 text-center">
            Key Features
          </h3>
          
          <div className="space-y-4">
            {features.map((feature) => (
              <div
                key={feature.id}
                className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow"
              >
                <button
                  onClick={() =>
                    setExpandedSection(
                      expandedSection === feature.id ? null : feature.id
                    )
                  }
                  className="w-full px-6 py-4 flex items-start justify-between hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start gap-4 text-left">
                    <div className="text-3xl pt-1">{feature.icon}</div>
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900">
                        {feature.title}
                      </h4>
                      <p className="text-gray-600 mt-1">{feature.description}</p>
                    </div>
                  </div>
                  <svg
                    className={`w-5 h-5 text-gray-400 flex-shrink-0 transition-transform mt-1 ${
                      expandedSection === feature.id ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 14l-7 7m0 0l-7-7m7 7V3"
                    />
                  </svg>
                </button>

                {expandedSection === feature.id && (
                  <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
                    <p className="text-gray-700">{feature.details}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How to Use Section */}
      <section className="bg-gray-50 py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-gray-900 mb-12 text-center">
            How to Use UWPathr
          </h3>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white font-semibold text-sm">
                  1
                </div>
                <h4 className="text-lg font-semibold text-gray-900">
                  Access Your Checklist
                </h4>
              </div>
              <p className="text-gray-700">
                Navigate to the Checklist page to see all the requirements for your chosen specialization. Your progress is displayed right at the top with a progress bar and percentage.
              </p>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white font-semibold text-sm">
                  2
                </div>
                <h4 className="text-lg font-semibold text-gray-900">
                  Search for Courses
                </h4>
              </div>
              <p className="text-gray-700">
                Use the Search Courses button in the sidebar to find courses. Type the course code, then a space, then the course number to filter results.
              </p>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white font-semibold text-sm">
                  3
                </div>
                <h4 className="text-lg font-semibold text-gray-900">
                  Add Courses to Lists
                </h4>
              </div>
              <p className="text-gray-700">
                Select a course and choose whether to add it to "Taken", "Planned", or "Wishlist". Your checklist will update automatically to reflect your selections.
              </p>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white font-semibold text-sm">
                  4
                </div>
                <h4 className="text-lg font-semibold text-gray-900">
                  Track Your Progress
                </h4>
              </div>
              <p className="text-gray-700">
                Watch your progress bar fill up as you mark courses as taken. When you've completed all requirements, you'll see a checkmark next to your progress.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white py-16 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <h3 className="text-3xl font-bold mb-4">Ready to Plan Your Degree?</h3>
          <p className="text-lg mb-8 text-blue-100">
            Start using UWPathr today to stay organized and on track with your CS degree.
          </p>
          <Link
            href="/dashboard"
            className="inline-block px-8 py-3 bg-white text-blue-600 font-medium rounded-lg hover:bg-gray-100 transition-colors"
          >
            Open Dashboard
          </Link>
        </div>
      </section>

      {/* Disclaimer Section */}
      <section className="bg-amber-50 border-t border-amber-200 py-8 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="bg-white border border-amber-200 rounded-lg p-6">
            <p className="text-sm text-amber-900">
              <strong>Disclaimer:</strong> UWPathr is an unofficial planning tool and is not a substitute for official degree regulations. Students are responsible for discussing their academic plans with their academic advisors and ensuring they officially meet all degree requirements. Always refer to the official University of Waterloo academic calendar and degree requirements.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <p>&copy; 2026 UWPathr. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
