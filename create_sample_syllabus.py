from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_sample_pdf(filename="sample_syllabus.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor("#1E293B"),
        alignment=0,
        spaceAfter=10
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10
    )

    story = []

    # Page 1: Title, Overview, Unit 1, Unit 2
    story.append(Paragraph("Course Syllabus: CS401 - Artificial Intelligence & Deep Learning", title_style))
    story.append(Paragraph("Department of Computer Science & Engineering | Academic Year 2024-2025", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#CBD5E1"), spaceAfter=15))

    story.append(Paragraph("Course Overview", heading_style))
    story.append(Paragraph("This course provides a comprehensive introduction to Artificial Intelligence, Machine Learning techniques, and Deep Learning architectures. Students will gain practical and theoretical understanding of intelligent search, neural networks, and computer vision.", body_style))

    story.append(Paragraph("Unit 1: Introduction to AI & Search Algorithms", heading_style))
    story.append(Paragraph("Foundations of AI, Problem Formulation, State Space Search, Uninformed Search strategies (BFS, DFS), Informed Search (Greedy Best-First, A* Algorithm), Heuristic Functions, Adversarial Search and Game Playing (Minimax Algorithm, Alpha-Beta Pruning).", body_style))

    story.append(Paragraph("Unit 2: Machine Learning Fundamentals", heading_style))
    story.append(Paragraph("Supervised vs Unsupervised Learning, Linear Regression, Logistic Regression for Classification, Decision Trees, Random Forests, Support Vector Machines (SVM), Evaluation Metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC curve), Overfitting and Regularization Techniques (L1, L2).", body_style))

    # Force Page Break to Page 2
    story.append(PageBreak())

    # Page 2: Unit 3, Unit 4, Unit 5, Grading
    story.append(Paragraph("Unit 3: Deep Learning & Computer Vision", heading_style))
    story.append(Paragraph("Multilayer Perceptrons (MLP), Backpropagation, Activation Functions (ReLU, Sigmoid, Softmax), Convolutional Neural Networks (CNN), Convolutional and Pooling Layers, Image Classification, Object Detection (YOLO), Transfer Learning (ResNet, VGG).", body_style))

    story.append(Paragraph("Unit 4: Natural Language Processing (NLP)", heading_style))
    story.append(Paragraph("Text Preprocessing, Tokenization, Stemming, Lemmatization, Bag of Words, TF-IDF, Word Embeddings (Word2Vec, GloVe), Recurrent Neural Networks (RNN), LSTM, Attention Mechanism, Transformer Architectures (BERT, GPT), Sentiment Analysis.", body_style))

    story.append(Paragraph("Unit 5: AI Ethics & Model Deployment", heading_style))
    story.append(Paragraph("Bias and Fairness in Machine Learning models, AI Ethics and Safety, Explainable AI (SHAP, LIME), Model Compression (Quantization, Pruning), Model Deployment using FastAPI and Docker, Continuous Monitoring.", body_style))

    story.append(Paragraph("Evaluation & Grading Scheme", heading_style))
    story.append(Paragraph("• Internal Assessment & Assignments: 20%<br/>• Mid-Semester Examination: 20%<br/>• Mini-Project Presentation: 20%<br/>• End-Semester Final Examination: 40%", body_style))

    doc.build(story)
    print(f"Sample syllabus PDF created successfully: {filename}")

if __name__ == "__main__":
    generate_sample_pdf()
