import { useApp } from "@modelcontextprotocol/ext-apps/react";
import type { App, McpUiHostContext } from "@modelcontextprotocol/ext-apps"
import { StrictMode, useEffect, useState } from "react";
import type { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { createRoot } from "react-dom/client";
import "./DraftEmailView.css";

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
      className="draft-shell"
      style={{
        paddingTop: hostContext?.safeAreaInsets?.top,
        paddingRight: hostContext?.safeAreaInsets?.right,
        paddingBottom: hostContext?.safeAreaInsets?.bottom,
        paddingLeft: hostContext?.safeAreaInsets?.left,
      }}
    >
        <header className="draft-header">
          <div>
            <h1 className={subject && body ? "draft-title" : "draft-title fading-animate"}>
              {(subject && body) ? "Draft mail is ready" : "Generating Draft mail..."}
            </h1>
          </div>
        </header>
        <article className="email-paper">
          <section className="email-meta" aria-labelledby="email-subject">
            <span className="meta-label">Subject</span>
            <h2 id="email-subject" className="email-subject">{subject ? subject : "Subject is loading..."}</h2>
          </section>
          <section className="email-content" aria-label="Email body">
            <p className="email-body">{body ? body : "Body is loading..."}</p>
            {(subject && body && !decision) && <div className="action-row">
              <button
                type="button"
                className="action-button approve"
                onClick={() => handleDecision("approve")}
              >
                Approve
              </button>
              <button
                type="button"
                className="action-button reject"
                onClick={() => handleDecision("reject")}
              >
                Reject
              </button>
            </div>}
            {decision && (
              <div className="decision-message" role="status" aria-live="polite">
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