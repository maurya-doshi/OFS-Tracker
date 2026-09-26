import React from "react";

export default function TermsAndConditions() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 md:p-12 text-gray-800 dark:text-gray-200">
        <h1 className="text-3xl font-bold mb-2">TERMS AND CONDITIONS</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">
          Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
        </p>

        <div className="space-y-6">
          <section>
            <h2 className="text-xl font-bold mb-2">1. AGREEMENT TO TERMS</h2>
            <p>
              These Terms and Conditions constitute a legally binding agreement made between you, whether personally or on behalf of an entity ("you") and MD Broking Private Limited ("we," "us," or "our"), concerning your access to and use of the OFS Tracker website (https://ofs-tracker.onrender.com) as well as any other media form, media channel, mobile website, or mobile application related, linked, or otherwise connected thereto (collectively, the "Site").
            </p>
            <p className="mt-2">
              By accessing the Site, you agree that you have read, understood, and agreed to be bound by all of these Terms and Conditions. IF YOU DO NOT AGREE WITH ALL OF THESE TERMS AND CONDITIONS, THEN YOU ARE EXPRESSLY PROHIBITED FROM USING THE SITE AND YOU MUST DISCONTINUE USE IMMEDIATELY.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">2. INTELLECTUAL PROPERTY RIGHTS</h2>
            <p>
              Unless otherwise indicated, the Site is our proprietary property and all source code, databases, functionality, software, website designs, audio, video, text, photographs, and graphics on the Site (collectively, the "Content") and the trademarks, service marks, and logos contained therein (the "Marks") are owned or controlled by us or licensed to us, and are protected by copyright and trademark laws and various other intellectual property rights.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">3. PROHIBITED ACTIVITIES</h2>
            <p>
              You may not access or use the Site for any purpose other than that for which we make the Site available. The Site may not be used in connection with any commercial endeavors except those that are specifically endorsed or approved by us.
            </p>
            <ul className="list-disc pl-6 mt-2 space-y-1">
              <li>Systematically retrieve data or other content from the Site to create or compile, directly or indirectly, a collection, compilation, database, or directory without written permission from us.</li>
              <li>Circumvent, disable, or otherwise interfere with security-related features of the Site.</li>
              <li>Engage in unauthorized framing of or linking to the Site.</li>
              <li>Interfere with, disrupt, or create an undue burden on the Site or the networks or services connected to the Site.</li>
              <li>Decipher, decompile, disassemble, or reverse engineer any of the software comprising or in any way making up a part of the Site.</li>
              <li>Use any automated system, including without limitation, any spider, robot, cheat utility, scraper, or offline reader that accesses the Site.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">4. SITE MANAGEMENT AND MODIFICATIONS</h2>
            <p>
              We reserve the right, but not the obligation, to: (1) monitor the Site for violations of these Terms and Conditions; (2) take appropriate legal action against anyone who, in our sole discretion, violates the law or these Terms and Conditions; (3) refuse, restrict access to, limit the availability of, or disable (to the extent technologically feasible) any of your Contributions or any portion thereof; (4) otherwise manage the Site in a manner designed to protect our rights and property and to facilitate the proper functioning of the Site.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">5. GOVERNING LAW</h2>
            <p>
              These Terms shall be governed by and defined following the laws of India. MD Broking Private Limited and yourself irrevocably consent that the courts of Rajkot, Gujarat, India shall have exclusive jurisdiction to resolve any dispute which may arise in connection with these terms.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">6. CONTACT US</h2>
            <p>
              In order to resolve a complaint regarding the Site or to receive further information regarding use of the Site, please contact us at:
            </p>
            <address className="mt-4 not-italic bg-gray-100 dark:bg-gray-700 p-4 rounded-md">
              MD Broking Private Limited<br />
              Office No. 401, 4th Floor, Gandhi Bhavan<br />
              Rajkot, Gujarat 360001<br />
              India<br />
              Email: mauryadoshi@gmail.com
            </address>
          </section>
        </div>
      </div>
    </div>
  );
}
