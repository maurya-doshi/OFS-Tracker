import React from "react";
import LegalLayout from "../_components/LegalLayout";

export default function TermsAndConditions() {
  return (
    <LegalLayout title="Terms and conditions">
      <div className="space-y-8 text-sm leading-relaxed">
        <section>
          <h2 className="text-base font-semibold text-white mb-3">1. Agreement to terms</h2>
          <p className="mb-3 text-gray-400">
            These Terms and Conditions constitute a legally binding agreement between you and{" "}
            <strong className="text-gray-300">MD Broking Private Limited</strong> ("we," "us," or
            "our"), concerning your access to and use of{" "}
            <a
              href="https://ofs-tracker.onrender.com"
              className="text-emerald-500 hover:text-emerald-400 underline underline-offset-2 transition-colors"
            >
              https://ofs-tracker.onrender.com
            </a>
            .
          </p>
          <p className="text-gray-400">
            By accessing the site, you agree that you have read, understood, and agreed to be
            bound by all of these Terms and Conditions. If you do not agree, you must discontinue
            use immediately.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">2. Intellectual property rights</h2>
          <p className="text-gray-400">
            Unless otherwise indicated, the site is our proprietary property and all source code,
            databases, functionality, software, website designs, text, and graphics are owned or
            controlled by us, and are protected by copyright and trademark laws.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">3. Prohibited activities</h2>
          <p className="mb-2 text-gray-400">
            You may not access or use the site for any purpose other than that for which we make
            it available. Prohibited activities include:
          </p>
          <ul className="list-disc pl-5 mt-2 space-y-1.5 text-gray-400">
            <li>Systematically retrieving data to create a collection or database without permission.</li>
            <li>Circumventing, disabling, or interfering with security-related features of the site.</li>
            <li>Engaging in unauthorised framing of or linking to the site.</li>
            <li>Interfering with or disrupting the site or connected networks.</li>
            <li>Decompiling, disassembling, or reverse engineering any software on the site.</li>
            <li>Using any automated system including spiders, robots, or scrapers to access the site.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">4. Site management and modifications</h2>
          <p className="text-gray-400">
            We reserve the right to monitor the site for violations, take legal action against
            those who violate the law or these terms, refuse or restrict access, and otherwise
            manage the site to protect our rights and property.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">
            5. Financial disclaimer and data accuracy
          </h2>
          <p className="mb-3 text-gray-400">
            The OFS Tracker aggregates data from public APIs of NSE and BSE. We do not control
            this data. The market data, statistics, and ladder information displayed may be
            delayed, inaccurate, interrupted, or out of date.
          </p>
          <p className="mb-3 text-gray-400">
            The information provided is for general informational purposes only and does{" "}
            <strong className="text-gray-300">not</strong> constitute financial, investment, or
            trading advice. Verify all pricing and bidding information independently with the
            respective exchanges or your registered broker before making any financial decisions.
          </p>
          <p className="font-medium text-red-400 bg-red-500/8 border border-red-500/20 rounded-lg px-4 py-3">
            Under no circumstance shall we have any liability for any loss or damage incurred as a
            result of using the site or relying on any information provided. Your use of the site
            is solely at your own risk.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">6. Governing law</h2>
          <p className="text-gray-400">
            These Terms shall be governed by the laws of India. MD Broking Private Limited and
            yourself irrevocably consent to the exclusive jurisdiction of the courts of Rajkot,
            Gujarat, India to resolve any dispute arising in connection with these terms.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">7. Contact us</h2>
          <p className="mb-3 text-gray-400">
            To resolve a complaint or receive further information regarding use of the site:
          </p>
          <address className="not-italic bg-gray-800/50 border border-gray-700/50 p-4 rounded-lg text-gray-400">
            MD Broking Private Limited
            <br />
            Office No. 401, 4th Floor, Gandhi Bhavan
            <br />
            Rajkot, Gujarat 360001
            <br />
            India
            <br />
            <a
              href="mailto:mauryadoshi@gmail.com"
              className="text-emerald-500 hover:text-emerald-400 underline underline-offset-2 transition-colors"
            >
              mauryadoshi@gmail.com
            </a>
          </address>
        </section>
      </div>
    </LegalLayout>
  );
}

