/**
 * Supply Chain Control Tower — Root App
 * Clean CopilotKit-only implementation (no Hashbrown dependency).
 *
 * The Shadify aesthetic:
 *  - Lavender-gray background
 *  - Centered white rounded card
 *  - "How can I help you today?" heading (shown when empty)
 *  - Suggestion pills below input
 */

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import "./index.css";

import React from 'react';

const RUNTIME_URL = "http://localhost:8000/api/copilotkit";

const SUGGESTIONS = [
  "Give me a complete supply chain status report",
  "Which SKUs are at risk of stock-out?",
  "Compare our top suppliers",
  "Show demand trends",
  "Active logistics risks",
];

const SYSTEM_INSTRUCTIONS = `You are the Supply Chain Orchestrator.
Use the task_dispatcher tool to delegate work to inventory, demand, logistics, supplier, and risk agents.
Always synthesize their responses into a clear, structured final answer.`;

export default function App() {
  return (
    <div style={{ height: '100vh', width: '100vw', display: 'flex', flexDirection: 'column' }}>
      <CopilotKit runtimeUrl={RUNTIME_URL} agent="supply_chain_orchestrator">
        <div className="sc-shell">

            {/* ── Top bar ── */}
            <div className="sc-topbar">
              <div className="sc-logo-icons">
                <div className="sc-logo-icon">🏭</div>
                <div className="sc-logo-icon">📦</div>
                <div className="sc-logo-icon">🚢</div>
              </div>
              <span className="sc-divider">|</span>
              <span className="sc-brand">ControlTower</span>
              <div className="sc-status">
                <span className="sc-dot" />
                Agent online
              </div>
            </div>

            {/* ── Chat area ── */}
            <div className="sc-chat-wrap">
              <div className="sc-chat-card">
                <div className="sc-copilot-wrap">
                  <CopilotChat
                    className="copilotKitChat"
                    instructions={SYSTEM_INSTRUCTIONS}
                    labels={{
                      initial: "How can I help you today?",
                      placeholder: "Type a message...",
                    }}
                  />
                </div>

                <div className="sc-disclaimer">
                  AI can make mistakes. Please verify important information.
                </div>

                <div className="sc-pills">
                  {SUGGESTIONS.map((text) => (
                    <button key={text} className="sc-pill">{text}</button>
                  ))}
                </div>
              </div>
            </div>

          </div>
        </CopilotKit>
    </div>
  );
}
