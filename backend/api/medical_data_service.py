from .models import MedicalData
from django.core.exceptions import ObjectDoesNotExist

class MedicalDataService:
    @staticmethod
    def save_medical_report(user_id: int, text_content: str) -> MedicalData:
        """Save medical report text for a user"""
        return MedicalData.objects.create(
            user_id=user_id,
            data_type="medical_report",
            data_content={"text": text_content},
            source="user_upload"
        )

    @staticmethod
    def get_latest_report(user_id: int) -> str:
        """Get the latest medical report for a user"""
        try:
            latest_report = MedicalData.objects.filter(
                user_id=user_id,
                data_type="medical_report"
            ).latest('date_uploaded')
            return latest_report.data_content.get('text', '')
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_report_history(user_id: int, limit: int = 5):
        """Get report history for a user"""
        reports = MedicalData.objects.filter(
            user_id=user_id,
            data_type="medical_report"
        ).order_by('-date_uploaded')[:limit]
        return [
            {
                'id': report.medical_data_id,
                'content': report.data_content.get('text', ''),
                'date': report.date_uploaded.isoformat()
            }
            for report in reports
        ]