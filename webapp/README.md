# Kickstarter Success Predictor - Web Application

A modern web interface for predicting Kickstarter campaign success using AI/ML models.

## 🎯 Features

✅ **Drag & Drop Upload** - Simply drag your Excel/CSV/JSON file into the browser  
✅ **Batch Processing** - Analyze multiple campaigns at once  
✅ **Visual Results** - Clean, modern interface with summary statistics  
✅ **Download Results** - Export predictions as Excel with one click  
✅ **Sample Templates** - Download pre-filled Excel or JSON templates to get started  
✅ **Real-time Analysis** - Instant predictions using trained TensorFlow model

## 🚀 Quick Start

### Option 1: Run Locally (Recommended for Development)

1. **Install Dependencies**
   ```bash
   cd webapp
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   ```
   http://localhost:5000
   ```

### Option 2: Using Docker

1. **Build and Run with Docker Compose**
   ```bash
   cd webapp
   docker-compose up --build
   ```

2. **Access the Application**
   ```
   http://localhost:5000
   ```

## 📊 How to Use

1. **Download Sample Template** - Click either "Download Excel Template" or "Download JSON Template" to see the required format
2. **Prepare Your Data** - Fill in your campaign information following the sample format
3. **Upload File** - Drag & drop your Excel/CSV/JSON file or click to browse
4. **View Results** - See predictions with success probabilities and verdicts
5. **Download Results** - Export the analyzed data with predictions

## 📝 Required Data Format

Your Excel/CSV/JSON file must include these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `name` | Campaign name (optional) | "Smart Home Device" |
| `goal` | Funding goal amount | 50000 |
| `pledged` | Amount pledged so far | 75000 |
| `backers` | Number of backers | 1250 |
| `usd pledged` | USD equivalent of pledged amount | 75000 |
| `category` | Specific category | "Technology" |
| `main_category` | Main category | "Technology" |
| `currency` | Currency code | "USD" |
| `country` | Country code | "US" |
| `deadline` | Campaign end date | "2024-12-31" |
| `launched` | Campaign launch date | "2024-09-01" |

**JSON Format Example:**
```json
[
  {
    "name": "Smart Home Device",
    "goal": 50000,
    "pledged": 75000,
    "backers": 1250,
    "usd pledged": 75000,
    "category": "Technology",
    "main_category": "Technology",
    "currency": "USD",
    "country": "US",
    "deadline": "2024-12-31",
    "launched": "2024-09-01"
  }
]
```

## 🎨 UI Preview

The web interface includes:
- **Upload Area**: Drag & drop zone with file browser
- **Loading Indicator**: Real-time progress feedback
- **Results Dashboard**: Summary statistics (total campaigns, success rate, etc.)
- **Results Table**: Detailed predictions for each campaign
- **Action Buttons**: Download results, upload another file

## 📈 Model Information

- **Model Type**: Deep Neural Network (TensorFlow/Keras)
- **Training Data**: 37,887 Kickstarter campaigns
- **Accuracy**: 92.08%
- **AUC Score**: 0.9780

The model analyzes:
- Campaign goals and funding metrics
- Category and geographic data
- Temporal features (campaign duration, launch timing)
- Backers and engagement metrics

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/upload` | POST | Upload and process file |
| `/download_results` | POST | Download results as Excel |
| `/sample` | GET | Download Excel sample template |
| `/sample/json` | GET | Download JSON sample template |
| `/health` | GET | Health check endpoint |

## 🐳 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Deploy to Cloud Platforms

**Heroku:**
```bash
# Add Procfile
echo "web: gunicorn app:app" > Procfile
heroku create your-app-name
git push heroku main
```

**AWS/Azure:**
- Use Elastic Beanstalk or App Service
- Configure Python runtime and install dependencies
- Set environment variables

**Docker:**
```bash
docker build -t kickstarter-predictor .
docker run -p 5000:5000 kickstarter-predictor
```

## 🛠️ Development

### Project Structure

```
webapp/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Web interface
├── static/               # Static assets (if needed)
├── uploads/              # Temporary file storage
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
└── README.md           # This file
```

### Environment Variables

- `FLASK_ENV`: Set to `production` for deployment
- `FLASK_APP`: Application entry point (default: `app.py`)

## 🔒 Security Notes

- Maximum file size: 16MB
- Allowed file types: `.xlsx`, `.xls`, `.csv`
- Uploaded files are stored temporarily in `uploads/` directory
- Consider adding authentication for production use
- Implement rate limiting for public deployments

## 🐛 Troubleshooting

**Model not loading:**
- Ensure `artifacts/` directory exists in parent folder
- Check that `kickstarter_model.keras`, `scaler.pkl`, and `feature_columns.json` are present

**Import errors:**
- Verify `src/model_pipeline.py` exists in parent directory
- Install all requirements: `pip install -r requirements.txt`

**File upload fails:**
- Check file size (max 16MB)
- Verify file format (Excel, CSV, or JSON)
- Ensure all required columns are present
- For JSON: ensure it's an array of objects with correct structure

## 📚 Additional Resources

- [Main Project Documentation](../docs/INDEX.md)
- [Model Training Details](../docs/MODEL.md)
- [API Documentation](../docs/API.md)
- [Quick Start Guide](../docs/QUICKSTART.md)

## 👨‍💻 Author

**Mohamed SharafEldin**  
Academic Number: 202201849

## 📄 License

This project is part of academic coursework. Please refer to the main project for licensing information.

## 🤝 Contributing

For contributions, please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Need Help?** Check the [main documentation](../docs/) or open an issue.
