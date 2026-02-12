'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { casesApi, agentApi } from '@/lib/api';
import { useParams } from 'next/navigation';
import { useState } from 'react';
import { CheckCircle, Clock, Mail, AlertCircle, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function CaseDetailPage() {
  const params = useParams();
  const caseId = params.id as string;
  const queryClient = useQueryClient();
  const [showLetterPreview, setShowLetterPreview] = useState(false);

  const { data: caseData, isLoading } = useQuery({
    queryKey: ['case', caseId],
    queryFn: () => casesApi.get(caseId),
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === 'analyzing' || data?.status === 'awaiting_approval') {
        return 3000; // Poll every 3 seconds
      }
      return false;
    },
  });

  const executeMutation = useMutation({
    mutationFn: () => agentApi.execute(caseId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['case', caseId] });
    },
  });

  const approveMutation = useMutation({
    mutationFn: ({ approved }: { approved: boolean }) => 
      agentApi.approve(caseId, approved),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['case', caseId] });
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (!caseData) {
    return <div className="text-center py-12">Case not found</div>;
  }

  const analysis = caseData.agent_state?.statutory_analysis;
  const demandLetter = caseData.agent_state?.demand_letter_draft;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Case: {caseData.tenant_name} vs. {caseData.landlord_name}
        </h1>
        <p className="text-gray-600">Case ID: {caseData.id}</p>
      </div>

      {/* Status Timeline */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-6">Case Progress</h2>
        <div className="flex items-center justify-between relative">
          <div className="absolute top-5 left-0 right-0 h-0.5 bg-gray-200 -z-10"></div>
          
          {/* Step 1: Draft */}
          <div className="flex flex-col items-center flex-1">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
              ['draft', 'analyzing', 'analyzed', 'awaiting_approval', 'mailed'].includes(caseData.status)
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-500'
            }`}>
              <CheckCircle className="w-5 h-5" />
            </div>
            <span className="text-sm mt-2 font-medium">Created</span>
          </div>

          {/* Step 2: Analyzing */}
          <div className="flex flex-col items-center flex-1">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
              caseData.status === 'analyzing'
                ? 'bg-primary-600 text-white animate-pulse'
                : ['analyzed', 'awaiting_approval', 'mailed'].includes(caseData.status)
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-500'
            }`}>
              {caseData.status === 'analyzing' ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <CheckCircle className="w-5 h-5" />
              )}
            </div>
            <span className="text-sm mt-2 font-medium">Analysis</span>
          </div>

          {/* Step 3: Review */}
          <div className="flex flex-col items-center flex-1">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
              caseData.status === 'awaiting_approval'
                ? 'bg-yellow-500 text-white'
                : caseData.status === 'mailed'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-500'
            }`}>
              <Clock className="w-5 h-5" />
            </div>
            <span className="text-sm mt-2 font-medium">Review</span>
          </div>

          {/* Step 4: Mailed */}
          <div className="flex flex-col items-center flex-1">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
              caseData.status === 'mailed'
                ? 'bg-green-600 text-white'
                : 'bg-gray-200 text-gray-500'
            }`}>
              <Mail className="w-5 h-5" />
            </div>
            <span className="text-sm mt-2 font-medium">Sent</span>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Case Details */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Case Details</h2>
          
          <dl className="space-y-3">
            <div>
              <dt className="text-sm font-medium text-gray-500">Deposit Amount</dt>
              <dd className="text-lg font-semibold">${caseData.deposit_amount}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Withheld Amount</dt>
              <dd className="text-lg font-semibold">${caseData.withheld_amount}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Move-Out Date</dt>
              <dd>{new Date(caseData.move_out_date).toLocaleDateString()}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Status</dt>
              <dd>
                <span className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${
                  caseData.status === 'mailed' ? 'bg-green-100 text-green-800' :
                  caseData.status === 'awaiting_approval' ? 'bg-yellow-100 text-yellow-800' :
                  caseData.status === 'analyzing' ? 'bg-blue-100 text-blue-800' :
                  caseData.status === 'error' ? 'bg-red-100 text-red-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {caseData.status}
                </span>
              </dd>
            </div>
          </dl>

          <div className="mt-6 pt-6 border-t">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Dispute Description</h3>
            <p className="text-gray-700">{caseData.dispute_description}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-6">
          {caseData.status === 'draft' && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Next Steps</h2>
              <p className="text-gray-600 mb-4">
                Start the AI analysis to review your case against Texas Property Code.
              </p>
              <button
                onClick={() => executeMutation.mutate()}
                disabled={executeMutation.isPending}
                className="w-full bg-primary-600 text-white py-3 rounded-md hover:bg-primary-700 disabled:opacity-50 font-medium"
              >
                {executeMutation.isPending ? 'Starting Analysis...' : 'Start AI Analysis'}
              </button>
            </div>
          )}

          {analysis && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Legal Analysis</h2>
              
              <div className="mb-4">
                <h3 className="font-medium text-gray-700 mb-2">Summary</h3>
                <p className="text-gray-600 text-sm">{analysis.summary}</p>
              </div>

              <div className="mb-4">
                <h3 className="font-medium text-gray-700 mb-2">Violations Found</h3>
                <ul className="space-y-2">
                  {analysis.violations?.map((v: any, i: number) => (
                    <li key={i} className="text-sm">
                      <span className="font-medium text-red-600">{v.statute}</span>
                      <p className="text-gray-600">{v.description}</p>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-green-50 rounded-md p-4">
                <h3 className="font-semibold text-green-900 mb-2">Total Damages</h3>
                <p className="text-3xl font-bold text-green-600">${analysis.total_damages}</p>
                <p className="text-sm text-gray-600 mt-1">
                  Base: ${analysis.base_damages} + Treble: ${analysis.treble_damages} + Penalty: $100
                </p>
              </div>
            </div>
          )}

          {demandLetter && caseData.status === 'awaiting_approval' && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Demand Letter</h2>
              
              <button
                onClick={() => setShowLetterPreview(!showLetterPreview)}
                className="w-full mb-4 px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                {showLetterPreview ? 'Hide' : 'Preview'} Letter
              </button>

              {showLetterPreview && (
                <div className="mb-4 p-4 border rounded-md bg-gray-50 max-h-96 overflow-y-auto">
                  <div dangerouslySetInnerHTML={{ __html: demandLetter.letter_html }} />
                </div>
              )}

              <div className="space-y-3">
                <button
                  onClick={() => approveMutation.mutate({ approved: true })}
                  disabled={approveMutation.isPending}
                  className="w-full bg-green-600 text-white py-3 rounded-md hover:bg-green-700 disabled:opacity-50 font-medium"
                >
                  {approveMutation.isPending ? 'Sending...' : 'Approve & Send Certified Mail'}
                </button>
                <button
                  onClick={() => approveMutation.mutate({ approved: false })}
                  disabled={approveMutation.isPending}
                  className="w-full border border-gray-300 text-gray-700 py-3 rounded-md hover:bg-gray-50"
                >
                  Reject
                </button>
              </div>
            </div>
          )}

          {caseData.status === 'mailed' && caseData.agent_state?.lob_mail_id && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">✅ Letter Sent!</h2>
              
              <div className="space-y-3">
                <div>
                  <span className="text-sm font-medium text-gray-500">Lob ID:</span>
                  <p className="font-mono text-sm">{caseData.agent_state.lob_mail_id}</p>
                </div>
                {caseData.agent_state.tracking_url && (
                  <div>
                    <a
                      href={caseData.agent_state.tracking_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:underline text-sm"
                    >
                      Track Shipment →
                    </a>
                  </div>
                )}
                {caseData.agent_state.expected_delivery && (
                  <div>
                    <span className="text-sm font-medium text-gray-500">Expected Delivery:</span>
                    <p>{new Date(caseData.agent_state.expected_delivery).toLocaleDateString()}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {caseData.status === 'error' && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
              <div className="flex items-start">
                <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 mr-3" />
                <div>
                  <h3 className="font-semibold text-red-900 mb-1">Error Occurred</h3>
                  <p className="text-red-700 text-sm">{caseData.agent_state?.error || 'An unknown error occurred'}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
