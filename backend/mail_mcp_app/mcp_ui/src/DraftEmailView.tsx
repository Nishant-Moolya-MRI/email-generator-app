import { useApp } from "@modelcontextprotocol/ext-apps/react";
import type { App, McpUiHostContext } from "@modelcontextprotocol/ext-apps"
import { StrictMode, useEffect, useState } from "react";
import type { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { createRoot } from "react-dom/client";

export const DraftEmailView = () => {
  const [toolResult, setToolResult] = useState<CallToolResult | null>(null);
  const [hostContext, setHostContext] = useState<McpUiHostContext | undefined>();

  // `useApp` (1) creates an `App` instance, (2) calls `onAppCreated` to
  // register handlers, and (3) calls `connect()` on the `App` instance.
  const { app, error } = useApp({
    appInfo: { name: "Draft Email View", version: "1.0.0" },
    capabilities: {},
    onAppCreated: (app) => {
      app.onteardown = async () => {
        console.info("App is being torn down");
        return {};
      };
      app.ontoolinput = async (input) => {
        console.info("Received tool call input:", input);
      };

      app.ontoolresult = async (result) => {
        console.info("Received tool call result:", result);
        setToolResult(result);
      };

      app.ontoolcancelled = (params) => {
        console.info("Tool call cancelled:", params.reason);
      };

      app.onerror = console.error;

      app.onhostcontextchanged = (params) => {
        setHostContext((prev) => ({ ...prev, ...params }));
      };
    },
  });

  useEffect(() => {
    if (app) {
      setHostContext(app.getHostContext());
    }
  }, [app]);

  if (error) return <div><strong>ERROR:</strong> {error.message}</div>;
  if (!app) return <div>Connecting...</div>;

  return <DraftEmailViewInner app={app} toolResult={toolResult} hostContext={hostContext} />;
}

interface DraftEmailViewInnerProps {
  app: App;
  toolResult: CallToolResult | null;
  hostContext?: McpUiHostContext;
}

export const DraftEmailViewInner = ({ toolResult, hostContext }: DraftEmailViewInnerProps) => {
    const [subject, setSubject] = useState<string | null>(null)
    const [body, setBody] = useState<string | null>(null)
    const [decision, setDecision] = useState<string | null>(null)

    useEffect(() => {
    const content = toolResult?.structuredContent;
    if (content && typeof content === "object") {
      const email = content as { subject: string; body_content: string };
      setSubject(typeof email.subject === "string" ? email.subject : "");
      setBody(typeof email.body_content === "string" ? email.body_content : "");
    }
  }, [toolResult]);

    const handleDecision = (action: "approve" | "reject") => {
      setDecision(
        action === "approve"
          ? "Approved: This draft is ready to send."
          : "Rejected: Please revise the message before sending."
      );
    };

    return (
    <main
      className="min-h-svh box-border w-full bg-[radial-gradient(circle_at_15%_0%,rgba(212,107,63,0.1),transparent_32rem)] bg-[#f4f6f8] px-4 py-6 text-left text-[#172033] sm:px-8 sm:py-10 lg:px-12"
      style={{
        paddingTop: hostContext?.safeAreaInsets?.top,
        paddingRight: hostContext?.safeAreaInsets?.right,
        paddingBottom: hostContext?.safeAreaInsets?.bottom,
        paddingLeft: hostContext?.safeAreaInsets?.left,
      }}
    >
        <header className="mb-7 flex items-start justify-between gap-6 max-sm:mb-5">
          <div>
            <h1 className={`m-0 font-[Georgia,'Times_New_Roman',serif] text-[clamp(30px,5vw,48px)] font-normal leading-[1.05] tracking-normal ${subject && body ? "" : "animate-pulse"}`}>
              {(subject && body) ? "Draft mail is ready" : "Generating Draft mail..."}
            </h1>
          </div>
        </header>
        <article className="overflow-hidden rounded-lg border border-[#dbe2ea] bg-white text-left shadow-[0_20px_50px_rgba(29,43,63,0.1)]">
          <section className="border-b border-[#dbe2ea] bg-[#fbfcfd] px-[clamp(22px,5vw,48px)] pb-5.5 pt-6.5" aria-labelledby="email-subject">
            <span className="mb-2.25 block font-sans text-[11px] font-bold uppercase tracking-[1.2px] text-[#687386]">Subject</span>
            <h2 id="email-subject" className="m-0 wrap-break-word font-[Georgia,'Times_New_Roman',serif] text-[clamp(22px,4vw,32px)] font-normal leading-[1.2] text-[#172033]">{subject ? subject : "Subject is loading..."}</h2>
          </section>
          <section className="px-[clamp(22px,5vw,48px)] pb-10.5 pt-8 max-sm:pt-6.5" aria-label="Email body">
            <p className="m-0 wrap-break-word whitespace-pre-wrap font-[Georgia,'Times_New_Roman',serif] text-[17px] leading-[1.75] text-[#3e4a5c]">{body ? body : "Body is loading..."}</p>
            {(subject && body && !decision) && <div className="mt-5.5 flex flex-wrap justify-end gap-3">
              <button
                type="button"
                className="cursor-pointer rounded-full border-0 bg-[#1f8f5f] px-4.5 py-2 font-[Georgia,'Times_New_Roman',serif] font-bold text-white transition-transform duration-150 hover:-translate-y-px"
                onClick={() => handleDecision("approve")}
              >
                Approve
              </button>
              <button
                type="button"
                className="cursor-pointer rounded-full border-0 bg-[#c4463a] px-4.5 py-2 font-[Georgia,'Times_New_Roman',serif] font-bold text-white transition-transform duration-150 hover:-translate-y-px"
                onClick={() => handleDecision("reject")}
              >
                Reject
              </button>
            </div>}
            {decision && (
              <div className="mt-4.5 rounded-[10px] border border-[#cfe0ff] bg-[#f1f7ff] px-3.5 py-3 font-semibold text-[#214a7b]" role="status" aria-live="polite">
                {decision}
              </div>
            )}
          </section>
        </article>
    </main>
    )
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <DraftEmailView />
  </StrictMode>
);