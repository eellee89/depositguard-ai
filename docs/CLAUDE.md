# DepositGuard AI - Project Standards & Build Plan

**Last Updated:** February 10, 2026  
**Status:** Plan Mode → Implementation Ready

---

## 🎯 Project Overview

**DepositGuard AI** is a legal-tech MVP that automates Texas security deposit dispute resolution by analyzing tenant claims, researching statutory requirements, and generating certified demand letters via mail automation.

### Core Value Proposition
- Tenant uploads dispute details + evidence
- AI agent analyzes claim against Texas Property Code Chapter 92
- Human reviews AI-generated demand letter
- System sends certified mail via Lob API
- Tracks case state through entire workflow

---

## 🏗️ Tech Stack

### Backend
- **Runtime:** Python 3.11+
- **Framework:** FastAPI 0.104+
- **AI Orchestration:** LangGraph 0.0.40+ (stateful agent workflows)
- **LLM:** Claude 3.5 Sonnet via Anthropic SDK
- **Database:** PostgreSQL 15+ (Supabase or Docker)
- **Mail Automation:** Lob API (certified mail)
- **Validation:** Pydantic v2
- **Testing:** pytest + httpx

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **UI Library:** React 18+
- **Styling:** Tailwind CSS
- **State Management:** React Query / TanStack Query
- **Forms:** React Hook Form + Zod validation
- **API Client:** Fetch API / Axios

### Infrastructure
- **Database:** Supabase (hosted PostgreSQL) OR Docker Compose (local)
- **Environment:** Docker for backend containerization
- **Secrets:** .env files (never committed)

---

## 📋 Project Standards

### Code Organization
```
depositguard-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Environment & settings
│   │   ├── models/
│   │   │   ├── database.py         # SQLAlchemy models
│   │   │   └── schemas.py          # Pydantic schemas
│   │   ├── agents/
│   │   │   ├── graph.py            # LangGraph state machine
│   │   │   ├── nodes.py            # Individual agent nodes
│   │   │   └── tools.py            # Custom tools
│   │   ├── services/
│   │   │   ├── claude_service.py   # Anthropic SDK wrapper
│   │   │   ├── lob_service.py      # Mail automation
│   │   │   └── db_service.py       # Database operations
│   │   └── routers/
│   │       ├── cases.py            # Case CRUD endpoints
│   │       └── agent.py            # Agent execution endpoints
│   ├── alembic/                    # Database migrations
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js app directory
│   │   ├── components/             # React components
│   │   ├── hooks/                  # Custom hooks
│   │   ├── lib/                    # Utilities & API client
│   │   └── types/                  # TypeScript types
│   ├── public/
│   ├── package.json
│   └── next.config.js
├── docs/
│   └── CLAUDE.md                   # This file
└── README.md
```

### Coding Conventions

#### Python (Backend)
- **Style:** Black formatter + isort for imports
- **Linting:** Ruff
- **Type Hints:** Required for all functions
- **Docstrings:** Google style for classes and public methods
- **Naming:**
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

#### TypeScript (Frontend)
- **Style:** Prettier
- **Linting:** ESLint with Next.js config
- **Naming:**
  - Components: `PascalCase.tsx`
  - Utilities: `camelCase.ts`
  - Constants: `UPPER_SNAKE_CASE`
- **Props:** Define interfaces for all component props

### Database Schema Standards
```sql
-- Every table has:
id          UUID PRIMARY KEY DEFAULT gen_random_uuid()
created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()

-- Use JSONB for flexible state storage
-- Use ENUMs for fixed state values
-- Index all foreign keys and query fields
```

### API Design Standards
- **REST Principles:** Resourceful routing
- **Status Codes:**
  - 200: Success with response body
  - 201: Resource created
  - 400: Client validation error
  - 404: Resource not found
  - 500: Server error
- **Response Format:**
```json
{
  "success": true,
  "data": {},
  "error": null,
  "timestamp": "2026-02-10T12:00:00Z"
}
```

### Error Handling
- **Backend:** Custom exception classes extending FastAPI HTTPException
- **Frontend:** Centralized error boundary + toast notifications
- **Logging:** Structured JSON logs with request IDs

---

## 🤖 LangGraph Agent Architecture

### State Schema
```python
from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages

class CaseState(TypedDict):
    case_id: str
    tenant_name: str
    landlord_name: str
    deposit_amount: float
    withheld_amount: float
    move_out_date: str
    days_elapsed: int
    tenant_address: dict
    landlord_address: dict
    dispute_description: str
    evidence_urls: List[str]
    
    # Agent workflow state
    messages: Annotated[list, add_messages]
    statutory_analysis: str | None
    violation_findings: List[dict]
    demand_letter_draft: str | None
    human_approved: bool
    lob_mail_id: str | None
    status: str  # "analyzing" | "awaiting_approval" | "mailed" | "error"
```

### Graph Structure
```
START
  ↓
[Statutory Research Node]
  - Analyze Texas Property Code §92.103-109
  - Calculate damages (3x + $100 + attorney fees)
  - Identify violations
  ↓
[Generate Letter Node]
  - Use Claude to draft demand letter
  - Include statutory citations
  - Format for Lob API
  ↓
[Human Approval Gate]
  - WAIT for user approval/edits
  - Loop back to Generate Letter if rejected
  ↓
[Mail Dispatch Node]
  - Send via Lob certified mail
  - Store tracking info
  ↓
END
```

### Checkpointing Strategy
- Use PostgreSQL for LangGraph checkpoints
- Store full state after each node
- Enable resume/retry on failures

---

## 📦 Build Plan (Step-by-Step)

### Phase 1: Foundation & Database (Steps 1-3)

#### Step 1: Project Initialization
**Goal:** Set up repository structure and core dependencies

**Tasks:**
- [ ] Create root directory structure
- [ ] Initialize Git repository with `.gitignore`
- [ ] Create backend `requirements.txt`:
  ```
  fastapi==0.104.1
  uvicorn[standard]==0.24.0
  sqlalchemy==2.0.23
  psycopg2-binary==2.9.9
  alembic==1.12.1
  pydantic==2.5.0
  pydantic-settings==2.1.0
  anthropic==0.7.8
  langgraph==0.0.40
  langchain-core==0.1.0
  lob==6.0.0
  python-dotenv==1.0.0
  httpx==0.25.2
  pytest==7.4.3
  pytest-asyncio==0.21.1
  ```
- [ ] Create frontend `package.json` with Next.js 14
- [ ] Create `.env.example` template
- [ ] Write initial `README.md`

**Success Criteria:**
- All directories exist
- Dependencies install without errors
- Environment template documented

---

#### Step 2: Database Setup
**Goal:** Configure PostgreSQL and create initial schema

**Choose ONE:**

**Option A: Supabase (Recommended for MVP)**
- [ ] Create Supabase project at https://supabase.com
- [ ] Get connection string and anon key
- [ ] Add to `.env`:
  ```
  DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
  SUPABASE_URL=https://[PROJECT].supabase.co
  SUPABASE_ANON_KEY=eyJ...
  ```

**Option B: Local Docker**
- [ ] Create `docker-compose.yml`:
  ```yaml
  version: '3.8'
  services:
    postgres:
      image: postgres:15-alpine
      environment:
        POSTGRES_DB: depositguard
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: local_dev_password
      ports:
        - "5432:5432"
      volumes:
        - postgres_data:/var/lib/postgresql/data
  volumes:
    postgres_data:
  ```
- [ ] Run `docker-compose up -d`

**Schema Creation:**
- [ ] Initialize Alembic: `alembic init alembic`
- [ ] Create migration for `cases` table:
  ```sql
  CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_name VARCHAR(255) NOT NULL,
    landlord_name VARCHAR(255) NOT NULL,
    deposit_amount DECIMAL(10,2) NOT NULL,
    withheld_amount DECIMAL(10,2) NOT NULL,
    move_out_date DATE NOT NULL,
    tenant_address JSONB NOT NULL,
    landlord_address JSONB NOT NULL,
    dispute_description TEXT NOT NULL,
    evidence_urls JSONB DEFAULT '[]',
    
    -- Agent state
    agent_state JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'draft',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
  );
  
  CREATE INDEX idx_cases_status ON cases(status);
  CREATE INDEX idx_cases_created_at ON cases(created_at DESC);
  ```
- [ ] Create migration for `checkpoints` table (LangGraph):
  ```sql
  CREATE TABLE checkpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    checkpoint_data JSONB NOT NULL,
    checkpoint_ns VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
  );
  
  CREATE INDEX idx_checkpoints_case_id ON checkpoints(case_id);
  ```
- [ ] Run migrations: `alembic upgrade head`

**Success Criteria:**
- Database accessible via connection string
- Tables exist with correct schema
- Can insert/query test data

---

#### Step 3: API Foundation
**Goal:** Create FastAPI app with config and basic endpoints

**Tasks:**
- [ ] Create `backend/app/config.py`:
  ```python
  from pydantic_settings import BaseSettings
  
  class Settings(BaseSettings):
      # Database
      DATABASE_URL: str
      
      # API Keys
      ANTHROPIC_API_KEY: str
      LOB_API_KEY: str
      
      # App Config
      APP_NAME: str = "DepositGuard AI"
      DEBUG: bool = False
      
      class Config:
          env_file = ".env"
  
  settings = Settings()
  ```

- [ ] Create `backend/app/main.py`:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  from app.config import settings
  from app.routers import cases, agent
  
  app = FastAPI(title=settings.APP_NAME)
  
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  
  app.include_router(cases.router, prefix="/api/cases", tags=["cases"])
  app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
  
  @app.get("/health")
  async def health_check():
      return {"status": "healthy"}
  ```

- [ ] Create SQLAlchemy models in `backend/app/models/database.py`
- [ ] Create Pydantic schemas in `backend/app/models/schemas.py`
- [ ] Create basic CRUD router in `backend/app/routers/cases.py`:
  - `POST /api/cases` - Create new case
  - `GET /api/cases/{case_id}` - Get case details
  - `GET /api/cases` - List all cases
  - `PATCH /api/cases/{case_id}` - Update case

- [ ] Test with: `uvicorn app.main:app --reload`

**Success Criteria:**
- FastAPI server starts without errors
- `/health` endpoint returns 200
- Can create and retrieve cases via API
- CORS allows frontend connections

---

### Phase 2: AI Agent Core (Steps 4-6)

#### Step 4: Claude Integration
**Goal:** Set up Anthropic SDK wrapper for legal reasoning

**Tasks:**
- [ ] Create `backend/app/services/claude_service.py`:
  ```python
  from anthropic import Anthropic
  from app.config import settings
  
  class ClaudeService:
      def __init__(self):
          self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
          self.model = "claude-sonnet-4-20250514"
      
      async def analyze_statutory_compliance(
          self, 
          case_data: dict
      ) -> dict:
          """Analyze case against Texas Property Code."""
          prompt = self._build_statutory_prompt(case_data)
          
          message = self.client.messages.create(
              model=self.model,
              max_tokens=4000,
              temperature=0.2,
              system="You are a Texas landlord-tenant law expert...",
              messages=[{"role": "user", "content": prompt}]
          )
          
          return self._parse_analysis(message.content[0].text)
      
      async def generate_demand_letter(
          self,
          case_data: dict,
          violations: list
      ) -> str:
          """Generate formatted demand letter."""
          # Implementation with structured output
          pass
  ```

- [ ] Create prompt templates for:
  - Statutory analysis
  - Violation identification
  - Damage calculation
  - Demand letter generation

- [ ] Write unit tests for Claude service

**Success Criteria:**
- Can call Claude API successfully
- Receives structured legal analysis
- Generates properly formatted demand letters
- Handles API errors gracefully

---

#### Step 5: LangGraph Agent
**Goal:** Build stateful multi-step agent workflow

**Tasks:**
- [ ] Create `backend/app/agents/graph.py`:
  ```python
  from langgraph.graph import StateGraph, END
  from langgraph.checkpoint.postgres import PostgresSaver
  from app.agents.nodes import (
      statutory_research_node,
      generate_letter_node,
      mail_dispatch_node
  )
  from app.models.schemas import CaseState
  
  def create_agent_graph():
      workflow = StateGraph(CaseState)
      
      # Add nodes
      workflow.add_node("research", statutory_research_node)
      workflow.add_node("generate", generate_letter_node)
      workflow.add_node("dispatch", mail_dispatch_node)
      
      # Define edges
      workflow.set_entry_point("research")
      workflow.add_edge("research", "generate")
      workflow.add_conditional_edges(
          "generate",
          lambda state: "dispatch" if state["human_approved"] else END
      )
      workflow.add_edge("dispatch", END)
      
      # Set up checkpointing
      checkpointer = PostgresSaver(conn_string=settings.DATABASE_URL)
      
      return workflow.compile(checkpointer=checkpointer)
  ```

- [ ] Create `backend/app/agents/nodes.py` with node implementations:
  ```python
  from app.services.claude_service import ClaudeService
  from app.models.schemas import CaseState
  
  claude = ClaudeService()
  
  async def statutory_research_node(state: CaseState) -> CaseState:
      """Research Texas Property Code violations."""
      analysis = await claude.analyze_statutory_compliance({
          "deposit_amount": state["deposit_amount"],
          "withheld_amount": state["withheld_amount"],
          "days_elapsed": state["days_elapsed"],
          "dispute_description": state["dispute_description"]
      })
      
      state["statutory_analysis"] = analysis["summary"]
      state["violation_findings"] = analysis["violations"]
      state["status"] = "analyzed"
      
      return state
  
  # Implement generate_letter_node and mail_dispatch_node
  ```

- [ ] Create agent execution endpoint in `backend/app/routers/agent.py`:
  ```python
  @router.post("/cases/{case_id}/execute")
  async def execute_agent(case_id: str):
      """Start agent workflow for a case."""
      # Load case from DB
      # Initialize graph
      # Execute until human approval needed
      # Return state
      pass
  
  @router.post("/cases/{case_id}/approve")
  async def approve_letter(case_id: str, approved: bool):
      """Continue agent after human review."""
      # Resume graph from checkpoint
      # Execute remaining steps if approved
      pass
  ```

**Success Criteria:**
- Agent executes all nodes in sequence
- State persists between steps
- Can pause at human approval gate
- Can resume from checkpoint

---

#### Step 6: Lob Integration
**Goal:** Implement certified mail automation

**Tasks:**
- [ ] Create `backend/app/services/lob_service.py`:
  ```python
  import lob
  from app.config import settings
  
  class LobService:
      def __init__(self):
          self.client = lob.Client(api_key=settings.LOB_API_KEY)
      
      async def send_certified_letter(
          self,
          to_address: dict,
          from_address: dict,
          letter_content: str
      ) -> dict:
          """Send certified mail via Lob."""
          try:
              letter = self.client.Letter.create(
                  description="Security Deposit Demand Letter",
                  to_address=to_address,
                  from_address=from_address,
                  file=letter_content,  # HTML or PDF
                  color=True,
                  double_sided=False,
                  extra_service="certified",
                  mail_type="usps_first_class"
              )
              
              return {
                  "lob_id": letter.id,
                  "tracking_url": letter.tracking_events[0].url if letter.tracking_events else None,
                  "expected_delivery": letter.expected_delivery_date
              }
          except lob.error.LobError as e:
              # Handle Lob API errors
              raise
  ```

- [ ] Create HTML template for demand letters
- [ ] Integrate into `mail_dispatch_node`
- [ ] Add tracking info to case records

**Success Criteria:**
- Can send test letters via Lob
- Tracking URLs stored in database
- Handles address validation errors
- Certified mail options configured

---

### Phase 3: Frontend (Steps 7-9)

#### Step 7: Next.js Setup
**Goal:** Create frontend foundation with API integration

**Tasks:**
- [ ] Initialize Next.js: `npx create-next-app@latest frontend`
- [ ] Install dependencies:
  ```json
  {
    "dependencies": {
      "react": "^18.2.0",
      "next": "^14.0.0",
      "@tanstack/react-query": "^5.0.0",
      "react-hook-form": "^7.48.0",
      "zod": "^3.22.0",
      "axios": "^1.6.0",
      "tailwindcss": "^3.3.0"
    }
  }
  ```

- [ ] Configure Tailwind CSS
- [ ] Create API client in `src/lib/api.ts`:
  ```typescript
  import axios from 'axios';
  
  const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  });
  
  export const casesApi = {
    create: (data: CreateCaseDto) => api.post('/api/cases', data),
    get: (id: string) => api.get(`/api/cases/${id}`),
    list: () => api.get('/api/cases'),
  };
  
  export const agentApi = {
    execute: (caseId: string) => api.post(`/api/agent/cases/${caseId}/execute`),
    approve: (caseId: string, approved: boolean) => 
      api.post(`/api/agent/cases/${caseId}/approve`, { approved }),
  };
  ```

- [ ] Set up React Query provider

**Success Criteria:**
- Next.js dev server runs
- Can call backend API
- TypeScript configured properly
- Tailwind classes work

---

#### Step 8: Core UI Components
**Goal:** Build case creation and review interfaces

**Tasks:**
- [ ] Create case intake form (`src/components/CaseForm.tsx`):
  - Tenant/landlord information
  - Deposit amounts
  - Move-out date
  - Dispute description
  - Evidence upload (store URLs)
  - Address inputs

- [ ] Create case dashboard (`src/app/dashboard/page.tsx`):
  - List all cases with status
  - Filter by status
  - Click to view details

- [ ] Create case detail view (`src/app/cases/[id]/page.tsx`):
  - Display case information
  - Show agent status
  - "Start Analysis" button
  - Letter preview when ready

- [ ] Create approval interface:
  - Markdown preview of demand letter
  - Edit functionality
  - Approve/Reject buttons
  - Mailing confirmation

**Success Criteria:**
- Can create cases via form
- Form validation works
- Dashboard shows real data
- UI is responsive

---

#### Step 9: Agent Status UI
**Goal:** Real-time workflow visualization

**Tasks:**
- [ ] Create status stepper component:
  ```
  [1. Analyzing] → [2. Review Letter] → [3. Mailing] → [4. Sent]
  ```

- [ ] Add polling/websockets for status updates
- [ ] Show violations found
- [ ] Display calculated damages
- [ ] Show Lob tracking after mail sent

- [ ] Add loading states for each step
- [ ] Error handling UI

**Success Criteria:**
- Status updates in real-time
- User knows what's happening
- Can track progress visually
- Errors displayed clearly

---

### Phase 4: Polish & Deploy (Steps 10-12)

#### Step 10: Testing
**Goal:** Ensure reliability

**Tasks:**
- [ ] Backend unit tests (pytest):
  - Test Claude service responses
  - Test LangGraph state transitions
  - Test Lob integration (mocked)
  - Test API endpoints

- [ ] Frontend tests:
  - Component tests (React Testing Library)
  - Form validation tests
  - API integration tests

- [ ] End-to-end test:
  - Create case → Execute agent → Approve → Verify mail sent

**Success Criteria:**
- 80%+ code coverage
- All critical paths tested
- E2E flow works end-to-end

---

#### Step 11: Documentation
**Goal:** Enable handoff and maintenance

**Tasks:**
- [ ] Update `README.md` with:
  - Setup instructions
  - Environment variables
  - Running locally
  - Deployment guide

- [ ] Add API documentation (FastAPI auto-docs at `/docs`)
- [ ] Document LangGraph flow with diagram
- [ ] Create `.env.example` with all required keys
- [ ] Add inline code comments

**Success Criteria:**
- New developer can run locally in <30 min
- All APIs documented
- Environment setup clear

---

#### Step 12: Deployment
**Goal:** Get MVP live

**Tasks:**
- [ ] Backend deployment options:
  - **Railway.app** (recommended for FastAPI)
  - **Render**
  - **Google Cloud Run**

- [ ] Frontend deployment:
  - **Vercel** (recommended for Next.js)
  - **Netlify**

- [ ] Database:
  - Keep Supabase (already hosted)
  - Or migrate to managed PostgreSQL

- [ ] Environment variables in production
- [ ] Enable HTTPS
- [ ] Set up error monitoring (optional: Sentry)

**Success Criteria:**
- Both services deployed
- Can access via public URLs
- Database connected
- All API keys working

---

## 🔐 Security Considerations

### API Keys
- Never commit `.env` to Git
- Use environment variables in production
- Rotate keys if exposed

### User Data
- Encrypt sensitive data at rest (addresses, SSNs if collected)
- Use HTTPS for all API calls
- Implement rate limiting on API endpoints

### Legal Compliance
- Add disclaimer: "Not a substitute for legal advice"
- Terms of service for using the platform
- Privacy policy for data handling

---

## 🚀 Future Enhancements (Post-MVP)

1. **Multi-state support** - Expand beyond Texas
2. **Email notifications** - Alert users when letter is mailed
3. **Payment integration** - Charge for letter sending
4. **Case templates** - Common dispute scenarios
5. **Evidence analysis** - OCR for receipts/photos
6. **Settlement tracking** - Did landlord respond?
7. **Attorney referrals** - If case needs escalation

---

## 📚 Key References

- [Texas Property Code Chapter 92](https://statutes.capitol.texas.gov/Docs/PR/htm/PR.92.htm)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Lob API Docs](https://docs.lob.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)

---

## ✅ Current Phase: PLAN MODE COMPLETE

**Next Action:** Begin Step 1 - Project Initialization

**Estimated Timeline:**
- Phase 1 (Foundation): 2-3 days
- Phase 2 (AI Agent): 3-4 days  
- Phase 3 (Frontend): 3-4 days
- Phase 4 (Polish): 2-3 days
- **Total MVP:** 10-14 days

---

*This document is the single source of truth for DepositGuard AI development. Update it as decisions are made or requirements change.*
