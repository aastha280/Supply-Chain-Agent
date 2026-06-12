Here's every relevant CopilotKit + LangGraph doc link, organized by category so you can navigate directly to what you need.

---

## Entry points

| Page | URL |
|---|---|
| LangGraph overview | https://docs.copilotkit.ai/langgraph |
| Quickstart (LangGraph) | https://docs.copilotkit.ai/langgraph/quickstart |
| LangGraph concept explainer | https://docs.copilotkit.ai/langgraph/concepts/langgraph |
| Deep Agents | https://docs.copilotkit.ai/langgraph/deep-agents |
| Subgraphs (multi-agent) | https://docs.copilotkit.ai/langgraph/subgraphs |

---

## Core features — LangGraph path

| Feature | URL |
|---|---|
| Shared State | https://docs.copilotkit.ai/langgraph/shared-state |
| State inputs & outputs | https://docs.copilotkit.ai/langgraph/shared-state/state-inputs-outputs |
| Generative UI (overview) | https://docs.copilotkit.ai/langgraph/generative-ui |
| Generative UI — tool-based | https://docs.copilotkit.ai/langgraph/generative-ui/tool-based |
| Generative UI — tool rendering | https://docs.copilotkit.ai/langgraph/generative-ui/tool-rendering |
| Generative UI — agentic state | https://docs.copilotkit.ai/langgraph/generative-ui/agentic |
| Generative UI — display-only components | https://docs.copilotkit.ai/langgraph/generative-ui/your-components/display-only |
| Programmatic control | https://docs.copilotkit.ai/langgraph/programmatic-control |
| Frontend Actions | https://docs.copilotkit.ai/frontend-actions |

---

## Human-in-the-loop (critical for your system)

| Page | URL |
|---|---|
| HITL — interrupt flow (LangGraph) | https://docs.copilotkit.ai/langgraph/human-in-the-loop/interrupt-flow |
| HITL — interrupt-based (coagents) | https://docs.copilotkit.ai/coagents/human-in-the-loop/interrupt-flow |

---

## UI components & customization

| Component / Feature | URL |
|---|---|
| All chat components | https://docs.copilotkit.ai/reference/components/chat |
| `<CopilotChat />` | https://docs.copilotkit.ai/reference/components/CopilotChat |
| `<CopilotPopup />` | https://docs.copilotkit.ai/reference/CopilotPopup |
| `<CopilotSidebar />` | https://docs.copilotkit.ai/reference/CopilotSidebar |
| `<CopilotKit />` provider | https://docs.copilotkit.ai/reference/components/CopilotKit |
| Headless UI (fully custom) | https://docs.copilotkit.ai/langgraph/custom-look-and-feel/headless-ui |
| Customize built-in UI components | https://docs.copilotkit.ai/langgraph/custom-look-and-feel/customize-built-in-ui-components |
| Styling / custom look and feel | https://docs.copilotkit.ai/langgraph/custom-look-and-feel |

---

## Hooks reference

| Hook | What it does | URL |
|---|---|---|
| `useCopilotAction` | Register actions the agent can call | https://docs.copilotkit.ai/reference/hooks/useCopilotAction |
| `useCoAgent` | Bidirectional state sync with agent | https://docs.copilotkit.ai/reference/hooks/useCoAgent |
| `useCoAgentStateRender` | Render agent state in chat UI | https://docs.copilotkit.ai/reference/hooks/useCoAgentStateRender |
| `useCopilotReadable` | Feed app state to the agent as context | https://docs.copilotkit.ai/reference/hooks/useCopilotReadable |
| `useCopilotChatSuggestions` | Auto-generate chat suggestions from state | https://docs.copilotkit.ai/reference/hooks/useCopilotChatSuggestions |
| `useCopilotChat` | Programmatic chat control | https://docs.copilotkit.ai/reference/v1/hooks/useCopilotChat |
| `useCopilotChatHeadless` | Fully headless chat control | https://docs.copilotkit.ai/reference/hooks/useCopilotChatHeadless_c |
| `useAgent` | Access AG-UI agent instances | https://docs.copilotkit.ai/reference/hooks/useAgent |
| `useFrontendTool` | Register client-side tool handlers | https://docs.copilotkit.ai/reference/hooks/useFrontendTool |
| `useRenderToolCall` | Render tool calls in chat | https://docs.copilotkit.ai/reference/hooks/useRenderToolCall |
| Full API reference | All components, classes, hooks | https://docs.copilotkit.ai/reference |

---

## Step-by-step tutorials (most useful for building)

| Step | URL |
|---|---|
| Step 4 — Agentic Chat UI | https://docs.copilotkit.ai/langgraph/tutorials/agent-native-app/step-4-agentic-chat-ui |
| Step 5 — Human in the Loop | https://docs.copilotkit.ai/langgraph/tutorials/agent-native-app/step-5-human-in-the-loop |
| Step 6 — Shared State | https://docs.copilotkit.ai/langgraph/tutorials/agent-native-app/step-6-shared-state |
| Step 7 — Generative UI | https://docs.copilotkit.ai/langgraph/tutorials/agent-native-app/step-7-generative-ui |
| Travel app — HITL step | https://docs.copilotkit.ai/langgraph/tutorials/ai-travel-app/step-6-human-in-the-loop |

---

## Protocols (for your agent-to-agent architecture)

| Protocol | URL |
|---|---|
| AG-UI (Agents ↔ Users) | https://docs.copilotkit.ai/agent-spec/langgraph |
| Full LLM context file (everything in one) | https://docs.copilotkit.ai/llms-full.txt |

---

The most important ones for your supply chain agent system specifically are `useCoAgent` (bidirectional state sync), `useCoAgentStateRender` (showing what each domain agent is doing in real time), the interrupt-based HITL pages (for your human escalation tier), and the headless UI page if you want a fully custom dashboard instead of the default chat bubble. The `llms-full.txt` link at the bottom is the entire docs in one file — useful to feed directly into Claude Code or Cursor when you're building.