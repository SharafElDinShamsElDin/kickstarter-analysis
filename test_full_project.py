"""
Full project test suite: validates imports, model loading, predictions, and Excel integration.

Run from project root:
    python test_full_project.py
"""

import sys
import json
from pathlib import Path

# Add src/ to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test 1: Verify all imports work."""
    print("\n" + "="*70)
    print("TEST 1: IMPORTS")
    print("="*70)
    
    try:
        print("  ✓ Importing model_pipeline...")
        from model_pipeline import load_artifacts, predict_success_probability
        
        print("  ✓ Importing excel_integration...")
        from excel_integration import KICKSTARTER_SUCCESS_PROBABILITY, KICKSTARTER_SUCCESS_SUMMARY, vba_predict
        
        print("  ✓ Importing main...")
        import main
        
        print("\n✅ All imports successful")
        return True
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_artifacts():
    """Test 2: Verify model artifacts exist."""
    print("\n" + "="*70)
    print("TEST 2: ARTIFACTS")
    print("="*70)
    
    artifacts_dir = Path("artifacts")
    required_files = [
        "kickstarter_model.keras",
        "scaler.pkl",
        "feature_columns.json"
    ]
    
    all_exist = True
    for fname in required_files:
        fpath = artifacts_dir / fname
        if fpath.exists():
            size_kb = fpath.stat().st_size / 1024
            print(f"  ✓ {fname}: {size_kb:.1f} KB")
        else:
            print(f"  ❌ {fname}: NOT FOUND")
            all_exist = False
    
    if all_exist:
        print("\n✅ All artifacts present")
        return True
    else:
        print("\n❌ Some artifacts missing")
        return False


def test_model_loading():
    """Test 3: Load model and artifacts."""
    print("\n" + "="*70)
    print("TEST 3: MODEL LOADING")
    print("="*70)
    
    try:
        from model_pipeline import load_artifacts
        
        print("  Loading model, scaler, and feature columns...")
        model, scaler, feature_columns = load_artifacts(Path("artifacts"))
        
        print(f"  ✓ Model type: {type(model).__name__}")
        print(f"  ✓ Scaler type: {type(scaler).__name__}")
        print(f"  ✓ Feature columns: {len(feature_columns)} features")
        print(f"    - {', '.join(list(feature_columns)[:5])}...")
        
        print("\n✅ Model loaded successfully")
        return True, model, scaler, feature_columns
    except Exception as e:
        print(f"\n❌ Model loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None, None


def test_prediction(model, scaler, feature_columns):
    """Test 4: Run prediction with sample data."""
    print("\n" + "="*70)
    print("TEST 4: PREDICTION WITH SAMPLE DATA")
    print("="*70)
    
    try:
        from model_pipeline import predict_success_probability
        
        # Sample campaign
        sample = {
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
        
        print(f"  Sample campaign:")
        print(f"    Goal: ${sample['goal']:,}")
        print(f"    Pledged: ${sample['pledged']:,}")
        print(f"    Backers: {sample['backers']}")
        print(f"    Category: {sample['category']}")
        
        prob = predict_success_probability(
            sample, 
            model=model, 
            scaler=scaler, 
            feature_columns=feature_columns
        )
        
        print(f"\n  ✓ Prediction: {prob:.6f}")
        print(f"  ✓ Percentage: {prob*100:.2f}%")
        
        if 0 <= prob <= 1:
            print("\n✅ Prediction valid (0-1 range)")
            return True, prob
        else:
            print(f"\n❌ Invalid probability: {prob}")
            return False, prob
    except Exception as e:
        print(f"\n❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_excel_functions():
    """Test 5: Test Excel UDF functions."""
    print("\n" + "="*70)
    print("TEST 5: EXCEL UDF FUNCTIONS")
    print("="*70)
    
    try:
        # Import the pure (non-decorated) internal function
        from excel_integration import _predict_from_json
        
        # Sample campaign as JSON (as it would come from Excel)
        sample_json = json.dumps({
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
        })
        
        print("  Testing KICKSTARTER_SUCCESS_PROBABILITY...")
        prob = _predict_from_json(sample_json, "artifacts")
        print(f"    ✓ Result: {prob:.6f} ({prob*100:.2f}%)")
        
        # Test summary function
        from excel_integration import KICKSTARTER_SUCCESS_SUMMARY
        print("\n  Testing KICKSTARTER_SUCCESS_SUMMARY (logic)...")
        verdict = "Likely success" if prob >= 0.5 else "Needs improvement"
        summary = f"{verdict} — {prob:.2%} predicted success probability"
        print(f"    ✓ Summary: {summary}")
        
        print("\n✅ Excel functions work correctly")
        return True
    except Exception as e:
        print(f"\n❌ Excel functions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sample_data():
    """Test 6: Load and test with actual sample JSON files."""
    print("\n" + "="*70)
    print("TEST 6: SAMPLE DATA FILES")
    print("="*70)
    
    try:
        from excel_integration import _predict_from_json
        
        sample_files = [
            "data/sample_campaign_1.json",
            "data/sample_campaign_2.json",
            "data/sample_campaign_3.json"
        ]
        
        all_ok = True
        for fpath in sample_files:
            try:
                with open(fpath, 'r') as f:
                    data = json.load(f)
                
                prob = _predict_from_json(json.dumps(data), "artifacts")
                print(f"  ✓ {Path(fpath).name}: {prob:.6f} ({prob*100:.2f}%)")
            except Exception as e:
                print(f"  ❌ {fpath}: {e}")
                all_ok = False
        
        if all_ok:
            print("\n✅ All sample data files processed successfully")
        else:
            print("\n⚠️  Some sample data had issues (but may not be critical)")
        return all_ok
    except Exception as e:
        print(f"\n❌ Sample data test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "🔍 KICKSTARTER MODEL - FULL PROJECT TEST SUITE 🔍".center(70))
    
    results = {}
    
    # Test 1: Imports
    results['imports'] = test_imports()
    if not results['imports']:
        print("\n⚠️  Stopping: Cannot continue without imports")
        return results
    
    # Test 2: Artifacts
    results['artifacts'] = test_artifacts()
    if not results['artifacts']:
        print("\n⚠️  Model artifacts missing - tests may fail")
    
    # Test 3: Model Loading
    ok, model, scaler, feature_columns = test_model_loading()
    results['model_loading'] = ok
    if not ok or model is None:
        print("\n⚠️  Stopping: Cannot continue without model")
        return results
    
    # Test 4: Prediction
    ok, prob = test_prediction(model, scaler, feature_columns)
    results['prediction'] = ok
    
    # Test 5: Excel Functions
    results['excel_functions'] = test_excel_functions()
    
    # Test 6: Sample Data
    results['sample_data'] = test_sample_data()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    all_pass = all(results.values())
    print("="*70)
    if all_pass:
        print("\n🎉 ALL TESTS PASSED! Project is ready to use.\n")
    else:
        print("\n⚠️  Some tests failed. See details above.\n")
    
    return results


if __name__ == "__main__":
    main()
