"""
Flask Web Application for Kickstarter Success Prediction

Author: Mohamed SharafEldin
Academic number: 202201849

Features:
- Upload Excel files with campaign data
- Batch prediction for multiple campaigns
- Download results as Excel
- Clean, modern UI
"""

import json
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import sys

# Add parent src directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir / "src"))

from model_pipeline import load_artifacts, predict_success_probability

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv', 'json'}

# Create upload folder if it doesn't exist
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# Load model artifacts once at startup
MODEL_DIR = parent_dir / "artifacts"
print(f"Loading model from: {MODEL_DIR}")
model, scaler, feature_columns = load_artifacts(MODEL_DIR)
print(f"Model loaded successfully!")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Main page with file upload interface"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process predictions"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload Excel (.xlsx, .xls), CSV, or JSON files'}), 400
    
    try:
        # Read the uploaded file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.json'):
            # Read JSON content and handle both list and dict formats
            json_content = json.load(file)
            if isinstance(json_content, list):
                df = pd.DataFrame(json_content)
            elif isinstance(json_content, dict):
                # If it's a dict with list values, use it directly
                # If it's a dict with scalar values, wrap in a list
                if all(isinstance(v, (list, tuple)) for v in json_content.values()):
                    df = pd.DataFrame(json_content)
                else:
                    df = pd.DataFrame([json_content])
            else:
                return jsonify({'error': 'Invalid JSON format. Expected a list of objects or a dictionary'}), 400
        else:
            df = pd.read_excel(file)
        
        # Validate required columns
        required_columns = ['goal', 'pledged', 'backers', 'usd pledged', 'category', 
                          'main_category', 'currency', 'country', 'deadline', 'launched']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {", ".join(missing_columns)}',
                'required': required_columns
            }), 400
        
        # Process each campaign
        results = []
        for idx, row in df.iterrows():
            campaign_data = row.to_dict()
            
            try:
                probability = predict_success_probability(
                    campaign_data, 
                    model=model, 
                    scaler=scaler, 
                    feature_columns=feature_columns
                )
                
                verdict = "Likely Success" if probability >= 0.5 else "Needs Improvement"
                confidence = "High" if (probability >= 0.7 or probability <= 0.3) else "Medium"
                
                results.append({
                    'row': idx + 1,
                    'campaign': campaign_data.get('name', f'Campaign {idx + 1}'),
                    'goal': float(campaign_data['goal']) if pd.notna(campaign_data['goal']) else 0,
                    'category': str(campaign_data['category']),
                    'country': str(campaign_data['country']),
                    'probability': round(float(probability) * 100, 2),
                    'verdict': verdict,
                    'confidence': confidence
                })
            except Exception as e:
                results.append({
                    'row': idx + 1,
                    'campaign': campaign_data.get('name', f'Campaign {idx + 1}'),
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'total_campaigns': len(df),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/download_results', methods=['POST'])
def download_results():
    """Download prediction results as Excel file"""
    try:
        data = request.json
        results = data.get('results', [])
        
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'kickstarter_predictions_{timestamp}.xlsx'
        filepath = app.config['UPLOAD_FOLDER'] / filename
        
        # Save to Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({'error': f'Error generating download: {str(e)}'}), 500

@app.route('/sample')
def download_sample():
    """Download a sample Excel template"""
    sample_data = {
        'name': ['Smart Home Device', 'Indie Film Project', 'Board Game Adventure'],
        'goal': [50000, 10000, 5000],
        'pledged': [75000, 5000, 6000],
        'backers': [1250, 150, 200],
        'usd pledged': [75000, 5000, 6000],
        'category': ['Technology', 'Film & Video', 'Games'],
        'main_category': ['Technology', 'Film & Video', 'Games'],
        'currency': ['USD', 'USD', 'GBP'],
        'country': ['US', 'US', 'GB'],
        'deadline': ['2024-12-31', '2024-11-30', '2024-10-15'],
        'launched': ['2024-09-01', '2024-10-01', '2024-08-01']
    }
    
    df = pd.DataFrame(sample_data)
    filepath = app.config['UPLOAD_FOLDER'] / 'sample_template.xlsx'
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    return send_file(filepath, as_attachment=True, download_name='kickstarter_sample_template.xlsx')

@app.route('/sample/json')
def download_sample_json():
    """Download a sample JSON template"""
    sample_data = [
        {
            'name': 'Smart Home Device',
            'goal': 50000,
            'pledged': 75000,
            'backers': 1250,
            'usd pledged': 75000,
            'category': 'Technology',
            'main_category': 'Technology',
            'currency': 'USD',
            'country': 'US',
            'deadline': '2024-12-31',
            'launched': '2024-09-01'
        },
        {
            'name': 'Indie Film Project',
            'goal': 10000,
            'pledged': 5000,
            'backers': 150,
            'usd pledged': 5000,
            'category': 'Film & Video',
            'main_category': 'Film & Video',
            'currency': 'USD',
            'country': 'US',
            'deadline': '2024-11-30',
            'launched': '2024-10-01'
        },
        {
            'name': 'Board Game Adventure',
            'goal': 5000,
            'pledged': 6000,
            'backers': 200,
            'usd pledged': 6000,
            'category': 'Games',
            'main_category': 'Games',
            'currency': 'GBP',
            'country': 'GB',
            'deadline': '2024-10-15',
            'launched': '2024-08-01'
        }
    ]
    
    filepath = app.config['UPLOAD_FOLDER'] / 'sample_template.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2)
    
    return send_file(filepath, as_attachment=True, download_name='kickstarter_sample_template.json')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/report')
def academic_report():
    """Display academic report page"""
    return render_template('report.html')

@app.route('/api/model_info')
def model_info():
    """Return model information as JSON"""
    info = {
        'project': {
            'title': 'Kickstarter Campaign Success Prediction',
            'author': 'Mohamed SharafEldin',
            'academic_id': '202201849',
            'institution': 'Cairo University',
            'supervisors': ['Dr. Tarek Ali', 'Prof. Mervat Gheith'],
            'date': '2025'
        },
        'model': {
            'type': 'Deep Neural Network',
            'framework': 'TensorFlow/Keras',
            'architecture': {
                'input_features': 58,
                'hidden_layers': [
                    {'units': 128, 'activation': 'relu'},
                    {'dropout': 0.2},
                    {'units': 64, 'activation': 'relu'},
                ],
                'output_layer': {'units': 1, 'activation': 'sigmoid'}
            },
            'optimizer': 'Adam',
            'loss_function': 'binary_crossentropy',
            'metrics': ['accuracy', 'AUC']
        },
        'performance': {
            'training_accuracy': 0.9136,
            'validation_accuracy': 0.9208,
            'auc_score': 0.9780,
            'training_samples': 37887
        },
        'features': {
            'total': 58,
            'categories': ['Temporal', 'Financial', 'Geographic', 'Categorical'],
            'engineering': ['One-hot encoding', 'Standard scaling', 'Date feature extraction']
        },
        'tech_stack': {
            'backend': ['Python 3.9+', 'Flask', 'TensorFlow', 'Scikit-learn', 'Pandas'],
            'frontend': ['HTML5', 'CSS3', 'JavaScript'],
            'deployment': ['Docker', 'Gunicorn']
        }
    }
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
