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

const extractToolResult = (callToolResult: CallToolResult): string => {
    const { text } = callToolResult.content?.find(c => c.type === "text")!;
    return text;
}

interface DraftEmailViewInnerProps {
  app: App;
  toolResult: CallToolResult | null;
  hostContext?: McpUiHostContext;
}

export const DraftEmailViewInner = ({ toolResult, hostContext }: DraftEmailViewInnerProps) => {
    const [subject, setSubject] = useState<string>("Subject is loading...")
    const [body, setBody] = useState<string>("Body is loading...")

    useEffect(() => {
    if (toolResult) {
      setSubject(extractToolResult(toolResult));
      setBody(extractToolResult(toolResult));
    }
  }, [toolResult]);

    return (
    <main
      style={{
        paddingTop: hostContext?.safeAreaInsets?.top,
        paddingRight: hostContext?.safeAreaInsets?.right,
        paddingBottom: hostContext?.safeAreaInsets?.bottom,
        paddingLeft: hostContext?.safeAreaInsets?.left,
      }}
    >
        <pre>Email Subject: {subject}</pre>
        <pre>Email Body: {body}</pre>
    </main>
    )
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <DraftEmailView />
  </StrictMode>
);