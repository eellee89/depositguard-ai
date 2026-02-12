export interface Address {
  name: string;
  address_line1: string;
  address_line2?: string;
  address_city: string;
  address_state: string;
  address_zip: string;
}

export interface Case {
  id: string;
  tenant_name: string;
  landlord_name: string;
  deposit_amount: string;
  withheld_amount: string;
  move_out_date: string;
  tenant_address: Address;
  landlord_address: Address;
  dispute_description: string;
  evidence_urls: string[];
  agent_state: Record<string, any>;
  status: 'draft' | 'analyzing' | 'analyzed' | 'awaiting_approval' | 'mailed' | 'error';
  created_at: string;
  updated_at: string;
}

export interface CreateCaseInput {
  tenant_name: string;
  landlord_name: string;
  deposit_amount: string;
  withheld_amount: string;
  move_out_date: string;
  tenant_address: Address;
  landlord_address: Address;
  dispute_description: string;
  evidence_urls?: string[];
}

export interface ViolationFinding {
  statute: string;
  violation_type: string;
  description: string;
  damages_applicable: boolean;
}

export interface StatutoryAnalysis {
  violations: ViolationFinding[];
  days_elapsed: number;
  is_compliant: boolean;
  base_damages: string;
  treble_damages: string;
  statutory_penalty: string;
  total_damages: string;
  summary: string;
}

export interface DemandLetter {
  letter_html: string;
  letter_text: string;
  citations: string[];
}

export interface AgentExecuteResponse {
  case_id: string;
  status: string;
  current_step: string;
  analysis?: StatutoryAnalysis;
  demand_letter?: DemandLetter;
  needs_approval: boolean;
}

export interface MailingResult {
  lob_id: string;
  tracking_url?: string;
  expected_delivery?: string;
}

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
}
