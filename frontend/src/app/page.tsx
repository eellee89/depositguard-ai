'use client';

import { Shield, FileText, Mail, CheckCircle } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Protect Your Security Deposit
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          AI-powered legal assistance for Texas tenants. Get your deposit back with automated demand letters and certified mail.
        </p>
        <Link 
          href="/new-case"
          className="inline-block bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-700 transition"
        >
          Start Your Case
        </Link>
      </div>

      {/* How It Works */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          How It Works
        </h2>
        <div className="grid md:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <FileText className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">1. Submit Details</h3>
            <p className="text-gray-600">Provide information about your security deposit dispute</p>
          </div>
          
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <Shield className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">2. AI Analysis</h3>
            <p className="text-gray-600">Our AI analyzes Texas Property Code violations</p>
          </div>
          
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">3. Review Letter</h3>
            <p className="text-gray-600">Approve the generated demand letter with statutory citations</p>
          </div>
          
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <Mail className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">4. Certified Mail</h3>
            <p className="text-gray-600">We send via certified mail with tracking</p>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Why DepositGuard AI?</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-lg mb-2">⚖️ Texas Law Expert</h3>
            <p className="text-gray-600">Our AI knows Texas Property Code Chapter 92 inside and out</p>
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-2">💰 Maximize Recovery</h3>
            <p className="text-gray-600">Calculate treble damages + $100 penalty automatically</p>
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-2">📝 Professional Letters</h3>
            <p className="text-gray-600">Attorney-quality demand letters with proper citations</p>
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-2">📬 Certified Mail</h3>
            <p className="text-gray-600">Automatic certified mail with tracking confirmation</p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="text-center bg-primary-600 text-white rounded-lg p-12">
        <h2 className="text-3xl font-bold mb-4">Ready to Get Your Deposit Back?</h2>
        <p className="text-xl mb-6">Start your case in less than 5 minutes</p>
        <Link 
          href="/new-case"
          className="inline-block bg-white text-primary-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100 transition"
        >
          Create Case Now
        </Link>
      </div>

      {/* Disclaimer */}
      <div className="mt-12 text-center text-sm text-gray-500">
        <p>⚠️ This service is not a substitute for legal advice. Consult with an attorney for complex cases.</p>
      </div>
    </div>
  );
}
