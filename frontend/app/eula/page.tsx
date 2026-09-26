import React from "react";

export default function EULA() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 md:p-12 text-gray-800 dark:text-gray-200">
        <h1 className="text-3xl font-bold mb-2">END-USER LICENSE AGREEMENT (EULA)</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">
          Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
        </p>

        <div className="space-y-6">
          <section>
            <p>
              This End-User License Agreement ("EULA") is a legal agreement between you and MD Broking Private Limited ("Company", "we", "us", or "our") governing your use of the OFS Tracker application and website (the "Software").
            </p>
            <p className="mt-2">
              Please read this EULA carefully before completing the installation process or using the Software. It provides a license to use the Software and contains warranty information and liability disclaimers.
            </p>
            <p className="mt-2 font-semibold">
              By accessing or using the Software, you are confirming your acceptance of the Software and agreeing to become bound by the terms of this EULA agreement.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">1. LICENSE GRANT</h2>
            <p>
              MD Broking Private Limited hereby grants you a personal, non-transferable, non-exclusive, and revocable license to use the OFS Tracker Software on your devices in accordance with the terms of this EULA agreement.
            </p>
            <p className="mt-2">
              You are permitted to load the OFS Tracker Software (for example a PC, laptop, mobile or tablet) under your control. You are responsible for ensuring your device meets the minimum requirements of the OFS Tracker Software.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">2. RESTRICTIONS ON USE</h2>
            <p>You are not permitted to:</p>
            <ul className="list-disc pl-6 mt-2 space-y-1">
              <li>Edit, alter, modify, adapt, translate or otherwise change the whole or any part of the Software nor permit the whole or any part of the Software to be combined with or become incorporated in any other software.</li>
              <li>Reproduce, copy, distribute, resell or otherwise use the Software for any commercial purpose without prior written consent.</li>
              <li>Allow any third party to use the Software on behalf of or for the benefit of any third party.</li>
              <li>Use the Software in any way which breaches any applicable local, national or international law.</li>
              <li>Use the Software for any purpose that MD Broking Private Limited considers is a breach of this EULA agreement.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">3. INTELLECTUAL PROPERTY AND OWNERSHIP</h2>
            <p>
              MD Broking Private Limited shall at all times retain ownership of the Software as originally provided and all subsequent updates. The Software (and the copyright, and other intellectual property rights of whatever nature in the Software, including any modifications made thereto) are and shall remain the property of MD Broking Private Limited.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">4. TERMINATION</h2>
            <p>
              This EULA agreement is effective from the date you first use the Software and shall continue until terminated. You may terminate it at any time upon written notice to MD Broking Private Limited.
            </p>
            <p className="mt-2">
              It will also terminate immediately if you fail to comply with any term of this EULA agreement. Upon such termination, the licenses granted by this EULA agreement will immediately terminate and you agree to stop all access and use of the Software.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">5. LIMITATION OF LIABILITY</h2>
            <p>
              IN NO EVENT WILL THE COMPANY BE LIABLE FOR ANY LOST PROFITS, LOSS OF DATA, OR ANY OTHER DIRECT, INDIRECT, SPECIAL, INCIDENTAL, PUNITIVE, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SOFTWARE, EVEN IF THE COMPANY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2">6. GOVERNING LAW</h2>
            <p>
              This EULA agreement, and any dispute arising out of or in connection with this EULA agreement, shall be governed by and construed in accordance with the laws of India.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
