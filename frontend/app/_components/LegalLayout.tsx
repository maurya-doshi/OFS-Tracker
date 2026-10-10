import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { ReactNode } from "react";

interface LegalLayoutProps {
  title: string;
  children: ReactNode;
}

export default function LegalLayout({ title, children }: LegalLayoutProps) {
  return (
    <div className="min-h-dvh bg-[#0c0c0c]">
      {/* Back nav */}
      <div className="max-w-4xl mx-auto px-6 pt-8 pb-2">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-xs text-[#505050] hover:text-[#a0a0a0] transition-colors group"
        >
          <ArrowLeft
            size={13}
            strokeWidth={1.75}
            className="group-hover:-translate-x-0.5 transition-transform"
          />
          Back to dashboard
        </Link>
      </div>

      {/* Content card */}
      <div className="max-w-4xl mx-auto px-6 py-6 pb-16">
        <div className="bg-[#111111] border border-[#1e1e1e] rounded-lg p-8 md:p-12">
          <h1 className="text-xl font-semibold text-[#f2f2f2] mb-1">{title}</h1>
          <p className="text-[11px] text-[#404040] mb-10">
            Last updated:{" "}
            {new Date().toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </p>

          <div className="text-[#808080]">{children}</div>
        </div>
      </div>
    </div>
  );
}
