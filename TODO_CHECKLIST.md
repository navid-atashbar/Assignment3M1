# Assignment 3 - Milestone 3 TODO Checklist

## 📋 REQUIRED TASKS (For Full M3 Credit)

### ✅ Already Completed:
- [x] Created 22 test queries (10 good, 12 poor)
- [x] Added 7 enhancements to `searcher.py`
- [x] Created documentation (`M3_TEST_QUERIES.txt`)
- [x] EXTRA CREDIT: Added exact duplicate detection

---

### 🔲 What YOU Need to Do:

#### 1. Test the Indexer with Duplicate Detection (30 min)
**If you haven't built the index yet or want to rebuild with duplicate detection:**

```bash
cd Assignment3M1
python indexer.py
```

**What to look for:**
- Progress messages every 2500 documents
- At the end: "Duplicates skipped: X (EXTRA CREDIT)"
- Should complete in 5-15 minutes for ~56K pages

**Expected output example:**
```
Summary DONE!
Documents indexed : 54789
Duplicates skipped: 1234 (EXTRA CREDIT)
Unique tokens     : 89456
Index size on disk: 12345.67 KB
```

---

#### 2. Test the Search Engine (15 min)
**Run the search interface:**

```bash
python user_interface.py
```

**Test these queries and take notes:**

| Query | What It Tests | Expected Result |
|-------|---------------|-----------------|
| `machine learning` | Baseline TF-IDF | Should return ML course/research pages |
| `AI ML` | Query expansion | Should find both "AI" and "artificial intelligence" pages |
| `cs 122` | Course code norm | Should find CS122 course pages |
| `informatics` | Stop word handling | Should rank results better despite common word |
| `how to apply` | Relaxed Boolean | Should return application pages (not empty) |
| `professor` | Length normalization | Should not be dominated by long CV pages |

**Take notes on:**
- Response times (should be < 300ms)
- Top 3-5 results for each query
- Whether results make sense

---

#### 3. Update Report if Needed (10 min)
**Open `M3_TEST_QUERIES.txt`**

- If any query behaves differently than described, update it
- Add actual response times you observed
- Note any surprising results

---

#### 4. Practice Your Demo (20 min)
**You'll need to explain to the TA:**

**A. Code Walkthrough (5 min):**
- Open `searcher.py`
- Point out the 7 enhancements (search for "M3 Enhancement:" comments)
- Briefly explain each one

**B. Live Demo (5 min):**
- Run `user_interface.py`
- Search for 3-4 queries
- Show response times < 300ms

**C. Extra Credit (2 min):**
- Show the duplicate count in `statistics.json`
- Explain: "We used MD5 hashing to detect exact duplicates"

**D. Questions (8 min):**
- Be ready to explain why improvements are generalizable
- Be able to discuss TF-IDF formula
- Explain how you maintain memory constraints

---

#### 5. Prepare Submission (10 min)

**Create a zip file named `Assignment3M1.zip` containing:**

```
Assignment3M1.zip
├── indexer.py
├── inverted_index.py
├── parser.py
├── tokenizer.py
├── searcher.py
├── user_interface.py
├── M3_TEST_QUERIES.txt
├── EXTRA_CREDIT.txt         (mention this in your submission!)
└── requirements.txt
```

**DO NOT include:**
- DEV/ folder (too large)
- index_data/ folder (TA will rebuild)
- Any test files or documentation files

**In your email/submission form, mention:**
- "Implemented all M3 requirements (7 enhancements for 12 poor queries)"
- "Added exact duplicate detection for +1 extra credit point"
- "See EXTRA_CREDIT.txt for details"

---

## 🎁 EXTRA CREDIT STATUS

### ✅ Exact Duplicate Detection (+1 point)
- [x] Code implemented in `inverted_index.py`
- [x] Uses MD5 content hashing
- [x] Statistics tracked
- [ ] **YOU: Test by running `python indexer.py`**
- [ ] **YOU: Note the duplicate count for your demo**

### Optional: Near-Duplicate Detection (+2 points)
- [ ] Not implemented (requires SimHash/MinHash - complex)
- [ ] Only do this if you want the challenge and have extra time

---

## 📅 TIMELINE SUGGESTION

If your demo is in **2-3 days:**
- **Day 1 (Today)**: 
  - ✅ Rebuild index with duplicate detection (30 min)
  - ✅ Test all queries (15 min)
  - ✅ Update report if needed (10 min)

- **Day 2 (Tomorrow)**:
  - Practice demo (20 min)
  - Review code to understand it deeply (30 min)
  - Prepare answers to likely TA questions (20 min)

- **Day 3 (Demo day)**:
  - Quick test run before demo (5 min)
  - Do the demo!

---

## ⚠️ COMMON ISSUES & FIXES

**Issue: "Module not found: nltk"**
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
```

**Issue: "FileNotFoundError: index_data/"**
- You need to run `python indexer.py` first to build the index

**Issue: "No results found"**
- Check that your index was built successfully
- Try a simpler query like "machine learning"

**Issue: "Response time > 300ms"**
- This is okay for complex queries
- Most queries should be < 200ms
- Only a few might hit 250-300ms

---

## 📞 BEFORE THE DEMO - FINAL CHECKLIST

- [ ] Index built successfully with duplicate detection
- [ ] Tested at least 5-6 queries and they work
- [ ] Can run `user_interface.py` without errors
- [ ] Understand where each enhancement is in the code
- [ ] Know your duplicate count number
- [ ] Submission zip file ready
- [ ] Can explain why improvements are generalizable

---

## 🎯 SUCCESS CRITERIA

**For Full M3 Credit (50 points):**
- ✅ 20+ test queries
- ✅ Documented problems
- ✅ Implemented improvements
- ✅ Code works
- ✅ Can demo and explain

**Bonus (+1 point):**
- ✅ Exact duplicate detection working

**You're ready! 🚀**
