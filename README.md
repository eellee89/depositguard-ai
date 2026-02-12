# DepositGuard AI

**AI-powered security deposit dispute resolution for Texas tenants**

DepositGuard AI analyzes Texas security deposit disputes, generates demand letters with statutory citations, and sends certified mail via the Lob API—all powered by Claude 3.5 Sonnet and LangGraph.

---

## 🎯 Features

- ✅ **AI Legal Analysis** - Claude analyzes cases against Texas Property Code Chapter 92
- ✅ **Stateful Workflows** - LangGraph manages multi-step agent processes
- ✅ **Damage Calculation** - Automatic treble damages + $100 penalty computation
- ✅ **Demand Letters** - Professional letters with statutory citations
- ✅ **Certified Mail** - Automated mailing via Lob API with tracking
- ✅ **Human-in-the-Loop** - Approval gate before sending mail

---

## 🏗️ Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **LangGraph** - Stateful AI agent workflows
- **Claude 3.5 Sonnet** - Legal reasoning engine
- **PostgreSQL** - Database for cases and checkpoints
- **Lob API** - Certified mail automation
- **SQLAlchemy** + **Pydantic** - ORM and validation

### Frontend
- **Next.js 14** (App Router) with TypeScript
- **React 18** + **Tailwind CSS**
- **TanStack Query** - Server state management
- **React Hook Form** - Form handling

---

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- PostgreSQL 15+ (or Docker for local setup)
- API Keys:
  - Anthropic API key (Claude)
  - Lob API key (certified mail)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd depositguard-ai
```

### 2. Backend Setup

#### Option A: Local Docker PostgreSQL (Recommended for Development)

```bash
cd backend

# Start PostgreSQL
docker-compose up -d

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env
```

Edit `.env` and add:
```env
DATABASE_URL=postgresql://postgres:local_dev_password@localhost:5432/depositguard
ANTHROPIC_API_KEY=sk-ant-your-key-here
LOB_API_KEY=test_your-key-here  # Use test_ prefix for sandbox
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
```

#### Option B: Supabase (Recommended for Production)

1. Create project at [supabase.com](https://supabase.com)
2. Get connection string from Settings > Database
3. Update `.env`:
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
SUPABASE_URL=https://[PROJECT].supabase.co
SUPABASE_ANON_KEY=eyJ...
ANTHROPIC_API_KEY=sk-ant-your-key-here
LOB_API_KEY=test_your-key-here
```

#### Run Database Migrations

```bash
# The app will auto-create tables on startup, or run manually:
python -c "from app.database import init_db; init_db()"
```

#### Start Backend Server

```bash
uvicorn app.main:app --reload
```

Backend will be running at `http://localhost:8000`

API Docs available at: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Frontend will be running at `http://localhost:3000`

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Manual Testing Flow

1. **Create Case**: Go to http://localhost:3000/new-case
2. **Fill Form**: Enter tenant/landlord info, deposit amounts, dispute description
3. **Start Analysis**: Click "Start AI Analysis" on case detail page
4. **Review Letter**: AI generates demand letter - preview it
5. **Approve**: Click "Approve & Send Certified Mail"
6. **Track**: View Lob tracking info on success

---

## 📁 Project Structure

```
depositguard-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings
│   │   ├── database.py          # DB connection
│   │   ├── models/
│   │   │   ├── database.py      # SQLAlchemy models
│   │   │   └── schemas.py       # Pydantic schemas
│   │   ├── services/
│   │   │   ├── claude_service.py # AI legal analysis
│   │   │   ├── lob_service.py    # Mail automation
│   │   │   └── db_service.py     # Database operations
│   │   ├── agents/
│   │   │   ├── graph.py          # LangGraph state machine
│   │   │   └── nodes.py          # Agent workflow nodes
│   │   └── routers/
│   │       ├── cases.py          # CRUD endpoints
│   │       └── agent.py          # Agent execution
│   ├── tests/
│   ├── requirements.txt
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   │   ├── app/                  # Next.js pages
│   │   ├── components/           # React components
│   │   ├── lib/                  # API client
│   │   └── types/                # TypeScript types
│   └── package.json
└── docs/
    └── CLAUDE.md                # Project standards
```

---

## 🤖 LangGraph Agent Workflow

```
START
  ↓
[Statutory Research]
  - Analyze Texas Property Code §92.103-109
  - Calculate damages (3x + $100)
  - Identify violations
  ↓
[Generate Letter]
  - Use Claude to draft demand letter
  - Include statutory citations
  - Format for Lob API
  ↓
[Human Approval Gate] ⏸️
  - User reviews letter
  - Can approve or reject
  ↓
[Mail Dispatch]
  - Send via Lob certified mail
  - Store tracking info
  ↓
END
```

---

## 🔑 API Endpoints

### Cases

- `POST /api/cases/` - Create new case
- `GET /api/cases/{id}` - Get case details
- `GET /api/cases/` - List all cases
- `PATCH /api/cases/{id}` - Update case
- `DELETE /api/cases/{id}` - Delete case

### Agent

- `POST /api/agent/cases/{id}/execute` - Start AI analysis
- `POST /api/agent/cases/{id}/approve` - Approve/reject letter
- `GET /api/agent/cases/{id}/status` - Get agent status

---

## 🔐 Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://...

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
LOB_API_KEY=test_...  # test_ for sandbox, live_ for production

# App Configuration
APP_NAME=DepositGuard AI
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
CLAUDE_MODEL=claude-sonnet-4-20250514
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📚 Key Dependencies

### Backend
- `fastapi` - Web framework
- `langgraph` - Stateful agent workflows
- `anthropic` - Claude API
- `lob` - Certified mail API
- `sqlalchemy` - ORM
- `pydantic` - Validation

### Frontend
- `next` - React framework
- `@tanstack/react-query` - Data fetching
- `react-hook-form` - Forms
- `tailwindcss` - Styling

---

## 🐛 Troubleshooting

### Backend won't start

- Check Python version: `python --version` (must be 3.11+)
- Verify PostgreSQL is running: `docker ps` or check Supabase
- Ensure all environment variables are set in `.env`
- Check API keys are valid

### Frontend can't connect to backend

- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Look for CORS errors in browser console
- Ensure `ALLOWED_ORIGINS` includes frontend URL

### Database errors

- Check `DATABASE_URL` format is correct
- For Docker: `docker-compose logs postgres`
- For Supabase: Check connection string from dashboard
- Try: `docker-compose down -v && docker-compose up -d`

### Lob API errors

- Verify API key starts with `test_` or `live_`
- Check address format matches Lob requirements
- Review Lob dashboard for delivery errors
- Ensure sufficient account balance

---

## 🚢 Deployment

### Backend (Railway.app recommended)

1. Create Railway account
2. New Project > Deploy from GitHub
3. Add environment variables
4. Connect to Railway PostgreSQL addon

### Frontend (Vercel recommended)

1. Create Vercel account
2. Import GitHub repository
3. Set `NEXT_PUBLIC_API_URL` to production backend URL
4. Deploy

### Database (Supabase)

1. Already set up if following Option B above
2. For production, upgrade from free tier
3. Enable connection pooling

---

## 📖 Legal Disclaimer

⚠️ **This software is for informational purposes only and does not constitute legal advice.**

- Not a substitute for consultation with a licensed attorney
- Does not create an attorney-client relationship
- Texas law may change after development
- Users should verify all statutory citations
- Consult an attorney for complex cases

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 💡 Future Enhancements

- [ ] Multi-state support (currently Texas only)
- [ ] Email notifications
- [ ] Payment integration
- [ ] Case templates
- [ ] Evidence upload and OCR
- [ ] Settlement tracking
- [ ] Attorney referral system

---

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check documentation in `/docs`
- Review API docs at `/docs` endpoint

---

Built with ❤️ using Claude 3.5 Sonnet, LangGraph, and FastAPI
