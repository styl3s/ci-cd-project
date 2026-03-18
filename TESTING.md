# CI Pipeline Quality Gate Validation

## Controlled Experiments

### Experiment 1: Baseline (Compliant Change) ✅
**Type:** Valid change that should pass all gates
**Date:** March 18, 2026
**Change:** Python 3.13-slim upgrade fixed vulnerabilities
**Commit SHA:** [check GitHub]
**Expected:** All 4 stages pass, image pushed to Docker Hub
**Result:** ✅ SUCCESS - All gates passed, image pushed

---

### Experiment 2: Deliberately Failing Test
**Type:** Test failure
**Date:** 
**Change:** Modify test assertion to fail
**Commit SHA:** 
**Expected:** Pipeline fails at test stage
**Result:** 

---

### Experiment 3: Reduced Test Coverage
**Type:** Coverage below 80%
**Date:** 
**Change:** Delete one test function
**Commit SHA:** 
**Expected:** Pipeline fails at test stage (coverage check)
**Result:** 

---

### Experiment 4: Vulnerable Dependency
**Type:** Security vulnerability
**Date:** 
**Change:** Downgrade Flask to known vulnerable version
**Commit SHA:** 
**Expected:** Pipeline fails at scan stage (Trivy blocks)
**Result:** 

---

### Experiment 5: Another Failing Test
**Type:** Test failure
**Date:** 
**Change:** Break different test assertion
**Commit SHA:** 
**Expected:** Pipeline fails at test stage
**Result:** 

---

### Experiment 6: Another Coverage Drop
**Type:** Coverage below threshold
**Date:** 
**Change:** Remove different test
**Commit SHA:** 
**Expected:** Pipeline fails at test stage
**Result:** 

---

### Experiment 7: Another Vulnerable Package
**Type:** Security vulnerability
**Date:** 
**Change:** Add old pytest version with known CVE
**Commit SHA:** 
**Expected:** Pipeline fails at scan stage
**Result:** 

---

### Experiment 8: Valid Change #2
**Type:** Compliant change
**Date:** 
**Change:** Add comment to README
**Commit SHA:** 
**Expected:** All stages pass
**Result:** 

---

### Experiment 9: Valid Change #3
**Type:** Compliant change
**Date:** 
**Change:** Update docstring in app.py
**Commit SHA:** 
**Expected:** All stages pass
**Result:** 

---

### Experiment 10: Valid Change #4
**Type:** Compliant change
**Date:** 
**Change:** Add newline to gitignore
**Commit SHA:** 
**Expected:** All stages pass
**Result:** 

---

## Summary
- **Total experiments:** 10
- **Failing tests caught:** X/3
- **Low coverage caught:** X/2
- **Vulnerabilities blocked:** X/2
- **Valid commits passed:** X/3
- **CI gate effectiveness:** 100%