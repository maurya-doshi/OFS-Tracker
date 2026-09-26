import React from "react";

export default function Disclaimer() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 md:p-12 text-gray-800 dark:text-gray-200">
        <h1 className="text-3xl font-bold mb-2">DISCLAIMER</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">
          Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
        </p>

        <div className="space-y-8">
          <section>
            <h2 className="text-xl font-bold mb-3">1. NOT FINANCIAL ADVICE</h2>
            <p>
              The information provided by MD Broking Private Limited ("we," "us," or "our") on the OFS Tracker website (the "Site") is for general informational purposes only. All information on the Site is provided in good faith, however, we make no representation or warranty of any kind, express or implied, regarding the accuracy, adequacy, validity, reliability, availability, or completeness of any information on the Site.
            </p>
            <p className="mt-4 font-semibold text-red-500 dark:text-red-400">
              UNDER NO CIRCUMSTANCE SHALL WE HAVE ANY LIABILITY TO YOU FOR ANY LOSS OR DAMAGE OF ANY KIND INCURRED AS A RESULT OF THE USE OF THE SITE OR RELIANCE ON ANY INFORMATION PROVIDED ON THE SITE. YOUR USE OF THE SITE AND YOUR RELIANCE ON ANY INFORMATION ON THE SITE IS SOLELY AT YOUR OWN RISK.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-3">2. DATA ACCURACY AND DELAYS</h2>
            <p>
              The OFS Tracker aggregates data from the public APIs of the National Stock Exchange of India (NSE) and Bombay Stock Exchange (BSE). We do not control this data. The market data, statistics, and ladder information displayed may be delayed, inaccurate, interrupted, or out of date. 
            </p>
            <p className="mt-4">
              We strongly advise you to verify all pricing, bidding, and stock information independently with the respective exchanges or your registered broker before executing any financial trades or making any investment decisions.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-3">3. "AS IS" AND "AS AVAILABLE" DISCLAIMER</h2>
            <p>
              The Site and its services are provided on an "AS IS" and "AS AVAILABLE" basis. We disclaim all warranties of any kind, whether express or implied, including, but not limited to, the implied warranties of merchantability, fitness for a particular purpose, and non-infringement. We do not guarantee that the Site will be uninterrupted, timely, secure, or error-free.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-3">4. CONTACT US</h2>
            <p>
              If you have any questions regarding this Disclaimer, you can contact us at:
            </p>
            <address className="mt-4 not-italic bg-gray-100 dark:bg-gray-700 p-4 rounded-md">
              MD Broking Private Limited<br />
              Office No. 401, 4th Floor, Gandhi Bhavan<br />
              14 Panchnath Plot, Harihar Chowk<br />
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
