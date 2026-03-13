from datetime import datetime

class REPORTING_AND_ANALYTICS:
    def __init__(self, db):
        self.db = db
        self.collection = db['reports']

    def generate_report(self, report_data):
        """Generates and stores a new report."""
        try:
            report_data["report_date"] = datetime.now().strftime("%Y-%m-%d")
            self.collection.insert_one(report_data)
            return {"message": "Report generation successful!", "report": report_data}, 201
        except Exception as e:
            return {"error": f"Error generating report: {str(e)}"}, 500

    def view_reports(self):
        """Retrieves all reports."""
        try:
            reports = list(self.collection.find())
            for report in reports:
                report['_id'] = str(report['_id'])
            return {"reports": reports}, 200
        except Exception as e:
            return {"error": f"Error viewing reports: {str(e)}"}, 500