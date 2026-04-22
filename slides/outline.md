# 🎤 Slide Deck Outline

## Build Your First AI Agent on AWS: A Hands-On Demo with Amazon Bedrock AgentCore

**AI Festival Summit — June 10-11, 2026**

---

## Slide 1: Title Slide

- **Title:** Build Your First AI Agent on AWS
- **Subtitle:** A Hands-On Demo with Amazon Bedrock AgentCore
- **Speaker:** [Your Name], AWS Authorized Instructor
- **Event:** AI Festival Summit 2026
- **Visual:** AgentCore logo + travel imagery

---

## Slide 2: The Problem — Why Agents?

**Left side:** Traditional chatbot flow (rigid, scripted, limited)

**Right side:** AI Agent flow (autonomous, tool-using, adaptive)

**Key message:**
> "Chatbots follow scripts. Agents take action."

**Bullet points:**
- Agents can reason about complex requests
- Agents can use tools (APIs, databases, code execution)
- Agents can remember context across conversations
- Agents can act on behalf of users

---

## Slide 3: The Challenge — Building Agents is Hard

**Visual:** Iceberg diagram

**Above water:** "The Agent" (the fun part — prompts, tools, logic)

**Below water:** All the infrastructure you need:
- Secure runtime & auto-scaling
- Tool integration & API management
- Identity & access management
- Memory & state management
- Observability & monitoring
- Evaluation & quality assurance
- Policy & governance

**Key message:**
> "80% of the work is infrastructure, not intelligence."

---

## Slide 4: The Solution — Amazon Bedrock AgentCore

**Visual:** AgentCore feature map

**Key message:**
> "AgentCore handles the infrastructure so you can focus on the intelligence."

**Features grid:**
| Feature | What It Does |
|---------|-------------|
| Runtime | Serverless, secure, auto-scaling agent hosting |
| Gateway | Turn any API into an agent tool (MCP-compatible) |
| Memory | Managed preference & context storage |
| Identity | OAuth/OIDC for agent-to-service auth |
| Tools | Built-in Code Interpreter & Browser |
| Observability | OpenTelemetry tracing & monitoring |
| Evaluation | LLM-as-a-Judge quality scoring |
| Policy | Cedar-based access control |

**Bottom line:**
> "Framework-agnostic. Model-agnostic. Bring your code, we handle the rest."

---

## Slide 5: What We're Building Today

**Visual:** Architecture diagram of the Smart Travel Concierge

**Components:**
- Strands Agent + Claude Sonnet (via Bedrock)
- Flight Search tool (Lambda → Gateway)
- Weather Lookup tool (Lambda → Gateway)
- Code Interpreter (built-in)
- Memory (managed)
- Observability (OpenTelemetry)

**Key message:**
> "In the next 35 minutes, we'll build and deploy a production-ready travel agent. Let's go."

---

## 🔴 LIVE DEMO STARTS HERE (35 min)

*Switch to Jupyter Notebook + Terminal + AWS Console*

---

## Slide 6: Recap — What We Built (Post-Demo)

**Visual:** Checklist with green checkmarks

- ✅ Scaffolded an agent project with AgentCore CLI
- ✅ Connected 2 Lambda functions as tools via Gateway
- ✅ Added Code Interpreter for charts & calculations
- ✅ Enabled Memory for cross-session personalization
- ✅ Deployed to production with `agentcore deploy`
- ✅ Viewed traces and monitoring in Observability

**Time:** ~35 minutes, ~50 lines of agent code

---

## Slide 7: What Else Can You Do?

**Features we didn't demo (but are available):**

- **Identity** — Let your agent book flights using the user's airline account (OAuth)
- **Evaluation** — Automatically score agent responses for accuracy and helpfulness
- **Policy** — Restrict which tools an agent can use based on user role (Cedar)
- **Browser Tool** — Let the agent browse the web to research destinations

**Key message:**
> "We showed 6 features in 35 minutes. There's a whole platform to explore."

---

## Slide 8: Get Started

**Resources:**

| Resource | Link |
|----------|------|
| This demo's code | github.com/mlungwsr/Smart-Travel-Concierge-Agent |
| AgentCore Samples | github.com/awslabs/agentcore-samples |
| Documentation | docs.aws.amazon.com/bedrock-agentcore |
| AgentCore CLI | github.com/aws/agentcore-cli |
| Workshop | Getting Started with AgentCore |

**3 commands to get started:**
```bash
npm install -g @aws/agentcore
agentcore create
agentcore deploy
```

---

## Slide 9: Thank You + Q&A

- **Speaker:** [Your Name]
- **Contact:** [Your info]
- **QR Code:** Link to the GitHub repo

> "The best time to build your first agent was yesterday. The second best time is right after this session."

---

## Presenter Notes

### Timing Guide
| Section | Duration | Cumulative |
|---------|----------|------------|
| Slides 1-5 (Intro) | 5 min | 5 min |
| Act 2: Scaffold & First Agent | 8 min | 13 min |
| Act 3: Add Tools | 10 min | 23 min |
| Act 4: Add Memory | 5 min | 28 min |
| Act 5: Deploy to Production | 7 min | 35 min |
| Slides 6-9 (Wrap-up) | 5 min | 40 min |
| Q&A | 5 min | 45 min |

### Tips
- Keep terminal font size at 18pt+ for visibility
- Use dark theme in Jupyter for better projection
- Have a pre-deployed backup agent ready in case deploy is slow
- When showing the console, zoom to 150%
- Pause after each "wow moment" to let it sink in
