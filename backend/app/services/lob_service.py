import lob
from app.config import settings
from app.models.schemas import AddressSchema, MailingResult
from typing import Dict, Any
from datetime import date


class LobService:
    """Service for sending certified mail via Lob API."""
    
    def __init__(self):
        self.client = lob.Client(api_key=settings.LOB_API_KEY)
    
    def _format_address_for_lob(self, address: Dict[str, Any]) -> Dict[str, str]:
        """
        Convert internal address format to Lob API format.
        
        Args:
            address: Dictionary with address fields
            
        Returns:
            Lob-formatted address dictionary
        """
        lob_address = {
            "name": address["name"],
            "address_line1": address["address_line1"],
            "address_city": address["address_city"],
            "address_state": address["address_state"],
            "address_zip": address["address_zip"]
        }
        
        if address.get("address_line2"):
            lob_address["address_line2"] = address["address_line2"]
        
        return lob_address
    
    async def send_certified_letter(
        self,
        to_address: Dict[str, Any],
        from_address: Dict[str, Any],
        letter_html: str,
        description: str = "Security Deposit Demand Letter"
    ) -> MailingResult:
        """
        Send certified mail via Lob API.
        
        Args:
            to_address: Recipient address
            from_address: Sender address
            letter_html: HTML content of letter
            description: Letter description
            
        Returns:
            MailingResult with tracking info
            
        Raises:
            lob.error.LobError: If API call fails
        """
        try:
            # Format addresses for Lob
            to_lob = self._format_address_for_lob(to_address)
            from_lob = self._format_address_for_lob(from_address)
            
            # Create letter via Lob API
            letter = self.client.Letter.create(
                description=description,
                to_address=to_lob,
                from_address=from_lob,
                file=letter_html,
                color=True,
                double_sided=False,
                extra_service="certified",
                mail_type="usps_first_class"
            )
            
            # Extract tracking information
            tracking_url = None
            if hasattr(letter, 'tracking_events') and letter.tracking_events:
                tracking_url = letter.tracking_events[0].get('url')
            
            expected_delivery = None
            if hasattr(letter, 'expected_delivery_date'):
                # Parse date string if needed
                expected_delivery = letter.expected_delivery_date
            
            return MailingResult(
                lob_id=letter.id,
                tracking_url=tracking_url,
                expected_delivery=expected_delivery
            )
            
        except lob.error.LobError as e:
            # Re-raise with more context
            raise ValueError(f"Lob API error: {str(e)}")
    
    async def verify_address(self, address: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify address using Lob's verification service.
        
        Args:
            address: Address to verify
            
        Returns:
            Verified/corrected address or original if verification fails
        """
        try:
            lob_address = self._format_address_for_lob(address)
            verified = self.client.USVerification.create(**lob_address)
            
            if hasattr(verified, 'deliverability') and verified.deliverability == 'deliverable':
                # Return corrected address
                return {
                    "name": address["name"],
                    "address_line1": verified.primary_line,
                    "address_line2": verified.secondary_line or "",
                    "address_city": verified.components.city,
                    "address_state": verified.components.state,
                    "address_zip": verified.components.zip_code
                }
            else:
                # Address not deliverable - return original
                return address
                
        except lob.error.LobError:
            # Verification failed - return original address
            return address


# Singleton instance
lob_service = LobService()
