#!/bin/bash

# START_HERE.sh - The Absolute Simplest Way to Run the Project

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          🚀 KICKSTARTER PREDICTOR - START HERE (SIMPLEST WAY) 🚀           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


📝 STEP 1: Copy and paste this into your Terminal
───────────────────────────────────────────────────────────────────────────────

    cd /Users/emkanlaptop/Desktop/model
    source .venv/bin/activate
    python scripts/excel_listener.py


✅ STEP 2: What happens next?
───────────────────────────────────────────────────────────────────────────────

   • Excel automatically opens
   • A spreadsheet appears with headers
   • You see example data in row 5
   • The terminal shows: "Monitoring Excel for changes..."


📊 STEP 3: Try it with the example data
───────────────────────────────────────────────────────────────────────────────

   In Excel:
   1. Look at row 5 (example campaign data is already there)
   2. Press Cmd+S to save the workbook
   3. Look at column L (far right)
   4. A prediction appears! (0.999981 = 99.99% success)


📝 STEP 4: Add your own campaign
───────────────────────────────────────────────────────────────────────────────

   In Excel:
   1. Click on cell A6 (start of row 6)
   2. Fill in columns A-J with your campaign data:
      
      A: Goal           (e.g., 50000)
      B: Pledged        (e.g., 75000)
      C: Backers        (e.g., 1250)
      D: USD Pledged    (e.g., 75000)
      E: Category       (e.g., Technology, Design, Film)
      F: Main Category  (e.g., Technology)
      G: Currency       (e.g., USD)
      H: Country        (e.g., US)
      I: Deadline       (e.g., 2024-12-31)
      J: Launched       (e.g., 2024-09-01)

   3. Press Cmd+S to save
   4. Wait 2 seconds
   5. Check column L for prediction!


🔄 STEP 5: Repeat for more campaigns
───────────────────────────────────────────────────────────────────────────────

   • Add campaigns in rows 7, 8, 9, etc.
   • Each one gets a prediction automatically
   • Keep adding as many as you want!


⛔ STEP 6: Stop when done
───────────────────────────────────────────────────────────────────────────────

   • In the Terminal, press: Ctrl+C
   • The listener stops
   • Excel stays open (you can save and close it manually)


═══════════════════════════════════════════════════════════════════════════════


📊 EXAMPLE RESULTS
═══════════════════════════════════════════════════════════════════════════════

Campaign 1 (Technology - well-funded):
   Goal: 50,000 | Pledged: 75,000 | Backers: 1,250
   Result: 99.99% ✅ (Very likely to succeed)

Campaign 2 (Art - underfunded):
   Goal: 10,000 | Pledged: 7,500 | Backers: 150
   Result: 75.60% ⚠️ (Good chance but risky)

Campaign 3 (Film - no funding):
   Goal: 100,000 | Pledged: 500 | Backers: 5
   Result: 0.02% ❌ (Almost impossible to succeed)


═══════════════════════════════════════════════════════════════════════════════


❓ COMMON QUESTIONS
═══════════════════════════════════════════════════════════════════════════════

Q: "What does the number in column L mean?"
A: It's a probability from 0 to 1
   • 0.99 = 99% chance of success
   • 0.5 = 50% chance (coin flip)
   • 0.01 = 1% chance (unlikely)

Q: "Which columns are required?"
A: All of them (A through J). The model needs complete information.

Q: "Can I use a different spreadsheet?"
A: The script creates a template for you. You can edit it, but keep the structure.

Q: "How accurate is the model?"
A: 92.08% accuracy on test data. It's excellent! ⭐⭐⭐⭐⭐

Q: "Can I modify the workbook?"
A: Yes! You can add columns, format it, change colors - as long as A-J stay intact.

Q: "What if I close Excel by mistake?"
A: Just open kickstarter_branded.xlsm again. The script keeps running.


═══════════════════════════════════════════════════════════════════════════════


🛠️ TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

Problem: "Excel won't open"
Solution: 
  • Make sure Excel is installed: ls /Applications/Microsoft\ Excel.app
  • Try opening Excel manually first, then run the script

Problem: "I get an error about model files"
Solution:
  • Make sure you're in the right directory: /Users/emkanlaptop/Desktop/model
  • Check files exist: ls artifacts/ (should show .keras, .pkl, .json files)

Problem: "Prediction doesn't appear"
Solution:
  • Make sure ALL columns A-J are filled (no empty cells)
  • Save the workbook after entering data (Cmd+S)
  • Wait 2-3 seconds for the listener to detect changes
  • Check the Terminal for error messages

Problem: "I want to stop the script"
Solution:
  • In Terminal, press: Ctrl+C
  • The listener will stop and Excel will stay open


═══════════════════════════════════════════════════════════════════════════════


🎓 ABOUT THE MODEL
═══════════════════════════════════════════════════════════════════════════════

Author:     Mohamed SharafEldin (202201849)
Supervisors: Dr. Tarek Ali, Prof. Mervat Gheith
Email:      12422021653750@pg.cu.edu.eg

Model Type:    Artificial Neural Network (TensorFlow/Keras)
Training Data: 37,887 real Kickstarter projects
Features:     221 campaign attributes
Accuracy:     92.08% ⭐⭐⭐⭐⭐
AUC Score:    0.9780 (excellent)

The model predicts whether a Kickstarter campaign will reach its funding goal.


═══════════════════════════════════════════════════════════════════════════════


📚 WANT TO LEARN MORE?
═══════════════════════════════════════════════════════════════════════════════

Read these files for more details:
  • QUICK_START_GUIDE.md              ← Simple walkthrough
  • BRANDED_WORKBOOK_GUIDE.md         ← Workbook features
  • README.md                         ← Project overview
  • CUSTOMIZATION_SUMMARY.md          ← Technical details


═══════════════════════════════════════════════════════════════════════════════

                    🎉 NOW RUN THIS COMMAND AND ENJOY! 🎉

                cd /Users/emkanlaptop/Desktop/model
                source .venv/bin/activate
                python scripts/excel_listener.py

═══════════════════════════════════════════════════════════════════════════════

EOF
