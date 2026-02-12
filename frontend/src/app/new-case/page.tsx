'use client';

import { useForm } from 'react-hook-form';
import { useMutation } from '@tanstack/react-query';
import { casesApi } from '@/lib/api';
import { useRouter } from 'next/navigation';
import type { CreateCaseInput } from '@/types';

export default function NewCasePage() {
  const router = useRouter();
  const { register, handleSubmit, formState: { errors } } = useForm<CreateCaseInput>();

  const createMutation = useMutation({
    mutationFn: casesApi.create,
    onSuccess: (data) => {
      router.push(`/cases/${data.id}`);
    },
  });

  const onSubmit = (data: CreateCaseInput) => {
    createMutation.mutate(data);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Create New Case</h1>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* Tenant Information */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Tenant Information</h2>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Full Name *
            </label>
            <input
              {...register('tenant_name', { required: 'Name is required' })}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              placeholder="John Doe"
            />
            {errors.tenant_name && (
              <p className="text-red-600 text-sm mt-1">{errors.tenant_name.message}</p>
            )}
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Street Address *
              </label>
              <input
                {...register('tenant_address.address_line1', { required: true })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
                placeholder="123 Main St"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Apt/Unit (Optional)
              </label>
              <input
                {...register('tenant_address.address_line2')}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
                placeholder="Apt 4"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mt-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                City *
              </label>
              <input
                {...register('tenant_address.address_city', { required: true })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
                placeholder="Austin"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                State *
              </label>
              <input
                {...register('tenant_address.address_state', { 
                  required: true,
                  pattern: /^[A-Z]{2}$/,
                  value: 'TX'
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
                placeholder="TX"
                maxLength={2}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ZIP Code *
              </label>
              <input
                {...register('tenant_address.address_zip', { 
                  required: true,
                  pattern: /^\d{5}$/
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
                placeholder="78701"
              />
            </div>
          </div>

          <input type="hidden" {...register('tenant_address.name')} value="" />
        </div>

        {/* Landlord Information */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Landlord Information</h2>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Landlord Name *
            </label>
            <input
              {...register('landlord_name', { required: true })}
              className="w-full px-4 py-2 border border-gray-300 rounded-md"
              placeholder="ABC Property Management"
            />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Street Address *
              </label>
              <input
                {...register('landlord_address.address_line1', { required: true })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Suite/Unit (Optional)
              </label>
              <input
                {...register('landlord_address.address_line2')}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mt-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                City *
              </label>
              <input
                {...register('landlord_address.address_city', { required: true })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                State *
              </label>
              <input
                {...register('landlord_address.address_state', { 
                  required: true,
                  value: 'TX'
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
                value="TX"
                maxLength={2}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ZIP Code *
              </label>
              <input
                {...register('landlord_address.address_zip', { required: true })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>

          <input type="hidden" {...register('landlord_address.name')} value="" />
        </div>

        {/* Deposit Details */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Deposit Details</h2>
          
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Original Deposit Amount *
              </label>
              <div className="relative">
                <span className="absolute left-3 top-2 text-gray-500">$</span>
                <input
                  type="number"
                  step="0.01"
                  {...register('deposit_amount', { required: true, min: 0 })}
                  className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md"
                  placeholder="1500.00"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Amount Withheld *
              </label>
              <div className="relative">
                <span className="absolute left-3 top-2 text-gray-500">$</span>
                <input
                  type="number"
                  step="0.01"
                  {...register('withheld_amount', { required: true, min: 0 })}
                  className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md"
                  placeholder="1500.00"
                />
              </div>
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Move-Out Date *
            </label>
            <input
              type="date"
              {...register('move_out_date', { required: true })}
              className="w-full px-4 py-2 border border-gray-300 rounded-md"
            />
          </div>
        </div>

        {/* Dispute Description */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Dispute Description</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe the dispute in detail *
            </label>
            <textarea
              {...register('dispute_description', { required: true, minLength: 10 })}
              rows={6}
              className="w-full px-4 py-2 border border-gray-300 rounded-md"
              placeholder="Landlord withheld full deposit without providing itemized deductions within 30 days of move-out. No damage or cleaning issues existed..."
            />
            {errors.dispute_description && (
              <p className="text-red-600 text-sm mt-1">Please provide at least 10 characters</p>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => router.push('/')}
            className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={createMutation.isPending}
            className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {createMutation.isPending ? 'Creating...' : 'Create Case'}
          </button>
        </div>

        {createMutation.isError && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-700">
            Error: {createMutation.error.message}
          </div>
        )}
      </form>
    </div>
  );
}
