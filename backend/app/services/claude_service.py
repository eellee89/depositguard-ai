from anthropic import Anthropic
from app.config import settings
from app.models.schemas import StatutoryAnalysis, ViolationFinding, DemandLetterDraft
from typing import Dict, Any, List
from decimal import Decimal
from datetime import date
import json


class ClaudeService:
    """Service for interacting with Claude API for legal analysis."""
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
    
    def _build_statutory_analysis_prompt(self, case_data: Dict[str, Any]) -> str:
        """Build prompt for statutory compliance analysis."""
        return f"""You are a Texas landlord-tenant law expert specializing in security deposit disputes under Texas Property Code Chapter 92.

Analyze the following case for statutory violations:

CASE DETAILS:
- Deposit Amount: ${case_data['deposit_amount']}
- Withheld Amount: ${case_data['withheld_amount']}
- Move-Out Date: {case_data['move_out_date']}
- Days Since Move-Out: {case_data['days_elapsed']}
- Dispute Description: {case_data['dispute_description']}

RELEVANT TEXAS LAW:
§92.103 - Landlord's obligations for refund/accounting
§92.104 - Presumption of refund if no accounting within 30 days
§92.109 - Tenant's remedies (deposit + $100 + 3x deposit + attorney fees)

TASK:
Analyze whether the landlord violated Texas Property Code. Respond ONLY with valid JSON matching this schema:

{{
  "violations": [
    {{
      "statute": "Texas Property Code §92.XXX",
      "violation_type": "string",
      "description": "string",
      "damages_applicable": boolean
    }}
  ],
  "days_elapsed": integer,
  "is_compliant": boolean,
  "base_damages": "decimal string",
  "treble_damages": "decimal string",
  "statutory_penalty": "100.00",
  "total_damages": "decimal string",
  "summary": "Plain English explanation of findings"
}}

CALCULATION RULES:
- If landlord failed to provide itemized accounting within 30 days of move-out, they forfeit the right to withhold ANY amount
- Base damages = amount wrongfully withheld
- If bad faith violation: treble damages = base_damages × 3
- Total = base_damages + treble_damages + $100 statutory penalty + attorney fees potential

Analyze now:"""
    
    async def analyze_statutory_compliance(self, case_data: Dict[str, Any]) -> StatutoryAnalysis:
        """
        Analyze case for Texas Property Code violations.
        
        Args:
            case_data: Dictionary with case details
            
        Returns:
            StatutoryAnalysis with violations and damages
        """
        prompt = self._build_statutory_analysis_prompt(case_data)
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=0.2,
            system="You are a precise legal analyst. Always respond with valid JSON only. No markdown, no explanations outside JSON.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # Parse JSON response
        try:
            if response_text.startswith("```"):
                # Remove markdown code blocks if present
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            analysis_data = json.loads(response_text)
            
            # Convert to Pydantic model
            violations = [
                ViolationFinding(**v) for v in analysis_data["violations"]
            ]
            
            return StatutoryAnalysis(
                violations=violations,
                days_elapsed=analysis_data["days_elapsed"],
                is_compliant=analysis_data["is_compliant"],
                base_damages=Decimal(analysis_data["base_damages"]),
                treble_damages=Decimal(analysis_data["treble_damages"]),
                statutory_penalty=Decimal(analysis_data.get("statutory_penalty", "100.00")),
                total_damages=Decimal(analysis_data["total_damages"]),
                summary=analysis_data["summary"]
            )
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse Claude response: {e}\nResponse: {response_text}")
    
    def _build_demand_letter_prompt(
        self,
        case_data: Dict[str, Any],
        analysis: StatutoryAnalysis
    ) -> str:
        """Build prompt for demand letter generation."""
        return f"""You are a Texas attorney drafting a demand letter for a security deposit dispute.

CLIENT INFORMATION:
Tenant: {case_data['tenant_name']}
Tenant Address: {case_data['tenant_address']['address_line1']}, {case_data['tenant_address']['address_city']}, TX {case_data['tenant_address']['address_zip']}

LANDLORD INFORMATION:
Name: {case_data['landlord_name']}
Address: {case_data['landlord_address']['address_line1']}, {case_data['landlord_address']['address_city']}, TX {case_data['landlord_address']['address_zip']}

CASE FACTS:
- Original Deposit: ${case_data['deposit_amount']}
- Withheld Amount: ${case_data['withheld_amount']}
- Move-Out Date: {case_data['move_out_date']}
- Days Elapsed: {analysis.days_elapsed}

LEGAL ANALYSIS:
{analysis.summary}

VIOLATIONS FOUND:
{chr(10).join(f"- {v.statute}: {v.description}" for v in analysis.violations)}

DAMAGES CALCULATION:
- Base Damages: ${analysis.base_damages}
- Treble Damages: ${analysis.treble_damages}
- Statutory Penalty: ${analysis.statutory_penalty}
- TOTAL DEMAND: ${analysis.total_damages}

TASK:
Draft a professional, firm demand letter demanding the full amount. The letter should:
1. State the facts clearly
2. Cite specific Texas Property Code sections violated
3. Demand payment of ${analysis.total_damages} within 7 days
4. Reference potential small claims court action if not resolved
5. Be formatted in proper business letter format with date

Respond ONLY with valid JSON:
{{
  "letter_html": "HTML formatted letter ready for Lob API",
  "letter_text": "Plain text version",
  "citations": ["list of statute citations used"]
}}

The HTML should be a complete professional letter with proper formatting, ready to be printed and mailed."""
    
    async def generate_demand_letter(
        self,
        case_data: Dict[str, Any],
        analysis: StatutoryAnalysis
    ) -> DemandLetterDraft:
        """
        Generate formatted demand letter.
        
        Args:
            case_data: Case details
            analysis: Statutory analysis results
            
        Returns:
            DemandLetterDraft with HTML and text versions
        """
        prompt = self._build_demand_letter_prompt(case_data, analysis)
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=6000,
            temperature=0.3,
            system="You are a professional attorney. Always respond with valid JSON only.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        try:
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            letter_data = json.loads(response_text)
            
            return DemandLetterDraft(
                letter_html=letter_data["letter_html"],
                letter_text=letter_data["letter_text"],
                citations=letter_data["citations"]
            )
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse letter response: {e}\nResponse: {response_text}")


# Singleton instance
claude_service = ClaudeService()
