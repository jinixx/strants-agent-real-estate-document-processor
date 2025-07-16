#!/usr/bin/env python3
"""
Create sample PDF documents for testing StrandsDocumentProcessor
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_settlement_pdf():
    """Create a sample settlement statement PDF"""
    filename = "sample_settlement_statement.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor='blue'
    )
    
    # Content
    story = []
    
    # Title
    story.append(Paragraph("SETTLEMENT STATEMENT", title_style))
    story.append(Spacer(1, 20))
    
    # Property Information
    story.append(Paragraph("PROPERTY INFORMATION", heading_style))
    story.append(Paragraph("Property Address: 123 Oak Street, Springfield, IL 62701", styles['Normal']))
    story.append(Paragraph("Sale Price: $425,000.00", styles['Normal']))
    story.append(Paragraph("Closing Date: January 15, 2024", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Buyer Information
    story.append(Paragraph("BUYER INFORMATION", heading_style))
    story.append(Paragraph("Name: John Smith", styles['Normal']))
    story.append(Paragraph("Address: 456 Elm Avenue, Springfield, IL 62702", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Seller Information
    story.append(Paragraph("SELLER INFORMATION", heading_style))
    story.append(Paragraph("Name: Jane Doe", styles['Normal']))
    story.append(Paragraph("Address: 789 Pine Road, Springfield, IL 62703", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Commission Details
    story.append(Paragraph("COMMISSION DETAILS", heading_style))
    story.append(Paragraph("Total Commission: $25,500.00 (6.0%)", styles['Normal']))
    story.append(Paragraph("Listing Agent Commission: $12,750.00 (3.0%)", styles['Normal']))
    story.append(Paragraph("Buyer Agent Commission: $12,750.00 (3.0%)", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Agent Information
    story.append(Paragraph("LISTING AGENT", heading_style))
    story.append(Paragraph("Name: Sarah Johnson", styles['Normal']))
    story.append(Paragraph("Brokerage: Premier Real Estate Group", styles['Normal']))
    story.append(Paragraph("License #: RE123456", styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("BUYER AGENT", heading_style))
    story.append(Paragraph("Name: Michael Brown", styles['Normal']))
    story.append(Paragraph("Brokerage: Springfield Realty Partners", styles['Normal']))
    story.append(Paragraph("License #: RE789012", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Settlement Charges
    story.append(Paragraph("SETTLEMENT CHARGES", heading_style))
    story.append(Paragraph("Loan Origination Fee: $2,125.00", styles['Normal']))
    story.append(Paragraph("Appraisal Fee: $500.00", styles['Normal']))
    story.append(Paragraph("Credit Report: $25.00", styles['Normal']))
    story.append(Paragraph("Title Insurance: $1,275.00", styles['Normal']))
    story.append(Paragraph("Recording Fees: $150.00", styles['Normal']))
    story.append(Paragraph("Transfer Tax: $850.00", styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("TOTAL SETTLEMENT CHARGES: $4,925.00", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Summary
    story.append(Paragraph("SETTLEMENT SUMMARY", heading_style))
    story.append(Paragraph("NET TO SELLER: $394,575.00", styles['Normal']))
    story.append(Paragraph("CASH FROM BUYER: $89,925.00", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Footer
    story.append(Paragraph("This settlement statement is prepared in accordance with RESPA requirements.", styles['Italic']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Closing Agent: Springfield Title Company", styles['Normal']))
    story.append(Paragraph("Date Prepared: January 10, 2024", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Created sample PDF: {filename}")
    return filename

def create_purchase_agreement_pdf():
    """Create a sample purchase agreement PDF"""
    filename = "sample_purchase_agreement.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor='blue'
    )
    
    story = []
    
    # Title
    story.append(Paragraph("REAL ESTATE PURCHASE AGREEMENT", title_style))
    story.append(Spacer(1, 20))
    
    # Property Information
    story.append(Paragraph("PROPERTY INFORMATION", heading_style))
    story.append(Paragraph("Property Address: 456 Maple Drive, Chicago, IL 60601", styles['Normal']))
    story.append(Paragraph("Purchase Price: $550,000.00", styles['Normal']))
    story.append(Paragraph("Earnest Money: $11,000.00", styles['Normal']))
    story.append(Paragraph("Closing Date: March 30, 2024", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Buyer Information
    story.append(Paragraph("BUYER INFORMATION", heading_style))
    story.append(Paragraph("Name: Robert Wilson", styles['Normal']))
    story.append(Paragraph("Address: 789 Cedar Lane, Chicago, IL 60602", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Seller Information
    story.append(Paragraph("SELLER INFORMATION", heading_style))
    story.append(Paragraph("Name: Lisa Anderson", styles['Normal']))
    story.append(Paragraph("Address: 321 Birch Street, Chicago, IL 60603", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Agent Information
    story.append(Paragraph("REAL ESTATE AGENTS", heading_style))
    story.append(Paragraph("Buyer's Agent: David Martinez", styles['Normal']))
    story.append(Paragraph("Brokerage: Chicago Premier Realty", styles['Normal']))
    story.append(Paragraph("Listing Agent: Emily Davis", styles['Normal']))
    story.append(Paragraph("Brokerage: Windy City Real Estate", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Contingencies
    story.append(Paragraph("CONTINGENCIES", heading_style))
    story.append(Paragraph("• Financing Contingency: 30 days", styles['Normal']))
    story.append(Paragraph("• Home Inspection Contingency: 10 days", styles['Normal']))
    story.append(Paragraph("• Appraisal Contingency: 21 days", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Terms
    story.append(Paragraph("ADDITIONAL TERMS", heading_style))
    story.append(Paragraph("Property sold in 'as-is' condition", styles['Normal']))
    story.append(Paragraph("Seller to provide clear title", styles['Normal']))
    story.append(Paragraph("Buyer responsible for all inspections", styles['Normal']))
    
    doc.build(story)
    print(f"✅ Created sample PDF: {filename}")
    return filename

if __name__ == "__main__":
    print("🔧 Creating sample PDF documents for testing...")
    
    settlement_pdf = create_settlement_pdf()
    purchase_pdf = create_purchase_agreement_pdf()
    
    print(f"\n📄 Sample PDFs created:")
    print(f"   • {settlement_pdf}")
    print(f"   • {purchase_pdf}")
    print(f"\n🚀 Ready to test! Upload these PDFs to the StrandsDocumentProcessor web interface.")
