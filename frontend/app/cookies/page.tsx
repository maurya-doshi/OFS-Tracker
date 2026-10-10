import React from "react";
import LegalLayout from "../_components/LegalLayout";

export default function CookiePolicy() {
  return (
    <LegalLayout title="Cookie policy">
      <div className="space-y-8 text-sm leading-relaxed">
        <section>
          <p className="mb-4 text-gray-400">
            This Cookie Policy explains how{" "}
            <strong className="text-gray-300">MD Broking Private Limited</strong> uses cookies and
            similar technologies to recognise you when you visit our website at{" "}
            <a
              href="https://ofs-tracker.onrender.com"
              className="text-emerald-500 hover:text-emerald-400 underline underline-offset-2 transition-colors"
            >
              https://ofs-tracker.onrender.com
            </a>
            . It explains what these technologies are and why we use them, as well as your rights
            to control their use.
          </p>
          <p className="text-gray-400">
            In some cases we may use cookies to collect personal information, or information that
            becomes personal when combined with other data.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">What are cookies?</h2>
          <p className="mb-3 text-gray-400">
            Cookies are small data files placed on your device when you visit a website. They are
            widely used to make websites work or work more efficiently, and to provide information
            to website owners.
          </p>
          <p className="text-gray-400">
            Cookies set by the website owner are called "first-party cookies." Cookies set by
            parties other than the website owner are "third-party cookies," which enable features
            or functionality provided on or through the website.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">Why do we use cookies?</h2>
          <p className="text-gray-400">
            We use first- and third-party cookies for several reasons. Some are required for
            technical reasons ("essential" or "strictly necessary" cookies). Others enable us to
            track and target user interests to enhance experience on our website.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">How can I control cookies?</h2>
          <p className="mb-3 text-gray-400">
            You have the right to decide whether to accept or reject cookies. Essential cookies
            cannot be rejected as they are strictly necessary to provide the service.
          </p>
          <p className="mb-3 text-gray-400">
            If you reject cookies, you may still use our website though your access to some
            functionality may be restricted. You may also set or amend your web browser controls
            to accept or refuse cookies.
          </p>
          <p className="text-gray-400">
            For information on managing cookies in your browser, visit your browser&apos;s help
            menu or these specific guides:
          </p>
          <ul className="list-disc pl-5 space-y-1.5 mt-3 text-gray-400">
            {[
              { name: "Chrome", href: "https://support.google.com/chrome/answer/95647#zippy=%2Callow-or-block-cookies" },
              { name: "Internet Explorer", href: "https://support.microsoft.com/en-us/windows/delete-and-manage-cookies-168dab11-0753-043d-7c16-ede5947fc64d" },
              { name: "Firefox", href: "https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop?redirectslug=enable-and-disable-cookies-website-preferences&redirectlocale=en-US" },
              { name: "Safari", href: "https://support.apple.com/en-ie/guide/safari/sfri11471/mac" },
              { name: "Edge", href: "https://support.microsoft.com/en-us/windows/microsoft-edge-browsing-data-and-privacy-bb8174ba-9d73-dcf2-9b4a-c582b4e640dd" },
              { name: "Opera", href: "https://help.opera.com/en/latest/web-preferences/" },
            ].map(({ name, href }) => (
              <li key={name}>
                <a
                  href={href}
                  className="text-emerald-500 hover:text-emerald-400 underline underline-offset-2 transition-colors"
                  target="_blank"
                  rel="noreferrer"
                >
                  {name}
                </a>
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">
            What about other tracking technologies?
          </h2>
          <p className="text-gray-400">
            We may use web beacons (tracking pixels or clear gifs) — tiny graphics files that
            contain a unique identifier to recognise website visits. These are often reliant on
            cookies to function properly, so declining cookies will impair their functioning.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">Do you serve targeted advertising?</h2>
          <p className="text-gray-400">
            Third parties may serve cookies on your device to serve advertising through our
            website. These companies may use information about your visits to provide relevant
            advertisements. The information collected does not enable us or them to identify your
            name or contact details unless you choose to provide them.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">How often will this policy be updated?</h2>
          <p className="mb-2 text-gray-400">
            We may update this Cookie Policy from time to time to reflect changes to the cookies
            we use or for other operational, legal, or regulatory reasons. Please revisit this
            policy regularly.
          </p>
          <p className="text-gray-400">
            The date at the top of this policy indicates when it was last updated.
          </p>
        </section>

        <section>
          <h2 className="text-base font-semibold text-white mb-3">Where can I get further information?</h2>
          <p className="mb-3 text-gray-400">
            If you have questions about our use of cookies or other technologies, contact us at:
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
              href="tel:9773291032"
              className="text-emerald-500 hover:text-emerald-400 underline underline-offset-2 transition-colors"
            >
              +91 97732 91032
            </a>
          </address>
        </section>
      </div>
    </LegalLayout>
  );
}

